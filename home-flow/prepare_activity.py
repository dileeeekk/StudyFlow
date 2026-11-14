from pathlib import Path
root=Path(__file__).resolve().parent
p=Path(r'C:\Users\admin\AndroidStudioProjects\StudyFlowApp')
rel=Path('app/src/main/java/com/example/studyflowapp/HomeActivity.kt')
s=(p/rel).read_text(encoding='utf-8')
s=s.replace('class HomeActivity : NetworkActivity() {','class HomeActivity : NetworkActivity() {\n    private var planner: com.example.studyflowapp.planner.PlannerUi? = null')
s=s.replace('                root.visibility = View.VISIBLE','''                root.visibility = View.VISIBLE
                if (planner == null) {
                    planner = com.example.studyflowapp.planner.PlannerUi(this, ::returnToLogin).also {
                        it.start(savedInstanceState?.getString("planner_tab") ?: "home")
                    }
                }''')
start=s.index('        // UI-only actions:')
end=s.index('\n    }\n\n    private fun dp',start)
s=s[:start]+'''        onBackPressedDispatcher.addCallback(this, object : androidx.activity.OnBackPressedCallback(true) {
            override fun handleOnBackPressed() {
                if (planner?.back() == true) return
                isEnabled = false; onBackPressedDispatcher.onBackPressed(); isEnabled = true
            }
        })'''+s[end:]
s=s.replace('    private fun dp','''    override fun onSaveInstanceState(outState: Bundle) {
        outState.putString("planner_tab", planner?.currentTab() ?: "home")
        super.onSaveInstanceState(outState)
    }

    private fun dp''')
f=root/'files'/rel;f.parent.mkdir(parents=True,exist_ok=True);f.write_text(s,encoding='utf-8')
