#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-3.0-only
"""Original FM EP bank. Recovered from the recorded implementation after workspace pruning."""
import argparse, hashlib, importlib.util, json, re, shutil, subprocess, wave
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
UPSTREAM=ROOT/'vendor/skiff'
OUT=ROOT/'build/firmware'
PIN='8eb0e273b62d964dc7f53ca78257c19fdc38bd9e'

def codec():
    spec=importlib.util.spec_from_file_location('codec',UPSTREAM/'tools/gen_fm6_patches.py')
    m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m

def designs():
    ds=json.loads((ROOT/'presets/designs.json').read_text())
    if not isinstance(ds,list) or len(ds)!=8:raise ValueError('exactly eight designs required')
    for d in ds:
        for key,pattern in [('id',r'[a-z0-9]+(?:-[a-z0-9]+)*'),('name',r'[A-Z0-9 ]{1,16}'),('syx_name',r'[A-Z0-9 ]{1,10}')]:
            if not re.fullmatch(pattern,d.get(key,'')):raise ValueError('invalid '+key)
        if len(d['fx'])!=3 or any(type(x)!=int or not 0<=x<=127 for x in d['fx']):raise ValueError('invalid FX')
    for key in ['id','name','syx_name']:
        if len({d[key] for d in ds})!=8:raise ValueError('duplicate '+key)
    return ds

def make_voice(d):
    limits={'body_decay':(0,96),'body_level':(8,99),'body_mod':(8,99),'tine_level':(0,99),
            'tine_ratio':(0,31),'tine_decay':(0,99),'tine_carrier':(0,99),'release':(0,99),'detune':(0,7),'spread':(0,127)}
    for k,(a,b) in limits.items():
        if type(d[k])!=int or not a<=d[k]<=b:raise ValueError('out of range: '+k)
    c=codec();op=c.op
    ops=[
      op(r=(93,d['body_decay'],24,d['release']),l=(99,82,0,0),ol=d['body_level'],kvs=2,rs=2,rd=10,rc=1),
      op(r=(97,41,29,76),l=(99,80,0,0),ol=d['body_mod'],fc=1,kvs=5,rs=2),
      op(r=(98,47,31,d['release']),l=(99,69,0,0),ol=d['tine_carrier'],kvs=3,rs=2,rd=18,rc=1),
      op(r=(99,d['tine_decay'],49,81),l=(99,38,0,0),ol=d['tine_level'],fc=d['tine_ratio'],kvs=6,rs=3,rd=20,rc=1),
      op(r=(91,d['body_decay']+3,27,d['release']),l=(99,85,0,0),ol=d['body_level']-8,kvs=2,det=7+d['detune'],rs=2),
      op(r=(95,37,30,73),l=(99,78,0,0),ol=d['body_mod']-8,fc=1,kvs=4,rs=2)]
    return c.voice(d['syx_name'],5,ops,fb=0,lfs=28,lfd=0,lpmd=0,lamd=0,lpms=0)

def voices():return [make_voice(d) for d in designs()]
def syx(v):return bytes([240,67,0,0,1,27]+v+[(-sum(v))&127,247])
def replace_once(s,a,b):
    if s.count(a)!=1:raise ValueError('unexpected source anchor: '+a)
    return s.replace(a,b,1)
def tracked_paths(root):return list(filter(None,subprocess.check_output(['git','ls-files','-z'],cwd=root).decode().split('\0')))
def export():
    dest=ROOT/'dist/presets';dest.mkdir(parents=True,exist_ok=True)
    for d,v in zip(designs(),voices()):(dest/(d['id']+'.syx')).write_bytes(syx(v))

def prepare():
    vs=voices()
    if subprocess.check_output(['git','rev-parse','HEAD'],cwd=UPSTREAM,text=True).strip()!=PIN:raise RuntimeError('unsupported source revision')
    if subprocess.check_output(['git','status','--porcelain','--untracked-files=no'],cwd=UPSTREAM,text=True).strip():raise RuntimeError('tracked upstream modifications')
    if OUT.exists():shutil.rmtree(OUT)
    for rel in tracked_paths(UPSTREAM):
        dst=OUT/rel;dst.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(UPSTREAM/rel,dst)
    for n in ['samples-cc0','breaks']:
        p=OUT/'assets'/n
        if p.exists():shutil.rmtree(p)
    p=OUT/'assets/breaks';p.mkdir(parents=True)
    for n,frames in [('break',44100),('funk',30650)]:
        with wave.open(str(p/(n+'.wav')),'wb') as w:w.setparams((1,2,22050,0,'NONE','not compressed'));w.writeframes(bytes(frames*2))
    c=codec();h=['#pragma once','#include <stdint.h>','#define FM6_NFACTORY 8',
       'static const uint8_t FM6_INIT[128] = {'+','.join(map(str,c.pack(c.INIT)))+'};',
       'static const uint8_t FM6_FACTORY[8][128] = {']
    h+=['{'+','.join(map(str,c.pack(v)))+'},' for v in vs];h+=['};']
    (OUT/'tools/gen_fm6_patches.py').write_text('# SPDX-License-Identifier: GPL-3.0-only\nimport sys\nfrom pathlib import Path\nPath(sys.argv[1]).write_text('+repr('\n'.join(h)+'\n')+')\n')
    p=OUT/'firmware/src/eng_fm6.c';s=p.read_text();a=s.index('static const preset_t FM6_PRESETS[] = {');b=s.index('\n};',a)+3
    rows=['static const preset_t FM6_PRESETS[] = {']
    for i,d in enumerate(designs()):
        fx=', '.join(map(str,[0]+d['fx']))
        rows.append('    {"%s", {0, 0, 0, 0, 0, 0, 0, %d}, {0, 0, 127, 0}, 0, 0, FX(%s), MORE({P_SPRD, %d}), TAG(PT_KEYS)},' % (d['name'],i,fx,d['spread']))
    rows+=['};'];s=s[:a]+'\n'.join(rows)+s[b:]
    p.write_text(replace_once(s,'.knob = {P_E2, P_E3, P_E4, P_E7}', '.knob = {P_E2, P_E4, P_E5, P_E7}'))
    p=OUT/'firmware/src/engines.c';p.write_text(replace_once(p.read_text(),'{{0, 4}, {ENGI_FM6, 4}','{{ENGI_FM6, 0}, {ENGI_FM6, 4}'))
    p=OUT/'firmware/src/felucca.c';p.write_text(replace_once(p.read_text(),'#define FELUCCA_VERSION "v2.0.3"','#define FELUCCA_VERSION "VEP90-a1"'))
    p=OUT/'tests/fm6_test.c';p.write_text(replace_once(p.read_text(),'"SOFT PAD  "','"DRY90     "'))
    inventory={str(p.relative_to(OUT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in OUT.rglob('*') if p.is_file()}
    (ROOT/'build/source-files.json').write_text(json.dumps(inventory,indent=2)+'\n')
    export();print('Prepared pinned Pro EP source; firmware not installed')

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('action',choices=['prepare','export']);a=p.parse_args();prepare() if a.action=='prepare' else export()
