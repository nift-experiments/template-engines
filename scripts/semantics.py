from certify import *
case=next(x for x in json.loads((R/'corpus/manifest.json').read_text()) if x.get('semantic_only'))
rows=[]
for engine in ENGINES:
 for mode in ('fresh','invalid'):
  p=subprocess.run(command(engine,case,mode),capture_output=True);assert p.returncode==0,(engine,mode,p.stderr)
  assert p.stdout==expected(case) if mode=='fresh' else json.loads(p.stdout)['rejected']
  rows.append({'engine':engine,'case':case['name'],'mode':mode,'ok':True})
(R/'work/semantic-gates.json').write_text(json.dumps(rows,indent=2)+'\n');print('PASS',len(rows),'raw-special-value/malformed-template gates')
