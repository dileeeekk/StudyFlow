from pathlib import Path
exec((Path(__file__).resolve().parent.parent/'register/verify.py').read_text(encoding='utf-8').split("size=adb('shell','wm','size')")[0])
def visible(t,key):return any(n.get('resource-id','').endswith('/'+key) for n in t.iter('node'))
def enabled(t,key,wanted):assert node(t,key).get('enabled')==str(wanted).lower(),key
def put(key,value,old_length=0):
    tap(ui('before-input'),key)
    if old_length:
        adb('shell','input','keyevent','123')
        adb('shell','input','keyevent',*(['67']*old_length))
    if value:adb('shell','input','text',value.replace(' ','%s'))
    back()
    return ui('after-input')
print(adb('install','-r',str(PROJECT/'app/build/outputs/apk/debug/app-debug.apk')),flush=True)
results={}
launch();t=ui('login-initial');enabled(t,'login_submit',False)
assert not visible(t,'login_remember') and not visible(t,'login_password_error');shot('Login-empty-disabled')
t=put('login_password','1234567');enabled(t,'login_submit',False);assert visible(t,'login_password_error');shot('Login-short-password')
t=put('login_password','8');enabled(t,'login_submit',False);assert not visible(t,'login_password_error')
t=put('login_email','test@example.com');enabled(t,'login_submit',True)
t=put('login_email','   ',16);enabled(t,'login_submit',False)
t=put('login_email','test@example.com',3);enabled(t,'login_submit',True)
t=put('login_password','',1);enabled(t,'login_submit',False);assert visible(t,'login_password_error')
t=put('login_password','',7);enabled(t,'login_submit',False);assert not visible(t,'login_password_error')
results['login_fields_whitespace_password_boundary_and_remember_removed']=True
print('Login: missing fields, spaces, password lengths 0/7/8 and Remember me passed.',flush=True)
tap(t,'login_create_account');t=ui('register-initial');enabled(t,'register_submit',False)
values={'register_name':'Test Student','register_email':'test@example.com','register_password':'12345678','register_university':'Test University'}
for i,(key,value) in enumerate(values.items()):
    t=put(key,value);enabled(t,'register_submit',i==3)
shot('Register-valid')
for key,value in values.items():
    t=put(key,'',len(value));enabled(t,'register_submit',False)
    t=put(key,value);enabled(t,'register_submit',True)
t=put('register_university','   ',15);enabled(t,'register_submit',False)
t=put('register_university','Test University',3);enabled(t,'register_submit',True)
t=put('register_password','',1);enabled(t,'register_submit',False);assert visible(t,'register_password_error')
t=put('register_password','8');enabled(t,'register_submit',True);assert not visible(t,'register_password_error')
tap(t,'register_agreement');t=ui('register-without-consent');enabled(t,'register_submit',False);shot('Register-filled-without-consent')
tap(t,'register_agreement');enabled(ui('register-with-consent'),'register_submit',True)
results['register_every_required_field_whitespace_password_and_agreement']=True
# Return through onboarding so that synthetic input is not left in Login either.
back();back();tap(ui('onboarding-clean'),'onboarding_login');shot('Login-empty-disabled')
results['test_values_cleared']=True
(ROOT/'verification.json').write_text(json.dumps(results,indent=2))
print('Register: each missing field, spaces, short password and agreement passed.',flush=True)
