from pathlib import Path
import shutil
r=Path(__file__).resolve().parent/'files/app/src/main'
k=r/'java/com/example/studyflowapp/planner'
for name in ('PlannerUi.kt','PlannerForm.kt'):
 p=k/name;s=p.read_text()
 s=s.replace('MaterialAlertDialogBuilder(activity)', 'MaterialAlertDialogBuilder(activity, R.style.StudyFlow_PlannerDialog)')
 s=s.replace('MaterialAlertDialogBuilder(requireContext())', 'MaterialAlertDialogBuilder(requireContext(), R.style.StudyFlow_PlannerDialog)')
 if name=='PlannerUi.kt':
  s=s.replace('for(id in listOf', 'for(id in listOf')
  s=s.replace('private fun open(kind:String,item:JSONObject?=null) { if(!busy)', 'private fun open(kind:String,item:JSONObject?=null) { if(!busy && vm.state.value?.data != null)')
  s=s.replace('view(id).isEnabled=!busy', 'view(id).isEnabled=!busy && vm.state.value?.data != null')
  s=s.replace('else -> "" })', 'else -> "" })')
  s=s.replace('state.error+" Your last loaded data is still shown."', 'state.error + if(state.data!=null) " Your last loaded data is still shown." else " Tap Retry to load your planner."')
  s=s.replace('row.setOnClickListener{open("lessons",item)}', '''val now=System.currentTimeMillis()
        val live=now >= (timestamp(item.optString("starts_at"))?:Long.MAX_VALUE) && now < (timestamp(item.optString("ends_at"))?:0L)
        row.findViewById<View>(R.id.planner_class_live).visibility=if(live)View.VISIBLE else View.GONE
        row.setOnClickListener{open("lessons",item)}''')
  s=s.replace('fun currentTab()=tab', 'fun refresh() { vm.load(true) }\n    fun currentTab()=tab')
 if name=='PlannerForm.kt':
  s=s.replace('vm.state.observe(this) { state ->','vm.state.removeObservers(this)\n        vm.state.observe(this) { state ->')
 p.write_text(s)
p=r/'res/layout/item_planner_field.xml';p.write_text(p.read_text().replace('@drawable/bg_login_card','@drawable/bg_login_field'))
p=r/'res/layout/item_home_class.xml';p.parent.mkdir(parents=True,exist_ok=True)
shutil.copy2(Path(__file__).resolve().parent.parent/'android/app/src/main/res/layout/item_home_class.xml',p)
p.write_text(p.read_text().replace('android:src="@drawable/ic_home_broadcast"','android:id="@+id/planner_class_live" android:src="@drawable/ic_home_broadcast"'))
p=r/'java/com/example/studyflowapp/HomeActivity.kt';s=p.read_text().replace('/** Authenticated account; empty dashboard until task and timetable features are connected. */','/** Authenticated dashboard backed by the account planner. */')
s=s.replace('    override fun onSaveInstanceState', '    override fun onResume() {\n        super.onResume()\n        planner?.refresh()\n    }\n\n    override fun onSaveInstanceState')
p.write_text(s)
