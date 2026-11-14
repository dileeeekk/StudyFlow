from pathlib import Path
exec((Path(__file__).resolve().parent.parent/'home/verify.py').read_text(encoding='utf-8').rsplit("size=adb('shell','wm','size')",1)[0])

def wait_for(key,name):
    for _ in range(6):
        t=ui(name)
        if visible(t,key):return t
        time.sleep(1)
    raise AssertionError('Missing screen/control: '+key)

def put_value(key,value,old_length=0):
    tap(ui('before-input'),key)
    if old_length:
        adb('shell','input','keyevent','123')
        adb('shell','input','keyevent',*(['67']*old_length))
    if value:adb('shell','input','text',value.replace(' ','%s'))
    back()
    return ui('after-input')

results={}
email=f'qa-ui-{int(time.time())}@example.com'
password='OrbitStudyFlow94'
(ROOT/'ui-test-account.json').write_text(json.dumps({'email':email}))
launch()
t=ui('login-empty');enabled(t,'login_submit',False)
tap(t,'login_create_account');t=ui('register-empty');enabled(t,'register_submit',False)
for key,value in [('name','Aruzhan Test'),('email',email),('password',password),('university','Test University')]:
    t=put_value('register_'+key,value)
enabled(t,'register_submit',True)
tap(t,'register_agreement');t=ui('no-consent');enabled(t,'register_submit',False)
tap(t,'register_agreement');tap(ui('register-ready'),'register_submit')
t=wait_for('home_greeting','registered-home')
assert node(t,'home_greeting').get('text')=='Hi, Aruzhan ✦'
shot('JWT-register-home');results['registration_from_ui_and_real_name']=True
print('UI registration and authenticated Home passed.',flush=True)

adb('shell','am','force-stop','com.example.studyflowapp');adb('shell','input','keyevent','3')
adb('shell','am','start','-n','com.example.studyflowapp/.MainActivity');time.sleep(6)
t=wait_for('home_greeting','restored-session');results['session_survives_process_restart']=True
tap(t,'home_tab_profile');t=ui('account-dialog');shot('JWT-account-dialog')
tap(t,'button1');t=wait_for('login_submit','logged-out')
assert node(t,'login_email').get('text')=='' and node(t,'login_password').get('text')==''
results['profile_logout_and_empty_login']=True
print('Process restart and logout passed.',flush=True)

put_value('login_email',email);t=put_value('login_password','WrongPassword94')
tap(t,'login_submit');t=wait_for('alertTitle','invalid-password')
assert node(t,'alertTitle').get('text')=='Unable to continue'
shot('JWT-invalid-password');tap(t,'button1')
results['wrong_password_does_not_open_home']=True
t=put_value('login_password',password,len('WrongPassword94'))
tap(t,'login_submit');t=wait_for('home_greeting','login-success')
assert node(t,'home_greeting').get('text')=='Hi, Aruzhan ✦'
results['real_login_from_ui']=True
shot('JWT-login-home')
print('Invalid password and real login passed.',flush=True)

# End with no active test session and empty fields for the user.
tap(t,'home_tab_profile');tap(ui('logout-dialog'),'button1');wait_for('login_submit','final-login')
shot('JWT-login-empty')
results['test_session_signed_out']=True
(ROOT/'ui-verification.json').write_text(json.dumps(results,indent=2))
