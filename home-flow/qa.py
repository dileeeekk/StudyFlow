from pathlib import Path
import subprocess,time,xml.etree.ElementTree as E,re,json,urllib.request,secrets,sys
root=Path(__file__).resolve().parent
adb=r'C:\Users\admin\AppData\Local\Android\Sdk\platform-tools\adb.exe'
def run(*args): return subprocess.check_output([adb,'-s','emulator-5554',*args])
def ui():
 path='/sdcard/planner-qa-'+secrets.token_hex(4)+'.xml'
 result=run('shell','uiautomator','dump',path)
 assert b'dumped to' in result, result
 tree=E.fromstring(run('shell','cat',path))
 run('shell','rm',path)
 return tree
def find(t,key):return next((n for n in t.iter('node') if n.get('resource-id','').endswith('/'+key)),None)
def click(n):
 assert n is not None
 x,y,X,Y=map(int,re.findall(r'\d+',n.get('bounds')));run('shell','input','tap',str((x+X)//2),str((y+Y)//2));time.sleep(.4)
def tap(key):click(find(ui(),key))
def taptext(text):click(next(n for n in ui().iter('node') if n.get('text')==text))
def put(key,value):
 tap(key);run('shell','input','text',value);run('shell','input','keyevent','4')
def field(index,value):
 node=[n for n in ui().iter('node') if n.get('class')=='android.widget.EditText'][index]
 click(node)
 run('shell','input','keyevent','KEYCODE_MOVE_END')
 if node.get('text'):run('shell','input','keyevent',*(['67']*len(node.get('text'))))
 run('shell','input','text',value.replace(' ','%s'));run('shell','input','keyevent','4')
def shot(name): (root/(name+'.png')).write_bytes(run('exec-out','screencap','-p'))
def show():
 for n in ui().iter('node'):
  if n.get('text') or n.get('clickable')=='true':print(n.get('resource-id'),n.get('class'),repr(n.get('text')),n.get('bounds'))
def api(path,body=None,token=None):
 h={'Content-Type':'application/json'}
 if token:h['Authorization']='Bearer '+token
 req=urllib.request.Request('https://dileeeekk.pythonanywhere.com/api/'+path,data=json.dumps(body).encode() if body is not None else None,headers=h)
 with urllib.request.urlopen(req,timeout=30) as r:return json.load(r)
def start():
 run('shell','am','force-stop','com.example.studyflowapp');run('shell','input','keyevent','3');run('shell','input','keyevent','224');time.sleep(1)
 run('shell','am','start','-n','com.example.studyflowapp/.MainActivity');time.sleep(8)
if __name__=='__main__':
 mode=sys.argv[1]
 if mode=='setup':
  data={'email':'planner-qa-'+secrets.token_hex(5)+'@example.com','password':secrets.token_urlsafe(18),'full_name':'Maya Test','university':'Test University','terms_accepted':True}
  result=api('auth/register/',data);data.update(result)
  private=root.parent/'.handoff-local';private.mkdir(exist_ok=True);(private/'planner-qa.json').write_text(json.dumps(data))
  assert api('planner/',token=result['access'])=={'tasks':[],'lessons':[],'notes':[],'focus':[],'goal':None}
  print('Cloud planner authenticated and empty for new QA account.')
  run('install','-r',r'C:\Users\admin\AndroidStudioProjects\StudyFlowApp\app\build\outputs\apk\debug\app-debug.apk');start()
  t=ui()
  if find(t,'splash_title') is not None:start();t=ui()
  if find(t,'home_tab_profile') is not None:tap('home_tab_profile');tap('button1');time.sleep(2)
  elif find(t,'onboarding_login') is not None:tap('onboarding_login')
  put('login_email',data['email']);put('login_password',data['password']);tap('login_submit');time.sleep(6)
  shot('01-fresh');show()
 elif mode=='show':show()
 elif mode=='start':start();show()
