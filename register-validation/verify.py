from pathlib import Path
exec((Path(__file__).resolve().parent.parent/'register/verify.py').read_text(encoding='utf-8').split("size=adb('shell','wm','size')")[0])
print(adb('install','-r',str(PROJECT/'app/build/outputs/apk/debug/app-debug.apk')),flush=True)
launch();tap(ui('login'),'login_create_account')
def error_visible(t):return any(n.get('resource-id','').endswith('/register_password_error') for n in t.iter('node'))
t=ui('initial');assert not error_visible(t)
tap(t,'register_agreement');t=ui('unchecked');assert node(t,'register_submit').get('enabled')=='false';shot('Register-disabled')
tap(t,'register_submit');assert node(ui('disabled-tapped'),'register_submit').get('enabled')=='false'
tap(ui('disabled-tapped'),'register_agreement');assert node(ui('checked'),'register_submit').get('enabled')=='true'
tap(ui('checked'),'register_password');adb('shell','input','text','1234567');t=ui('seven');assert error_visible(t)
back();shot('Register-short-password')
tap(ui('seven-no-keyboard'),'register_password');adb('shell','input','text','8');assert not error_visible(ui('eight'))
adb('shell','input','keyevent','67');assert error_visible(ui('seven-again'))
for _ in range(7):adb('shell','input','keyevent','67')
assert not error_visible(ui('empty-again'))
back();tap(ui('before-return'),'register_login');tap(ui('returned-login'),'login_create_account');shot('Register-initial')
(ROOT/'verification.json').write_text(json.dumps({'unchecked_disables':True,'checked_enables':True,'empty_has_no_error':True,'seven_has_error':True,'eight_hides_error':True,'deletion_updates_error':True},indent=2))
print('Consent state and password lengths 0, 7, 8, 7, 0 passed.',flush=True)
