from pathlib import Path
import json,re,subprocess,time,xml.etree.ElementTree as ET
HERE=Path(__file__).resolve().parent
ADB=r'C:\Users\admin\AppData\Local\Android\Sdk\platform-tools\adb.exe'
PROJECT=Path(r'C:\Users\admin\AndroidStudioProjects\StudyFlowApp')
def raw(*args):return subprocess.run([ADB,'-s','emulator-5554',*args],capture_output=True,check=True,timeout=40).stdout
def adb(*args):return raw(*args).decode('utf-8',errors='replace').strip()
def shot(name): (HERE/f'{name}.png').write_bytes(raw('exec-out','screencap','-p'))
def ui(name):
    adb('shell','uiautomator','dump','/sdcard/studyflow-login-qa.xml')
    raw('pull','/sdcard/studyflow-login-qa.xml',str(HERE/f'{name}.xml'))
    return ET.parse(HERE/f'{name}.xml')
def node(tree,key):return next(n for n in tree.iter('node') if n.get('resource-id','').endswith('/'+key))
def bounds(n):return list(map(int,re.findall(r'\d+',n.get('bounds'))))
def tap(tree,key):
    a,b,c,d=bounds(node(tree,key));assert c>a and d>b
    adb('shell','input','tap',str((a+c)//2),str((b+d)//2));time.sleep(.6)
def back():adb('shell','input','keyevent','4');time.sleep(.6)
def launch():
    adb('shell','am','force-stop','com.example.studyflowapp')
    adb('shell','am','start','-W','-n','com.example.studyflowapp/.MainActivity');time.sleep(2.5)
def restore_value(text):
    m=re.search(r'Override \w+: (.+)',text);return m.group(1) if m else 'reset'
size=adb('shell','wm','size');density=adb('shell','wm','density');font=adb('shell','settings','get','system','font_scale')
results={'original_size':size,'original_density':density,'original_font_scale':font}
(HERE/'emulator-settings-before-test.json').write_text(json.dumps(results,indent=2))
try:
    print(adb('install','-r',str(PROJECT/'app/build/outputs/apk/debug/app-debug.apk')),flush=True)
    adb('shell','wm','size','1170x2532');adb('shell','wm','density','480');adb('shell','settings','put','system','font_scale','1.0')
    launch();tree=ui('onboarding-0');tap(tree,'onboarding_login')
    tree=ui('login-reference');shot('Login-390x844')
    results['reference_bounds_dp']={key:[round(v/3,2) for v in bounds(node(tree,key))] for key in ['login_title','login_card','login_email','login_password','login_remember','login_submit','login_legal']}
    print('Reference Login captured.',flush=True)
    tap(tree,'login_remember');assert node(ui('unchecked'),'login_remember').get('checked')=='false'
    tap(ui('unchecked'),'login_remember');assert node(ui('checked'),'login_remember').get('checked')=='true'
    results['checkbox']=True
    tap(tree,'login_email');adb('shell','input','text','test@example.com');time.sleep(.5)
    keyboard=ui('keyboard-email');shot('Login-keyboard')
    assert node(keyboard,'login_email').get('text')=='test@example.com'
    # Navigate using IME Next, then type synthetic test text only.
    adb('shell','input','keyevent','61');time.sleep(.5)
    focused=ui('focus-next')
    if node(focused,'login_password').get('focused')!='true':tap(focused,'login_password')
    adb('shell','input','text','StudyFlow42');back()
    hidden=ui('password-hidden');assert node(hidden,'login_password').get('password')=='true'
    tap(hidden,'login_password_toggle');shown=ui('password-shown')
    assert node(shown,'login_password').get('text')=='StudyFlow42'
    assert node(shown,'login_password_toggle').get('content-desc')=='Hide password'
    tap(shown,'login_password_toggle');assert node(ui('password-hidden-again'),'login_password').get('password')=='true'
    results['password_visibility']=True
    tap(ui('submit-before'),'login_submit');node(ui('submit-after'),'login_title')
    results['submit_stays_on_login']=True
    back();tree=ui('back-onboarding');tap(tree,'onboarding_skip');node(ui('skip-login'),'login_title');back()
    tree=ui('step0')
    for i in [1,2]:tap(tree,'onboarding_get_started');tree=ui(f'step{i}')
    tap(tree,'onboarding_get_started');node(ui('final-cta-login'),'login_title')
    results['login_skip_final_cta_navigation']=True
    print('Input, eye toggle, checkbox and navigation passed.',flush=True)
    adb('shell','wm','size','720x1280');adb('shell','wm','density','320');adb('shell','settings','put','system','font_scale','1.3');time.sleep(2)
    adb('shell','input','swipe','360','1100','360','250','450');time.sleep(.6)
    small=ui('small');shot('Login-small-font130');node(small,'login_submit');node(small,'login_create_account')
    tap(small,'login_password');time.sleep(.8);small_ime=ui('small-keyboard');shot('Login-small-keyboard')
    b=bounds(node(small_ime,'login_password'));assert b[3]-b[1]>=100
    results['small_screen_keyboard_field_visible']=True
    print('360x640 dp, 130% font and keyboard passed.',flush=True)
finally:
    adb('shell','wm','size',restore_value(size));adb('shell','wm','density',restore_value(density))
    if font=='null':adb('shell','settings','delete','system','font_scale')
    else:adb('shell','settings','put','system','font_scale',font)
    launch();tap(ui('restored-onboarding'),'onboarding_login');shot('Login-emulator')
    results['settings_restored']=True
    (HERE/'verification.json').write_text(json.dumps(results,indent=2),encoding='utf-8')
