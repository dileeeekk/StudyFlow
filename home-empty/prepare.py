from pathlib import Path
import xml.etree.ElementTree as E
import shutil
root=Path(__file__).resolve().parent
p=Path(r'C:\Users\admin\AndroidStudioProjects\StudyFlowApp')
a='http://schemas.android.com/apk/res/android'; app='http://schemas.android.com/apk/res-auto'
E.register_namespace('android',a);E.register_namespace('app',app);E.register_namespace('tools','http://schemas.android.com/tools')
layout=p/'app/src/main/res/layout/activity_home.xml'
old=E.parse(layout).getroot()
def write(rel,text):
 f=root/'files'/rel;f.parent.mkdir(parents=True,exist_ok=True);f.write_text(text,encoding='utf-8')
def xml(node):
 E.indent(node);return '<?xml version="1.0" encoding="utf-8"?>\n'+E.tostring(node,encoding='unicode')+'\n'
def res(rel,text):write('app/src/main/res/'+rel,text)
def text(s,size=14,color='studyflow_ink',font='regular',extra=''):
 return f'<androidx.appcompat.widget.AppCompatTextView style="@style/StudyFlow.Home.Text" android:layout_width="wrap_content" android:layout_height="wrap_content" android:text="@string/{s}" android:textSize="{size}sp" android:textColor="@color/{color}" android:fontFamily="@font/inter_{font}" {extra}/>'
strings={'fresh_label':'YOUR FRESH START','fresh_greeting':'Hello, %1$s.','fresh_focus':'A little focus, daily','fresh_no_tasks':'No completed tasks yet','fresh_no_deadlines':'No deadlines yet','fresh_zero':'0','fresh_percent':'0%','fresh_progress':'0 percent completed','fresh_setup':'Make room for your best','fresh_setup_count':'0 of 3','fresh_classes':'Add your classes','fresh_task':'Create your first task','fresh_goal':'Set a study goal','fresh_add':'Add your first task','fresh_timetable':'Set up your timetable','fresh_tasks_later':'Your tasks will appear here once task creation is available.','fresh_schedule_later':'Your classes will appear here once the timetable is available.','fresh_goal_later':'Study goals will be available in a later step.','fresh_profile':'Open your profile'}
values=E.Element('resources')
for k,v in strings.items():E.SubElement(values,'string',name=k).text=v
res('values/home_empty_strings.xml',xml(values))
res('drawable/bg_home_empty_card.xml',f'<shape xmlns:android="{a}"><solid android:color="#FFFFFF"/><corners android:radius="24dp"/></shape>')
res('drawable/bg_home_empty_button.xml',f'<ripple xmlns:android="{a}" android:color="#22FFFFFF"><item><shape><corners android:radius="16dp"/><gradient android:angle="270" android:startColor="#4564ED" android:endColor="#7952C7"/></shape></item></ripple>')
res('drawable/ic_home_empty_progress.xml',f'<shape xmlns:android="{a}" android:shape="oval"><solid android:color="#FFFFFF"/><stroke android:width="6dp" android:color="#EDF1FF"/></shape>')
res('drawable/ic_home_chevron.xml',f'<vector xmlns:android="{a}" android:width="20dp" android:height="20dp" android:viewportWidth="20" android:viewportHeight="20"><path android:pathData="M7,5 L12,10 L7,15" android:fillColor="@android:color/transparent" android:strokeColor="@color/studyflow_muted" android:strokeWidth="1.5" android:strokeLineCap="round" android:strokeLineJoin="round"/></vector>')
res('drawable/ic_home_goal.xml',f'<vector xmlns:android="{a}" android:width="22dp" android:height="22dp" android:viewportWidth="22" android:viewportHeight="22"><path android:pathData="M5,19 V3 Q8,1 11,3 Q14,5 17,3 V12 Q14,14 11,12 Q8,10 5,12" android:fillColor="@android:color/transparent" android:strokeColor="@color/studyflow_primary" android:strokeWidth="1.4" android:strokeLineCap="round" android:strokeLineJoin="round"/></vector>')
nav=next(n for n in old if n.get('{'+a+'}id')=='@+id/home_navigation')
body=f'''<androidx.constraintlayout.widget.ConstraintLayout xmlns:android="{a}" xmlns:app="{app}" android:id="@+id/home_root" android:layout_width="match_parent" android:layout_height="match_parent" android:background="@color/studyflow_register_background">
<androidx.core.widget.NestedScrollView android:id="@+id/home_scroll" android:layout_width="0dp" android:layout_height="0dp" android:fillViewport="true" android:clipToPadding="true" android:scrollbars="none" app:layout_constraintTop_toTopOf="parent" app:layout_constraintBottom_toTopOf="@id/home_navigation" app:layout_constraintStart_toStartOf="parent" app:layout_constraintEnd_toEndOf="parent">
<LinearLayout android:layout_width="match_parent" android:layout_height="wrap_content" android:orientation="vertical" android:paddingStart="24dp" android:paddingEnd="24dp" android:paddingBottom="28dp">
<RelativeLayout android:layout_width="match_parent" android:layout_height="64dp">
{text('fresh_label',10,'studyflow_primary','semibold','android:letterSpacing="0.1"')}
{text('home_greeting',26,font='bold',extra='android:id="@+id/home_greeting" android:layout_marginTop="22dp" android:layout_toStartOf="@id/home_avatar" android:layout_alignParentStart="true"')}
<androidx.appcompat.widget.AppCompatTextView android:id="@+id/home_avatar" android:layout_width="48dp" android:layout_height="48dp" android:layout_alignParentEnd="true" android:background="@drawable/bg_home_selected" android:gravity="center" android:fontFamily="@font/inter_semibold" android:textColor="@color/studyflow_primary" android:textSize="18sp" android:contentDescription="@string/fresh_profile" android:clickable="true" android:focusable="true"/>
</RelativeLayout>
<LinearLayout android:layout_width="match_parent" android:layout_height="wrap_content" android:orientation="horizontal" android:gravity="center_vertical" android:padding="20dp" android:layout_marginTop="8dp" android:background="@drawable/bg_home_empty_card">
<FrameLayout android:layout_width="84dp" android:layout_height="84dp" android:background="@drawable/ic_home_empty_progress" android:contentDescription="@string/fresh_progress">
{text('fresh_percent',25,font='bold',extra='android:layout_gravity="center" android:importantForAccessibility="no"')}
</FrameLayout><LinearLayout android:layout_width="0dp" android:layout_weight="1" android:layout_height="wrap_content" android:orientation="vertical" android:layout_marginStart="20dp">
{text('fresh_focus',15,font='semibold')}{text('fresh_no_tasks',12,'studyflow_muted',extra='android:layout_marginTop="8dp"')}{text('fresh_no_deadlines',12,'studyflow_primary',extra='android:layout_marginTop="8dp"')}
</LinearLayout></LinearLayout>
<LinearLayout android:layout_width="match_parent" android:layout_height="wrap_content" android:orientation="horizontal" android:paddingTop="22dp" android:paddingBottom="22dp">'''
for label in ['home_nav_tasks','home_nav_schedule','home_nav_notes']:
 if label=='home_nav_schedule':
  E.SubElement(values,'string',name='fresh_classes_count_label').text='Classes'; label='fresh_classes_count_label'
 body+=f'<LinearLayout android:layout_width="0dp" android:layout_weight="1" android:layout_height="wrap_content" android:orientation="vertical" android:gravity="center">{text("fresh_zero",23,font="semibold")}{text(label,11,"studyflow_muted",extra="android:layout_marginTop=\"4dp\"")}</LinearLayout>'
body+='</LinearLayout><LinearLayout android:layout_width="match_parent" android:layout_height="wrap_content" android:orientation="vertical" android:padding="18dp" android:background="@drawable/bg_home_empty_card">'
body+=f'<LinearLayout android:layout_width="match_parent" android:layout_height="wrap_content" android:orientation="horizontal" android:gravity="center_vertical">{text("fresh_setup",16,font="semibold",extra="android:layout_weight=\"1\"")}{text("fresh_setup_count",11,"studyflow_muted")}</LinearLayout>'
for id,label,icon in [('classes','fresh_classes','ic_home_schedule'),('task','fresh_task','ic_home_tasks'),('goal','fresh_goal','ic_home_goal')]:
 body+=f'<LinearLayout android:id="@+id/home_setup_{id}" android:layout_width="match_parent" android:layout_height="wrap_content" android:minHeight="56dp" android:orientation="horizontal" android:gravity="center_vertical" android:clickable="true" android:focusable="true" android:background="?attr/selectableItemBackground"><androidx.appcompat.widget.AppCompatImageView android:layout_width="22dp" android:layout_height="22dp" android:src="@drawable/{icon}" app:tint="@color/studyflow_primary" android:importantForAccessibility="no"/>{text(label,13,extra="android:layout_marginStart=\"14dp\" android:layout_weight=\"1\"")}<ImageView android:layout_width="18dp" android:layout_height="18dp" android:src="@drawable/ic_home_chevron" android:importantForAccessibility="no"/></LinearLayout>'
body+='</LinearLayout>'
for id,label,bg,color,margin in [('add','fresh_add','bg_home_empty_button','studyflow_white',20),('timetable','fresh_timetable','bg_login_card','studyflow_primary',12)]:
 body+=f'<androidx.appcompat.widget.AppCompatButton android:id="@+id/home_{id}" android:layout_width="match_parent" android:layout_height="wrap_content" android:minHeight="52dp" android:layout_marginTop="{margin}dp" android:padding="14dp" android:background="@drawable/{bg}" android:text="@string/{label}" android:textColor="@color/{color}" android:textAllCaps="false" android:textSize="14sp" android:fontFamily="@font/inter_semibold" app:backgroundTint="@null"/>'
body+='</LinearLayout></androidx.core.widget.NestedScrollView></androidx.constraintlayout.widget.ConstraintLayout>'
new=E.fromstring(body);new.append(nav);res('layout/activity_home.xml',xml(new));res('values/home_empty_strings.xml',xml(values))
# Keep the original populated design as reusable resources for the future task data.
for id,name in [('home_task_problem','item_home_task'),('home_class_card','item_home_class')]:
 node=next(n for n in old.iter() if n.get('{'+a+'}id')=='@+id/'+id)
 for n in node.iter():
  for attr in ['text','contentDescription']:
   key='{'+a+'}'+attr
   if key in n.attrib: n.set('{http://schemas.android.com/tools}'+attr,n.attrib.pop(key))
 res('layout/'+name+'.xml',xml(node))
k=p/'app/src/main/java/com/example/studyflowapp/HomeActivity.kt'
s=k.read_text(encoding='utf-8').replace('task and schedule cards still contain Figma preview data.','empty dashboard until task and timetable features are connected.')
s=s.replace('getString(R.string.auth_greeting, firstName)','getString(R.string.fresh_greeting, firstName)\n                findViewById<TextView>(R.id.home_avatar).text = firstName.take(1).uppercase()')
s=s.replace('val add = findViewById<View>(R.id.home_add_container)','')
s=s.replace('            add.updateLayoutParams<ViewGroup.MarginLayoutParams> { marginEnd = dp(24) + safe.right }','')
start=s.index('        // Enlarge small visual controls')
end=s.index('\n    }\n\n    private fun dp',start)
s=s[:start]+'''        findViewById<View>(R.id.home_avatar).setOnClickListener {
            findViewById<View>(R.id.home_tab_profile).performClick()
        }
        // UI-only actions: no demonstration tasks are created or saved.
        for ((ids, message) in listOf(
            listOf(R.id.home_add, R.id.home_setup_task, R.id.home_tab_tasks) to R.string.fresh_tasks_later,
            listOf(R.id.home_timetable, R.id.home_setup_classes, R.id.home_tab_schedule) to R.string.fresh_schedule_later,
            listOf(R.id.home_setup_goal) to R.string.fresh_goal_later
        )) {
            ids.forEach { id -> findViewById<View>(id).setOnClickListener {
                Toast.makeText(this, message, Toast.LENGTH_SHORT).show()
            } }
        }'''+s[end:]
for imp in ['android.graphics.Rect','android.view.TouchDelegate','android.view.ViewGroup','androidx.core.view.updateLayoutParams']:
 s=s.replace('import '+imp+'\n','')
write('app/src/main/java/com/example/studyflowapp/HomeActivity.kt',s)
print('Prepared empty home screen and reusable task/class layouts.')
