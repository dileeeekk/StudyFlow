package com.example.studyflowapp.planner

import android.app.DatePickerDialog
import android.app.Dialog
import android.app.TimePickerDialog
import android.os.Bundle
import android.text.InputType
import android.view.View
import android.view.WindowManager
import android.widget.*
import androidx.appcompat.app.AlertDialog
import androidx.fragment.app.DialogFragment
import androidx.lifecycle.ViewModelProvider
import com.example.studyflowapp.R
import com.google.android.material.dialog.MaterialAlertDialogBuilder
import org.json.JSONObject
import java.text.SimpleDateFormat
import java.util.*

class PlannerForm : DialogFragment() {
    private val fields = linkedMapOf<String, EditText>()
    private lateinit var host: LinearLayout
    private lateinit var error: TextView
    private lateinit var vm: PlannerViewModel
    private lateinit var draft: JSONObject
    private lateinit var kind: String
    private var id: Long? = null
    private var operation: String? = null
    private var due = System.currentTimeMillis() + 3600000
    private var end = due + 3600000
    private var priority = "medium"
    private val repeatDays = linkedSetOf<Int>()
    private val repeatControls = mutableListOf<CheckBox>()
    private val timeFormat get() = SimpleDateFormat("yyyy-MM-dd'T'HH:mm:ssXXX", Locale.US)

    override fun onCreateDialog(savedInstanceState: Bundle?): Dialog {
        vm = ViewModelProvider(requireActivity())[PlannerViewModel::class.java]
        kind = requireArguments().getString("kind")!!
        draft = JSONObject(savedInstanceState?.getString("draft") ?: requireArguments().getString("data", "{}"))
        id = if (draft.has("id")) draft.getLong("id") else null
        operation = savedInstanceState?.getString("operation")
        due = savedInstanceState?.getLong("due") ?: parse(draft.optString(if (kind == "tasks") "due_at" else "starts_at"))
        end = savedInstanceState?.getLong("end") ?: parse(draft.optString("ends_at"), due + 3600000)
        priority = savedInstanceState?.getString("priority") ?: draft.optString("priority", "medium")
        repeatDays.clear()
        draft.optString("repeat_days").split(",")
            .mapNotNull { it.toIntOrNull() }
            .filter { it in Calendar.MONDAY..Calendar.SUNDAY }
            .forEach { repeatDays.add(it) }
        val view = layoutInflater.inflate(R.layout.dialog_planner_form, null)
        host = view.findViewById(R.id.planner_form_fields); error = view.findViewById(R.id.planner_form_error)
        val title = when(kind) {
            "tasks" -> if (id == null) getString(R.string.form_task_new) else getString(R.string.form_task_edit)
            "lessons" -> if (id == null) "Add a class" else getString(R.string.form_class_edit)
            "notes" -> if (id == null) getString(R.string.form_note_new) else getString(R.string.form_note_edit)
            "goal" -> getString(R.string.form_goal_title)
            else -> if (id == null) getString(R.string.form_focus_new) else getString(R.string.form_focus_edit)
        }
        when (kind) {
            "tasks" -> {
                field("title", getString(R.string.form_task_name), 160); field("subject", getString(R.string.form_subject_optional), 120)
                picker(getString(R.string.form_deadline), false)
                val labels = arrayOf(getString(R.string.planner_priority_high), getString(R.string.planner_priority_medium), getString(R.string.planner_priority_low))
                val row = field("priority_display", getString(R.string.form_priority), 20)
                row.setText(when (priority.lowercase(Locale.US)) { "high" -> getString(R.string.planner_priority_high); "medium" -> getString(R.string.planner_priority_medium); "low" -> getString(R.string.planner_priority_low); else -> priority }); row.isFocusable = false
                row.setOnClickListener {
                    plannerDialog(requireContext()).setTitle(R.string.planner_priority_title).setSingleChoiceItems(labels, labels.indexOfFirst { it.equals(priority, true) }) { d, index ->
                        priority = labels[index].lowercase(Locale.US); row.setText(labels[index]); d.dismiss()
                    }.show()
                }
            }
            "lessons" -> {
                field("title", getString(R.string.form_class_name), 160)
                field("room", getString(R.string.form_room_optional), 120)
                field("lecturer", getString(R.string.form_lecturer_optional), 120)
                picker(getString(R.string.form_starts), false)
                picker(getString(R.string.form_ends), true)
                if (id == null) addWeeklyRepeatControls()
            }
            "notes" -> { field("title",getString(R.string.form_title),160); field("body",getString(R.string.form_note),5000).apply { inputType = InputType.TYPE_CLASS_TEXT or InputType.TYPE_TEXT_FLAG_MULTI_LINE; setSingleLine(false); minLines = 4 } }
            "goal" -> field("hours", getString(R.string.form_study_hours), 6).apply {
                inputType = InputType.TYPE_CLASS_NUMBER or InputType.TYPE_NUMBER_FLAG_DECIMAL
                if (!draft.has("hours") && draft.has("weekly_minutes")) setText((draft.getInt("weekly_minutes")/60.0).toString())
            }
            "focus" -> {
                field("minutes",getString(R.string.form_minutes),4).inputType = InputType.TYPE_CLASS_NUMBER
                val date = field("date", getString(R.string.form_date), 10); date.isFocusable = false
                if (date.text.isBlank()) date.setText(SimpleDateFormat("yyyy-MM-dd",Locale.US).format(Date()))
                date.setOnClickListener {
                    val c=Calendar.getInstance(); DatePickerDialog(requireContext(), { _, y,m,d -> date.setText(String.format(Locale.US,"%04d-%02d-%02d",y,m+1,d)) },c.get(Calendar.YEAR),c.get(Calendar.MONTH),c.get(Calendar.DAY_OF_MONTH)).apply { datePicker.maxDate=System.currentTimeMillis() }.show()
                }
            }
        }
        val builder = plannerDialog(requireContext()).setTitle(title).setView(view)
            .setNegativeButton(R.string.common_cancel, null).setPositiveButton(R.string.common_save,null)
        if (id != null || (kind=="goal" && draft.has("weekly_minutes"))) builder.setNeutralButton(R.string.common_delete,null)
        return builder.create()
    }
    override fun onStart() {
        super.onStart()
        val dialog = requireDialog() as AlertDialog
        dialog.window?.setSoftInputMode(WindowManager.LayoutParams.SOFT_INPUT_ADJUST_RESIZE)
        dialog.getButton(AlertDialog.BUTTON_POSITIVE).setOnClickListener { save() }
        dialog.getButton(AlertDialog.BUTTON_NEUTRAL)?.setOnClickListener {
            plannerDialog(requireContext()).setTitle(R.string.form_delete_title).setMessage(R.string.form_delete_message)
                .setNegativeButton(R.string.common_cancel,null).setPositiveButton(R.string.common_delete) { _, _ ->
                    operation=UUID.randomUUID().toString(); vm.delete(kind,id,operation!!)
                }.show()
        }
        vm.state.removeObservers(this)
        vm.state.observe(this) { state ->
            dialog.getButton(AlertDialog.BUTTON_POSITIVE).isEnabled = !state.busy
            dialog.getButton(AlertDialog.BUTTON_NEGATIVE).isEnabled = !state.busy
            dialog.getButton(AlertDialog.BUTTON_NEUTRAL)?.isEnabled = !state.busy
            isCancelable = !state.busy
            for (field in fields.values) field.isEnabled = !state.busy
            for (checkbox in repeatControls) checkbox.isEnabled = !state.busy
            if (!state.busy && operation != null && state.operation == operation) {
                if (state.error == null) dismiss() else showError(state.error)
            }
        }
    }
    private fun field(key:String, label:String, limit:Int): EditText {
        val row=layoutInflater.inflate(R.layout.item_planner_field,host,false)
        row.findViewById<TextView>(R.id.planner_field_label).text=label
        val input=row.findViewById<EditText>(R.id.planner_field_input)
        input.id=View.generateViewId(); input.tag=key
        row.findViewById<TextView>(R.id.planner_field_label).labelFor=input.id
        input.filters=arrayOf(android.text.InputFilter.LengthFilter(limit))
        input.setText(draft.optString(key,"")); fields[key]=input;host.addView(row); return input
    }
    private fun addWeeklyRepeatControls() {
        val heading = TextView(requireContext()).apply {
            text = getString(R.string.form_repeat_title)
            textSize = 13f
            setTextColor(android.graphics.Color.rgb(23, 36, 67))
            setPadding(0, dp(14), 0, dp(8))
        }
        host.addView(heading)

        val row = LinearLayout(requireContext()).apply {
            orientation = LinearLayout.HORIZONTAL
            gravity = android.view.Gravity.CENTER
        }

        val initials = requireContext().resources.getStringArray(R.array.planner_weekday_initials)
        val fullNames = requireContext().resources.getStringArray(R.array.planner_weekday_names)
        val days = listOf(
            Calendar.MONDAY, Calendar.TUESDAY, Calendar.WEDNESDAY,
            Calendar.THURSDAY, Calendar.FRIDAY, Calendar.SATURDAY, Calendar.SUNDAY
        ).mapIndexed { index, day -> day to initials[index] }

        days.forEachIndexed { index, pair ->
            val checkbox = CheckBox(requireContext()).apply {
                text = pair.second
                textSize = 12f
                gravity = android.view.Gravity.CENTER
                contentDescription = fullNames[index]
                isChecked = repeatDays.contains(pair.first)
                setPadding(0, 0, 0, 0)
                setOnCheckedChangeListener { _, checked ->
                    if (checked) repeatDays.add(pair.first)
                    else repeatDays.remove(pair.first)
                }
            }
            repeatControls.add(checkbox)
            row.addView(
                checkbox,
                LinearLayout.LayoutParams(0, -2, 1f)
            )
        }
        host.addView(row)

        val hint = TextView(requireContext()).apply {
            text = getString(R.string.form_repeat_hint)
            textSize = 11f
            setTextColor(android.graphics.Color.rgb(102, 114, 139))
            setPadding(0, dp(5), 0, dp(10))
        }
        host.addView(hint)
    }

    private fun dp(value: Int): Int =
        (value * resources.displayMetrics.density + 0.5f).toInt()

    private fun picker(label:String, isEnd:Boolean) {
        val input=field(if(isEnd) "end_display" else "due_display",label,80)
        input.isFocusable=false
        fun update() { input.setText(SimpleDateFormat("EEE, d MMM yyyy · HH:mm",Locale.ENGLISH).format(Date(if(isEnd)end else due))) }
        update()
        input.setOnClickListener {
            val c=Calendar.getInstance().apply { timeInMillis=if(isEnd)end else due }
            DatePickerDialog(requireContext(),{_,y,m,d ->
                c.set(y,m,d)
                TimePickerDialog(requireContext(),{_,h,min ->
                    c.set(Calendar.HOUR_OF_DAY,h);c.set(Calendar.MINUTE,min);c.set(Calendar.SECOND,0);c.set(Calendar.MILLISECOND,0)
                    if(isEnd)end=c.timeInMillis else due=c.timeInMillis
                    update()
                },c.get(Calendar.HOUR_OF_DAY),c.get(Calendar.MINUTE),true).show()
            },c.get(Calendar.YEAR),c.get(Calendar.MONTH),c.get(Calendar.DAY_OF_MONTH)).show()
        }
    }
    private fun save() {
        val data=JSONObject()
        for((key,input) in fields) if(!key.endsWith("_display")) data.put(key,input.text.toString().trim())
        if(kind in listOf("tasks","lessons","notes") && data.optString("title").isBlank()) { fields["title"]?.error="Enter a title";return }
        when(kind) {
            "tasks" -> { data.put("due_at",timeFormat.format(Date(due)));data.put("priority",priority) }
            "lessons" -> {
                if (end <= due) {
                    showError("End time must be after start time.")
                    return
                }

                if (repeatDays.isNotEmpty() && id == null) {
                    val duration = end - due
                    val cursor = Calendar.getInstance().apply {
                        timeInMillis = due
                    }
                    val occurrences = mutableListOf<JSONObject>()

                    repeat(84) {
                        if (cursor.get(Calendar.DAY_OF_WEEK) in repeatDays) {
                            val occurrenceStart = cursor.timeInMillis
                            val occurrenceEnd = occurrenceStart + duration

                            occurrences.add(
                                JSONObject(data.toString())
                                    .put("starts_at", timeFormat.format(Date(occurrenceStart)))
                                    .put("ends_at", timeFormat.format(Date(occurrenceEnd)))
                            )
                        }
                        cursor.add(Calendar.DAY_OF_YEAR, 1)
                    }

                    if (occurrences.isEmpty()) {
                        showError("No matching class dates were generated.")
                        return
                    }

                    operation = UUID.randomUUID().toString()
                    vm.saveLessons(occurrences, operation!!)
                    return
                }

                data.put("starts_at", timeFormat.format(Date(due)))
                data.put("ends_at", timeFormat.format(Date(end)))
            }
            "goal" -> {
                val hours=data.optString("hours").replace(',','.').toDoubleOrNull()
                if(hours==null || !hours.isFinite() || hours !in 0.5..168.0) { fields["hours"]?.error="Enter 0.5 to 168 hours";return }
                data.remove("hours");data.put("weekly_minutes",(hours*60).toInt())
            }
            "focus" -> {
                val minutes=data.optString("minutes").toIntOrNull()
                if(minutes==null || minutes !in 1..1440) { fields["minutes"]?.error="Enter 1 to 1440 minutes";return }
                data.put("minutes",minutes)
            }
        }
        operation=UUID.randomUUID().toString();vm.save(kind,data,id,operation!!)
    }
    private fun showError(message:String) { error.text=message;error.visibility=View.VISIBLE }
    override fun onSaveInstanceState(outState:Bundle) {
        for((k,v) in fields) draft.put(k,v.text.toString())
        outState.putString("draft",draft.toString());outState.putString("operation",operation)
        outState.putLong("due",due);outState.putLong("end",end);outState.putString("priority",priority)
        draft.put("repeat_days", repeatDays.sorted().joinToString(","))
        super.onSaveInstanceState(outState)
    }
    private fun parse(value:String, fallback:Long=System.currentTimeMillis()+3600000):Long = PlannerUi.timestamp(value) ?: fallback
    companion object {
        fun show(activity:androidx.fragment.app.FragmentActivity,kind:String,data:JSONObject?=null) {
            if(activity.supportFragmentManager.findFragmentByTag("planner_form")!=null)return
            PlannerForm().apply { arguments=Bundle().apply { putString("kind",kind);putString("data",data?.toString()?:"{}") } }.show(activity.supportFragmentManager,"planner_form")
        }
    }
}
