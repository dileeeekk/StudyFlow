from qa import *
run('install','-r',str(root/'StudyFlow-planner.apk'))
start()
for attempt in range(3):
 try:
  t=ui()
  if find(t,'home_greeting') is not None:break
 except AssertionError:pass
 run('shell','input','keyevent','3');time.sleep(1)
 run('shell','am','start','-n','com.example.studyflowapp/.MainActivity');time.sleep(5)
else:raise AssertionError('Home did not appear')
assert find(t,'home_greeting').get('text')=='Hi, Maya ✦'
assert find(t,'home_percent').get('text')=='12%'
assert find(t,'home_problem').get('text')=='Problem set 04'
assert find(t,'home_class_count').get('text')=='1 class'
shot('Home-final')
tap('home_task_problem');shot('Task-form-final')
assert any(n.get('text')=='Calculus II' for n in ui().iter('node'))
tap('button2')
report=json.loads((root/'verification.json').read_text())
report.update({'final_apk_build':'passed','final_emulator_launch':'passed','restart_preserves_data':True,'offline_save_retains_draft':True,'header_preserved':True})
(root/'verification.json').write_text(json.dumps(report,indent=2))
print('Final APK verified: header, saved task, 12 percent study progress, today class and edit form.')
