"""Rotated same-CPU official sampling; all raw rows retained in ignored work/."""
import os,json,time,subprocess,tempfile,hashlib,platform,sys
from pathlib import Path
from certify import command,expected,ENGINES,R

def fresh(cmd,oracle):
 with tempfile.TemporaryFile() as out,tempfile.TemporaryFile() as err:
  start=time.perf_counter_ns();p=subprocess.Popen(cmd,stdout=out,stderr=err);_,status,usage=os.wait4(p.pid,0);p.returncode=os.waitstatus_to_exitcode(status);elapsed=time.perf_counter_ns()-start
  out.seek(0);data=out.read();err.seek(0);errors=err.read()
  assert p.returncode==0 and data==oracle,(cmd,p.returncode,errors.decode()[:500],data[:100],oracle[:100])
  return {'ns':elapsed,'cpu_user_s':usage.ru_utime,'cpu_system_s':usage.ru_stime,'max_child_rss_mib':usage.ru_maxrss/1024,'output_sha256':hashlib.sha256(data).hexdigest(),'output_bytes':len(data),'operations':1}
def main():
 plan=json.loads((R/'docs/TIMING-PLAN.json').read_text());output=Path(sys.argv[1] if len(sys.argv)>1 else R/'work/official');output.mkdir(parents=True,exist_ok=True)
 env=dict(os.environ,BENCH_GATE='1',NO_COLOR='1',DO_NOT_TRACK='1');cpu=min(os.sched_getaffinity(0));prefix=['taskset','-c',str(cpu)]
 (output/'environment.json').write_text(json.dumps({'uname':platform.uname()._asdict(),'cpu_affinity':cpu,'cpuinfo':Path('/proc/cpuinfo').read_text(),'meminfo':Path('/proc/meminfo').read_text(),'tools':json.loads((R/'docs/VERSIONS.json').read_text()),'suite_sha':subprocess.check_output(['git','rev-parse','HEAD'],cwd=R,text=True).strip(),'runtimes':{k:subprocess.check_output(v,text=True).strip() for k,v in {'node':['node','--version'],'python':[str(R/'.venv/bin/python'),'--version'],'compiler':['g++','--version']}.items()}},indent=2)+'\n')
 with (output/'observations.jsonl').open('w') as records:
  for case in json.loads((R/'corpus/manifest.json').read_text()):
   if case.get('semantic_only'):continue
   if '--pilot' in sys.argv and case['name'] not in ('literal','loop-100','includes-4','many-renders-100'):continue
   engines=ENGINES
   count=2 if '--pilot' in sys.argv else plan[case['name']]['fresh_samples'];oracle=expected(case)
   for round in range(-2,count):
    rotated=engines[round%len(engines):]+engines[:round%len(engines)]
    for eng in rotated:
     row=fresh(prefix+command(eng,case,'fresh'),oracle);row.update(engine=eng,case=case['name'],mode='fresh',sample=round,warmup=round<0);records.write(json.dumps(row)+'\n');records.flush()
   for mode in ['render','reuse','parse']+(['files'] if case['partials'] else []):
    engines=[e for e in ENGINES if e!='nift' or mode not in ('reuse','parse')];count=2 if '--pilot' in sys.argv else plan[case['name']]['persistent_samples'];workers={}
    with (output/'adapter-stderr.log').open('a') as errors:
     for eng in engines:
      batch=plan[case['name']]['batch'][eng][mode];p=subprocess.Popen(prefix+command(eng,case,mode,batch,count),stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=errors,env=env,text=True,bufsize=1);workers[eng]=p
     for round in range(-2,count):
      rotated=engines[round%len(engines):]+engines[:round%len(engines)]
      for eng in rotated:
       p=workers[eng];p.stdin.write('go\n');p.stdin.flush();line=p.stdout.readline();assert line,('worker failed',case['name'],eng,mode)
       row=json.loads(line);assert row['sample']==round;row.update(engine=eng,case=case['name'],mode='source-reuse' if eng=='nift' and mode=='render' else mode);records.write(json.dumps(row)+'\n');records.flush()
     for eng,p in workers.items():
      _,status,usage=os.wait4(p.pid,0);p.returncode=os.waitstatus_to_exitcode(status);assert p.returncode==0,(eng,case['name'],mode)
      with (output/'worker-lifetimes.jsonl').open('a') as memory:memory.write(json.dumps({'engine':eng,'case':case['name'],'mode':'source-reuse' if eng=='nift' and mode=='render' else mode,'max_process_rss_mib':usage.ru_maxrss/1024,'cpu_user_s':usage.ru_utime,'cpu_system_s':usage.ru_stime,'scope':'Whole persistent worker lifetime: runtime, preload, preparation, timed batches, retained outputs and correctness validation'})+'\n')
   print('completed',case['name'],flush=True)
 print('measurement complete',output,flush=True)
if __name__=='__main__':main()
