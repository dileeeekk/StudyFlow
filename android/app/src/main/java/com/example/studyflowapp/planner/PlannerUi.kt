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
class PlannerUi(private val activity: AppCompatActivity, private val expired: () -> Unit, private val onRemindersAvailable: () -> Unit = {}) {
    private val vm=ViewModelProvider(activity)[PlannerViewModel::class.java]
    private var data=JSONObject()
    private var tab="home"
    private var taskFilter="all"
    private var taskSort=0
    private var busy=false
    private var scheduleDay=Calendar.getInstance()
    private fun view(id:Int):View=activity.findViewById(id)
    private fun text(id:Int,value:String) { activity.findViewById<TextView>(id).text=value }
    private fun list(key:String):List<JSONObject> { val a=data.optJSONArray(key)?:return emptyList();return (0 until a.length()).map{a.getJSONObject(it)} }
    private fun open(kind:String,item:JSONObject?=null) { if(!busy && vm.state.value?.data != null)PlannerForm.show(activity,kind,item) }
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
            if(tab=="home")plannerDialog(activity).setTitle(R.string.planner_add_title).setItems(activity.resources.getStringArray(R.array.planner_add_options)) { _,i ->
                val kind=listOf("tasks","lessons","notes","focus","goal")[i];open(kind,if(kind=="goal")data.optJSONObject("goal") else null)
            }.show() else open(tab)
        }
        view(R.id.home_notifications).setOnClickListener { deadlines() }
        vm.state.observe(activity) { state ->
            busy=state.busy
            if(state.expired) { expired();return@observe }
            state.data?.let { snapshot ->
                data = snapshot
                if (DeadlineReminderScheduler.sync(activity, snapshot)) {
                    onRemindersAvailable()
                }
            }
            text(R.id.planner_status,when { state.busy -> activity.getString(R.string.planner_syncing);state.error!=null -> state.error + ". " + activity.getString(R.string.planner_stale_data_suffix);else -> "" })
            view(R.id.planner_status).visibility=if(state.busy||state.error!=null)View.VISIBLE else View.GONE
            view(R.id.planner_retry).visibility=if(state.error!=null&&!busy)View.VISIBLE else View.GONE
            render()
        }
        view(R.id.schedule_previous).setOnClickListener { scheduleDay.add(Calendar.DAY_OF_YEAR,-7);render() }
        view(R.id.schedule_next).setOnClickListener { scheduleDay.add(Calendar.DAY_OF_YEAR,7);render() }
        view(R.id.schedule_week).setOnClickListener { scheduleDay=Calendar.getInstance();render() }
        view(R.id.schedule_add).setOnClickListener {
            val start=(scheduleDay.clone() as Calendar).apply { set(Calendar.HOUR_OF_DAY,9);set(Calendar.MINUTE,0) }
            val end=(start.clone() as Calendar).apply { add(Calendar.HOUR_OF_DAY,1) }
            val f=SimpleDateFormat("yyyy-MM-dd'T'HH:mm:ssXXX",Locale.US)
            open("lessons",JSONObject().put("starts_at",f.format(start.time)).put("ends_at",f.format(end.time)))
        }
        view(R.id.tasks_first).setOnClickListener { open("tasks") }
        mapOf(R.id.tasks_filter_all to "all",R.id.tasks_filter_soon to "soon",R.id.tasks_filter_done to "done").forEach { (id,key)->view(id).setOnClickListener { taskFilter=key;render() } }
        view(R.id.tasks_sort).setOnClickListener {
            plannerDialog(activity).setTitle(R.string.planner_sort_title).setSingleChoiceItems(activity.resources.getStringArray(R.array.planner_sort_options),taskSort){d,i->taskSort=i;d.dismiss();render()}.show()
        }
        vm.load()
    }
    fun refresh() { vm.load(true) }
    fun currentTab()=tab
    fun back():Boolean { if(tab=="home")return false;select("home");return true }
    private fun select(key:String) { tab=key;render();activity.findViewById<androidx.core.widget.NestedScrollView>(R.id.home_scroll).smoothScrollTo(0,0) }
    private fun render() {
        val tasks=list("tasks");val lessons=list("lessons");val notes=list("notes");val focus=list("focus")
        view(R.id.home_notification_dot).visibility=if(tasks.any { !it.optBoolean("completed") })View.VISIBLE else View.GONE
        val goal=data.optJSONObject("goal")
        val populated=tasks.isNotEmpty()||lessons.isNotEmpty()||notes.isNotEmpty()||focus.isNotEmpty()||goal!=null
        view(R.id.planner_empty).visibility=if(tab=="home"&&!populated)View.VISIBLE else View.GONE
        view(R.id.planner_populated).visibility=if(tab=="home"&&populated)View.VISIBLE else View.GONE
        view(R.id.planner_collection).visibility=if(tab!="home" && tab!="lessons" && tab!="tasks")View.VISIBLE else View.GONE
        view(R.id.planner_add_container).visibility=if(populated||tab!="home")View.VISIBLE else View.GONE
        for(id in listOf(R.id.home_add,R.id.home_timetable,R.id.home_setup_task,R.id.home_setup_classes,R.id.home_setup_goal,R.id.planner_add))view(id).isEnabled=!busy && vm.state.value?.data != null
        view(R.id.home_header).visibility=if(tab=="lessons" || tab=="tasks")View.GONE else View.VISIBLE
        view(R.id.schedule_root).visibility=if(tab=="lessons")View.VISIBLE else View.GONE
        if(tab=="lessons")view(R.id.planner_add_container).visibility=View.GONE
        view(R.id.schedule_add).isEnabled=!busy && vm.state.value?.data!=null
        view(R.id.tasks_root).visibility=if(tab=="tasks")View.VISIBLE else View.GONE
        if(tab=="tasks")view(R.id.planner_add_container).visibility=if(tasks.isEmpty())View.GONE else View.VISIBLE
        val keys=listOf("home","lessons","tasks","notes")
        val navIds=listOf(R.id.home_tab_home,R.id.home_tab_schedule,R.id.home_tab_tasks,R.id.home_tab_notes)
        navIds.forEachIndexed { i,id ->
            val group=view(id) as LinearLayout;group.isSelected=tab==keys[i]
            group.getChildAt(0).setBackgroundResource(if(tab==keys[i])R.drawable.bg_home_selected else android.R.color.transparent)
            (group.getChildAt(1) as TextView).setTextColor(Color.parseColor(if(tab==keys[i])"#4564ED" else "#66728B"))
        }
        text(R.id.planner_count_tasks,tasks.size.toString());text(R.id.planner_count_lessons,lessons.size.toString());text(R.id.planner_count_notes,notes.size.toString())
        text(R.id.planner_setup_count,"${listOf(tasks.isNotEmpty(),lessons.isNotEmpty(),goal!=null).count{it}} of 3")
        if(tab=="tasks") { renderTasks(tasks);return }
        if(tab=="lessons") { renderSchedule(lessons);return }
        if(tab!="home") {
            text(R.id.planner_collection_title, when(tab) {
                "tasks" -> activity.getString(R.string.collection_tasks)
                "lessons" -> activity.getString(R.string.collection_schedule)
                "focus" -> activity.getString(R.string.collection_history)
                else -> activity.getString(R.string.collection_notes)
            })
            val items=when(tab){"tasks"->tasks.sortedWith(compareBy<JSONObject>{it.optBoolean("completed")}.thenBy{timestamp(it.optString("due_at"))?:0L});"lessons"->lessons.sortedBy{timestamp(it.optString("starts_at"))};"focus"->focus.sortedByDescending{it.optString("date")};else->notes.reversed()}
            text(R.id.planner_collection_hint, if (items.isEmpty())
                activity.getString(R.string.collection_empty)
            else activity.getString(R.string.collection_items, items.size))
            val parent=activity.findViewById<LinearLayout>(R.id.planner_collection_list);parent.removeAllViews()
            items.forEach { item -> when(tab){"tasks"->taskCard(parent,item);"lessons"->classCard(parent,item);else->noteCard(parent,if(tab=="focus")activity.resources.getQuantityString(R.plurals.planner_minutes_count,item.optInt("minutes"),item.optInt("minutes")) else item.optString("title"),if(tab=="focus")item.optString("date") else item.optString("body")){open(tab,item)}} }
            return
        }
        if(!populated)return
        val done=tasks.count{it.optBoolean("completed")}
        val today=day(System.currentTimeMillis());val start=Calendar.getInstance().apply { add(Calendar.DAY_OF_YEAR,-6) }.let{day(it.timeInMillis)}
        val minutes=focus.filter{it.optString("date") in start..today}.sumOf{it.optInt("minutes")}
        val target=goal?.optInt("weekly_minutes")?:0
        val percent=if(target>0)(minutes*100/target).coerceIn(0,100) else if(tasks.isNotEmpty())done*100/tasks.size else 0
        text(R.id.home_week, activity.getString(if(target>0) R.string.home_week_history else R.string.home_week_tasks))
        text(R.id.home_momentum, activity.getString(when {
            percent >= 75 -> R.string.home_momentum_great
            percent > 0 -> R.string.home_momentum_keep
            else -> R.string.home_momentum_fresh
        }))
        text(R.id.home_hours, if (target > 0)
            activity.getString(R.string.home_hours_goal, hours(minutes), hours(target))
        else activity.getString(R.string.home_hours_tasks, done, tasks.size))
        text(R.id.home_percent,"$percent%")
        activity.findViewById<CircularProgressIndicator>(R.id.planner_ring).setProgressCompat(percent,false)
        (view(R.id.planner_ring).parent as View).contentDescription=activity.getString(R.string.home_percent_completed, percent)
        text(R.id.home_done, activity.getString(R.string.home_tasks_done_count, done, tasks.size))
        val days=(focus.map{it.optString("date")}+tasks.filter{it.optBoolean("completed")}.mapNotNull{timestamp(it.optString("completed_at"))?.let(::day)}).toSet()
        val c=Calendar.getInstance();if(today !in days)c.add(Calendar.DAY_OF_YEAR,-1)
        var streak=0;while(day(c.timeInMillis) in days){streak++;c.add(Calendar.DAY_OF_YEAR,-1)}
        text(R.id.home_streak, activity.resources.getQuantityString(R.plurals.home_streak_count, streak, streak))
        val pending=tasks.filter{!it.optBoolean("completed")}.sortedBy{timestamp(it.optString("due_at"))?:Long.MAX_VALUE}
        val next=pending.firstOrNull()
        text(R.id.home_problem,next?.optString("title") ?: activity.getString(R.string.home_no_deadlines))
        text(R.id.home_due,if(next!=null)next.optString("subject") else activity.getString(R.string.home_add_task_plan))
        text(R.id.home_countdown,if(next!=null)remaining(next.optString("due_at")) else "—")
        text(R.id.home_remaining,if(next!=null)format(next.optString("due_at"),"d MMM, HH:mm") else "")
        view(R.id.home_deadline).setOnClickListener { if(next!=null)open("tasks",next) else open("tasks") }
        val priorities=activity.findViewById<LinearLayout>(R.id.planner_priority_list);priorities.removeAllViews()
        if(pending.isEmpty())noteCard(priorities,activity.getString(R.string.home_all_clear),activity.getString(R.string.home_add_task_ready)){open("tasks")}
        else pending.take(3).forEach{taskCard(priorities,it)}
        val todays=lessons.filter{timestamp(it.optString("starts_at"))?.let(::day)==today}.sortedBy{timestamp(it.optString("starts_at"))}
        text(R.id.home_class_count, activity.resources.getQuantityString(R.plurals.home_classes_count, todays.size, todays.size))
        val classes=activity.findViewById<LinearLayout>(R.id.planner_today_list);classes.removeAllViews()
        if(todays.isEmpty())noteCard(classes,activity.getString(R.string.home_no_classes),activity.getString(R.string.home_setup_timetable)){open("lessons")}
        else todays.forEach{classCard(classes,it)}
        val upcoming=lessons.filter{(timestamp(it.optString("starts_at"))?:0)>System.currentTimeMillis()}.minByOrNull{timestamp(it.optString("starts_at"))?:Long.MAX_VALUE}
        text(R.id.home_up_next, if (upcoming == null) activity.getString(R.string.home_no_upcoming_classes)
            else activity.getString(R.string.planner_home_up_next_dynamic,
                format(upcoming.optString("starts_at"), "EEE HH:mm"),
                upcoming.optString("title"), upcoming.optString("room")))
    }
    private fun renderTasks(tasks:List<JSONObject>) {
        val empty=tasks.isEmpty();val done=tasks.filter { it.optBoolean("completed") };val pending=tasks.filter { !it.optBoolean("completed") }
        text(R.id.tasks_title, activity.getString(if(empty) R.string.tasks_title_default else R.string.tasks_title_deadlines))
        text(R.id.tasks_subtitle, activity.getString(if(empty) R.string.tasks_subtitle_empty else R.string.tasks_subtitle_filled))
        view(R.id.tasks_eyebrow).visibility=if(empty)View.VISIBLE else View.GONE
        view(R.id.tasks_progress).visibility=if(empty)View.GONE else View.VISIBLE
        text(R.id.tasks_progress_title, activity.getString(R.string.tasks_progress_title, done.size, tasks.size, if(empty) 0 else done.size*100/tasks.size))
        val weekEnd=System.currentTimeMillis()+7*24*60*60*1000L
        val soon=pending.filter { (timestamp(it.optString("due_at"))?:Long.MAX_VALUE)<=weekEnd }
        text(R.id.tasks_progress_detail, activity.getString(R.string.tasks_progress_detail, pending.size, soon.size))
        view(R.id.tasks_filter_hint).visibility=if(empty)View.VISIBLE else View.GONE
        mapOf(R.id.tasks_filter_all to "all",R.id.tasks_filter_soon to "soon",R.id.tasks_filter_done to "done").forEach { (id,key)->
            view(id).isEnabled=!empty;view(id).alpha=if(empty)0.5f else 1f
            view(id).setBackgroundResource(if(!empty && taskFilter==key)R.drawable.bg_login_card else android.R.color.transparent)
        }
        view(R.id.tasks_empty).visibility=if(empty)View.VISIBLE else View.GONE
        view(R.id.tasks_content).visibility=if(empty)View.GONE else View.VISIBLE
        view(R.id.tasks_first).isEnabled=!busy && vm.state.value?.data!=null
        text(R.id.tasks_sort, activity.getString(listOf(
            R.string.tasks_sort_deadline,
            R.string.tasks_sort_priority,
            R.string.tasks_sort_title
        )[taskSort.coerceIn(0, 2)]) + " ↓")
        val upcoming=activity.findViewById<LinearLayout>(R.id.tasks_pending);upcoming.removeAllViews()
        val completed=activity.findViewById<LinearLayout>(R.id.tasks_completed);completed.removeAllViews()
        view(R.id.tasks_pending_title).visibility=if(taskFilter=="done")View.GONE else View.VISIBLE
        view(R.id.tasks_completed_title).visibility=if(taskFilter=="soon")View.GONE else View.VISIBLE
        val filtered=if(taskFilter=="soon")soon else pending
        val sorted=when(taskSort){1->filtered.sortedWith(compareBy<JSONObject>{listOf("high","medium","low").indexOf(it.optString("priority"))}.thenBy{timestamp(it.optString("due_at"))});2->filtered.sortedBy{it.optString("title").lowercase(Locale.ROOT)};else->filtered.sortedBy{timestamp(it.optString("due_at"))}}
        if(taskFilter!="done") {
            if(sorted.isEmpty())noteCard(upcoming,activity.getString(R.string.home_all_clear),activity.getString(if(taskFilter=="soon") R.string.tasks_no_soon else R.string.tasks_no_open)){open("tasks")}
            sorted.forEach { taskCard(upcoming,it) }
        }
        if(taskFilter!="soon") {
            if(done.isEmpty())noteCard(completed,activity.getString(R.string.tasks_no_completed),activity.getString(R.string.tasks_check_off)){taskFilter="all";render()}
            done.sortedByDescending { timestamp(it.optString("completed_at"))?:0 }.forEach { taskCard(completed,it) }
        }
    }
    private fun renderSchedule(lessons:List<JSONObject>) {
        val monday=(scheduleDay.clone() as Calendar).apply { add(Calendar.DAY_OF_YEAR,-((get(Calendar.DAY_OF_WEEK)+5)%7));set(Calendar.HOUR_OF_DAY,0);set(Calendar.MINUTE,0);set(Calendar.SECOND,0);set(Calendar.MILLISECOND,0) }
        val end=(monday.clone() as Calendar).apply { add(Calendar.DAY_OF_YEAR,7) }
        val week=lessons.filter { (timestamp(it.optString("starts_at"))?:0) in monday.timeInMillis until end.timeInMillis }
        val locale = activity.resources.configuration.locales[0]
        val f=SimpleDateFormat("d MMM",locale)
        text(R.id.schedule_range,f.format(monday.time)+" – "+f.format(Date(end.timeInMillis-1))+", "+monday.get(Calendar.YEAR))
        text(R.id.schedule_week, activity.getString(if(System.currentTimeMillis() in monday.timeInMillis until end.timeInMillis) R.string.schedule_this_week else R.string.schedule_back_week))
        val days=activity.findViewById<LinearLayout>(R.id.schedule_days);days.removeAllViews()
        repeat(7) { offset ->
            val date=(monday.clone() as Calendar).apply { add(Calendar.DAY_OF_YEAR,offset) }
            val selected=day(date.timeInMillis)==day(scheduleDay.timeInMillis)
            val count=week.count { timestamp(it.optString("starts_at"))?.let(::day)==day(date.timeInMillis) }
            val cell=TextView(activity).apply {
                layoutParams=LinearLayout.LayoutParams(0,dp(68),1f).apply { setMargins(dp(2),0,dp(2),0) }
                gravity=android.view.Gravity.CENTER;text=SimpleDateFormat("EEE",Locale.ENGLISH).format(date.time)+"\n"+date.get(Calendar.DAY_OF_MONTH)+(if(count>0)"\n•" else "\n")
                textSize=12f;typeface=androidx.core.content.res.ResourcesCompat.getFont(activity,R.font.inter_medium)
                setTextColor(if(selected)Color.WHITE else Color.rgb(23,36,67))
                setBackgroundResource(if(selected)R.drawable.bg_home_plus else R.drawable.bg_login_field)
                contentDescription=activity.getString(R.string.schedule_day_description,SimpleDateFormat("EEEE, d MMMM",locale).format(date.time),count)
                setOnClickListener { scheduleDay=date;render() }
            };days.addView(cell)
        }
        val today=week.filter { timestamp(it.optString("starts_at"))?.let(::day)==day(scheduleDay.timeInMillis) }.sortedBy { timestamp(it.optString("starts_at")) }
        text(R.id.schedule_day_title,activity.getString(R.string.schedule_day_title,SimpleDateFormat("EEEE, d MMMM",locale).format(scheduleDay.time),activity.resources.getQuantityString(R.plurals.schedule_class_count,today.size,today.size)))
        val cards=activity.findViewById<LinearLayout>(R.id.schedule_cards);cards.removeAllViews()
        today.forEachIndexed { index,item ->
            val start=timestamp(item.optString("starts_at"))?:0;val finish=timestamp(item.optString("ends_at"))?:0;val now=System.currentTimeMillis()
            val live=now in start until finish
            if(live)noteCard(cards,activity.getString(R.string.schedule_in_progress),activity.resources.getQuantityString(R.plurals.schedule_minutes_remaining,((finish-now)/60000).coerceAtLeast(0).toInt(),((finish-now)/60000).coerceAtLeast(0).toInt())){open("lessons",item)}
            classCard(cards,item)
            val row=cards.getChildAt(cards.childCount-1)
            row.setBackgroundResource(if(live)R.drawable.bg_login_field else R.drawable.bg_login_card)
            if(finish<now)row.alpha=0.6f
            if(live)cards.addView(ProgressBar(activity,null,android.R.attr.progressBarStyleHorizontal).apply { max=100;progress=((now-start)*100/(finish-start).coerceAtLeast(1)).toInt();progressTintList=android.content.res.ColorStateList.valueOf(Color.rgb(69,100,237));layoutParams=LinearLayout.LayoutParams(-1,dp(4)).apply { topMargin=dp(8) } })
            val next=today.getOrNull(index+1)?.let { timestamp(it.optString("starts_at")) }
            if(next!=null && next>finish)noteCard(cards,activity.getString(R.string.schedule_break,((next-finish)/60000).toInt()),activity.getString(R.string.schedule_recharge)){open("lessons",today[index+1])}
        }
        view(R.id.schedule_empty).visibility=if(today.isEmpty())View.VISIBLE else View.GONE
        text(R.id.schedule_empty_title,activity.getString(if(week.isEmpty()) R.string.schedule_empty_week else R.string.schedule_empty_day))
        text(R.id.schedule_empty_detail,activity.getString(R.string.schedule_empty_detail))
    }
    private fun dp(value:Int)=(value*activity.resources.displayMetrics.density).toInt()
    private fun taskCard(parent:LinearLayout,item:JSONObject) {
        val row=activity.layoutInflater.inflate(R.layout.item_home_task,parent,false)
        row.findViewById<TextView>(R.id.home_problem_title).apply { text=item.optString("title");paintFlags=if(item.optBoolean("completed"))paintFlags or Paint.STRIKE_THRU_TEXT_FLAG else paintFlags and Paint.STRIKE_THRU_TEXT_FLAG.inv() }
        row.findViewById<TextView>(R.id.home_problem_detail).text=listOf(item.optString("subject"),if(item.optBoolean("completed"))activity.getString(R.string.planner_completed) else remaining(item.optString("due_at"))).filter{it.isNotBlank()}.joinToString(" · ")
        row.findViewById<TextView>(R.id.home_high).apply {
            val priority=item.optString("priority");text=priorityLabel(priority)
            setBackgroundResource(when(priority){"high"->R.drawable.bg_home_high;"medium"->R.drawable.bg_home_medium;else->R.drawable.bg_home_class})
            setTextColor(Color.parseColor(when(priority){"high"->"#B94958";"medium"->"#996923";else->"#4564ED"}))
        }
        row.findViewById<CheckBox>(R.id.home_check_problem).apply {
            isChecked=item.optBoolean("completed");isEnabled=!busy;contentDescription=activity.getString(R.string.planner_task_complete_accessibility, item.optString("title"))
            setOnCheckedChangeListener{_,checked->vm.save("tasks",JSONObject().put("completed",checked),item.getLong("id"),UUID.randomUUID().toString())}
        }
        if(tab=="tasks") {
            val completed=item.optBoolean("completed")
            row.findViewById<TextView>(R.id.home_problem_detail).text=listOf(item.optString("subject"),format(item.optString("due_at"),"EEE, d MMM · HH:mm"),if(completed)activity.getString(R.string.planner_done_prefix, format(item.optString("completed_at"),"d MMM")) else remaining(item.optString("due_at"))).filter{it.isNotBlank()}.joinToString("\n")
            if(completed)row.findViewById<TextView>(R.id.home_high).apply {
                text=activity.getString(R.string.planner_completed);setTextColor(Color.rgb(0,132,110))
                background=android.graphics.drawable.GradientDrawable().apply { setColor(Color.rgb(229,245,239));cornerRadius=dp(12).toFloat() }
            }
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
        plannerDialog(activity).setTitle(R.string.planner_progress_title)
            .setItems(activity.resources.getStringArray(R.array.planner_study_menu)) { _, i ->
                when (i) {
                    0 -> startStudyTimer()
                    1 -> open("focus")
                    2 -> open("goal", data.optJSONObject("goal"))
                    3 -> select("focus")
                }
            }.show()
    }

    private fun startStudyTimer() {
        val prefs = activity.getSharedPreferences("studyflow_study_timer", android.content.Context.MODE_PRIVATE)
        var elapsedMs = prefs.getLong("elapsed_ms", 0L)
        var startedAt = prefs.getLong("started_at_elapsed_ms", 0L)

        val now = android.os.SystemClock.elapsedRealtime()
        if (startedAt > now) {
            elapsedMs = 0L
            startedAt = 0L
            prefs.edit().clear().apply()
        }

        val handler = android.os.Handler(android.os.Looper.getMainLooper())

        val root = LinearLayout(activity).apply {
            orientation = LinearLayout.VERTICAL
            gravity = android.view.Gravity.CENTER_HORIZONTAL
            setPadding(dp(24), dp(12), dp(24), dp(8))
        }

        val timerText = TextView(activity).apply {
            textSize = 38f
            gravity = android.view.Gravity.CENTER
            setTextColor(Color.parseColor("#172443"))
            setTypeface(null, android.graphics.Typeface.BOLD)
        }

        val hint = TextView(activity).apply {
            textSize = 13f
            gravity = android.view.Gravity.CENTER
            setTextColor(Color.parseColor("#66728B"))
            setPadding(0, dp(8), 0, dp(16))
        }

        val toggle = com.google.android.material.button.MaterialButton(activity).apply {
            isAllCaps = false
            text = activity.getString(R.string.planner_start)
        }

        root.addView(timerText, LinearLayout.LayoutParams(-1, dp(76)))
        root.addView(hint, LinearLayout.LayoutParams(-1, -2))
        root.addView(toggle, LinearLayout.LayoutParams(-1, dp(48)))

        fun totalTime(): Long {
            val running = if (startedAt > 0L) {
                (android.os.SystemClock.elapsedRealtime() - startedAt).coerceAtLeast(0L)
            } else 0L
            return elapsedMs + running
        }

        fun persist() {
            prefs.edit()
                .putLong("elapsed_ms", elapsedMs)
                .putLong("started_at_elapsed_ms", startedAt)
                .apply()
        }

        fun renderTimer() {
            val seconds = totalTime() / 1000L
            val hours = seconds / 3600
            val minutes = (seconds % 3600) / 60
            val remainingSeconds = seconds % 60

            timerText.text = String.format(
                Locale.US, "%02d:%02d:%02d", hours, minutes, remainingSeconds
            )

            val running = startedAt > 0L
            toggle.text = activity.getString(if (running) R.string.planner_pause else R.string.planner_start)
            hint.text = if (running) {
                activity.getString(R.string.planner_running)
            } else {
                activity.getString(R.string.planner_paused)
            }
        }

        val ticker = object : Runnable {
            override fun run() {
                renderTimer()
                if (startedAt > 0L) handler.postDelayed(this, 1000L)
            }
        }

        val dialog = MaterialAlertDialogBuilder(activity)
            .setTitle(R.string.planner_timer_title)
            .setView(root)
            .setNegativeButton(R.string.common_close, null)
            .setPositiveButton(R.string.planner_finish_save, null)
            .create()

        toggle.setOnClickListener {
            if (startedAt == 0L) {
                startedAt = android.os.SystemClock.elapsedRealtime()
                persist()
                handler.removeCallbacks(ticker)
                handler.post(ticker)
            } else {
                elapsedMs = totalTime()
                startedAt = 0L
                persist()
                handler.removeCallbacks(ticker)
            }
            renderTimer()
        }

        dialog.setOnShowListener {
            val saveButton = dialog.getButton(androidx.appcompat.app.AlertDialog.BUTTON_POSITIVE)
            val closeButton = dialog.getButton(androidx.appcompat.app.AlertDialog.BUTTON_NEGATIVE)

            closeButton.setOnClickListener { dialog.dismiss() }

            saveButton.setOnClickListener {
                val total = totalTime()
                val minutes = (total / 60000L).toInt()

                if (minutes < 1) {
                    hint.text = activity.getString(R.string.planner_min_duration)
                    return@setOnClickListener
                }

                elapsedMs = total
                startedAt = 0L
                persist()
                handler.removeCallbacks(ticker)

                toggle.isEnabled = false
                saveButton.isEnabled = false
                closeButton.isEnabled = false
                dialog.setCancelable(false)
                hint.text = activity.getString(R.string.planner_saving)

                val operation = UUID.randomUUID().toString()
                lateinit var observer: androidx.lifecycle.Observer<PlannerState>

                observer = androidx.lifecycle.Observer { result ->
                    if (result.operation == operation && !result.busy) {
                        vm.state.removeObserver(observer)

                        if (result.error == null) {
                            prefs.edit().clear().apply()
                            android.widget.Toast.makeText(
                                activity,
                                activity.getString(R.string.planner_minutes_saved, minutes),
                                android.widget.Toast.LENGTH_LONG
                            ).show()
                            dialog.dismiss()
                        } else {
                            hint.text = activity.getString(R.string.planner_save_error, result.error ?: "")
                            toggle.isEnabled = true
                            saveButton.isEnabled = true
                            closeButton.isEnabled = true
                            dialog.setCancelable(true)
                            renderTimer()
                        }
                    }
                }

                vm.state.observe(activity, observer)

                vm.save(
                    "focus",
                    JSONObject()
                        .put("minutes", minutes.coerceAtMost(1440))
                        .put("date", day(System.currentTimeMillis())),
                    null,
                    operation
                )
            }

            renderTimer()
            if (startedAt > 0L) handler.post(ticker)
        }

        dialog.setOnDismissListener {
            handler.removeCallbacks(ticker)
        }

        dialog.show()
    }
    private fun deadlines() {
        val tasks=list("tasks").filter{!it.optBoolean("completed")}.sortedBy{timestamp(it.optString("due_at"))}
        val b=plannerDialog(activity).setTitle(R.string.planner_deadlines_title).setNegativeButton(R.string.common_close,null)
        if(tasks.isEmpty())b.setMessage(R.string.planner_no_deadlines)
        else b.setItems(tasks.map{"${it.optString("title")} · ${remaining(it.optString("due_at"))}"}.toTypedArray()){_,i->open("tasks",tasks[i])}
        b.show()
    }
    private fun priorityLabel(value: String): String = when (value.lowercase(Locale.US)) {
        "high" -> activity.getString(R.string.planner_priority_high)
        "medium" -> activity.getString(R.string.planner_priority_medium)
        "low" -> activity.getString(R.string.planner_priority_low)
        else -> value
    }

    private fun remaining(value:String):String {
        val ms=(timestamp(value)?:return "")-System.currentTimeMillis()
        if(ms<0)return activity.getString(R.string.planner_overdue)
        val minutes=ms/60000
        return when {
            minutes>=1440 -> activity.getString(R.string.planner_days_hours, minutes/1440, minutes%1440/60)
            minutes>=60 -> activity.getString(R.string.planner_hours_minutes, minutes/60, minutes%60)
            else -> activity.getString(R.string.planner_minutes_left, minutes)
        }
    }
    private fun hours(minutes:Int)=String.format(Locale.US,"%.1f",minutes/60.0).removeSuffix(".0")
    private fun day(ms:Long)=SimpleDateFormat("yyyy-MM-dd",Locale.US).format(Date(ms))
    private fun format(value:String,pattern:String)=timestamp(value)?.let{SimpleDateFormat(pattern,activity.resources.configuration.locales[0]).format(Date(it))}?:""
    companion object {
        fun timestamp(value:String):Long? {
            if(value.isBlank()||value=="null")return null
            // DRF may emit fractional seconds. Millisecond accuracy is enough for display.
            val normalized=value.replace(Regex("\\.\\d+(?=Z|[+-]\\d\\d:\\d\\d$)"),"")
            return runCatching{SimpleDateFormat("yyyy-MM-dd'T'HH:mm:ssXXX",Locale.US).parse(normalized)?.time}.getOrNull()
        }
    }
}
