from pathlib import Path
import hashlib
import json
import re
import shutil
import struct
import xml.etree.ElementTree as ET

HERE=Path(__file__).resolve().parent
PROJECT=Path(r'C:\Users\admin\AndroidStudioProjects\StudyFlowApp')
PACKAGE=HERE/'StudyFlowApp-focus'
MAIN=PACKAGE/'app/src/main'

def write(rel,text):
    path=MAIN/rel
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(text.strip()+'\n',encoding='utf-8')

layout=(PROJECT/'app/src/main/res/layout/activity_onboarding_classes.xml').read_text(encoding='utf-8')
layout=layout.replace('@drawable/onboarding_classes_illustration','@drawable/onboarding_focus_illustration')
layout=layout.replace('@string/onboarding_classes_','@string/onboarding_focus_')
# The SVG has a 36px baseline step for the two-line 32px heading.
layout=layout.replace('            android:textSize="32sp"','            android:textSize="32sp"\n            app:lineHeight="36sp"',1)
start=layout.index('        <LinearLayout\n            android:id="@+id/onboarding_pagination"')
end=layout.index('        </LinearLayout>',start)+len('        </LinearLayout>')
pagination=layout[start:end]
index=0
def page_view(match):
    global index
    view=match.group(0)
    width='26' if index==2 else '7'
    state='active' if index==2 else 'inactive'
    view=re.sub(r'android:layout_width="\d+dp"',f'android:layout_width="{width}dp"',view)
    view=re.sub(r'bg_onboarding_page_(?:in)?active',f'bg_onboarding_page_{state}',view)
    index+=1
    return view
pagination=re.sub(r'<View\b[\s\S]*?/>',page_view,pagination)
assert index==3
write('res/layout/activity_onboarding_focus.xml',layout[:start]+pagination+layout[end:])

write('res/values/onboarding_focus_strings.xml',r'''
<?xml version="1.0" encoding="utf-8"?>
<resources>
    <string name="onboarding_focus_card_title">A little focus goes a long way</string>
    <string name="onboarding_focus_card_detail">Weekly focus goal · 9 of 12 hours</string>
    <string name="onboarding_focus_badge">03 / YOUR ACADEMIC LIFE, SIMPLIFIED</string>
    <string name="onboarding_focus_title">Make Time Work for\nYou</string>
    <string name="onboarding_focus_description">Build a study rhythm that fits your life. Turn\nfocused moments into goals you can actually\nreach.</string>
</resources>
''')

kotlin=(PROJECT/'app/src/main/java/com/example/studyflowapp/OnboardingActivity.kt').read_text(encoding='utf-8')
assert 'coerceIn(0, 1)' in kotlin
kotlin=kotlin.replace('coerceIn(0, 1)','coerceIn(0, 2)')
old='''            if (pageIndex == 1) R.layout.activity_onboarding_classes
            else R.layout.activity_onboarding'''
assert old in kotlin
kotlin=kotlin.replace(old,'''            when (pageIndex) {
                1 -> R.layout.activity_onboarding_classes
                2 -> R.layout.activity_onboarding_focus
                else -> R.layout.activity_onboarding
            }''')
kotlin=kotlin.replace('between the two completed onboarding layouts','between the three completed onboarding layouts')
kotlin=kotlin.replace('if (pageIndex == 0) {','if (pageIndex < 2) {')
kotlin=kotlin.replace('.putExtra(EXTRA_PAGE_INDEX, 1)','.putExtra(EXTRA_PAGE_INDEX, pageIndex + 1)')
write('java/com/example/studyflowapp/OnboardingActivity.kt',kotlin)

image=Path(r'C:\Users\admin\Downloads\Academic illustration (6).png')
assert struct.unpack('>II',image.read_bytes()[16:24])==(1026,840)
(MAIN/'res/drawable-xxhdpi').mkdir(parents=True,exist_ok=True)
shutil.copy2(image,MAIN/'res/drawable-xxhdpi/onboarding_focus_illustration.png')
for p in PACKAGE.rglob('*.xml'): ET.parse(p)
expected={}
for p in PACKAGE.rglob('*'):
    if p.is_file():
        rel=p.relative_to(PACKAGE).as_posix()
        dest=PROJECT/rel
        expected[rel]=hashlib.sha256(dest.read_bytes()).hexdigest() if dest.exists() else None
(HERE/'expected-source.json').write_text(json.dumps(expected,indent=2),encoding='utf-8')
protected={}
for p in (PROJECT/'app/src/main').rglob('*'):
    if p.is_file() and p.relative_to(PROJECT).as_posix() not in expected:
        protected[p.relative_to(PROJECT).as_posix()]=hashlib.sha256(p.read_bytes()).hexdigest()
(HERE/'protected-files.json').write_text(json.dumps(protected,indent=2),encoding='utf-8')
install=(HERE.parent/'onboarding-classes/install.ps1').read_text(encoding='utf-8').replace('StudyFlowApp-classes','StudyFlowApp-focus')
(HERE/'install.ps1').write_text(install,encoding='utf-8')
print('Prepared four files. Existing layouts and Splash are protected.')
