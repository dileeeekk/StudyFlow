package com.example.studyflowapp.planner

import android.Manifest
import android.app.NotificationChannel
import android.app.NotificationManager
import android.app.PendingIntent
import android.content.Context
import android.content.Intent
import android.content.pm.PackageManager
import android.os.Build
import androidx.core.app.NotificationCompat
import androidx.core.app.NotificationManagerCompat
import androidx.core.content.ContextCompat
import androidx.work.Data
import androidx.work.ExistingWorkPolicy
import androidx.work.OneTimeWorkRequestBuilder
import androidx.work.WorkManager
import androidx.work.Worker
import androidx.work.WorkerParameters
import com.example.studyflowapp.MainActivity
import org.json.JSONObject
import java.text.SimpleDateFormat
import java.util.Date
import java.util.Locale
import java.util.concurrent.TimeUnit

private data class ReminderSpec(
    val key: String,
    val fingerprint: String,
    val type: String,
    val title: String,
    val eventAt: Long
)

object DeadlineReminderScheduler {
    private const val PREFS = "studyflow_deadline_schedule"
    private const val SNAPSHOT = "scheduled_snapshot"
    private const val WORK_PREFIX = "studyflow_deadline_"
    private const val CHANNEL_ID = "studyflow_deadlines"

    fun sync(context: Context, snapshot: JSONObject): Boolean {
        createChannel(context)

        val now = System.currentTimeMillis()
        val current = JSONObject()
        val reminders = mutableListOf<ReminderSpec>()

        // Task reminders: 30 minutes before deadline.
        val tasks = snapshot.optJSONArray("tasks")
        if (tasks != null) {
            for (i in 0 until tasks.length()) {
                val task = tasks.optJSONObject(i) ?: continue
                if (task.optBoolean("completed")) continue

                val id = task.optLong("id", -1L)
                val title = task.optString("title").trim()
                val dueAt = PlannerUi.timestamp(task.optString("due_at"))

                if (id <= 0L || title.isBlank() || dueAt == null || dueAt <= now) {
                    continue
                }

                val key = "task_$id"
                val fingerprint = "$dueAt:${title.hashCode()}"

                current.put(key, fingerprint)
                reminders.add(
                    ReminderSpec(key, fingerprint, "task", title, dueAt)
                )
            }
        }

        // Class reminders: 15 minutes before lesson starts.
        val lessons = snapshot.optJSONArray("lessons")
        if (lessons != null) {
            for (i in 0 until lessons.length()) {
                val lesson = lessons.optJSONObject(i) ?: continue

                val id = lesson.optLong("id", -1L)
                val title = lesson.optString("title").trim()
                val startsAt = PlannerUi.timestamp(lesson.optString("starts_at"))

                if (id <= 0L || title.isBlank() || startsAt == null || startsAt <= now) {
                    continue
                }

                val key = "class_$id"
                val fingerprint = "$startsAt:${title.hashCode()}"

                current.put(key, fingerprint)
                reminders.add(
                    ReminderSpec(key, fingerprint, "class", title, startsAt)
                )
            }
        }

        val prefs = context.getSharedPreferences(PREFS, Context.MODE_PRIVATE)
        val previous = try {
            JSONObject(prefs.getString(SNAPSHOT, "{}") ?: "{}")
        } catch (_: Exception) {
            JSONObject()
        }

        val manager = WorkManager.getInstance(context)

        // Cancel reminders for deleted, completed, or expired entries.
        val oldKeys = previous.keys()
        while (oldKeys.hasNext()) {
            val key = oldKeys.next()
            if (!current.has(key)) {
                manager.cancelUniqueWork(WORK_PREFIX + key)
            }
        }

        // Schedule only new or changed reminders.
        val keys = current.keys()
        while (keys.hasNext()) {
            val key = keys.next()
            val fingerprint = current.optString(key)

            if (previous.optString(key) == fingerprint) continue

            val reminder = reminders.firstOrNull { it.key == key } ?: continue

            val leadTime = if (reminder.type == "class") {
                TimeUnit.MINUTES.toMillis(15)
            } else {
                TimeUnit.MINUTES.toMillis(30)
            }

            val reminderAt = reminder.eventAt - leadTime
            val delay = (reminderAt - now).coerceAtLeast(0L)

            val input = Data.Builder()
                .putString("reminder_key", reminder.key)
                .putString("reminder_type", reminder.type)
                .putString("reminder_title", reminder.title)
                .putLong("event_at", reminder.eventAt)
                .build()

            val request = OneTimeWorkRequestBuilder<DeadlineReminderWorker>()
                .setInputData(input)
                .setInitialDelay(delay, TimeUnit.MILLISECONDS)
                .addTag(WORK_PREFIX + reminder.type)
                .build()

            manager.enqueueUniqueWork(
                WORK_PREFIX + key,
                ExistingWorkPolicy.REPLACE,
                request
            )
        }

        prefs.edit().putString(SNAPSHOT, current.toString()).apply()

        // HomeActivity uses this result to request notification permission.
        return current.length() > 0
    }

    internal fun channelId() = CHANNEL_ID

    private fun createChannel(context: Context) {
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
            val channel = NotificationChannel(
                CHANNEL_ID,
                "StudyFlow reminders",
                NotificationManager.IMPORTANCE_DEFAULT
            ).apply {
                description = "Upcoming tasks and class reminders"
            }

            context.getSystemService(NotificationManager::class.java)
                .createNotificationChannel(channel)
        }
    }
}

class DeadlineReminderWorker(
    context: Context,
    params: WorkerParameters
) : Worker(context, params) {

    override fun doWork(): Result {
        val context = applicationContext

        val key = inputData.getString("reminder_key").orEmpty()
        val type = inputData.getString("reminder_type").orEmpty()
        val title = inputData.getString("reminder_title").orEmpty()
        val eventAt = inputData.getLong("event_at", -1L)

        if (key.isBlank() || title.isBlank() || eventAt <= 0L ||
            type !in setOf("task", "class")) {
            return Result.failure()
        }

        val notifications = NotificationManagerCompat.from(context)

        if (!notifications.areNotificationsEnabled()) {
            return Result.success()
        }

        if (Build.VERSION.SDK_INT >= 33 &&
            ContextCompat.checkSelfPermission(
                context,
                Manifest.permission.POST_NOTIFICATIONS
            ) != PackageManager.PERMISSION_GRANTED) {
            return Result.success()
        }

        val now = System.currentTimeMillis()

        // Do not send a stale class reminder after the lesson has started.
        if (type == "class" && now >= eventAt) {
            return Result.success()
        }

        val dateText = SimpleDateFormat(
            "EEE, d MMM · HH:mm",
            Locale.getDefault()
        ).format(Date(eventAt))

        val heading: String
        val message: String

        if (type == "class") {
            heading = "Class starts in 15 minutes"
            message = "$title · Starts at $dateText"
        } else {
            heading = if (now < eventAt) {
                "Upcoming deadline"
            } else {
                "Deadline time"
            }
            message = "$title · Due $dateText"
        }

        val intent = Intent(context, MainActivity::class.java).apply {
            flags = Intent.FLAG_ACTIVITY_NEW_TASK or Intent.FLAG_ACTIVITY_CLEAR_TOP
        }

        val pendingIntent = PendingIntent.getActivity(
            context,
            key.hashCode(),
            intent,
            PendingIntent.FLAG_UPDATE_CURRENT or PendingIntent.FLAG_IMMUTABLE
        )

        val notification = NotificationCompat.Builder(
            context,
            DeadlineReminderScheduler.channelId()
        )
            .setSmallIcon(android.R.drawable.ic_dialog_info)
            .setContentTitle(heading)
            .setContentText(message)
            .setStyle(NotificationCompat.BigTextStyle().bigText(message))
            .setContentIntent(pendingIntent)
            .setAutoCancel(true)
            .setPriority(NotificationCompat.PRIORITY_DEFAULT)
            .build()

        return try {
            notifications.notify(key.hashCode(), notification)
            Result.success()
        } catch (_: SecurityException) {
            Result.success()
        }
    }
}
