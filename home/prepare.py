from pathlib import Path
import hashlib,json,xml.etree.ElementTree as ET
from xml.sax.saxutils import escape,quoteattr

ROOT=Path(__file__).resolve().parent
PROJECT=Path(r'C:\Users\admin\AndroidStudioProjects\StudyFlowApp')
OUT=ROOT/'StudyFlowApp-home'
assert not (ROOT/'before.json').exists(), 'Preparation already run'
(ROOT/'before.json').write_text(json.dumps({str(p.relative_to(PROJECT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in (PROJECT/'app/src/main').rglob('*') if p.is_file()},indent=2))
def write(rel,text):
    p=OUT/rel;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(text,encoding='utf-8')
def res(rel,text):write('app/src/main/res/'+rel,text)
A='http://schemas.android.com/apk/res/android'
ET.register_namespace('android',A)
ET.register_namespace('app','http://schemas.android.com/apk/res-auto')
def xml(s):
    root=ET.fromstring(s);ET.indent(root,space='    ')
    return '<?xml version="1.0" encoding="utf-8"?>\n'+ET.tostring(root,encoding='unicode')+'\n'
def shape(name,color,radius,stroke=None,ripple=False):
    s=f'<shape xmlns:android="{A}"><solid android:color="{color}"/><corners android:radius="{radius}dp"/>'
    if stroke:s+=f'<stroke android:width="1dp" android:color="{stroke}"/>'
    s+='</shape>'
    if ripple:s=f'<ripple xmlns:android="{A}" android:color="#164564ED"><item>{s}</item></ripple>'
    res('drawable/'+name+'.xml',xml(s))
shape('bg_home_deadline','#F2EDFC',22,'#E6DDF6')
shape('bg_home_hourglass','#E4D9F8',12)
shape('bg_home_stats','#16FFFFFF',14,'#29FFFFFF')
shape('bg_home_high','#FCEEF0',11)
shape('bg_home_medium','#FFF5E4',11)
shape('bg_home_class','@color/studyflow_badge_background',18)
shape('bg_home_selected','@color/studyflow_badge_background',14)
shape('bg_home_bell','@color/studyflow_white',14,ripple=True)
shape('bg_home_plus','@color/studyflow_primary',18,ripple=True)
shape('bg_home_dot','@color/studyflow_primary',3)
shape('bg_home_divider','@color/studyflow_primary',2)
res('drawable/bg_home_hero.xml',xml(f'''<shape xmlns:android="{A}">
<corners android:radius="22dp"/><gradient android:angle="270" android:startColor="#273D86" android:centerColor="#4969E8" android:endColor="#9672D6" android:centerY="0.55"/></shape>'''))
res('drawable/bg_home_checkbox.xml',xml(f'''<selector xmlns:android="{A}">
<item android:state_checked="true" android:drawable="@drawable/ic_home_checked"/>
<item><shape><solid android:color="@color/studyflow_white"/><corners android:radius="8dp"/><stroke android:width="1.5dp" android:color="#C7D1E3"/></shape></item></selector>'''))
res('drawable/ic_home_checked.xml',xml(f'''<vector xmlns:android="{A}" android:width="24dp" android:height="24dp" android:viewportWidth="24" android:viewportHeight="24">
<path android:fillColor="@color/studyflow_primary" android:pathData="M8,0 H16 Q24,0 24,8 V16 Q24,24 16,24 H8 Q0,24 0,16 V8 Q0,0 8,0 Z"/>
<path android:fillColor="@android:color/transparent" android:strokeColor="@color/studyflow_white" android:strokeWidth="1.5" android:strokeLineCap="round" android:strokeLineJoin="round" android:pathData="M6,12 L10,16 L18,8"/></vector>'''))
# Keep Figma's exact path geometry; translate it into each icon's local viewport.
svg=ET.parse(Path(r'C:\Users\admin\Downloads\Home dashboard.svg'))
paths=list(svg.iter('{http://www.w3.org/2000/svg}path'))
icons=[('bell',[3],333,83,22),('progress',[4,5],266,168,80),('hourglass',[6],49,373,22),('broadcast',[7],333,762.5,19),('plus',[8],328,858,22),('home',[11],36.5,931.5,21),('schedule',[12],110.5,931.5,21),('tasks',[13],184.5,931.5,21),('notes',[14],258.5,931.5,21),('profile',[15],332.5,931.5,21)]
for name,indices,x,y,size in icons:
    s=f'<vector xmlns:android="{A}" android:width="{size}dp" android:height="{size}dp" android:viewportWidth="{size}" android:viewportHeight="{size}"><group android:translateX="{-x}" android:translateY="{-y}">'
    for i in indices:
        p=paths[i];fill=p.get('fill','@android:color/transparent');fill='#FFFFFF' if fill=='white' else fill
        attrs={'pathData':p.get('d'),'fillColor':fill}
        if p.get('fill-opacity'):attrs['fillAlpha']=p.get('fill-opacity')
        if p.get('stroke'):
            attrs.update(strokeColor='#FFFFFF' if p.get('stroke')=='white' else p.get('stroke'),strokeWidth=p.get('stroke-width','1'),strokeLineCap=p.get('stroke-linecap','butt'),strokeLineJoin='round')
        s+='<path '+' '.join('android:'+k+'='+quoteattr(v) for k,v in attrs.items())+'/>'
    res('drawable/ic_home_'+name+'.xml',xml(s+'</group></vector>'))

strings={
'home_date':'MONDAY, OCTOBER 5','home_greeting':'Hi, Aruzhan ✦','home_subtitle':'Let’s make today a little lighter.',
'home_week':'YOUR LAST 7 DAYS','home_momentum':'Great momentum.','home_hours':'9 of 12 focused hours','home_percent':'75%',
'home_done':'6 / 10 tasks done','home_streak':'✦ 5-day streak','home_next_deadline':'NEXT DEADLINE','home_problem':'Problem set 04',
'home_due':'Calculus II · Tue, 18:00','home_countdown':'1d 7h','home_remaining':'36m remaining','home_priorities':'Your priorities','home_see_all':'See all',
'home_problem_detail':'Calculus II · 1d 7h left','home_high':'High','home_diagram':'ER diagram project','home_diagram_detail':'Database Systems · 2d 13h left','home_medium':'Medium',
'home_classes':'Today’s classes','home_class_count':'4 classes','home_start':'10:00','home_end':'11:20','home_calculus':'Calculus II','home_room':'B-204 · In class now',
'home_up_next':'Up next · 13:00 Physics II · Lab C-112','home_nav_home':'Home','home_nav_schedule':'Schedule','home_nav_tasks':'Tasks','home_nav_notes':'Notes','home_nav_profile':'Profile',
'home_notifications':'Notifications','home_add':'Add','home_check_problem':'Mark Problem set 04 as completed','home_check_diagram':'Mark ER diagram project as completed',
'home_progress_description':'Weekly focus progress: 75 percent, 9 of 12 hours'
}
res('values/home_strings.xml',xml('<resources>'+''.join(f'<string name="{k}">{escape(v)}</string>' for k,v in strings.items())+'</resources>'))
res('values/home_styles.xml',xml('''<resources xmlns:android="http://schemas.android.com/apk/res/android">
<style name="Theme.StudyFlowApp.Home" parent="Theme.StudyFlowApp.Onboarding"><item name="android:windowBackground">@color/studyflow_register_background</item></style>
<style name="StudyFlow.Home.Text" parent="StudyFlow.Onboarding.Text"/>
</resources>'''))

def tag(name,attrs,children=''):
    return '<'+name+' '+attrs+('>'+children+'</'+name+'>' if children else '/>')
def tv(key,size,font='regular',color='@color/studyflow_ink',attrs='',width='wrap_content',height='wrap_content'):
    return tag('androidx.appcompat.widget.AppCompatTextView',f'android:id="@+id/{key}" style="@style/StudyFlow.Home.Text" android:layout_width="{width}" android:layout_height="{height}" android:text="@string/{key}" android:textSize="{size}sp" android:fontFamily="@font/inter_{font}" android:textColor="{color}" '+attrs)
def img(icon,size,attrs=''):
    return tag('androidx.appcompat.widget.AppCompatImageView',f'android:layout_width="{size}dp" android:layout_height="{size}dp" android:src="@drawable/ic_home_{icon}" android:importantForAccessibility="no" '+attrs)
def linear(children,attrs='',width='match_parent',height='wrap_content',orientation='vertical'):
    return tag('LinearLayout',f'android:layout_width="{width}" android:layout_height="{height}" android:orientation="{orientation}" '+attrs,children)
def frame(children,attrs='',width='match_parent',height='wrap_content'):
    return tag('FrameLayout',f'android:layout_width="{width}" android:layout_height="{height}" '+attrs,children)
ink='@color/studyflow_ink';muted='@color/studyflow_muted';primary='@color/studyflow_primary';white='@color/studyflow_white'
click='android:clickable="true" android:focusable="true" android:background="?attr/selectableItemBackground"'
header=linear(tv('home_date',11,'medium',muted,height='14dp')+tv('home_greeting',25,'bold',attrs='android:layout_marginTop="4dp"')+tv('home_subtitle',12,color=muted,attrs='android:layout_marginTop="5dp"'),'android:layout_marginEnd="56dp" android:minHeight="68dp"')
bell=tag('androidx.appcompat.widget.AppCompatImageButton',f'android:id="@+id/home_notifications" android:layout_width="44dp" android:layout_height="44dp" android:layout_gravity="end|top" android:layout_marginTop="12dp" android:src="@drawable/ic_home_bell" android:padding="11dp" android:background="@drawable/bg_home_bell" android:contentDescription="@string/home_notifications"')
dot=tag('View','android:layout_width="6dp" android:layout_height="6dp" android:layout_gravity="end|top" android:layout_marginEnd="12dp" android:layout_marginTop="22dp" android:background="@drawable/bg_home_dot" android:importantForAccessibility="no"')
content=frame(header+bell+dot,'android:id="@+id/home_header"')
hero_left=linear(tv('home_week',10,'semibold','#CCFFFFFF')+tv('home_momentum',21,'bold',white,'android:layout_marginTop="7dp"')+tv('home_hours',12,color='#DDFFFFFF',attrs='android:layout_marginTop="6dp"'),'android:layout_weight="1" android:paddingTop="7dp" android:layout_marginEnd="12dp"',width='0dp')
ring=frame(img('progress',80)+tv('home_percent',25,'bold',white,'android:layout_gravity="center"'),f'android:contentDescription="@string/home_progress_description" android:importantForAccessibility="yes" android:descendantFocusability="blocksDescendants"',width='80dp',height='80dp')
hero_row=linear(hero_left+ring,orientation='horizontal')
stats=linear(tv('home_done',11,color=white,attrs='android:layout_weight="1"',width='0dp')+tv('home_streak',11,color=white),'android:minHeight="37dp" android:gravity="center_vertical" android:paddingHorizontal="12dp" android:paddingVertical="8dp" android:layout_marginTop="18dp" android:background="@drawable/bg_home_stats"',orientation='horizontal')
content+=linear(hero_row+stats,'android:id="@+id/home_hero" android:layout_marginTop="20dp" android:padding="20dp" android:minHeight="175dp" android:background="@drawable/bg_home_hero"')
deadline_icon=frame(img('hourglass',22,'android:layout_gravity="center"'),'android:background="@drawable/bg_home_hourglass"',width='40dp',height='40dp')
deadline_text=linear(tv('home_next_deadline',10,'semibold',muted)+tv('home_problem',13,'semibold',attrs='android:layout_marginTop="4dp"')+tv('home_due',10,color=muted,attrs='android:layout_marginTop="4dp"'),'android:layout_weight="1" android:layout_marginStart="12dp" android:layout_marginEnd="8dp"',width='0dp')
deadline_right=linear(tv('home_countdown',19,'bold','#8060CC')+tv('home_remaining',10,color=muted,attrs='android:layout_marginTop="5dp"'),'android:gravity="end"',width='wrap_content')
content+=linear(deadline_icon+deadline_text+deadline_right,'android:id="@+id/home_deadline" android:gravity="center_vertical" android:padding="16dp" android:minHeight="82dp" android:layout_marginTop="20dp" android:background="@drawable/bg_home_deadline"',orientation='horizontal')
def section(title,link):
    return linear(tv(title,17,'bold',attrs='android:layout_weight="1"',width='0dp')+tv(link,12,'semibold',primary,click+' android:gravity="center_vertical"',height='match_parent'),'android:layout_marginTop="20dp" android:gravity="center_vertical"',orientation='horizontal')
content+=section('home_priorities','home_see_all')
def task(key,title,detail,badge,color):
    check=tag('androidx.appcompat.widget.AppCompatCheckBox',f'android:id="@+id/home_check_{key}" android:layout_width="24dp" android:layout_height="24dp" android:layout_marginEnd="12dp" android:button="@null" android:background="@drawable/bg_home_checkbox" android:padding="0dp" android:minWidth="0dp" android:minHeight="0dp" android:contentDescription="@string/home_check_{key}"')
    text=linear(tv(title,14,'semibold')+tv(detail,11,color=muted,attrs='android:layout_marginTop="7dp"')+tv('home_'+badge,10,'semibold',color,f'android:layout_marginTop="7dp" android:background="@drawable/bg_home_{badge}" android:paddingHorizontal="9dp" android:paddingVertical="5dp" android:minHeight="22dp" android:gravity="center"'),'android:layout_weight="1"',width='0dp')
    body=linear(check+text,'android:background="@drawable/bg_login_card" android:padding="16dp" android:minHeight="98dp"',orientation='horizontal')
    shadow=tag('ImageView','android:layout_width="match_parent" android:layout_height="match_parent" android:layout_marginStart="-20dp" android:layout_marginEnd="-20dp" android:layout_marginTop="-15dp" android:layout_marginBottom="-25dp" android:src="@drawable/home_card_shadow" android:scaleType="fitXY" android:importantForAccessibility="no"')
    return frame(shadow+body,f'android:id="@+id/home_task_{key}" android:layout_marginTop="12dp" android:clipChildren="false" android:clipToPadding="false"')
content+=task('problem','home_problem_title','home_problem_detail','high','#B94958').replace('@string/home_problem_title','@string/home_problem')
content+=task('diagram','home_diagram','home_diagram_detail','medium','#996923')
content+=section('home_classes','home_class_count')
times=linear(tv('home_start',13,'bold',primary)+tv('home_end',10,color=muted,attrs='android:layout_marginTop="7dp"'),width='62dp')
divider=tag('View','android:layout_width="3dp" android:layout_height="38dp" android:layout_marginEnd="12dp" android:background="@drawable/bg_home_divider" android:importantForAccessibility="no"')
class_text=linear(tv('home_calculus',13,'semibold')+tv('home_room',11,color=muted,attrs='android:layout_marginTop="7dp"'),'android:layout_weight="1" android:layout_marginEnd="8dp"',width='0dp')
content+=linear(times+divider+class_text+img('broadcast',19),'android:id="@+id/home_class_card" android:minHeight="66dp" android:gravity="center_vertical" android:paddingHorizontal="14dp" android:paddingVertical="14dp" android:layout_marginTop="12dp" android:background="@drawable/bg_home_class"',orientation='horizontal')
content+=tv('home_up_next',11,color=muted,attrs='android:layout_marginTop="14dp"')
scroll=tag('androidx.core.widget.NestedScrollView','android:id="@+id/home_scroll" android:layout_width="0dp" android:layout_height="0dp" android:clipToPadding="false" android:fillViewport="true" android:scrollbars="none" app:layout_constraintTop_toTopOf="parent" app:layout_constraintBottom_toTopOf="@id/home_navigation" app:layout_constraintStart_toStartOf="parent" app:layout_constraintEnd_toEndOf="parent"',linear(content,'android:paddingHorizontal="24dp" android:paddingBottom="86dp" android:clipChildren="false" android:clipToPadding="false"'))
nav=''
for key in ['home','schedule','tasks','notes','profile']:
    active=key=='home'
    pill=frame(img(key,21,'android:layout_gravity="center"'),'android:layout_gravity="center_horizontal"'+(' android:background="@drawable/bg_home_selected"' if active else ''),width='48dp',height='28dp')
    label=tv('home_nav_'+key,10,'bold' if active else 'medium',primary if active else muted,'android:layout_marginTop="4dp" android:gravity="center"',width='match_parent')
    nav+=linear(pill+label,f'android:id="@+id/home_tab_{key}" android:layout_weight="1" android:minHeight="54dp" android:paddingTop="8dp" android:paddingBottom="2dp" android:gravity="center_horizontal" android:contentDescription="@string/home_nav_{key}" android:importantForAccessibility="yes" '+click,width='0dp')
nav=linear(nav,'android:paddingHorizontal="10dp"',orientation='horizontal')
border=tag('View','android:layout_width="match_parent" android:layout_height="1dp" android:background="@color/studyflow_outline" android:importantForAccessibility="no"')
nav=tag('FrameLayout','android:id="@+id/home_navigation" android:layout_width="0dp" android:layout_height="wrap_content" android:background="@color/studyflow_white" app:layout_constraintBottom_toBottomOf="parent" app:layout_constraintStart_toStartOf="parent" app:layout_constraintEnd_toEndOf="parent"',nav+border)
fabshadow=tag('ImageView','android:layout_width="94dp" android:layout_height="94dp" android:layout_gravity="center" android:translationY="8dp" android:src="@drawable/home_plus_shadow" android:importantForAccessibility="no"')
fabbutton=tag('androidx.appcompat.widget.AppCompatImageButton','android:id="@+id/home_add" android:layout_width="54dp" android:layout_height="54dp" android:src="@drawable/ic_home_plus" android:padding="16dp" android:background="@drawable/bg_home_plus" android:contentDescription="@string/home_add"')
fab=tag('FrameLayout','android:id="@+id/home_add_container" android:layout_width="54dp" android:layout_height="54dp" android:clipChildren="false" android:clipToPadding="false" android:layout_marginEnd="24dp" android:layout_marginBottom="24dp" app:layout_constraintBottom_toTopOf="@id/home_navigation" app:layout_constraintEnd_toEndOf="parent"',fabshadow+fabbutton)
layout=f'<androidx.constraintlayout.widget.ConstraintLayout xmlns:android="{A}" xmlns:app="http://schemas.android.com/apk/res-auto" android:id="@+id/home_root" android:layout_width="match_parent" android:layout_height="match_parent" android:background="@color/studyflow_register_background" android:clipChildren="false">'+scroll+fab+nav+'</androidx.constraintlayout.widget.ConstraintLayout>'
res('layout/activity_home.xml',xml(layout))

write('app/src/main/java/com/example/studyflowapp/HomeActivity.kt','''package com.example.studyflowapp

import android.graphics.Color
import android.graphics.Rect
import android.os.Bundle
import android.view.TouchDelegate
import android.view.View
import android.view.ViewGroup
import androidx.activity.SystemBarStyle
import androidx.activity.enableEdgeToEdge
import androidx.appcompat.app.AppCompatActivity
import androidx.core.view.ViewCompat
import androidx.core.view.WindowInsetsCompat
import androidx.core.view.updateLayoutParams
import androidx.core.view.updatePadding

/** Figma preview data only. Tasks, notifications and other tabs are not connected yet. */
class HomeActivity : AppCompatActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        enableEdgeToEdge(
            statusBarStyle = SystemBarStyle.light(Color.TRANSPARENT, Color.TRANSPARENT),
            navigationBarStyle = SystemBarStyle.light(Color.TRANSPARENT, Color.rgb(23, 36, 67))
        )
        setContentView(R.layout.activity_home)
        val root = findViewById<View>(R.id.home_root)
        val scroll = findViewById<View>(R.id.home_scroll)
        val navigation = findViewById<View>(R.id.home_navigation)
        val add = findViewById<View>(R.id.home_add_container)
        ViewCompat.setOnApplyWindowInsetsListener(root) { _, insets ->
            val safe = insets.getInsets(WindowInsetsCompat.Type.systemBars() or WindowInsetsCompat.Type.displayCutout())
            scroll.updatePadding(left = safe.left, top = maxOf(safe.top, dp(44)) + dp(16), right = safe.right)
            navigation.updatePadding(left = safe.left, right = safe.right, bottom = maxOf(safe.bottom, dp(34)))
            add.updateLayoutParams<ViewGroup.MarginLayoutParams> { marginEnd = dp(24) + safe.right }
            insets
        }
        ViewCompat.requestApplyInsets(root)
        findViewById<View>(R.id.home_tab_home).isSelected = true
        // Enlarge small visual controls without changing the Figma layout.
        for (id in listOf(R.id.home_check_problem, R.id.home_check_diagram,
                R.id.home_notifications, R.id.home_see_all, R.id.home_class_count)) {
            val target = findViewById<View>(id)
            val parent = target.parent as View
            parent.post {
                val rect = Rect()
                target.getHitRect(rect)
                rect.inset(-maxOf(0, (dp(48) - rect.width()) / 2), -maxOf(0, (dp(48) - rect.height()) / 2))
                parent.touchDelegate = TouchDelegate(rect, target)
            }
        }
    }

    private fun dp(value: Int): Int = (value * resources.displayMetrics.density + 0.5f).toInt()
}
''')
for activity in ['Login','Register']:
    rel=f'app/src/main/java/com/example/studyflowapp/{activity}Activity.kt'
    t=(PROJECT/rel).read_text(encoding='utf-8')
    if 'import android.content.Intent' not in t:t=t.replace('import android.graphics.Color','import android.content.Intent\nimport android.graphics.Color')
    t=t.replace(f'class {activity}Activity : AppCompatActivity() {{',f'class {activity}Activity : AppCompatActivity() {{\n    private var openingHome = false')
    old='submit.setOnClickListener { if (formIsValid()) closeKeyboard() }'
    assert old in t
    t=t.replace(old,'''submit.setOnClickListener {
            if (formIsValid() && !openingHome) {
                openingHome = true
                closeKeyboard()
                startActivity(Intent(this, HomeActivity::class.java))
            }
        }''')
    if 'override fun onResume()' in t:t=t.replace('super.onResume()','super.onResume()\n        openingHome = false')
    else:t=t.replace('    private fun dp(','''    override fun onResume() {
        super.onResume()
        openingHome = false
    }

    private fun dp(''')
    write(rel,t)
rel='app/src/main/AndroidManifest.xml'
t=(PROJECT/rel).read_text(encoding='utf-8').replace('    </application>','''        <activity
            android:name=".HomeActivity"
            android:exported="false"
            android:theme="@style/Theme.StudyFlowApp.Home" />
    </application>''')
write(rel,t)
print('Home resources and validated form navigation prepared.')
