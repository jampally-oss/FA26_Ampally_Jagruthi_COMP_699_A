import json
import networkx as nx
from process_simulator import repository as repo
from process_simulator.graph import graph

def _truth(value):
 if value is None or value=='': return True
 return str(value).strip().lower() not in {'false','0','no','skip','disabled'}

def simulate(path,pid,scenario_id=None):
 proc=repo.process(path,pid)
 if not proc: raise LookupError('Process not found.')
 acts=repo.activities(path,pid); deps=repo.dependencies(path,pid); amap={a['id']:a for a in acts}
 g=nx.DiGraph(); g.add_nodes_from(amap)
 for d in deps:g.add_edge(d['predecessor_id'],d['successor_id'],condition=d.get('condition_expression',''))
 if not nx.is_directed_acyclic_graph(g): raise ValueError('Cannot simulate a process with circular dependencies.')
 changed={}; removed_edges=set(); added_edges=[]
 if scenario_id:
  sc=repo.scenario(path,scenario_id)
  if not sc or sc['process_id']!=pid: raise LookupError('Scenario not found for this process.')
  for c in sc['changes']:
   value=json.loads(c['new_value'])
   if c['target_type']=='activity' and c['target_id'] in amap:
    if c['change_type']=='skip': changed[c['target_id']]={'skip':bool(value)}
    elif c['change_type']=='rename': changed[c['target_id']]={'name':str(value)}
    elif c['change_type']=='condition': changed[c['target_id']]={'condition':str(value)}
   elif c['target_type']=='dependency':
    if c['change_type']=='remove':
     d=next((x for x in deps if x['id']==c['target_id']),None)
     if d: removed_edges.add((d['predecessor_id'],d['successor_id']))
    elif c['change_type']=='add' and isinstance(value,dict): added_edges.append((int(value['from']),int(value['to'])))
 for a,b in removed_edges:
  if g.has_edge(a,b):g.remove_edge(a,b)
 for a,b in added_edges:
  if a in g and b in g:g.add_edge(a,b,condition='')
 # Evaluate reachable flow from designated start or all source nodes.
 starts=[proc['start_activity_id']] if proc.get('start_activity_id') in g else [n for n in g if g.in_degree(n)==0]
 executed=set(); queue=list(starts)
 while queue:
  n=queue.pop(0)
  if n in executed or changed.get(n,{}).get('skip'): continue
  condition=changed.get(n,{}).get('condition',amap[n].get('condition_expression',''))
  if not _truth(condition): continue
  executed.add(n)
  for nxt in g.successors(n):
   edge_cond=g[n][nxt].get('condition','')
   if _truth(edge_cond):queue.append(nxt)
 return {'process':proc,'scenario':repo.scenario(path,scenario_id) if scenario_id else None,
         'executed_activities':[amap[i] for i in sorted(executed)],
         'skipped_activities':[amap[i] for i in sorted(set(amap)-executed)],
         'execution_order':[amap[i] for i in nx.topological_sort(g) if i in executed],
         'final_outputs':[amap[i] for i in sorted(executed) if amap[i]['activity_type']=='output']}

def compare(path,pid,sid):
 original=simulate(path,pid); modified=simulate(path,pid,sid)
 old={a['id'] for a in original['executed_activities']}; new={a['id'] for a in modified['executed_activities']}
 amap={a['id']:a for a in repo.activities(path,pid)}
 return {'original':original,'modified':modified,
  'executed_in_original_but_skipped': [amap[i] for i in sorted(old-new)],
  'newly_executed_in_modified':[amap[i] for i in sorted(new-old)],
  'original_outputs':original['final_outputs'],'modified_outputs':modified['final_outputs']}
