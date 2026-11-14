from pathlib import Path
import subprocess,time,xml.etree.ElementTree as E,re,json,urllib.request,secrets
root=Path(__file__).resolve().parent
adb=r'C:\Users\admin\AppData\Local\Android\Sdk\platform-tools\adb.exe'
def run(*args):return subprocess.check_output([adb,'-s','emulator-5554',*args])
def ui():
 run('shell','uiautomator','dump','/sdcard/home-empty.xml')
 return E.fromstring(run('shell','cat','/sdcard/home-empty.xml'))
def find(t,key):return next((n for n in t.iter('node') if n.get('resource-id','').endswith('/'+key)),None)
def tap(t,key):
 n=find(t,key);assert n is not None,key
 x,y,X,Y=map(int,re.findall(r'\d+',n.get('bounds')));run('shell','input','tap',str((x+X)//2),str((y+Y)//2));time.sleep(.5)
def put(key,value):
 tap(ui(),key);run('shell','input','text',value);run('shell','input','keyevent','4')
run('install','-r',r'C:\Users\admin\AndroidStudioProjects\StudyFlowApp\app\build\outputs\apk\debug\app-debug.apk')
run('shell','am','force-stop','com.example.studyflowapp')
run('shell','input','keyevent','3')
run('shell','input','keyevent','224')
time.sleep(1)
run('shell','am','start','-n','com.example.studyflowapp/.MainActivity');time.sleep(8)
t=ui()
for _ in range(2):
 if find(t,'splash_title') is None:break
 run('shell','am','force-stop','com.example.studyflowapp');run('shell','input','keyevent','3');time.sleep(1)
 run('shell','am','start','-n','com.example.studyflowapp/.MainActivity');time.sleep(8);t=ui()
if find(t,'home_tab_profile') is not None:
 tap(t,'home_tab_profile');tap(ui(),'button1');time.sleep(2)
elif find(t,'onboarding_login') is not None:tap(t,'onboarding_login')
data={'email':'empty-home-'+secrets.token_hex(5)+'@example.com','password':secrets.token_urlsafe(18),'full_name':'Maya Test','university':'Test University','terms_accepted':True}
req=urllib.request.Request('https://dileeeekk.pythonanywhere.com/api/auth/register/',data=json.dumps(data).encode(),headers={'Content-Type':'application/json'})
with urllib.request.urlopen(req,timeout=30) as r:assert r.status==201
put('login_email',data['email']);put('login_password',data['password']);tap(ui(),'login_submit');time.sleep(6)
t=ui();assert find(t,'home_greeting').get('text')=='Hello, Maya.'
texts=[n.get('text','') for n in t.iter('node')]
assert '0%' in texts and texts.count('0')==3
assert not any('Calculus' in s or 'Problem set' in s or '75%' in s for s in texts)
assert find(t,'home_add') is not None and find(t,'home_timetable') is not None
(root/'Home-empty.png').write_bytes(run('exec-out','screencap','-p'))
(root/'verification.json').write_text(json.dumps({'new_account_empty':True,'real_name':True,'zero_counters':True,'no_sample_tasks':True,'cloud_login':True},indent=2))
print('Fresh account dashboard verified; screenshot saved.')
