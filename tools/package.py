#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-3.0-only
import gzip,hashlib,io,json,shutil,tarfile
from pathlib import Path
from velvet import ROOT,OUT,tracked_paths,PIN
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
files=json.loads((ROOT/'build/source-files.json').read_text())
for rel,h in files.items():
 if sha(OUT/rel)!=h:raise SystemExit('source changed; prepare/rebuild/verify: '+rel)
if 'All host checks passed' not in (ROOT/'build/verification.log').read_text():raise SystemExit('verification required')
dist=ROOT/'dist';fw=OUT/'build/skiff-smk37.fwsc';shutil.copy2(fw,dist/'velvet-ep90-smk37-pro-v0.1.0-alpha.1.fwsc')
with (dist/'velvet-ep90-corresponding-source.tar.gz').open('wb') as out,gzip.GzipFile(fileobj=out,mode='wb',filename='',mtime=0) as gz,tarfile.open(fileobj=gz,mode='w') as t:
 def add(p,name):
  b=p.read_bytes();i=tarfile.TarInfo(name);i.size=len(b);i.mode=0o755 if p.stat().st_mode&0o111 else 0o644;t.addfile(i,io.BytesIO(b))
 for rel in sorted(files):
  if Path(rel).parts[0] in {'firmware','tools','tests','assets','LICENSES','web'} or rel in {'build.sh','BUILDING.md','LICENSE','LICENSING.md','SMK37.md','README.md'}:add(OUT/rel,'velvet-ep90/firmware/'+rel)
 for rel in tracked_paths(ROOT):
  if Path(rel).parts[0] in {'tools','tests','presets','docs','.github'} or rel in {'README.md','LICENSE','requirements.txt'}:add(ROOT/rel,'velvet-ep90/project/'+rel)
(dist/'manifest.json').write_text(json.dumps(dict(version='0.1.0-alpha.1',upstream_commit=PIN,model='SMK-37 Pro',firmware_sha256=sha(fw),hardware_tested=False,reference_audio_compared=False),indent=2)+'\n')
(dist/'SHA256SUMS').write_text(''.join(sha(p)+'  '+str(p.relative_to(dist))+'\n' for p in sorted(dist.rglob('*')) if p.is_file() and p.name!='SHA256SUMS'))
