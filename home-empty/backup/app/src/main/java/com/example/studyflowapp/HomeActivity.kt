package com.example.studyflowapp

import android.content.Intent
import android.widget.TextView
import android.widget.Toast
import android.graphics.Color
import android.graphics.Rect
import android.os.Bundle
import android.view.TouchDelegate
import android.view.View
import android.view.ViewGroup
import androidx.activity.SystemBarStyle
import androidx.activity.enableEdgeToEdge
import androidx.lifecycle.ViewModelProvider
import com.example.studyflowapp.auth.AuthViewModel
import com.example.studyflowapp.auth.NetworkActivity
import com.google.android.material.dialog.MaterialAlertDialogBuilder
import androidx.core.view.ViewCompat
import androidx.core.view.WindowInsetsCompat
import androidx.core.view.updateLayoutParams
import androidx.core.view.updatePadding

/** Authenticated account; task and schedule cards still contain Figma preview data. */
class HomeActivity : NetworkActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        enableEdgeToEdge(
            statusBarStyle = SystemBarStyle.light(Color.TRANSPARENT, Color.TRANSPARENT),
            navigationBarStyle = SystemBarStyle.light(Color.TRANSPARENT, Color.rgb(23, 36, 67))
        )
        setContentView(R.layout.activity_home)
        val root = findViewById<View>(R.id.home_root)
        val auth = ViewModelProvider(this)[AuthViewModel::class.java]
        root.visibility = View.INVISIBLE
        fun returnToLogin() {
            startActivity(Intent(this, LoginActivity::class.java)
                .addFlags(Intent.FLAG_ACTIVITY_NEW_TASK or Intent.FLAG_ACTIVITY_CLEAR_TASK))
            finish()
        }
        auth.state.observe(this) { state ->
            if (state.expired || state.loggedOut) {
                state.error?.let { Toast.makeText(this, it, Toast.LENGTH_LONG).show() }
                returnToLogin()
            } else if (state.user != null) {
                root.visibility = View.VISIBLE
                val user = state.user
                val firstName = user.fullName.trim().split(Regex("\\s+"), limit = 2).first()
                findViewById<TextView>(R.id.home_greeting).text = getString(R.string.auth_greeting, firstName)
                findViewById<View>(R.id.home_tab_profile).setOnClickListener {
                    if (auth.state.value?.loading == true) return@setOnClickListener
                    MaterialAlertDialogBuilder(this).setTitle(R.string.auth_account)
                        .setMessage("${user.fullName}\n${user.email}\n${user.university}")
                        .setNegativeButton(R.string.auth_cancel, null)
                        .setPositiveButton(R.string.auth_logout) { _, _ -> auth.logout() }.show()
                }
            } else if (state.error != null) {
                MaterialAlertDialogBuilder(this).setTitle(R.string.auth_offline_title)
                    .setMessage(state.error).setCancelable(false)
                    .setPositiveButton(R.string.auth_retry) { _, _ -> withNetworkAccess { auth.loadProfile(retry = true) } }
                    .setNegativeButton(R.string.auth_logout) { _, _ -> auth.logout() }.show()
            }
        }
        withNetworkAccess { auth.loadProfile() }

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
