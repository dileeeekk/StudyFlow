package com.example.studyflowapp

import android.graphics.Color
import android.graphics.Rect
import android.os.Bundle
import android.view.TouchDelegate
import android.view.View
import androidx.activity.SystemBarStyle
import androidx.activity.enableEdgeToEdge
import androidx.appcompat.app.AppCompatActivity
import androidx.core.view.ViewCompat
import androidx.core.view.WindowInsetsCompat
import androidx.core.view.updatePadding

class OnboardingActivity : AppCompatActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        enableEdgeToEdge(
            statusBarStyle = SystemBarStyle.light(Color.TRANSPARENT, Color.TRANSPARENT),
            navigationBarStyle = SystemBarStyle.light(
                Color.TRANSPARENT,
                Color.rgb(23, 36, 67)
            )
        )
        setContentView(R.layout.activity_onboarding)

        // The View API works from API 21; the XML attribute requires API 31.
        findViewById<View>(R.id.onboarding_hero).clipToOutline = true

        val scroll = findViewById<View>(R.id.onboarding_scroll)
        ViewCompat.setOnApplyWindowInsetsListener(scroll) { view, insets ->
            val bars = insets.getInsets(WindowInsetsCompat.Type.systemBars())
            val cutout = insets.getInsets(WindowInsetsCompat.Type.displayCutout())
            view.updatePadding(
                left = maxOf(bars.left, cutout.left),
                top = maxOf(bars.top, cutout.top, dp(44)) + dp(10),
                right = maxOf(bars.right, cutout.right),
                bottom = maxOf(bars.bottom, cutout.bottom, dp(34))
            )
            insets
        }
        ViewCompat.requestApplyInsets(scroll)

        // Make the small Log In text easier to tap without changing its position.
        val login = findViewById<View>(R.id.onboarding_login)
        val footer = findViewById<View>(R.id.onboarding_account_row)
        footer.post {
            val touchArea = Rect()
            login.getHitRect(touchArea)
            touchArea.inset(-dp(12), 0)
            footer.touchDelegate = TouchDelegate(touchArea, login)
        }
        // Buttons currently use their XML ripple feedback only.
    }

    private fun dp(value: Int): Int =
        (value * resources.displayMetrics.density + 0.5f).toInt()
}
