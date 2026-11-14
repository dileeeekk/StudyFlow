from pathlib import Path
import subprocess
import time
import json

HERE = Path(__file__).resolve().parent
ADB = r'C:\Users\admin\AppData\Local\Android\Sdk\platform-tools\adb.exe'

def adb(*args):
    return subprocess.run([ADB,'-s','emulator-5554',*args],capture_output=True,check=True,timeout=30).stdout

def screenshot(name):
    (HERE/name).write_bytes(adb('exec-out','screencap','-p'))

print(adb('install','-r',r'C:\Users\admin\AndroidStudioProjects\StudyFlowApp\app\build\outputs\apk\debug\app-debug.apk').decode(),flush=True)
adb('shell','am','force-stop','com.example.studyflowapp')
start=adb('shell','am','start','-W','-n','com.example.studyflowapp/.MainActivity').decode()
t=time.monotonic()
time.sleep(.15)
screenshot('Splash-visible-early.png')
first=time.monotonic()-t
time.sleep(max(0,.85-(time.monotonic()-t)))
screenshot('Splash-visible-later.png')
second=time.monotonic()-t
time.sleep(1.5)
screenshot('Onboarding-after-splash.png')
activity=adb('shell','dumpsys','activity','activities').decode()
resumed=[line.strip() for line in activity.splitlines() if 'ResumedActivity' in line]
result={'launch':start,'first_capture_after_launch_s':round(first,3),'second_capture_after_launch_s':round(second,3),'resumed':resumed}
(HERE/'verification.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
print(json.dumps(result,indent=2),flush=True)
