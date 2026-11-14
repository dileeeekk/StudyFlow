exec(__import__('pathlib').Path(__file__).with_name('verify.py').read_text(encoding='utf-8').split('results={}')[0])
print(adb('install','-r',str(PROJECT/'app/build/outputs/apk/debug/app-debug.apk')),flush=True)
launch();tap(ui('email-initial'),'login_email');shot('Email-keyboard');keyboard('email-latest')
print('Email screenshot captured.',flush=True)
