package com.example.studyflowapp

import android.content.Intent
import android.graphics.Color
import android.os.Bundle
import android.os.Handler
import android.os.Looper
import androidx.activity.SystemBarStyle
import androidx.activity.enableEdgeToEdge
import androidx.appcompat.app.AppCompatActivity

class MainActivity : AppCompatActivity() {
    private val handler = Handler(Looper.getMainLooper())
    private val openOnboarding = Runnable {
        startActivity(Intent(this, OnboardingActivity::class.java))
        finish()
    }

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        enableEdgeToEdge(
            statusBarStyle = SystemBarStyle.dark(Color.TRANSPARENT),
            navigationBarStyle = SystemBarStyle.dark(Color.TRANSPARENT)
        )
        setContentView(R.layout.activity_main)
    }

    override fun onStart() {
        super.onStart()
        // Temporary UI transition; no loading or account checks yet.
        handler.postDelayed(openOnboarding, 1_200L)
    }

    override fun onStop() {
        handler.removeCallbacks(openOnboarding)
        super.onStop()
    }
}
