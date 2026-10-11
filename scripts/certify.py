from pathlib import Path
import subprocess,json,time,sys
R=Path(__file__).resolve().parents[1]
ENGINES=['nift','jinja','nunjucks','handlebars','liquid']
def command(engine,case,mode,batch=1,samples=1):
 if engine=='nift':return [str(R/'work/nift-adapter'),str(R/'corpus'/case['name']),mode,str(batch),str(samples),str(case['renders']),str(case['distinct'])]
 if engine=='jinja':return [str(R/'.venv/bin/python'),str(R/'adapters/python.py'),case['name'],mode,str(batch),str(samples)]
 return ['node',str(R/'adapters/node.js'),engine,case['name'],mode,str(batch),str(samples)]
def expected(case):
 return b''.join((R/'corpus'/case['name']/f'expected{i%2}.txt').read_bytes()+(('<!--'+str(i%case['distinct'])+'-->').encode() if case['distinct']>1 else b'') for i in range(case['renders']*case['distinct']))
def main():
 records=[];start=time.time()
 for case in json.loads((R/'corpus/manifest.json').read_text()):
  for eng in ENGINES:
   for mode in ['fresh','render','reuse','parse']+(['files'] if case['partials'] else []):
    if eng=='nift' and mode in ['reuse','parse']:continue
    p=subprocess.run(command(eng,case,mode),capture_output=True)
    ok=p.returncode==0 and (p.stdout==expected(case) if mode=='fresh' else True)
    records.append({'engine':eng,'case':case['name'],'mode':mode,'ok':ok,'stderr':p.stderr.decode()[:1000]})
    if not ok:print('FAIL',records[-1],flush=True)
  print('checked',case['name'],flush=True)
 out=R/'work/local-certification.json';out.write_text(json.dumps({'seconds':time.time()-start,'records':records,'pass':all(x['ok'] for x in records)},indent=2)+'\n')
 if not all(x['ok'] for x in records):sys.exit(1)
 print('PASS',len(records),'cells')
if __name__=='__main__':main()
