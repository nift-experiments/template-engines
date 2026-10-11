from certify import *
import math
records=[];plan={}
for case in json.loads((R/'corpus/manifest.json').read_text()):
 if case.get('semantic_only'):continue
 entry={'fresh_samples':30 if case['renders']*case['distinct']>1 or case['output_bytes']>10000 else 50,'persistent_samples':50,'batch':{}}
 for eng in ENGINES:
  entry['batch'][eng]={}
  for mode in ['render','reuse','parse']+(['files'] if case['partials'] else []):
   if eng=='nift' and mode in ('reuse','parse'):continue
   p=subprocess.run(command(eng,case,mode,1,3),capture_output=True,text=True);assert p.returncode==0,(eng,case['name'],mode,p.stderr)
   rows=[json.loads(line) for line in p.stdout.splitlines()];elapsed=max(1,min(x['ns'] for x in rows if not x['warmup']))
   batch=max(1,min(1000,math.ceil(10000000/elapsed),max(1,16000000//max(1,case['output_bytes']*case['renders']*case['distinct']))))
   entry['batch'][eng][mode]=batch;records.append({'engine':eng,'case':case['name'],'mode':mode,'pilot':rows,'batch':batch})
 plan[case['name']]=entry;print('planned',case['name'],flush=True)
(R/'docs/TIMING-PLAN.json').write_text(json.dumps(plan,indent=2)+'\n');(R/'work/local-feasibility.json').write_text(json.dumps(records,indent=2)+'\n')
print('Persistent nominal 10ms target, 50 samples; estimated official total 10–20 minutes plus installation/build. Max retained output per batch ~16MB.')
