from pathlib import Path
import json
import re
import subprocess
import time
import xml.etree.ElementTree as ET

HERE = Path(__file__).resolve().parent
ADB = r'C:\Users\admin\AppData\Local\Android\Sdk\platform-tools\adb.exe'
PROJECT = Path(r'C:\Users\admin\AndroidStudioProjects\StudyFlowApp')

def adb(*args):
    p = subprocess.run([ADB, '-s', 'emulator-5554', *args], capture_output=True, text=True, encoding='utf-8', errors='replace', timeout=30)
    if p.returncode:
        raise RuntimeError(p.stdout + p.stderr)
    return p.stdout.strip()

def capture(name):
    adb('shell', 'screencap', '-p', f'/sdcard/{name}.png')
    adb('pull', f'/sdcard/{name}.png', str(HERE/f'{name}.png'))
    adb('shell', 'uiautomator', 'dump', '/sdcard/onboarding-qa.xml')
    adb('pull', '/sdcard/onboarding-qa.xml', str(HERE/f'{name}.xml'))
    return ET.parse(HERE/f'{name}.xml')

def find(tree, key):
    return next(n for n in tree.iter('node') if n.get('resource-id', '').endswith('/'+key))

def bounds(node):
    return [int(n) for n in re.findall(r'\d+', node.get('bounds'))]

def shown(tree, key):
    n = find(tree, key)
    b = bounds(n)
    return b[2] > b[0] and b[3] > b[1]

def override_or_reset(output):
    override = re.search(r'Override \w+: (.+)', output)
    return override.group(1) if override else 'reset'

size = adb('shell', 'wm', 'size')
density = adb('shell', 'wm', 'density')
font_scale = adb('shell', 'settings', 'get', 'system', 'font_scale')
results = {'original_size':size, 'original_density':density, 'original_font_scale':font_scale}
(HERE/'emulator-settings-before-test.json').write_text(json.dumps(results, indent=2), encoding='utf-8')

try:
    print(adb('install', '-r', str(PROJECT/'app/build/outputs/apk/debug/app-debug.apk')), flush=True)
    adb('shell', 'wm', 'size', '1170x2532')
    adb('shell', 'wm', 'density', '480')
    adb('shell', 'settings', 'put', 'system', 'font_scale', '1.0')
    adb('shell', 'am', 'force-stop', 'com.example.studyflowapp')
    results['launch'] = adb('shell', 'am', 'start', '-W', '-n', 'com.example.studyflowapp/.MainActivity')
    time.sleep(3)
    reference = capture('Onboarding-390x844')
    assert shown(reference, 'onboarding_get_started')
    assert shown(reference, 'onboarding_login')
    results['reference_bounds_dp'] = {
        key: [round(x/3, 2) for x in bounds(find(reference,key))]
        for key in ['onboarding_hero','onboarding_badge','onboarding_title','onboarding_description','onboarding_pagination','onboarding_get_started','onboarding_login']
    }
    print('Reference screenshot and bounds captured.', flush=True)

    # The CTA must remain on the same UI until its destination has a design.
    b = bounds(find(reference,'onboarding_get_started'))
    adb('shell','input','tap',str((b[0]+b[2])//2),str((b[1]+b[3])//2))
    resumed = adb('shell','dumpsys','activity','activities')
    results['cta_stays_on_onboarding'] = any('OnboardingActivity' in line and ('mResumedActivity' in line or 'topResumedActivity' in line) for line in resumed.splitlines())
    assert results['cta_stays_on_onboarding']

    adb('shell','wm','size','720x1280')
    adb('shell','wm','density','320')
    adb('shell','settings','put','system','font_scale','1.3')
    time.sleep(2)
    adb('shell','input','swipe','360','1100','360','250','450')
    time.sleep(1)
    small = capture('Onboarding-small-font130')
    results['small_screen_cta_visible'] = shown(small,'onboarding_get_started')
    results['small_screen_login_visible'] = shown(small,'onboarding_login')
    assert results['small_screen_cta_visible'] and results['small_screen_login_visible']
    print('360x640 dp with 130% font: both actions reachable by scrolling.',flush=True)
finally:
    adb('shell','wm','size',override_or_reset(size))
    adb('shell','wm','density',override_or_reset(density))
    if font_scale == 'null':
        adb('shell','settings','delete','system','font_scale')
    else:
        adb('shell','settings','put','system','font_scale',font_scale)
    time.sleep(2)
    adb('shell','am','force-stop','com.example.studyflowapp')
    adb('shell','am','start','-W','-n','com.example.studyflowapp/.MainActivity')
    time.sleep(3)
    capture('StudyFlow-Onboarding-emulator')
    results['settings_restored'] = {
        'size': adb('shell','wm','size') == size,
        'density': adb('shell','wm','density') == density,
        'font_scale': adb('shell','settings','get','system','font_scale') == font_scale,
    }
    (HERE/'verification.json').write_text(json.dumps(results,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps(results,ensure_ascii=False,indent=2),flush=True)
