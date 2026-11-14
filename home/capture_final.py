from pathlib import Path
exec((Path(__file__).resolve().parent/'verify.py').read_text(encoding='utf-8').rsplit("size=adb('shell','wm','size')",1)[0])
size=adb('shell','wm','size');density=adb('shell','wm','density');font=adb('shell','settings','get','system','font_scale')
try:
    print(adb('install','-r',str(PROJECT/'app/build/outputs/apk/debug/app-debug.apk')),flush=True)
    launch();put('login_email','test@example.com');t=put('login_password','12345678')
    tap(t,'login_submit');node(ui('final-home'),'home_greeting')
    # Change display geometry only after the application has completed its cold launch.
    adb('shell','wm','size','780x2016');adb('shell','wm','density','320');adb('shell','settings','put','system','font_scale','1.0');time.sleep(3)
    t=ui('home-reference');shot('Home-390x1008')
    positions={k:[round(v/2,2) for v in bounds(node(t,k))] for k in ['home_greeting','home_hero','home_deadline','home_task_problem','home_task_diagram','home_class_card','home_up_next','home_navigation','home_add']}
    (ROOT/'reference-bounds.json').write_text(json.dumps(positions,indent=2))
    assert bounds(node(t,'home_up_next'))[3] < bounds(node(t,'home_add'))[1]
    print('Reference at 390 x 1008 dp captured.',flush=True)
    adb('shell','wm','size','720x1280');adb('shell','wm','density','320');adb('shell','settings','put','system','font_scale','1.3');time.sleep(3)
    t=ui('home-small-top');shot('Home-small-top-font130');nav=bounds(node(t,'home_navigation'))
    adb('shell','input','swipe','360','950','360','200','450');time.sleep(1)
    t=ui('home-small-bottom');shot('Home-small-bottom-font130')
    assert bounds(node(t,'home_navigation'))==nav
    a,b,c,d=bounds(node(t,'home_up_next'));assert d>b and d<bounds(node(t,'home_add'))[1]
    print('Small layout and safe scrolling captured.',flush=True)
finally:
    adb('shell','wm','size',restore(size));adb('shell','wm','density',restore(density))
    if font=='null':adb('shell','settings','delete','system','font_scale')
    else:adb('shell','settings','put','system','font_scale',font)
    time.sleep(2)
    # Return the Home scroll position to its beginning.
    adb('shell','input','swipe','540','400','540','1900','450');time.sleep(1)
    shot('Home-emulator')
