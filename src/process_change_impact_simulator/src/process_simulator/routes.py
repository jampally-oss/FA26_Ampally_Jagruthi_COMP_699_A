import json
from flask import Blueprint,current_app,request,jsonify,abort,render_template,redirect,url_for,flash,send_file
from io import BytesIO
from process_simulator import repository as repo
from process_simulator.process_service import create_process,add_activity,ValidationError
from process_simulator.dependency_service import add_dependency,DependencyError
from process_simulator.impact_service import analyze_activity_impact
from process_simulator.importer import import_json
from process_simulator.validators import validate_dependency_payload
from process_simulator.exporter import export_process
from process_simulator.simulation_service import simulate,compare

def register_routes(app):
 bp=Blueprint('application',__name__)
 def path(): return current_app.config['DATABASE_PATH']
 def body(): return request.get_json(silent=True) or {}
 @bp.get('/processes')
 def process_list(): return render_template('process_list.html',processes=repo.list_processes(path()))
 @bp.post('/processes')
 def process_create_form():
  try:
   x=create_process(path(),request.form.to_dict()); flash('Process saved.','success'); return redirect(url_for('application.process_detail',pid=x['id']))
  except ValueError as e: flash(str(e),'error'); return redirect(url_for('dashboard'))
 @bp.get('/processes/<int:pid>')
 def process_detail(pid):
  x=repo.process(path(),pid)
  if not x: abort(404,description='Process not found.')
  return render_template('process_detail.html',process=x,activities=repo.activities(path(),pid),dependencies=repo.dependencies(path(),pid),scenarios=repo.scenarios(path(),pid))
 @bp.post('/processes/<int:pid>/activities')
 def activity_form(pid):
  try: add_activity(path(),pid,request.form.to_dict()); flash('Activity saved.','success')
  except (ValueError,LookupError) as e: flash(str(e),'error')
  return redirect(url_for('application.process_detail',pid=pid))
 @bp.post('/processes/<int:pid>/dependencies')
 def dependency_form(pid):
  try: add_dependency(path(),pid,int(request.form['predecessor_id']),int(request.form['successor_id'])); flash('Dependency saved.','success')
  except Exception as e: flash(str(e),'error')
  return redirect(url_for('application.process_detail',pid=pid))
 @bp.get('/processes/<int:pid>/impact/<int:aid>')
 def impact_page(pid,aid):
  try:r=analyze_activity_impact(path(),pid,aid)
  except LookupError as e:abort(404,description=str(e))
  return render_template('impact_results.html',process=repo.process(path(),pid),result=r)
 @bp.post('/processes/<int:pid>/scenarios')
 def scenario_form(pid):
  try:
   sid=repo.create_scenario(path(),pid,request.form['name'],request.form.get('description',''))
   repo.add_scenario_change(path(),sid,'activity',int(request.form['activity_id']),request.form['change_type'],request.form.get('new_value','true'))
   flash('Scenario and proposed change saved.','success')
  except Exception as e: flash(str(e),'error')
  return redirect(url_for('application.process_detail',pid=pid))
 @bp.get('/processes/<int:pid>/scenarios/<int:sid>/compare')
 def scenario_compare_page(pid,sid):
  try:r=compare(path(),pid,sid)
  except (ValueError,LookupError) as e:abort(400,description=str(e))
  return render_template('comparison.html',process=repo.process(path(),pid),result=r)
 @bp.get('/api/health')
 def health():return jsonify({'status':'ok','application':'Process Change Impact Simulator'})
 @bp.post('/api/processes')
 def api_create_process():
  try:return jsonify(create_process(path(),body())),201
  except ValueError as e:abort(400,description=str(e))
 @bp.get('/api/processes')
 def api_list_processes():return jsonify(repo.list_processes(path()))
 @bp.get('/api/processes/<int:pid>')
 def api_detail(pid):
  x=repo.process(path(),pid)
  if not x:abort(404,description='Process not found.')
  x['activities']=repo.activities(path(),pid);x['dependencies']=repo.dependencies(path(),pid);return jsonify(x)
 @bp.patch('/api/processes/<int:pid>')
 def api_update_process(pid):
  d=body()
  if not d.get('name'):abort(400,description='Process name is required.')
  if not repo.update_process(path(),pid,d['name'],d.get('description','')):abort(404,description='Process not found.')
  return jsonify(repo.process(path(),pid))
 @bp.post('/api/processes/<int:pid>/activities')
 def api_add_activity(pid):
  try:
   x=add_activity(path(),pid,body());return jsonify(x),201
  except LookupError as e:abort(404,description=str(e))
  except ValueError as e:abort(400,description=str(e))
 @bp.patch('/api/processes/<int:pid>/activities/<int:aid>')
 def api_edit_activity(pid,aid):
  d=body()
  if not repo.update_activity(path(),pid,aid,d):abort(404,description='Activity not found.')
  return jsonify(next(x for x in repo.activities(path(),pid) if x['id']==aid))
 @bp.delete('/api/processes/<int:pid>/activities/<int:aid>')
 def api_delete_activity(pid,aid):
  if not repo.delete_activity(path(),pid,aid):abort(404,description='Activity not found.')
  return jsonify({'deleted':True})
 @bp.post('/api/processes/<int:pid>/dependencies')
 def api_dependency(pid):
  d=body(); errs=validate_dependency_payload(d)
  if errs:abort(400,description=' '.join(errs))
  try:return jsonify({'id':add_dependency(path(),pid,int(d['predecessor_id']),int(d['successor_id']))}),201
  except LookupError as e:abort(404,description=str(e))
  except DependencyError as e:abort(409,description=str(e))
 @bp.delete('/api/processes/<int:pid>/dependencies/<int:did>')
 def api_delete_dependency(pid,did):
  if not repo.delete_dependency(path(),pid,did):abort(404,description='Dependency not found.')
  return jsonify({'deleted':True})
 @bp.put('/api/processes/<int:pid>/endpoints')
 def api_endpoints(pid):
  d=body(); ids={a['id'] for a in repo.activities(path(),pid)}
  start=d.get('start_activity_id');end=d.get('end_activity_id')
  if start is not None and start not in ids or end is not None and end not in ids:abort(400,description='Start and end activities must belong to this process.')
  repo.set_endpoints(path(),pid,start,end);return jsonify(repo.process(path(),pid))
 @bp.get('/api/processes/<int:pid>/activities/<int:aid>/impact')
 def api_impact(pid,aid):
  try:return jsonify(analyze_activity_impact(path(),pid,aid))
  except LookupError as e:abort(404,description=str(e))
 @bp.post('/api/import')
 def api_import():
  try:return jsonify(import_json(path(),body())),201
  except ValueError as e:
   repo.log_error(path(),'import_validation',str(e));abort(400,description=str(e))
 @bp.get('/api/processes/<int:pid>/export')
 def api_export(pid):
  try:return jsonify(export_process(path(),pid))
  except LookupError as e:abort(404,description=str(e))
 @bp.post('/api/processes/<int:pid>/scenarios')
 def api_scenario(pid):
  d=body()
  if not d.get('name'):abort(400,description='Scenario name is required.')
  sid=repo.create_scenario(path(),pid,d['name'],d.get('description',''))
  changes=d.get('changes',[])
  try:
   for c in changes:repo.add_scenario_change(path(),sid,c['target_type'],int(c['target_id']),c['change_type'],c.get('new_value',True))
  except Exception as e:abort(400,description=f'Invalid scenario change: {e}')
  return jsonify(repo.scenario(path(),sid)),201
 @bp.get('/api/processes/<int:pid>/scenarios')
 def api_scenarios(pid):return jsonify(repo.scenarios(path(),pid))
 @bp.delete('/api/processes/<int:pid>/scenarios/<int:sid>')
 def api_delete_scenario(pid,sid):
  if not repo.delete_scenario(path(),pid,sid):abort(404,description='Scenario not found.')
  return jsonify({'deleted':True})
 @bp.post('/api/processes/<int:pid>/simulate')
 def api_simulate(pid):
  try:return jsonify(simulate(path(),pid,body().get('scenario_id')))
  except (ValueError,LookupError) as e:abort(400,description=str(e))
 @bp.get('/api/processes/<int:pid>/scenarios/<int:sid>/compare')
 def api_compare(pid,sid):
  try:return jsonify(compare(path(),pid,sid))
  except (ValueError,LookupError) as e:abort(400,description=str(e))
 @bp.get('/api/admin/errors')
 def admin_errors():return jsonify(repo.errors(path()))
 app.register_blueprint(bp)
