from pathlib import Path
import hashlib
import json
import shutil
import struct
import xml.etree.ElementTree as ET

HERE = Path(__file__).resolve().parent
PROJECT = Path(r'C:\Users\admin\AndroidStudioProjects\StudyFlowApp')
PACKAGE = HERE/'StudyFlowApp-classes'
MAIN = PACKAGE/'app/src/main'

def write(rel, text):
    p = MAIN/rel
    p.parent.mkdir(parents=True,exist_ok=True)
    p.write_text(text.strip()+'\n',encoding='utf-8')

layout=(PROJECT/'app/src/main/res/layout/activity_onboarding.xml').read_text(encoding='utf-8')
for old,new in {
    '@drawable/onboarding_academic_illustration':'@drawable/onboarding_classes_illustration',
    '@string/onboarding_deadline_title':'@string/onboarding_classes_card_title',
    '@string/onboarding_deadline_detail':'@string/onboarding_classes_card_detail',
    '@string/onboarding_badge':'@string/onboarding_classes_badge',
    '@string/onboarding_title':'@string/onboarding_classes_title',
    '@string/onboarding_description':'@string/onboarding_classes_description',
    'android:minWidth="207dp"':'android:minWidth="208dp"',
}.items():
    assert old in layout,old
    layout=layout.replace(old,new)

start=layout.index('        <LinearLayout\n            android:id="@+id/onboarding_pagination"')
end=layout.index('        </LinearLayout>',start)+len('        </LinearLayout>')
pagination=layout[start:end]
pagination=pagination.replace('android:layout_width="26dp"','android:layout_width="7dp"',1)
pagination=pagination.replace('@drawable/bg_onboarding_page_active','@drawable/bg_onboarding_page_inactive',1)
second='''            <View
                android:layout_width="7dp"
                android:layout_height="7dp"
                android:layout_marginStart="6dp"
                android:background="@drawable/bg_onboarding_page_inactive" />'''
assert second in pagination
pagination=pagination.replace(second,second.replace('android:layout_width="7dp"','android:layout_width="26dp"').replace('bg_onboarding_page_inactive','bg_onboarding_page_active'),1)
layout=layout[:start]+pagination+layout[end:]
write('res/layout/activity_onboarding_classes.xml',layout)

write('res/values/onboarding_classes_strings.xml',r'''
<?xml version="1.0" encoding="utf-8"?>
<resources>
    <string name="onboarding_classes_card_title">Right class. Right place.</string>
    <string name="onboarding_classes_card_detail">Calculus II · Room B-204</string>
    <string name="onboarding_classes_badge">02 / YOUR ACADEMIC LIFE, SIMPLIFIED</string>
    <string name="onboarding_classes_title">Never Miss a Class</string>
    <string name="onboarding_classes_description">See your classes, rooms and lecturers at a glance.\nArrive ready, with your day already mapped out.</string>
</resources>
''')

kotlin=(PROJECT/'app/src/main/java/com/example/studyflowapp/OnboardingActivity.kt').read_text(encoding='utf-8')
kotlin=kotlin.replace('import android.graphics.Color','import android.content.Intent\nimport android.graphics.Color',1)
kotlin=kotlin.replace('class OnboardingActivity : AppCompatActivity() {','''class OnboardingActivity : AppCompatActivity() {
    private var openingNextPage = false

    private companion object {
        const val EXTRA_PAGE_INDEX = "com.example.studyflowapp.ONBOARDING_PAGE"
    }
''',1)
kotlin=kotlin.replace('        setContentView(R.layout.activity_onboarding)','''        val pageIndex = intent.getIntExtra(EXTRA_PAGE_INDEX, 0).coerceIn(0, 1)
        setContentView(
            if (pageIndex == 1) R.layout.activity_onboarding_classes
            else R.layout.activity_onboarding
        )''',1)
kotlin=kotlin.replace('        // Buttons currently use their XML ripple feedback only.','''        // Temporary navigation between the two completed onboarding layouts.
        if (pageIndex == 0) {
            findViewById<View>(R.id.onboarding_get_started).setOnClickListener {
                if (!openingNextPage) {
                    openingNextPage = true
                    startActivity(
                        Intent(this, OnboardingActivity::class.java)
                            .putExtra(EXTRA_PAGE_INDEX, 1)
                    )
                }
            }
        }
        // Skip, Log In and the final page CTA use ripple feedback only.''',1)
kotlin=kotlin.replace('    private fun dp(value: Int): Int =','''    override fun onResume() {
        super.onResume()
        openingNextPage = false
    }

    private fun dp(value: Int): Int =''',1)
write('java/com/example/studyflowapp/OnboardingActivity.kt',kotlin)

image=Path(r'C:\Users\admin\Downloads\Academic illustration (5).png')
assert struct.unpack('>II',image.read_bytes()[16:24]) == (1026,840)
(MAIN/'res/drawable-xxhdpi').mkdir(parents=True,exist_ok=True)
shutil.copy2(image,MAIN/'res/drawable-xxhdpi/onboarding_classes_illustration.png')

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
print('Prepared 4 files; existing Splash and onboarding resources protected.')
