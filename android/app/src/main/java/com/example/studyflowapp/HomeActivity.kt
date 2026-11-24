package com.example.studyflowapp

import android.content.Intent
import android.content.pm.PackageManager
import android.Manifest
import android.widget.TextView
import android.widget.Toast
import android.graphics.Color
import android.os.Bundle
import android.os.Build
import android.view.View
import androidx.activity.SystemBarStyle
import androidx.activity.result.contract.ActivityResultContracts
import androidx.activity.enableEdgeToEdge
import androidx.core.content.ContextCompat
import androidx.lifecycle.ViewModelProvider
import com.example.studyflowapp.auth.AuthViewModel
import com.example.studyflowapp.auth.NetworkActivity
import com.google.android.material.dialog.MaterialAlertDialogBuilder
import androidx.core.view.ViewCompat
import androidx.core.view.WindowInsetsCompat
import androidx.core.view.updatePadding

/** Authenticated dashboard backed by the account planner. */
class HomeActivity : NetworkActivity() {
    private val notificationPermissionLauncher =
        registerForActivityResult(ActivityResultContracts.RequestPermission()) { granted ->
            if (!granted) {
                Toast.makeText(
                    this,
                    getString(R.string.notification_disabled),
                    Toast.LENGTH_LONG
                ).show()
            }
        }

    private var planner: com.example.studyflowapp.planner.PlannerUi? = null
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
                if (planner == null) {
                    planner = com.example.studyflowapp.planner.PlannerUi(this, ::returnToLogin, ::requestDeadlinePermission).also {
                        it.start(savedInstanceState?.getString("planner_tab") ?: "home")
                    }
                }
                val user = state.user
                val firstName = user.fullName.trim().split(Regex("\\s+"), limit = 2).first()
                findViewById<TextView>(R.id.home_greeting).text = getString(R.string.auth_greeting, firstName)
                findViewById<View>(R.id.home_tab_profile).setOnClickListener {
                    if (auth.state.value?.loading == true) return@setOnClickListener
                    startActivity(Intent(this, ProfileActivity::class.java))
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
        
        ViewCompat.setOnApplyWindowInsetsListener(root) { _, insets ->
            val safe = insets.getInsets(WindowInsetsCompat.Type.systemBars() or WindowInsetsCompat.Type.displayCutout())
            scroll.updatePadding(left = safe.left, top = maxOf(safe.top, dp(44)) + dp(16), right = safe.right)
            navigation.updatePadding(left = safe.left, right = safe.right, bottom = maxOf(safe.bottom, dp(34)))

            insets
        }
        ViewCompat.requestApplyInsets(root)
        findViewById<View>(R.id.home_tab_home).isSelected = true
        // Show the actual date rather than the date in the Figma example.
        findViewById<TextView>(R.id.home_date).text = java.text.SimpleDateFormat(
            "EEEE, d MMMM", resources.configuration.locales[0]
        ).format(java.util.Date()).uppercase(resources.configuration.locales[0])
        onBackPressedDispatcher.addCallback(this, object : androidx.activity.OnBackPressedCallback(true) {
            override fun handleOnBackPressed() {
                if (planner?.back() == true) return
                isEnabled = false; onBackPressedDispatcher.onBackPressed(); isEnabled = true
            }
        })
    }

    override fun onResume() {
        super.onResume()
        planner?.refresh()
    }

    override fun onSaveInstanceState(outState: Bundle) {
        outState.putString("planner_tab", planner?.currentTab() ?: "home")
        super.onSaveInstanceState(outState)
    }


    private fun requestDeadlinePermission() {
        if (Build.VERSION.SDK_INT < Build.VERSION_CODES.TIRAMISU) return

        if (ContextCompat.checkSelfPermission(
                this, Manifest.permission.POST_NOTIFICATIONS
            ) == PackageManager.PERMISSION_GRANTED
        ) return

        val preferences = getSharedPreferences("studyflow_permissions", MODE_PRIVATE)
        if (preferences.getBoolean("deadline_permission_prompt_shown", false)) return

        preferences.edit()
            .putBoolean("deadline_permission_prompt_shown", true)
            .apply()

        MaterialAlertDialogBuilder(this)
            .setTitle(getString(R.string.reminder_title))
            .setMessage(
                getString(R.string.reminder_message)
            )
            .setNegativeButton(getString(R.string.reminder_not_now), null)
            .setPositiveButton(getString(R.string.reminder_enable)) { _, _ ->
                notificationPermissionLauncher.launch(Manifest.permission.POST_NOTIFICATIONS)
            }
            .show()
    }

    private fun dp(value: Int): Int = (value * resources.displayMetrics.density + 0.5f).toInt()
}
