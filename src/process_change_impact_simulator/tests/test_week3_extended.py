import json

def make_process(client):
 p=client.post('/api/processes',json={'name':'Purchase Flow','description':'test'}).get_json(); pid=p['id']
 a=client.post(f'/api/processes/{pid}/activities',json={'name':'Submit','activity_type':'task'}).get_json()
 b=client.post(f'/api/processes/{pid}/activities',json={'name':'Approve','activity_type':'approval'}).get_json()
 c=client.post(f'/api/processes/{pid}/activities',json={'name':'Create PO','activity_type':'output'}).get_json()
 client.post(f'/api/processes/{pid}/dependencies',json={'predecessor_id':a['id'],'successor_id':b['id']})
 client.post(f'/api/processes/{pid}/dependencies',json={'predecessor_id':b['id'],'successor_id':c['id']})
 return pid,a,b,c

def test_process_crud_and_export(client):
 pid,a,b,c=make_process(client)
 assert client.patch(f'/api/processes/{pid}',json={'name':'Purchase Approval','description':'edited'}).status_code==200
 assert client.patch(f'/api/processes/{pid}/activities/{a["id"]}',json={'name':'Submit request','description':'','activity_type':'task','condition_expression':''}).status_code==200
 data=client.get(f'/api/processes/{pid}/export').get_json()
 assert data['process']['name']=='Purchase Approval' and len(data['activities'])==3

def test_impact_and_cycle_validation(client):
 pid,a,b,c=make_process(client)
 result=client.get(f'/api/processes/{pid}/activities/{a["id"]}/impact').get_json()
 assert [x['id'] for x in result['direct_downstream']]==[b['id']]
 assert [x['id'] for x in result['indirect_downstream']]==[c['id']]
 r=client.post(f'/api/processes/{pid}/dependencies',json={'predecessor_id':c['id'],'successor_id':a['id']})
 assert r.status_code==409

def test_scenario_simulation_comparison(client):
 pid,a,b,c=make_process(client)
 sc=client.post(f'/api/processes/{pid}/scenarios',json={'name':'Skip approval','changes':[{'target_type':'activity','target_id':b['id'],'change_type':'skip','new_value':True}]}).get_json()
 result=client.get(f'/api/processes/{pid}/scenarios/{sc["id"]}/compare').get_json()
 assert b['id'] in [x['id'] for x in result['executed_in_original_but_skipped']]
 assert c['id'] in [x['id'] for x in result['executed_in_original_but_skipped']]

def test_import_invalid_fields(client):
 r=client.post('/api/import',json={'process':{'name':''},'activities':[],'dependencies':[]})
 assert r.status_code==400
