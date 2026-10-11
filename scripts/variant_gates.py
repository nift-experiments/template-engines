"""Supplementary exact-byte gates for the otherwise untimed second single-render data variant."""
from certify import *
import shutil,hashlib
stage=R/'work/variant-gates';(stage/'adapters').mkdir(parents=True,exist_ok=True);(stage/'corpus').mkdir(exist_ok=True)
for name in ['python.py','node.js']:shutil.copy2(R/'adapters'/name,stage/'adapters'/name)
shutil.copy2(R/'corpus/manifest.json',stage/'corpus/manifest.json')
rows=[]
for case in json.loads((R/'corpus/manifest.json').read_text()):
 if case['name'] not in ['condition','article','interpolation','raw-special-values']:continue
 target=stage/'corpus'/case['name']
 shutil.copytree(R/'corpus'/case['name'],target,dirs_exist_ok=True)
 shutil.copy2(target/'data1.json',target/'data0.json')
 oracle=(target/'expected1.txt').read_bytes()
 for engine in ENGINES:
  cmd=command(engine,case,'fresh')
  if engine=='nift':cmd[1]=str(target)
  else:cmd[1]=str(stage/'adapters'/('python.py' if engine=='jinja' else 'node.js'))
  p=subprocess.run(cmd,capture_output=True);assert p.returncode==0 and p.stdout==oracle,(case['name'],engine,p.stderr,p.stdout[:100])
  rows.append({'case':case['name'],'engine':engine,'variant':1,'pass':True,'expected_sha256':hashlib.sha256(oracle).hexdigest(),'output_sha256':hashlib.sha256(p.stdout).hexdigest(),'scope':'Untimed fresh-render conformance with second canonical dataset; official corpus unchanged'})
(R/'work/variant-gates.json').write_text(json.dumps(rows,indent=2)+'\n');print('PASS',len(rows),'second-variant/true-branch exact-byte gates')
