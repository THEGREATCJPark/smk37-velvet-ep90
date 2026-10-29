#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-3.0-only
import csv,hashlib,importlib.util,itertools,json,subprocess,tempfile,wave
from pathlib import Path
import numpy as np
from velvet import ROOT,OUT,designs,voices,syx,codec

def run(cmd,**kwargs):return subprocess.run([str(x) for x in cmd],check=True,**kwargs)
vs=voices();assert len({bytes(v) for v in vs})==8
for v in vs:
 assert len(v)==155 and all(0<=x<128 for x in v)
 s=syx(v);assert len(s)==163 and sum(s[6:-1])%128==0
 assert v not in [p for _,p in codec().PATCHES]
spec=importlib.util.spec_from_file_location('b',OUT/'tools/build.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);m.generate()
(ROOT/'build/host').mkdir(exist_ok=True)
flags=['cc','-O2','-w','-DBOARD_SMK37=1','-Ifirmware/hal','-Ibuild/gen','-Ifirmware/src']
for name,src in [('render',ROOT/'tools/render.c'),('fm6_test','tests/fm6_test.c'),('smk_flash_test','tests/smk_flash_test.c'),('smk_owner_test','tests/smk_owner_test.c'),('smk_ui_test','tests/smk_ui_test.c')]:
 run(flags+[src,'-lm','-o',ROOT/'build/host'/name],cwd=OUT)
 if name!='render':run([ROOT/'build/host'/name],cwd=OUT)
package=OUT/'build/skiff-smk37.fwsc'
if package.exists():run(['python3','tests/smk_pkg_test.py',package,'SMK-37 Pro_700'],cwd=OUT)
FS=44100;rows=[];render=ROOT/'build/host/render'
def metrics(x):
 def rms(a,b):return float(np.sqrt(np.mean(x[int(a*FS):int(b*FS)]**2)))
 def centroid(a,b):
  y=x[int(a*FS):int(b*FS)];mag=abs(np.fft.rfft(y*np.hanning(len(y))))**2
  return float(np.dot(mag,np.fft.rfftfreq(len(y),1/FS))/(mag.sum()+1e-30))
 return dict(peak=float(max(abs(x))),dc=float(abs(np.mean(x))),rms_early=rms(.02,.25),rms_late=rms(.8,1.2),centroid_early=centroid(.02,.15),centroid_late=centroid(.8,1.2))
with tempfile.TemporaryDirectory() as td:
 for pi,d in enumerate(designs()):
  for note,vel in itertools.product(range(36,97,6),[16,32,48,64,80,96,112,127]):
   p=Path(td)/'audio.f32';run([render,pi,note,vel,2,p]);x=np.fromfile(p,dtype='<f4');assert len(x)==88200 and np.isfinite(x).all()
   m=metrics(x);assert m['peak']<2 and m['dc']<.01 and m['rms_early']>.00001
   rows.append(dict(preset=d['id'],note=note,velocity=vel,**m))
for d in designs():
 for note in range(36,97,6):
  r=[x for x in rows if x['preset']==d['id'] and x['note']==note];assert r[-1]['rms_early']>r[0]['rms_early']
md=ROOT/'docs/measurements';md.mkdir(parents=True,exist_ok=True)
with (md/'preset-grid.csv').open('w',newline='') as f:w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
summary=dict(render_count=len(rows),worst_voice_peak=max(x['peak'] for x in rows),worst_abs_dc=max(x['dc'] for x in rows),failures=[],hardware_tested=False,reference_audio_compared=False)
(md/'summary.json').write_text(json.dumps(summary,indent=2)+'\n')
dest=ROOT/'dist/demos';dest.mkdir(parents=True,exist_ok=True);demos=[]
for pi,d in enumerate(designs()):
 for vel in [64,112]:
  p=dest/f"{d['id']}-v{vel}.wav";run([render,pi,60,vel,8,p,'-','wet'])
  with wave.open(str(p)) as w:x=np.frombuffer(w.readframes(w.getnframes()),dtype='<i2').reshape(-1,2)/32768.
  if d['spread']:assert np.any(x[:,0]!=x[:,1])
  rms=lambda y:float(np.sqrt(np.mean(y*y)))
  loss=20*np.log10(rms(x.mean(axis=1))/rms(x));assert loss> -3
  demos.append(dict(file=p.name,peak=float(max(abs(x).flatten())),mono_loss_db=float(loss)))
(md/'demos.json').write_text(json.dumps(demos,indent=2)+'\n')
print(json.dumps(summary));print('All host checks passed; 16 demos rendered. Hardware and reference audio unverified.')
