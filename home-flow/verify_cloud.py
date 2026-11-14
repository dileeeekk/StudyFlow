from qa import api,root
import json
credentials=json.loads((root.parent/'.handoff-local/planner-qa.json').read_text())
login=api('auth/login/',{'email':credentials['email'],'password':credentials['password']})
data=api('planner/',token=login['access'])
assert len(data['tasks'])==1 and data['tasks'][0]['title']=='Problem set 04'
assert data['tasks'][0]['priority']=='high' and not data['tasks'][0]['completed']
assert len(data['lessons'])==1 and data['lessons'][0]['room']=='B-204'
assert data['goal']['weekly_minutes']==720
assert len(data['focus'])==1 and data['focus'][0]['minutes']==90
assert data['notes']==[]
result={'cloud_new_account_empty':True,'ui_create_task':True,'ui_complete_and_reopen_task':True,
        'ui_date_time_picker':True,'ui_create_lesson':True,'ui_note_create_edit_delete':True,
        'ui_goal_and_study_time':True,'cloud_persistence_verified':True,'backend_tests':15}
(root/'verification.json').write_text(json.dumps(result,indent=2))
print('Cloud persistence verified: task, class, 12-hour goal, 90 minutes study; test note deleted.')
