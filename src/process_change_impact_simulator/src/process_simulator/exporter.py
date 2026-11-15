from process_simulator import repository as repo

def export_process(path,pid):
 proc=repo.process(path,pid)
 if not proc: raise LookupError('Process not found.')
 acts=repo.activities(path,pid); keymap={a['id']:f"activity_{a['id']}" for a in acts}
 return {'process':{'name':proc['name'],'description':proc['description']},
 'activities':[{'key':keymap[a['id']],'name':a['name'],'description':a['description'],'activity_type':a['activity_type'],'condition_expression':a.get('condition_expression','')} for a in acts],
 'dependencies':[{'from':keymap[d['predecessor_id']],'to':keymap[d['successor_id']],'condition_expression':d.get('condition_expression','')} for d in repo.dependencies(path,pid)]}
