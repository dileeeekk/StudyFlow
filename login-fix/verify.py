from pathlib import Path
import subprocess,time,re,json,xml.etree.ElementTree as ET
ROOT=Path(__file__).resolve().parent
ADB=r'C:\Users\admin\AppData\Local\Android\Sdk\platform-tools\adb.exe'
PROJECT=Path(r'C:\Users\admin\AndroidStudioProjects\StudyFlowApp')
def raw(*a):return subprocess.run([ADB,'-s','emulator-5554',*a],capture_output=True,check=True,timeout=40).stdout
def adb(*a):return raw(*a).decode('utf-8',errors='replace')
def ui(name):
    adb('shell','uiautomator','dump','/sdcard/studyflow-login-fix.xml')
    raw('pull','/sdcard/studyflow-login-fix.xml',str(ROOT/f'{name}.xml'))
    return ET.parse(ROOT/f'{name}.xml')
def node(t,key):return next(n for n in t.iter('node') if n.get('resource-id','').endswith('/'+key))
def point(t,key):
    b=list(map(int,re.findall(r'\d+',node(t,key).get('bounds'))));return (b[0]+b[2])//2,(b[1]+b[3])//2
def tap(t,key):
    x,y=point(t,key);adb('shell','input','tap',str(x),str(y));time.sleep(1)
def shot(name):(ROOT/f'{name}.png').write_bytes(raw('exec-out','screencap','-p'))
def keyboard(name):
    state=adb('shell','dumpsys','input_method');(ROOT/f'{name}-ime.txt').write_text(state,encoding='utf-8')
    assert 'mInputShown=true' in state or 'mIsInputViewShown=true' in state, name+' no keyboard'
def launch():
    adb('shell','am','force-stop','com.example.studyflowapp')
    adb('shell','input','keyevent','3')
    adb('shell','am','start','-W','-n','com.example.studyflowapp/.MainActivity');time.sleep(2.5)
    for attempt in range(4):
        tree=ui('onboarding')
        if any(n.get('resource-id','').endswith('/onboarding_login') for n in tree.iter('node')):
            tap(tree,'onboarding_login');return
        time.sleep(1)
    raise AssertionError('Onboarding did not appear')
results={}
print(adb('install','-r',str(PROJECT/'app/build/outputs/apk/debug/app-debug.apk')),flush=True)
try:
    launch();tree=ui('empty');shot('Login-empty')
    for key in ['login_email','login_password']:assert node(tree,key).get('text','')==''
    results['both_fields_empty']=True
    tap(tree,'login_email');keyboard('email');shot('Email-keyboard')
    adb('shell','input','text','test@example.com');tree=ui('email-typed');assert node(tree,'login_email').get('text')=='test@example.com'
    adb('shell','input','keyevent','4');time.sleep(.6)
    tap(ui('email-dismissed'),'login_email');keyboard('email-reopened')
    results['email_keyboard_opens_and_reopens']=True
    adb('shell','input','keyevent','4');time.sleep(.6)
    tree=ui('before-stylus');x,y=point(tree,'login_email')
    adb('shell','input','stylus','swipe',str(x-40),str(y),str(x+40),str(y+5),'300');time.sleep(.8)
    tap(ui('after-stylus'),'login_email');keyboard('stylus-email');shot('Email-after-stylus')
    results['email_keyboard_after_stylus']=True
    adb('shell','input','keyevent','4');time.sleep(.5)
    tap(ui('before-password'),'login_password');keyboard('password');shot('Password-keyboard')
    adb('shell','input','text','StudyFlow42');adb('shell','input','keyevent','4');time.sleep(.5)
    tree=ui('password-hidden');assert node(tree,'login_password').get('password')=='true'
    tap(tree,'login_password_toggle');assert node(ui('password-visible'),'login_password').get('text')=='StudyFlow42'
    results['password_keyboard_and_toggle']=True
    print('Empty fields, email tap/reopen, stylus and password checks passed.',flush=True)
finally:
    launch();shot('Login-empty')
    (ROOT/'verification.json').write_text(json.dumps(results,indent=2),encoding='utf-8')
