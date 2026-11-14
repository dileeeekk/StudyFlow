from pathlib import Path
import json
import re
import subprocess
import time
import xml.etree.ElementTree as ET

HERE=Path(__file__).resolve().parent
ADB=r'C:\Users\admin\AppData\Local\Android\Sdk\platform-tools\adb.exe'
PROJECT=Path(r'C:\Users\admin\AndroidStudioProjects\StudyFlowApp')
TITLES=['Track Every Deadline','Never Miss a Class','Make Time Work for You']

def raw(*args):
    return subprocess.run([ADB,'-s','emulator-5554',*args],capture_output=True,check=True,timeout=30).stdout

def adb(*args): return raw(*args).decode('utf-8',errors='replace').strip()

def screenshot(name): (HERE/f'{name}.png').write_bytes(raw('exec-out','screencap','-p'))

def ui(name):
    adb('shell','uiautomator','dump','/sdcard/studyflow-focus-qa.xml')
    adb('pull','/sdcard/studyflow-focus-qa.xml',str(HERE/f'{name}.xml'))
    return ET.parse(HERE/f'{name}.xml')

def node(tree,key): return next(n for n in tree.iter('node') if n.get('resource-id','').endswith('/'+key))
def bounds(n): return [int(v) for v in re.findall(r'\d+',n.get('bounds'))]

def tap(tree,key):
    b=bounds(node(tree,key))
    assert b[2]>b[0] and b[3]>b[1]
    adb('shell','input','tap',str((b[0]+b[2])//2),str((b[1]+b[3])//2))
    time.sleep(.6)

def page(tree,index): assert ' '.join(node(tree,'onboarding_title').get('text').split())==TITLES[index]

def reset_value(text):
    m=re.search(r'Override \w+: (.+)',text)
    return m.group(1) if m else 'reset'

size=adb('shell','wm','size')
density=adb('shell','wm','density')
font=adb('shell','settings','get','system','font_scale')
results={'original_size':size,'original_density':density,'original_font_scale':font}
(HERE/'emulator-settings-before-test.json').write_text(json.dumps(results,indent=2),encoding='utf-8')
try:
    print(adb('install','-r',str(PROJECT/'app/build/outputs/apk/debug/app-debug.apk')),flush=True)
    adb('shell','am','force-stop','com.example.studyflowapp')
    results['launch']=adb('shell','am','start','-W','-n','com.example.studyflowapp/.MainActivity')
    time.sleep(2.5)
    tree=ui('page-0')
    page(tree,0)
    for index in [1,2]:
        tap(tree,'onboarding_get_started')
        tree=ui(f'page-{index}')
        page(tree,index)
    results['forward_through_all_pages']=True

    adb('shell','wm','size','1170x2577')
    adb('shell','wm','density','480')
    adb('shell','settings','put','system','font_scale','1.0')
    time.sleep(2)
    screenshot('Make-Time-Work-for-You-390x859')
    reference=ui('reference')
    page(reference,2)
    results['reference_bounds_dp']={key:[round(v/3,2) for v in bounds(node(reference,key))] for key in ['onboarding_hero','onboarding_badge','onboarding_title','onboarding_description','onboarding_pagination','onboarding_get_started','onboarding_login']}
    results['title_text']=node(reference,'onboarding_title').get('text')
    results['description_text']=node(reference,'onboarding_description').get('text')
    assert len(results['title_text'].splitlines())==2
    assert len(results['description_text'].splitlines())==3
    print('Reference 390x859 dp captured; title and paragraph breaks verified.',flush=True)

    tap(reference,'onboarding_get_started')
    final=ui('final-page-cta')
    page(final,2)
    results['final_cta_feedback_only']=True
    for index in [1,0]:
        adb('shell','input','keyevent','4')
        time.sleep(.6)
        tree=ui(f'back-{index}')
        page(tree,index)
    results['back_through_all_pages']=True
    for index in [1,2]:
        tap(tree,'onboarding_get_started')
        tree=ui(f'forward-again-{index}')
        page(tree,index)
    results['forward_after_back']=True

    adb('shell','wm','size','720x1280')
    adb('shell','wm','density','320')
    adb('shell','settings','put','system','font_scale','1.3')
    time.sleep(2)
    adb('shell','input','swipe','360','1100','360','180','450')
    time.sleep(.5)
    screenshot('Make-Time-Work-for-You-small-font130')
    small=ui('small-font130')
    for key in ['onboarding_get_started','onboarding_login']:
        b=bounds(node(small,key))
        assert b[2]>b[0] and b[3]>b[1]
    results['small_screen_actions_reachable']=True
    print('Navigation and 360x640 dp with 130% text passed.',flush=True)
finally:
    adb('shell','wm','size',reset_value(size))
    adb('shell','wm','density',reset_value(density))
    if font=='null': adb('shell','settings','delete','system','font_scale')
    else: adb('shell','settings','put','system','font_scale',font)
    time.sleep(1)
    adb('shell','input','swipe','540','400','540','1800','350')
    time.sleep(.5)
    screenshot('Make-Time-Work-for-You-emulator')
    results['settings_restored']={
        'size':adb('shell','wm','size')==size,
        'density':adb('shell','wm','density')==density,
        'font_scale':adb('shell','settings','get','system','font_scale')==font,
    }
    (HERE/'verification.json').write_text(json.dumps(results,indent=2),encoding='utf-8')
    print(json.dumps(results,indent=2),flush=True)
