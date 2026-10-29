# SPDX-License-Identifier: GPL-3.0-only
import sys,unittest,tempfile,subprocess
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'tools'))
import velvet as v
class Tests(unittest.TestCase):
 def test_voice_and_checksum(self):
  vs=v.voices();self.assertEqual(len({bytes(x) for x in vs}),8)
  for x in vs:self.assertEqual(len(v.syx(x)),163);self.assertEqual(sum(v.syx(x)[6:-1])%128,0)
 def test_limits(self):
  for k,x in [('body_decay',97),('body_level',7),('tine_ratio',32),('spread',128)]:
   with self.assertRaises(ValueError):v.make_voice(dict(v.designs()[0],**{k:x}))
 def test_guard(self):
  for text in ['missing','old old']:
   with self.assertRaises(ValueError):v.replace_once(text,'old','new')
 def test_inventory(self):
  with tempfile.TemporaryDirectory() as td:
   p=Path(td);subprocess.run(['git','init','-q',td],check=True)
   (p/'.gitignore').write_text('private.bin\n');(p/'source.c').write_text('int x;')
   subprocess.run(['git','add','.gitignore','source.c'],cwd=p,check=True)
   (p/'private.bin').write_bytes(b'private');(p/'untracked.txt').write_text('local')
   self.assertEqual(set(v.tracked_paths(p)),{'.gitignore','source.c'})
if __name__=='__main__':unittest.main()
