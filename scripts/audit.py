"""Independent completeness/statistics audit of the frozen official observation stream."""
from pathlib import Path
import json,hashlib,statistics,math,sys,collections
R=Path(__file__).resolve().parents[1];folder=Path(sys.argv[1] if len(sys.argv)>1 else R/'work/official');rows=[json.loads(x) for x in (folder/'observations.jsonl').read_text().splitlines()];groups=collections.defaultdict(list)
for row in rows:
 assert row['ns']>0 and row['operations']>0
 groups[(row['case'],row['engine'],row['mode'])].append(row)
plan=json.loads((R/'docs/TIMING-PLAN.json').read_text());cases=[x for x in json.loads((R/'corpus/manifest.json').read_text()) if not x.get('semantic_only')];expected_cells=set();summary=[]
for case in cases:
 for engine in ['nift','jinja','nunjucks','handlebars','liquid']:
  modes=['fresh','source-reuse'] if engine=='nift' else ['fresh','render','reuse','parse']
  if case['partials']:modes.append('files')
  for mode in modes:
   key=(case['name'],engine,mode);expected_cells.add(key);g=groups[key];count=plan[case['name']]['fresh_samples' if mode=='fresh' else 'persistent_samples'];assert sorted(x['sample'] for x in g)==list(range(-2,count)),key
   expected=b''.join((R/'corpus'/case['name']/f'expected{i%2}.txt').read_bytes()+(('<!--'+str(i%case['distinct'])+'-->').encode() if case['distinct']>1 else b'') for i in range(case['renders']*case['distinct']));digest=hashlib.sha256(expected).hexdigest()
   for x in g:
    assert x['warmup']==(x['sample']<0)
    if mode=='fresh':assert x['output_sha256']==digest and x['output_bytes']==len(expected)
    elif mode!='parse':assert x['expected_output_sha256']==digest and x['all_rendered_outputs_exactly_checked']
   measured=[x for x in g if not x['warmup']];values=sorted(x['ns']/x['operations']/1e6 for x in measured)
   item={'case':case['name'],'engine':engine,'mode':mode,'samples':len(values),'median_ms':statistics.median(values),'p95_ms':values[math.ceil(.95*len(values))-1],'min_ms':values[0],'max_ms':values[-1],'output_bytes_per_render':case['output_bytes'],'renders_per_operation':case['renders']*case['distinct'],'batch':g[0].get('batch',1)}
   if mode=='fresh':item.update(median_child_rss_mib=statistics.median(x['max_child_rss_mib'] for x in measured),median_cpu_s=statistics.median(x['cpu_user_s']+x['cpu_system_s'] for x in measured))
   summary.append(item)
assert set(groups)==expected_cells
memory=[json.loads(x) for x in (folder/'worker-lifetimes.jsonl').read_text().splitlines()];assert len(memory)==len([k for k in expected_cells if k[2]!='fresh'])
assert {(x['case'],x['engine'],x['mode']) for x in memory}=={k for k in expected_cells if k[2]!='fresh'}
files={str(p.relative_to(R)):hashlib.sha256(p.read_bytes()).hexdigest() for p in (R/'corpus').rglob('*') if p.is_file()};assert files==json.loads((R/'docs/CORPUS-HASHES.json').read_text())
audit={'pass':True,'cells':len(groups),'measured_observations':sum(not x['warmup'] for x in rows),'warmup_observations':sum(x['warmup'] for x in rows),'timed_engine_operations':sum(x['operations'] for x in rows if not x['warmup']),'retained_observations':len(rows),'exact_corpus_hashes_verified':len(files),'no_outlier_removal':True,'unsupported_nift_modes':['parse-only','prepared-AST reuse']}
(folder/'audit.json').write_text(json.dumps(audit,indent=2)+'\n');(folder/'summary.json').write_text(json.dumps({'audit':audit,'environment':json.loads((folder/'environment.json').read_text()),'cells':summary,'worker_memory':memory},indent=2)+'\n');print(json.dumps(audit))
