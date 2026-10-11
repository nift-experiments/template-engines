import sys,json,time,os
from pathlib import Path
from jinja2 import Environment,DictLoader,FileSystemLoader
root=Path(__file__).resolve().parents[1];name,mode=sys.argv[1:3];batch=int(sys.argv[3]) if len(sys.argv)>3 else 1;samples=int(sys.argv[4]) if len(sys.argv)>4 else 1
path=root/'corpus'/name;meta=next(x for x in json.loads((root/'corpus/manifest.json').read_text()) if x['name']==name)
data=[{'d':json.loads((path/f'data{i}.json').read_text())} for i in range(2)];texts={p.name:p.read_text() for p in (path/'jinja').iterdir()};env=Environment(loader=FileSystemLoader(path/'jinja') if mode=='files' else DictLoader(texts),autoescape=False,keep_trailing_newline=True,cache_size=0 if mode=='files' else 400)
if mode=='invalid':
 try:env.compile('{% for x in d.records %}')
 except Exception:print(json.dumps({'rejected':True}));sys.exit(0)
 raise RuntimeError('malformed template accepted')
prepared=[env.from_string(texts[f'main{i}']) for i in range(meta['distinct'])] if mode=='reuse' else []
def op():
 outputs=[]
 for i in range(meta['renders']*meta['distinct']):
  k=i%meta['distinct'];source=(path/'jinja'/f'main{k}').read_text() if mode=='files' else texts[f'main{k}']
  if mode=='parse':env.compile(source);continue
  template=prepared[k] if mode=='reuse' else env.from_string(source)
  outputs.append((i%2,k,template.render(data[i%2])))
 return outputs
if mode=='fresh':
 print(''.join(x[2] for x in op()),end='');sys.exit()
for s in range(samples+2):
 if os.environ.get('BENCH_GATE'):sys.stdin.readline()
 start=time.perf_counter_ns();results=[op() for _ in range(batch)];elapsed=time.perf_counter_ns()-start
 for group in results:
  for v,k,out in group:
   expected=(path/f'expected{v}.txt').read_text()+('<!--'+str(k)+'-->' if meta['distinct']>1 else '')
   assert out==expected,(name,mode,v,k,out[:80],expected[:80])
 print(json.dumps({'sample':s-2,'warmup':s<2,'ns':elapsed,'batch':batch,'operations':batch*meta['renders']*meta['distinct']}),flush=True)
