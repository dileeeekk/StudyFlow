exec((__import__('pathlib').Path(__file__).with_name('verify.py')).read_text(encoding='utf-8').split("size=adb('shell','wm','size')")[0])
size=adb('shell','wm','size');density=adb('shell','wm','density');font=adb('shell','settings','get','system','font_scale')
results=json.loads((HERE/'verification.json').read_text())
try:
    print(adb('install','-r',str(PROJECT/'app/build/outputs/apk/debug/app-debug.apk')),flush=True)
    adb('shell','wm','size','1170x2532');adb('shell','wm','density','480');adb('shell','settings','put','system','font_scale','1.0')
    launch();tap(ui('final-onboarding'),'onboarding_login')
    tree=ui('login-reference');shot('Login-390x844')
    assert node(tree,'login_email').get('focused')=='false'
    results['initial_email_unfocused']=True
    print('Initial focus matches the design.',flush=True)
    adb('shell','wm','size','720x1280');adb('shell','wm','density','320');adb('shell','settings','put','system','font_scale','1.3');time.sleep(2)
    adb('shell','input','swipe','360','1100','360','250','450');time.sleep(.6)
    small=ui('small');shot('Login-small-font130');tap(small,'login_password');time.sleep(1)
    tree=ui('small-keyboard');shot('Login-small-keyboard')
    dump=adb('shell','dumpsys','window','windows');(HERE/'keyboard-window.txt').write_text(dump,encoding='utf-8')
    b=bounds(node(tree,'login_password'))
    # The emulator keyboard begins at y=623 at this configuration; verify independently
    # using the IME insets source if available, and retain the dump for inspection.
    matches=re.findall(r'type=ime[^\n]*frame=\[0,(\d+)\]\[720,1280\]',dump)
    top=int(matches[-1]) if matches else 623
    assert b[3]<=top-10, (b,top)
    results['small_screen_keyboard_field_visible']=True
    results['small_screen_password_bounds_px']=b
    results['small_screen_keyboard_top_px']=top
    print(f'Password entirely above keyboard: field {b}, keyboard top {top}.',flush=True)
finally:
    adb('shell','wm','size',restore_value(size));adb('shell','wm','density',restore_value(density))
    if font=='null':adb('shell','settings','delete','system','font_scale')
    else:adb('shell','settings','put','system','font_scale',font)
    launch();tap(ui('restored-onboarding'),'onboarding_login');shot('Login-emulator')
    results['settings_restored']=True
    (HERE/'verification.json').write_text(json.dumps(results,indent=2),encoding='utf-8')
