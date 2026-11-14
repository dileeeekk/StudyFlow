package com.example.studyflowapp.planner

import android.graphics.Color
import android.graphics.Paint
import android.view.View
import android.widget.*
import androidx.appcompat.app.AppCompatActivity
import androidx.lifecycle.ViewModelProvider
import com.example.studyflowapp.R
import com.google.android.material.dialog.MaterialAlertDialogBuilder
import com.google.android.material.progressindicator.CircularProgressIndicator
import org.json.JSONObject
import java.text.SimpleDateFormat
import java.util.*

/** Binds real account data to the original XML cards and fresh-account screen. */
class PlannerUi(private val activity: AppCompatActivity, private val expired: () -> Unit) {
    private val vm=ViewModelProvider(activity)[PlannerViewModel::class.java]
    private var data=JSONObject()
    private var tab="home"
    private var busy=false
    private fun view(id:Int):View=activity.findViewById(id)
    private fun text(id:Int,value:String) { activity.findViewById<TextView>(id).text=value }
    private fun list(key:String):List<JSONObject> { val a=data.optJSONArray(key)?:return emptyList();return (0 until a.length()).map{a.getJSONObject(it)} }
    private fun open(kind:String,item:JSONObject?=null) { if(!busy)PlannerForm.show(activity,kind,item) }
    fun start(initialTab:String="home") {
        tab=initialTab
        val actions=mapOf(R.id.home_add to "tasks",R.id.home_setup_task to "tasks",R.id.home_setup_classes to "lessons",R.id.home_timetable to "lessons",R.id.home_setup_goal to "goal")
        actions.forEach { (id,kind)->view(id).setOnClickListener { open(kind,if(kind=="goal")data.optJSONObject("goal") else null) } }
        mapOf(R.id.home_tab_home to "home",R.id.home_tab_tasks to "tasks",R.id.home_tab_schedule to "lessons",R.id.home_tab_notes to "notes").forEach { (id,key)->view(id).setOnClickListener { select(key) } }
        view(R.id.home_see_all).setOnClickListener { select("tasks") }
        view(R.id.home_class_count).setOnClickListener { select("lessons") }
        view(R.id.home_hero).setOnClickListener { studyMenu() }
        view(R.id.planner_retry).setOnClickListener { vm.load(true) }
        view(R.id.planner_add).setOnClickListener {
            if(tab=="home")MaterialAlertDialogBuilder(activity).setTitle("Add to StudyFlow").setItems(arrayOf("Task","Class","Note","Study time","Weekly goal")) { _,i ->
                val kind=listOf("tasks","lessons","notes","focus","goal")[i];open(kind,if(kind=="goal")data.optJSONObject("goal") else null)
            }.show() else open(tab)
        }
        view(R.id.home_notifications).setOnClickListener { deadlines() }
        vm.state.observe(activity) { state ->
            busy=state.busy
            if(state.expired) { expired();return@observe }
            state.data?.let { data=it }
            text(R.id.planner_status,when { state.busy -> "Syncing your planner…";state.error!=null -> state.error+" Your last loaded data is still shown.";else -> "" })
            view(R.id.planner_status).visibility=if(state.busy||state.error!=null)View.VISIBLE else View.GONE
            view(R.id.planner_retry).visibility=if(state.error!=null&&!busy)View.VISIBLE else View.GONE
            render()
        }
        vm.load()
    }
    fun currentTab()=tab
    fun back():Boolean { if(tab=="home")return false;select("home");return true }
    private fun select(key:String) { tab=key;render();activity.findViewById<androidx.core.widget.NestedScrollView>(R.id.home_scroll).smoothScrollTo(0,0) }
    private fun render() {
        val tasks=list("tasks");val lessons=list("lessons");val notes=list("notes");val focus=list("focus")
        val goal=data.optJSONObject("goal")
        val populated=tasks.isNotEmpty()||lessons.isNotEmpty()||notes.isNotEmpty()||focus.isNotEmpty()||goal!=null
        view(R.id.planner_empty).visibility=if(tab=="home"&&!populated)View.VISIBLE else View.GONE
        view(R.id.planner_populated).visibility=if(tab=="home"&&populated)View.VISIBLE else View.GONE
        view(R.id.planner_collection).visibility=if(tab!="home")View.VISIBLE else View.GONE
        view(R.id.planner_add_container).visibility=if(populated||tab!="home")View.VISIBLE else View.GONE
        for(id in listOf(R.id.home_add,R.id.home_timetable,R.id.home_setup_task,R.id.home_setup_classes,R.id.home_setup_goal,R.id.planner_add))view(id).isEnabled=!busy
        val keys=listOf("home","lessons","tasks","notes")
        val navIds=listOf(R.id.home_tab_home,R.id.home_tab_schedule,R.id.home_tab_tasks,R.id.home_tab_notes)
        navIds.forEachIndexed { i,id ->
            val group=view(id) as LinearLayout;group.isSelected=tab==keys[i]
            group.getChildAt(0).setBackgroundResource(if(tab==keys[i])R.drawable.bg_home_selected else android.R.color.transparent)
            (group.getChildAt(1) as TextView).setTextColor(Color.parseColor(if(tab==keys[i])"#4564ED" else "#66728B"))
        }
        text(R.id.planner_count_tasks,tasks.size.toString());text(R.id.planner_count_lessons,lessons.size.toString());text(R.id.planner_count_notes,notes.size.toString())
        text(R.id.planner_setup_count,"${listOf(tasks.isNotEmpty(),lessons.isNotEmpty(),goal!=null).count{it}} of 3")
        if(tab!="home") {
            text(R.id.planner_collection_title,when(tab){"tasks"->"Your tasks";"lessons"->"Your timetable";"focus"->"Study history";else->"Your notes"})
            val items=when(tab){"tasks"->tasks.sortedWith(compareBy<JSONObject>{it.optBoolean("completed")}.thenBy{timestamp(it.optString("due_at"))?:0L});"lessons"->lessons.sortedBy{timestamp(it.optString("starts_at"))};"focus"->focus.sortedByDescending{it.optString("date")};else->notes.reversed()}
            text(R.id.planner_collection_hint,if(items.isEmpty())"Nothing here yet. Tap + to add your first item." else "${items.size} items · Tap a card to edit")
            val parent=activity.findViewById<LinearLayout>(R.id.planner_collection_list);parent.removeAllViews()
            items.forEach { item -> when(tab){"tasks"->taskCard(parent,item);"lessons"->classCard(parent,item);else->noteCard(parent,if(tab=="focus")"${item.optInt("minutes")} minutes" else item.optString("title"),if(tab=="focus")item.optString("date") else item.optString("body")){open(tab,item)}} }
            return
        }
        if(!populated)return
        val done=tasks.count{it.optBoolean("completed")}
        val today=day(System.currentTimeMillis());val start=Calendar.getInstance().apply { add(Calendar.DAY_OF_YEAR,-6) }.let{day(it.timeInMillis)}
        val minutes=focus.filter{it.optString("date") in start..today}.sumOf{it.optInt("minutes")}
        val target=goal?.optInt("weekly_minutes")?:0
        val percent=if(target>0)(minutes*100/target).coerceIn(0,100) else if(tasks.isNotEmpty())done*100/tasks.size else 0
        text(R.id.home_week,if(target>0)"YOUR LAST 7 DAYS" else "YOUR TASK PROGRESS")
        text(R.id.home_momentum,when { percent>=75 -> "Great momentum.";percent>0 -> "Keep it flowing.";else -> "A fresh start." })
        text(R.id.home_hours,if(target>0)"${hours(minutes)} of ${hours(target)} focused hours" else "$done of ${tasks.size} tasks completed")
        text(R.id.home_percent,"$percent%")
        activity.findViewById<CircularProgressIndicator>(R.id.planner_ring).setProgressCompat(percent,false)
        (view(R.id.planner_ring).parent as View).contentDescription="$percent percent completed"
        text(R.id.home_done,"$done / ${tasks.size} tasks done")
        val days=(focus.map{it.optString("date")}+tasks.filter{it.optBoolean("completed")}.mapNotNull{timestamp(it.optString("completed_at"))?.let(::day)}).toSet()
        val c=Calendar.getInstance();if(today !in days)c.add(Calendar.DAY_OF_YEAR,-1)
        var streak=0;while(day(c.timeInMillis) in days){streak++;c.add(Calendar.DAY_OF_YEAR,-1)}
        text(R.id.home_streak,"✦ $streak-day streak")
        val pending=tasks.filter{!it.optBoolean("completed")}.sortedBy{timestamp(it.optString("due_at"))?:Long.MAX_VALUE}
        val next=pending.firstOrNull()
        text(R.id.home_problem,next?.optString("title")?:"No deadlines yet")
        text(R.id.home_due,if(next!=null)next.optString("subject") else "Add a task to plan ahead")
        text(R.id.home_countdown,if(next!=null)remaining(next.optString("due_at")) else "—")
        text(R.id.home_remaining,if(next!=null)format(next.optString("due_at"),"d MMM, HH:mm") else "")
        view(R.id.home_deadline).setOnClickListener { if(next!=null)open("tasks",next) else open("tasks") }
        val priorities=activity.findViewById<LinearLayout>(R.id.planner_priority_list);priorities.removeAllViews()
        if(pending.isEmpty())noteCard(priorities,"All clear","Add a task when you’re ready."){open("tasks")}
        else pending.take(3).forEach{taskCard(priorities,it)}
        val todays=lessons.filter{timestamp(it.optString("starts_at"))?.let(::day)==today}.sortedBy{timestamp(it.optString("starts_at"))}
        text(R.id.home_class_count,"${todays.size} classes")
        val classes=activity.findViewById<LinearLayout>(R.id.planner_today_list);classes.removeAllViews()
        if(todays.isEmpty())noteCard(classes,"No classes today","Set up your timetable to see your classes here."){open("lessons")}
        else todays.forEach{classCard(classes,it)}
        val upcoming=lessons.filter{(timestamp(it.optString("starts_at"))?:0)>System.currentTimeMillis()}.minByOrNull{timestamp(it.optString("starts_at"))?:Long.MAX_VALUE}
        text(R.id.home_up_next,if(upcoming==null)"No upcoming classes" else "Up next · ${format(upcoming.optString("starts_at"),"EEE HH:mm")} ${upcoming.optString("title")} · ${upcoming.optString("room")}")
    }
    private fun taskCard(parent:LinearLayout,item:JSONObject) {
        val row=activity.layoutInflater.inflate(R.layout.item_home_task,parent,false)
        row.findViewById<TextView>(R.id.home_problem_title).apply { text=item.optString("title");paintFlags=if(item.optBoolean("completed"))paintFlags or Paint.STRIKE_THRU_TEXT_FLAG else paintFlags and Paint.STRIKE_THRU_TEXT_FLAG.inv() }
        row.findViewById<TextView>(R.id.home_problem_detail).text=listOf(item.optString("subject"),if(item.optBoolean("completed"))"Completed" else remaining(item.optString("due_at"))).filter{it.isNotBlank()}.joinToString(" · ")
        row.findViewById<TextView>(R.id.home_high).apply {
            val priority=item.optString("priority");text=priority.replaceFirstChar{it.uppercase()}
            setBackgroundResource(when(priority){"high"->R.drawable.bg_home_high;"medium"->R.drawable.bg_home_medium;else->R.drawable.bg_home_class})
            setTextColor(Color.parseColor(when(priority){"high"->"#B94958";"medium"->"#996923";else->"#4564ED"}))
        }
        row.findViewById<CheckBox>(R.id.home_check_problem).apply {
            isChecked=item.optBoolean("completed");isEnabled=!busy;contentDescription="Complete ${item.optString("title") }"
            setOnCheckedChangeListener{_,checked->vm.save("tasks",JSONObject().put("completed",checked),item.getLong("id"),UUID.randomUUID().toString())}
        }
        row.setOnClickListener{open("tasks",item)};parent.addView(row)
    }
    private fun classCard(parent:LinearLayout,item:JSONObject) {
        val row=activity.layoutInflater.inflate(R.layout.item_home_class,parent,false)
        row.findViewById<TextView>(R.id.home_start).text=format(item.optString("starts_at"),"HH:mm")
        row.findViewById<TextView>(R.id.home_end).text=format(item.optString("ends_at"),"HH:mm")
        row.findViewById<TextView>(R.id.home_calculus).text=item.optString("title")
        row.findViewById<TextView>(R.id.home_room).text=listOf(format(item.optString("starts_at"),"EEE, d MMM"),item.optString("room"),item.optString("lecturer")).filter{it.isNotBlank()}.joinToString(" · ")
        row.setOnClickListener{open("lessons",item)};parent.addView(row)
    }
    private fun noteCard(parent:LinearLayout,title:String,detail:String,click:()->Unit) {
        val row=activity.layoutInflater.inflate(R.layout.item_planner_note,parent,false)
        row.findViewById<TextView>(R.id.planner_item_title).text=title;row.findViewById<TextView>(R.id.planner_item_detail).text=detail
        row.setOnClickListener{click()};parent.addView(row)
    }
    private fun studyMenu() {
        MaterialAlertDialogBuilder(activity).setTitle("Your study progress").setItems(arrayOf("Log study time","Edit weekly goal","Study history")){_,i->
            when(i){0->open("focus");1->open("goal",data.optJSONObject("goal"));else->select("focus")}
        }.show()
    }
    private fun deadlines() {
        val tasks=list("tasks").filter{!it.optBoolean("completed")}.sortedBy{timestamp(it.optString("due_at"))}
        val b=MaterialAlertDialogBuilder(activity).setTitle("Upcoming deadlines").setNegativeButton("Close",null)
        if(tasks.isEmpty())b.setMessage("You have no pending deadlines.")
        else b.setItems(tasks.map{"${it.optString("title")} · ${remaining(it.optString("due_at"))}"}.toTypedArray()){_,i->open("tasks",tasks[i])}
        b.show()
    }
    private fun remaining(value:String):String {
        val ms=(timestamp(value)?:return "")-System.currentTimeMillis()
        if(ms<0)return "Overdue"
        val minutes=ms/60000;return when{minutes>=1440->"${minutes/1440}d ${minutes%1440/60}h left";minutes>=60->"${minutes/60}h ${minutes%60}m left";else->"${minutes}m left"}
    }
    private fun hours(minutes:Int)=String.format(Locale.US,"%.1f",minutes/60.0).removeSuffix(".0")
    private fun day(ms:Long)=SimpleDateFormat("yyyy-MM-dd",Locale.US).format(Date(ms))
    private fun format(value:String,pattern:String)=timestamp(value)?.let{SimpleDateFormat(pattern,Locale.ENGLISH).format(Date(it))}?:""
    companion object {
        fun timestamp(value:String):Long? {
            if(value.isBlank()||value=="null")return null
            // DRF may emit fractional seconds. Millisecond accuracy is enough for display.
            val normalized=value.replace(Regex("\\.\\d+(?=Z|[+-]\\d\\d:\\d\\d$)"),"")
            return runCatching{SimpleDateFormat("yyyy-MM-dd'T'HH:mm:ssXXX",Locale.US).parse(normalized)?.time}.getOrNull()
        }
    }
}
