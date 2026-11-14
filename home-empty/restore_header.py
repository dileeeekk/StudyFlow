from pathlib import Path
import xml.etree.ElementTree as E
import shutil
root=Path(__file__).resolve().parent
p=Path(r'C:\Users\admin\AndroidStudioProjects\StudyFlowApp')
a='http://schemas.android.com/apk/res/android'
E.register_namespace('android',a);E.register_namespace('app','http://schemas.android.com/apk/res-auto')
rel=Path('app/src/main/res/layout/activity_home.xml')
old=E.parse(root/'backup'/rel).getroot()
header=next(n for n in old.iter() if n.get('{'+a+'}id')=='@+id/home_header')
tree=E.parse(p/rel);content=tree.getroot()[0][0]
content.remove(content[0]);content.insert(0,header)
E.indent(tree)
for target in [p/rel,root/'files'/rel]:
 tree.write(target,encoding='utf-8',xml_declaration=True)
k=Path('app/src/main/java/com/example/studyflowapp/HomeActivity.kt')
s=(p/k).read_text(encoding='utf-8')
s=s.replace('getString(R.string.fresh_greeting, firstName)','getString(R.string.auth_greeting, firstName)')
s=s.replace('                findViewById<TextView>(R.id.home_avatar).text = firstName.take(1).uppercase()\n','')
s=s.replace('''        findViewById<View>(R.id.home_avatar).setOnClickListener {
            findViewById<View>(R.id.home_tab_profile).performClick()
        }
''','')
s=s.replace('        // UI-only actions:', '''        // Show the actual date rather than the date in the Figma example.
        findViewById<TextView>(R.id.home_date).text = java.text.SimpleDateFormat(
            "EEEE, MMMM d", java.util.Locale.ENGLISH
        ).format(java.util.Date()).uppercase(java.util.Locale.ENGLISH)
        // UI-only actions:''')
for target in [p/k,root/'files'/k]:target.write_text(s,encoding='utf-8')
print('Restored original header; empty dashboard retained.')
