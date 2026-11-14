exec(__import__('pathlib').Path(__file__).with_name('verify.py').read_text(encoding='utf-8').split('results={}')[0])
results={}
adb('shell','input','keyevent','4');time.sleep(.6)
tree=ui('empty');assert node(tree,'login_email').get('text','')=='';assert node(tree,'login_password').get('text','')==''
results['both_fields_empty']=True
tap(tree,'login_email');keyboard('email');shot('Email-keyboard')
adb('shell','input','text','test@example.com');tree=ui('email-typed');assert node(tree,'login_email').get('text')=='test@example.com'
adb('shell','input','keyevent','4');time.sleep(.5);tap(ui('reopen'),'login_email');keyboard('email-reopened');shot('Email-reopened')
results['email_keyboard_opens_and_reopens']=True
adb('shell','input','keyevent','4');time.sleep(.5);tap(ui('before-password'),'login_password');keyboard('password');shot('Password-keyboard')
adb('shell','input','text','StudyFlow42');adb('shell','input','keyevent','4');time.sleep(.5)
tree=ui('password-hidden');assert node(tree,'login_password').get('password')=='true'
tap(tree,'login_password_toggle');assert node(ui('password-visible'),'login_password').get('text')=='StudyFlow42'
results['password_keyboard_and_toggle']=True
adb('shell','input','keyevent','4');time.sleep(.6);tap(ui('back-onboarding'),'onboarding_login');tree=ui('final-empty')
assert node(tree,'login_email').get('text','')=='';assert node(tree,'login_password').get('text','')==''
shot('Login-empty');tap(tree,'login_email');keyboard('after-reentry');shot('Email-after-reentry');adb('shell','input','keyevent','4');time.sleep(.5)
results['keyboard_after_reentry']=True
(ROOT/'verification.json').write_text(json.dumps(results,indent=2),encoding='utf-8')
print('Empty fields, keyboard reopening, password toggle and screen reentry passed.',flush=True)
