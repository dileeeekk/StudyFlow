from pathlib import Path
exec((Path(__file__).resolve().parent.parent/'register/verify.py').read_text(encoding='utf-8').split("size=adb('shell','wm','size')")[0])
print(adb('install','-r',str(PROJECT/'app/build/outputs/apk/debug/app-debug.apk')),flush=True)
launch();tap(ui('login'),'login_create_account');t=ui('updated-register');shot('Register-university-empty')
for key in ['name','email','password','university']:assert node(t,'register_'+key).get('text','')==''
assert not any(n.get('resource-id','').endswith(('/register_year','/register_group')) for n in t.iter('node'))
assert node(t,'register_university').get('class')=='android.widget.EditText'
tap(t,'register_university');keyboard('university');adb('shell','input','text','Test%sUniversity')
t=ui('university-typed');assert node(t,'register_university').get('text')=='Test University'
shot('University-keyboard');back()
tap(ui('register-before-back'),'register_login');tap(ui('login-return'),'login_create_account')
t=ui('fresh-register');assert node(t,'register_university').get('text','')==''
shot('Register-university-empty')
(ROOT/'verification.json').write_text(json.dumps({'year_group_removed':True,'university_editable':True,'keyboard_and_text_input':True,'initially_empty':True,'navigation':True},indent=2))
print('Removed fields, empty University, keyboard, input and navigation passed.',flush=True)
