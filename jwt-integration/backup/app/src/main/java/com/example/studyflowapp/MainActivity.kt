package com.example.studyflowapp

import android.content.Intent
import android.graphics.Color
import android.os.Build
import android.os.Bundle
import android.os.Handler
import android.os.Looper
import android.view.View
import androidx.activity.SystemBarStyle
import androidx.activity.enableEdgeToEdge
import androidx.appcompat.app.AppCompatActivity
import androidx.core.view.doOnPreDraw

class MainActivity : AppCompatActivity() {
    private val handler = Handler(Looper.getMainLooper())
    private var activityStarted = false
    private var contentDrawn = false
    private var systemSplashDismissed = Build.VERSION.SDK_INT < Build.VERSION_CODES.S

    private val openOnboarding = Runnable {
        if (activityStarted && contentDrawn && systemSplashDismissed) {
            startActivity(Intent(this, OnboardingActivity::class.java))
            finish()
        }
    }

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        enableEdgeToEdge(
            statusBarStyle = SystemBarStyle.dark(Color.TRANSPARENT),
            navigationBarStyle = SystemBarStyle.dark(Color.TRANSPARENT)
        )
        setContentView(R.layout.activity_main)
        val content = findViewById<View>(R.id.main)

        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.S) {
            splashScreen.setOnExitAnimationListener { systemSplash ->
                systemSplash.remove()
                content.postOnAnimation {
                    systemSplashDismissed = true
                    scheduleOnboardingIfVisible()
                }
            }
        }

        content.doOnPreDraw {
            content.postOnAnimation {
                contentDrawn = true
                scheduleOnboardingIfVisible()
            }
        }
    }

    override fun onStart() {
        super.onStart()
        activityStarted = true
        scheduleOnboardingIfVisible()
    }

    override fun onStop() {
        activityStarted = false
        handler.removeCallbacks(openOnboarding)
        super.onStop()
    }

    private fun scheduleOnboardingIfVisible() {
        handler.removeCallbacks(openOnboarding)
        if (activityStarted && contentDrawn && systemSplashDismissed) {
            // UI preview duration; real data loading has not been connected yet.
            handler.postDelayed(openOnboarding, 1_500L)
        }
    }
}
