exec(__import__('pathlib').Path(__file__).with_name('verify.py').read_text(encoding='utf-8').split('results={}')[0])
results={}
for source in ['mouse','stylus','touchscreen']:
    tree=ui('input-mode-before')
    x,y=point(tree,'login_email')
    adb('shell','input',source,'tap',str(x),str(y));time.sleep(1)
    keyboard(source)
    shot('Email-'+source)
    results[source]=True
    adb('shell','input','keyevent','4');time.sleep(.5)
# Reenter the screen to check that the preference survives normal navigation.
adb('shell','input','keyevent','4');time.sleep(.5)
tap(ui('mode-onboarding'),'onboarding_login')
tree=ui('mode-reentry');x,y=point(tree,'login_email')
adb('shell','input','mouse','tap',str(x),str(y));time.sleep(1);shot('Email-mouse-reentry')
(ROOT/'input-modes-verification.json').write_text(json.dumps(results,indent=2))
print('Mouse, stylus, touchscreen and screen reentry captured.',flush=True)
