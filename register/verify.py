from pathlib import Path
import subprocess,time,re,json,xml.etree.ElementTree as ET
ROOT=Path(__file__).resolve().parent
ADB=r'C:\Users\admin\AppData\Local\Android\Sdk\platform-tools\adb.exe'
PROJECT=Path(r'C:\Users\admin\AndroidStudioProjects\StudyFlowApp')
def raw(*args):return subprocess.run([ADB,'-s','emulator-5554',*args],capture_output=True,check=True,timeout=40).stdout
def adb(*args):return raw(*args).decode('utf-8',errors='replace').strip()
def ui(name):
    adb('shell','uiautomator','dump','/sdcard/studyflow-register-qa.xml');raw('pull','/sdcard/studyflow-register-qa.xml',str(ROOT/f'{name}.xml'))
    return ET.parse(ROOT/f'{name}.xml')
def node(t,key):return next(n for n in t.iter('node') if n.get('resource-id','').endswith('/'+key))
def bounds(n):return list(map(int,re.findall(r'\d+',n.get('bounds'))))
def tap(t,key):
    a,b,c,d=bounds(node(t,key));assert c>a and d>b
    adb('shell','input','tap',str((a+c)//2),str((b+d)//2));time.sleep(.7)
def shot(name):(ROOT/f'{name}.png').write_bytes(raw('exec-out','screencap','-p'))
def back():adb('shell','input','keyevent','4');time.sleep(.7)
def launch():
    for attempt in range(3):
        adb('shell','am','force-stop','com.example.studyflowapp');adb('shell','input','keyevent','3')
        adb('shell','am','start','-W','-n','com.example.studyflowapp/.MainActivity');time.sleep(3)
        t=ui('onboarding')
        if any(n.get('resource-id','').endswith('/onboarding_login') for n in t.iter('node')):
            tap(t,'onboarding_login');return
    raise AssertionError('Onboarding unavailable after cold launch')
def keyboard(name):
    dump=adb('shell','dumpsys','input_method');(ROOT/f'{name}-ime.txt').write_text(dump,encoding='utf-8')
    assert 'mInputShown=true' in dump or 'mIsInputViewShown=true' in dump
def restore(t):
    m=re.search(r'Override \w+: (.+)',t);return m.group(1) if m else 'reset'
size=adb('shell','wm','size');density=adb('shell','wm','density');font=adb('shell','settings','get','system','font_scale')
result={'original_size':size,'original_density':density,'original_font_scale':font}
(ROOT/'emulator-settings-before.json').write_text(json.dumps(result,indent=2))
try:
    print(adb('install','-r',str(PROJECT/'app/build/outputs/apk/debug/app-debug.apk')),flush=True)
    adb('shell','wm','size','1170x2787');adb('shell','wm','density','480');adb('shell','settings','put','system','font_scale','1.0');time.sleep(2)
    launch();tap(ui('login'),'login_create_account');t=ui('register-reference');shot('Register-390x929')
    for key in ['name','email','password','university','year','group']:assert node(t,'register_'+key).get('text','')==''
    result['six_fields_empty']=True
    result['reference_bounds_dp']={key:[round(v/3,2) for v in bounds(node(t,key))] for key in ['register_title','register_card','register_name','register_email','register_password','register_university','register_year','register_group','register_submit']}
    assert node(t,'register_name').get('focused')=='false'
    print('Reference captured; six empty fields and no initial focus verified.',flush=True)
    tap(t,'register_name');keyboard('name');adb('shell','input','text','Test% sStudent'.replace('% s','%s'));back()
    t=ui('name-entered');assert node(t,'register_name').get('text')=='Test Student'
    tap(t,'register_email');keyboard('email');shot('Register-email-keyboard');adb('shell','input','text','test@example.com');back()
    t=ui('email-entered');assert node(t,'register_email').get('text')=='test@example.com'
    tap(t,'register_password');keyboard('password');adb('shell','input','text','StudyFlow42');back()
    t=ui('password-hidden');assert node(t,'register_password').get('password')=='true'
    tap(t,'register_password_toggle');t=ui('password-shown');assert node(t,'register_password').get('text')=='StudyFlow42'
    tap(t,'register_password_toggle');t=ui('password-hidden-again');assert node(t,'register_password').get('password')=='true'
    result['inputs_and_password_toggle']=True
    tap(t,'register_agreement');assert node(ui('unchecked'),'register_agreement').get('checked')=='false'
    tap(ui('unchecked'),'register_agreement');assert node(ui('checked'),'register_agreement').get('checked')=='true'
    result['agreement_toggle']=True
    tap(ui('submit-before'),'register_submit');node(ui('submit-after'),'register_title')
    tap(ui('return-before'),'register_login');node(ui('login-return'),'login_title')
    tap(ui('login-return'),'login_create_account');tap(ui('register-back-before'),'register_back');node(ui('back-login'),'login_title')
    tap(ui('back-login'),'login_create_account');t=ui('register-fresh')
    for key in ['name','email','password']:assert node(t,'register_'+key).get('text','')==''
    result['navigation_and_no_authentication']=True
    print('Text input, password, checkbox, submit and both return controls passed.',flush=True)
    adb('shell','wm','size','720x1280');adb('shell','wm','density','320');adb('shell','settings','put','system','font_scale','1.3');time.sleep(2)
    adb('shell','input','swipe','360','1080','360','250','450');time.sleep(.5)
    t=ui('small');shot('Register-small-font130');node(t,'register_submit');node(t,'register_login')
    # Scroll a little toward the form so that the password can be tapped.
    adb('shell','input','swipe','360','450','360','750','350');time.sleep(.5)
    t=ui('small-password-before');tap(t,'register_password');keyboard('small-password');time.sleep(.5)
    shot('Register-small-keyboard');t=ui('small-keyboard')
    result['small_password_bounds_px']=bounds(node(t,'register_password'))
    result['small_screen_actions_reachable']=True
    back()
    print('360x640 dp and 130% text captured.',flush=True)
finally:
    adb('shell','wm','size',restore(size));adb('shell','wm','density',restore(density))
    if font=='null':adb('shell','settings','delete','system','font_scale')
    else:adb('shell','settings','put','system','font_scale',font)
    time.sleep(1)
    # Clear temporary values via normal navigation, leaving the new screen open.
    back();t=ui('restored-login')
    if any(n.get('resource-id','').endswith('/login_create_account') for n in t.iter('node')):tap(t,'login_create_account')
    shot('Register-emulator');result['settings_restored']=True
    (ROOT/'verification.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
