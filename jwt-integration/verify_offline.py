from pathlib import Path
exec((Path(__file__).resolve().parent/'verify_ui.py').read_text(encoding='utf-8').split('results={}')[0])
import hashlib
BACKEND=ROOT.parent/'studyflow-backend'
server_python=BACKEND/'.venv/Scripts/python.exe'
server_stopped=False

def restart_server():
    log=(BACKEND/'server-restarted.log').open('ab')
    process=subprocess.Popen([str(server_python),'-u','manage.py','runserver','127.0.0.1:8000','--noreload'],
                             cwd=BACKEND,stdout=log,stderr=subprocess.STDOUT,creationflags=subprocess.CREATE_NO_WINDOW)
    log.close();(ROOT/'backend-process-id.txt').write_text(str(process.pid))
    time.sleep(2)

try:
    email=json.loads((ROOT/'ui-test-account.json').read_text())['email']
    put_value('login_email',email);t=put_value('login_password','OrbitStudyFlow94')
    tap(t,'login_submit');wait_for('home_greeting','online-home')
    before=hashlib.sha256(raw('exec-out','run-as','com.example.studyflowapp','cat','no_backup/auth-session.bin')).hexdigest()
    process_id=int((ROOT/'backend-process-id.txt').read_text(encoding='utf-8-sig').strip())
    # Stop only the exact local development process created for this task.
    expected=str(server_python.resolve()).replace("'","''")
    command=f"$p=Get-CimInstance Win32_Process -Filter 'ProcessId={process_id}'; if ($p.ExecutablePath -ne '{expected}' -or $p.CommandLine -notmatch 'manage.py.*runserver.*127.0.0.1:8000.*--noreload') {{ throw 'Unexpected process' }}; Stop-Process -Id {process_id}"
    subprocess.run(['powershell.exe','-NoProfile','-Command',command],check=True,capture_output=True)
    server_stopped=True
    adb('shell','am','force-stop','com.example.studyflowapp');adb('shell','input','keyevent','3')
    adb('shell','am','start','-n','com.example.studyflowapp/.MainActivity');time.sleep(5)
    t=wait_for('alertTitle','offline-dialog')
    assert node(t,'alertTitle').get('text')=='Cannot load your account'
    after=hashlib.sha256(raw('exec-out','run-as','com.example.studyflowapp','cat','no_backup/auth-session.bin')).hexdigest()
    assert before==after
    shot('JWT-offline-retry')
    restart_server();server_stopped=False
    tap(t,'button1');t=wait_for('home_greeting','reconnected-home')
    tap(t,'home_tab_profile');tap(ui('logout-after-reconnect'),'button1');wait_for('login_submit','clean-login')
    (ROOT/'offline-verification.json').write_text(json.dumps({'offline_preserves_tokens':True,'retry_recovers_home':True,'server_restored':True},indent=2))
    print('Offline session preserved; retry recovered Home; server running and app signed out.',flush=True)
finally:
    if server_stopped:restart_server()
