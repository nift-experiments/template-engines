"""Neutral semantic corpus and independent byte oracle; participant syntax is emitted separately."""
from pathlib import Path
import json,hashlib,html
R=Path(__file__).resolve().parents[1]
def T(s):return ('text',s)
def V(p):return ('value',p)
def L(p,n,b):return ('loop',p,n,b)
def I(p,a,b):return ('if',p,a,b)
def P(n):return ('include',n)
def lookup(d,p):
 for k in p.split('.'):d=d[k]
 return d
def oracle(nodes,data,partials):
 out=[]
 for n in nodes:
  op=n[0]
  if op=='text':out.append(n[1])
  elif op=='value':
   x=lookup(data,n[1]);out.append(str(x).lower() if isinstance(x,bool) else str(x))
  elif op=='upper':out.append(lookup(data,n[1]).upper())
  elif op=='if':out.append(oracle(n[2] if lookup(data,n[1]) else n[3],data,partials))
  elif op=='loop':
   for x in lookup(data,n[1]):out.append(oracle(n[3],dict(data,**{n[2]:x}),partials))
  elif op=='include':out.append(oracle(partials[n[1]],data,partials))
 return ''.join(out)
def emit(nodes,engine):
 out=[]
 for n in nodes:
  op=n[0];p=n[1]
  if op=='text':s=p
  elif op=='value':s={'nift':'$['+p+']','jinja':'{{ '+p+' }}','nunjucks':'{{ '+p+' }}','handlebars':'{{{'+p+'}}}','liquid':'{{ '+p+' }}'}[engine]
  elif op=='upper':s={'nift':'$['+p+'.to_upper()]','jinja':'{{ '+p+' | upper }}','nunjucks':'{{ '+p+' | upper }}','handlebars':'{{upper '+p+'}}','liquid':'{{ '+p+' | upcase }}'}[engine]
  elif op=='include':s={'nift':"@input('"+p+"')",'jinja':'{% include "'+p+'" %}','nunjucks':'{% include "'+p+'" %}','handlebars':'{{> '+p+'}}','liquid':"{% include '"+p+"' %}"}[engine]
  elif op=='if':
   a,b=emit(n[2],engine),emit(n[3],engine)
   s={'nift':'@if('+p+'){'+a+'}else{'+b+'}','jinja':'{% if '+p+' %}'+a+'{% else %}'+b+'{% endif %}','nunjucks':'{% if '+p+' %}'+a+'{% else %}'+b+'{% endif %}','handlebars':'{{#if '+p+'}}'+a+'{{else}}'+b+'{{/if}}','liquid':'{% if '+p+' %}'+a+'{% else %}'+b+'{% endif %}'}[engine]
  elif op=='loop':
   name=n[2];b=emit(n[3],engine)
   if engine=='handlebars':
    import re
    b=re.sub(r'\b'+name+r'\.', 'this.',b);s='{{#each '+p+'}}'+b+'{{/each}}'
   else:s={'nift':'@for('+name+' : '+p+'){'+b+'}','jinja':'{% for '+name+' in '+p+' %}'+b+'{% endfor %}','nunjucks':'{% for '+name+' in '+p+' %}'+b+'{% endfor %}','liquid':'{% for '+name+' in '+p+' %}'+b+'{% endfor %}'}[engine]
  out.append(s)
 return ''.join(out)
def main():
 cases=[];base={'title':'Template lab','author':{'name':'Nick','active':True},'count':7,'featured':True}
 def add(name,nodes,data=None,partials=None,renders=1,distinct=1):
  data=data or base;partials=partials or {};path=R/'corpus'/name;path.mkdir(parents=True,exist_ok=True)
  variants=[dict(data,title=data['title']+str(i),featured=bool(i%2),count=7+i) for i in range(2)]
  for i,d in enumerate(variants):
   (path/f'data{i}.json').write_text(json.dumps(d,separators=(',',':')))
   (path/f'expected{i}.txt').write_text(oracle(nodes,{'d':d},partials))
  for eng in ('nift','jinja','nunjucks','handlebars','liquid'):
   dest=path/eng;dest.mkdir(exist_ok=True)
   for k in range(distinct):(dest/f'main{k}').write_text(emit(nodes,eng)+('<!--'+str(k)+'-->' if distinct>1 else ''))
   for key,value in partials.items():(dest/key).write_text(emit(value,eng))
  cases.append({'name':name,'renders':renders,'distinct':distinct,'output_bytes':len((path/'expected0.txt').read_bytes()),'partials':len(partials)})
 row=[T('<li>'),V('item.id'),T(':'),V('item.name'),T('</li>')]
 add('literal',[T('template-engine baseline\n')])
 add('interpolation',[V('d.title'),T('|'),V('d.author.name'),T('|'),V('d.count')])
 add('condition',[I('d.featured',[T('featured')],[T('ordinary')])])
 add('nested-object',[V('d.author.name'),T('/'),V('d.title')])
 for size in (10,100,1000,10000):add('loop-'+str(size),[T('<ul>'),L('d.records','item',row),T('</ul>')],dict(base,records=[{'id':i,'name':f'record-{i}'} for i in range(size)]))
 add('nested-loops',[L('d.categories','cat',[T('<section>'),V('cat.name'),L('cat.records','item',row),T('</section>')])],dict(base,categories=[{'name':f'category-{i}','records':[{'id':j,'name':f'item-{j}'} for j in range(20)]} for i in range(10)]))
 for depth in (1,4,8):
  parts={f'p{i}':[T('<aside>'),P(f'p{i+1}') if i+1<depth else V('d.title'),T('</aside>')] for i in range(depth)}
  add('includes-'+str(depth),[T('<header>'),V('d.title'),T('</header>'),P('p0'),T('<footer>'),V('d.author.name'),T('</footer>')],partials=parts)
 article=[T('<article><h1>'),V('d.title'),T('</h1><nav>'),L('d.links','item',[T('<a href="'),V('item.url'),T('">'),V('item.name'),T('</a>')]),T('</nav>'),I('d.featured',[T('<strong>Featured</strong>')],[]),L('d.sections','item',[T('<section><h2>'),V('item.name'),T('</h2><p>'),V('item.body'),T('</p></section>')]),T('<footer>'),V('d.author.name'),T('</footer></article>')]
 add('article',article,dict(base,links=[{'url':f'/page-{i}','name':f'Page {i}'} for i in range(8)],sections=[{'name':f'Section {i}','body':'Documentation content. '*20} for i in range(10)]))
 add('collection',[L('d.records','item',row)],dict(base,records=[{'id':i,'name':f'collection-{i}'} for i in range(2000)]))
 for count in (100,1000):add('many-renders-'+str(count),[V('d.title'),T('|'),V('d.count')],renders=count)
 for count in (10,100,1000):add('many-templates-'+str(count),[T('<p>'),V('d.title'),T('</p>')],distinct=count)
 add('transform',[('upper','d.title')])
 (R/'corpus/manifest.json').write_text(json.dumps(cases,indent=2)+'\n')
 files={str(p.relative_to(R)):hashlib.sha256(p.read_bytes()).hexdigest() for p in (R/'corpus').rglob('*') if p.is_file()}
 (R/'docs/CORPUS-HASHES.json').write_text(json.dumps(files,indent=2)+'\n')
 print(len(cases),'scenarios')
if __name__=='__main__':main()
