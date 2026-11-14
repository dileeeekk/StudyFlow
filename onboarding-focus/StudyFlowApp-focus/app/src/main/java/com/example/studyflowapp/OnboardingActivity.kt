package com.example.studyflowapp

import android.content.Intent
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
    private var openingNextPage = false

    private companion object {
        const val EXTRA_PAGE_INDEX = "com.example.studyflowapp.ONBOARDING_PAGE"
    }

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        enableEdgeToEdge(
            statusBarStyle = SystemBarStyle.light(Color.TRANSPARENT, Color.TRANSPARENT),
            navigationBarStyle = SystemBarStyle.light(
                Color.TRANSPARENT,
                Color.rgb(23, 36, 67)
            )
        )
        val pageIndex = intent.getIntExtra(EXTRA_PAGE_INDEX, 0).coerceIn(0, 2)
        setContentView(
            when (pageIndex) {
                1 -> R.layout.activity_onboarding_classes
                2 -> R.layout.activity_onboarding_focus
                else -> R.layout.activity_onboarding
            }
        )

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
        // Temporary navigation between the three completed onboarding layouts.
        if (pageIndex < 2) {
            findViewById<View>(R.id.onboarding_get_started).setOnClickListener {
                if (!openingNextPage) {
                    openingNextPage = true
                    startActivity(
                        Intent(this, OnboardingActivity::class.java)
                            .putExtra(EXTRA_PAGE_INDEX, pageIndex + 1)
                    )
                }
            }
        }
        // Skip, Log In and the final page CTA use ripple feedback only.
    }

    override fun onResume() {
        super.onResume()
        openingNextPage = false
    }

    private fun dp(value: Int): Int =
        (value * resources.displayMetrics.density + 0.5f).toInt()
}
