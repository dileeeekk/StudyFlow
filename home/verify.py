from pathlib import Path
exec((Path(__file__).resolve().parent.parent/'register/verify.py').read_text(encoding='utf-8').split("size=adb('shell','wm','size')")[0])

def visible(t,key):return any(n.get('resource-id','').endswith('/'+key) for n in t.iter('node'))
def enabled(t,key,wanted):assert node(t,key).get('enabled')==str(wanted).lower(),key
def ui(name):
    for attempt in range(3):
        output=adb('shell','uiautomator','dump','/sdcard/studyflow-home-qa.xml')
        if 'dumped to' in output:
            raw('pull','/sdcard/studyflow-home-qa.xml',str(ROOT/f'{name}.xml'))
            return ET.parse(ROOT/f'{name}.xml')
        time.sleep(2)
    raise AssertionError('UI dump unavailable: '+output)
def put(key,value):
    tap(ui('before-input'),key)
    adb('shell','input','text',value.replace(' ','%s'));back()
    return ui('after-input')

def launch():
    for attempt in range(3):
        adb('shell','am','force-stop','com.example.studyflowapp')
        adb('shell','input','keyevent','224');adb('shell','wm','dismiss-keyguard')
        adb('shell','input','keyevent','3');time.sleep(1)
        adb('shell','am','start','-n','com.example.studyflowapp/.MainActivity');time.sleep(8)
        t=ui('onboarding')
        if visible(t,'onboarding_login'):
            tap(t,'onboarding_login');return
    raise AssertionError('Onboarding unavailable after cold launch')

size=adb('shell','wm','size');density=adb('shell','wm','density');font=adb('shell','settings','get','system','font_scale')
(ROOT/'emulator-settings-before.json').write_text(json.dumps({'size':size,'density':density,'font':font}))
result={}
try:
    print(adb('install','-r',str(PROJECT/'app/build/outputs/apk/debug/app-debug.apk')),flush=True)
    adb('shell','wm','size','1170x3024');adb('shell','wm','density','480');adb('shell','settings','put','system','font_scale','1.0');time.sleep(3)
    launch();t=ui('login-empty');enabled(t,'login_submit',False)
    assert not visible(t,'login_remember') and not visible(t,'login_password_error')
    t=put('login_email','test@example.com');enabled(t,'login_submit',False)
    t=put('login_password','1234567');enabled(t,'login_submit',False);assert visible(t,'login_password_error')
    t=put('login_password','8');enabled(t,'login_submit',True);assert not visible(t,'login_password_error')
    tap(t,'login_submit');time.sleep(1);t=ui('home-reference');shot('Home-390x1008')
    node(t,'home_greeting');node(t,'home_nav_home');node(t,'home_up_next')
    result['login_validation_and_home_transition']=True
    (ROOT/'reference-bounds.json').write_text(json.dumps({k:[round(v/3,2) for v in bounds(node(t,k))] for k in ['home_greeting','home_hero','home_deadline','home_task_problem','home_task_diagram','home_class_card','home_up_next','home_navigation','home_add']},indent=2))
    tap(t,'home_check_problem');t=ui('task-checked');assert node(t,'home_check_problem').get('checked')=='true'
    tap(t,'home_check_problem');assert node(ui('task-unchecked'),'home_check_problem').get('checked')=='false'
    result['temporary_checkbox_feedback']=True
    print('Login validation, Home transition and checkbox passed; reference screenshot saved.',flush=True)
    back();tap(ui('login-return'),'login_create_account');t=ui('register-empty');enabled(t,'register_submit',False)
    for key,value in [('name','Test Student'),('email','test@example.com'),('password','12345678'),('university','Test University')]:t=put('register_'+key,value)
    enabled(t,'register_submit',True)
    tap(t,'register_agreement');t=ui('register-no-consent');enabled(t,'register_submit',False)
    tap(t,'register_agreement');t=ui('register-consent');enabled(t,'register_submit',True)
    tap(t,'register_submit');node(ui('home-from-register'),'home_greeting')
    result['register_validation_and_home_transition']=True
    print('Register validation, agreement and Home transition passed.',flush=True)
    adb('shell','wm','size','720x1280');adb('shell','wm','density','320');adb('shell','settings','put','system','font_scale','1.3');time.sleep(3)
    t=ui('home-small-top');shot('Home-small-top-font130');nav=bounds(node(t,'home_navigation'))
    adb('shell','input','swipe','360','950','360','200','450');time.sleep(1)
    t=ui('home-small-bottom');shot('Home-small-bottom-font130')
    assert bounds(node(t,'home_navigation'))==nav
    node(t,'home_up_next');node(t,'home_add');node(t,'home_nav_profile')
    result['small_screen_scrolling_and_fixed_navigation']=True
    print('Small-screen scrolling and fixed navigation passed.',flush=True)
finally:
    adb('shell','wm','size',restore(size));adb('shell','wm','density',restore(density))
    if font=='null':adb('shell','settings','delete','system','font_scale')
    else:adb('shell','settings','put','system','font_scale',font)
    time.sleep(2)
    shot('Home-emulator')
    result['emulator_settings_restored']=True
    (ROOT/'verification.json').write_text(json.dumps(result,indent=2))
