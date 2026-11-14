package com.example.studyflowapp

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
