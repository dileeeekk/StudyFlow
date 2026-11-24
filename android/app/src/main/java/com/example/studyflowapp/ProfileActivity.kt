package com.example.studyflowapp

import android.content.Intent
import android.content.res.ColorStateList
import android.graphics.Color
import android.graphics.Typeface
import android.graphics.drawable.GradientDrawable
import android.os.Bundle
import android.view.Gravity
import android.view.View
import android.widget.LinearLayout
import android.widget.ScrollView
import android.widget.TextView
import android.widget.Toast
import androidx.activity.SystemBarStyle
import androidx.activity.enableEdgeToEdge
import androidx.lifecycle.ViewModelProvider
import com.example.studyflowapp.auth.AuthViewModel
import com.example.studyflowapp.auth.NetworkActivity
import com.google.android.material.button.MaterialButton
import com.google.android.material.card.MaterialCardView
import com.google.android.material.dialog.MaterialAlertDialogBuilder

class ProfileActivity : NetworkActivity() {
    private val ink = Color.rgb(23, 36, 67)
    private val muted = Color.rgb(102, 114, 139)
    private val primary = Color.rgb(69, 100, 237)
    private val page = Color.rgb(246, 248, 253)

    private lateinit var auth: AuthViewModel
    private lateinit var name: TextView
    private lateinit var email: TextView
    private lateinit var university: TextView
    private lateinit var initials: TextView
    private lateinit var status: TextView
    private lateinit var retry: MaterialButton
    private lateinit var logout: MaterialButton
    private lateinit var languageValue: TextView
    private var leaving = false

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)

        auth = ViewModelProvider(this)[AuthViewModel::class.java]

        enableEdgeToEdge(
            statusBarStyle = SystemBarStyle.light(page, page),
            navigationBarStyle = SystemBarStyle.light(Color.WHITE, Color.WHITE)
        )

        val scroll = ScrollView(this).apply {
            setBackgroundColor(page)
            clipToPadding = false
            isFillViewport = true
        }

        val content = LinearLayout(this).apply {
            orientation = LinearLayout.VERTICAL
            setPadding(dp(22), dp(18), dp(22), dp(28))
        }

        scroll.addView(content)
        setContentView(scroll)
        ViewCompatInsets.apply(scroll, dp(18), dp(18))

        val back = TextView(this).apply {
            text = getString(R.string.profile_back)
            textSize = 16f
            setTextColor(primary)
            typeface = Typeface.create("sans-serif-medium", Typeface.NORMAL)
            setPadding(0, dp(8), 0, dp(18))
            isClickable = true
            isFocusable = true
            setOnClickListener { finish() }
        }
        content.addView(back)

        content.addView(label(getString(R.string.profile_title), 28f, ink, true))
        content.addView(label(getString(R.string.profile_subtitle), 14f, muted, false).withTop(6))

        val hero = card()
        val heroBody = vertical().apply {
            setPadding(dp(18), dp(20), dp(18), dp(20))
        }

        val top = LinearLayout(this).apply {
            orientation = LinearLayout.HORIZONTAL
            gravity = Gravity.CENTER_VERTICAL
        }

        initials = TextView(this).apply {
            gravity = Gravity.CENTER
            textSize = 22f
            setTextColor(primary)
            typeface = Typeface.create("sans-serif", Typeface.BOLD)
            background = GradientDrawable().apply {
                shape = GradientDrawable.OVAL
                setColor(Color.rgb(234, 238, 255))
            }
        }
        top.addView(initials, LinearLayout.LayoutParams(dp(62), dp(62)))

        val identity = vertical().apply {
            setPadding(dp(14), 0, 0, 0)
        }

        name = label(getString(R.string.profile_loading), 18f, ink, true)
        email = label("", 13f, muted, false).withTop(5)
        identity.addView(name)
        identity.addView(email)

        top.addView(identity, LinearLayout.LayoutParams(0, -2, 1f))
        heroBody.addView(top)
        hero.addView(heroBody)
        content.addView(hero, marginTop(22))

        content.addView(label(getString(R.string.profile_account_details), 11f, muted, true).withTop(26))

        val details = card()
        val detailsBody = vertical().apply {
            setPadding(dp(18), dp(8), dp(18), dp(8))
        }

        university = addDetail(detailsBody, getString(R.string.profile_university), getString(R.string.profile_loading_value))
        addDivider(detailsBody)
        addStaticDetail(detailsBody, getString(R.string.profile_account_type), getString(R.string.profile_student_account))
        details.addView(detailsBody)
        content.addView(details, marginTop(12))


        content.addView(label(getString(R.string.profile_language_section), 11f, muted, true).withTop(26))

        val languageCard = card().apply {
            isClickable = true
            isFocusable = true
            setOnClickListener { showLanguagePicker() }
        }
        val languageBody = vertical().apply {
            setPadding(dp(18), dp(16), dp(18), dp(16))
            addView(label(getString(R.string.profile_language_title), 15f, ink, true))
            languageValue = label(
                AppLanguage.displayName(this@ProfileActivity, AppLanguage.currentTag(this@ProfileActivity)),
                14f, primary, true
            ).withTop(7)
            addView(languageValue)
            addView(label(getString(R.string.profile_language_description), 12f, muted, false).withTop(5))
        }
        languageCard.addView(languageBody)
        content.addView(languageCard, marginTop(12))


        content.addView(label(getString(R.string.profile_account_status), 11f, muted, true).withTop(26))

        val statusCard = card()
        val statusBody = vertical().apply {
            setPadding(dp(18), dp(16), dp(18), dp(16))
        }
        statusBody.addView(label(getString(R.string.profile_connected), 15f, ink, true))
        statusBody.addView(
            label(
                getString(R.string.profile_connected_description),
                13f, muted, false
            ).withTop(7)
        )
        statusCard.addView(statusBody)
        content.addView(statusCard, marginTop(12))

        status = label(getString(R.string.profile_loading_account), 13f, muted, false).withTop(18)
        content.addView(status)

        retry = MaterialButton(this).apply {
            text = getString(R.string.profile_retry)
            isAllCaps = false
            visibility = View.GONE
            cornerRadius = dp(14)
            backgroundTintList = ColorStateList.valueOf(Color.WHITE)
            setTextColor(primary)
            strokeWidth = dp(1)
            strokeColor = ColorStateList.valueOf(Color.rgb(220, 226, 240))
            setOnClickListener {
                status.text = getString(R.string.profile_refreshing)
                visibility = View.GONE
                withNetworkAccess { auth.loadProfile(retry = true) }
            }
        }
        content.addView(retry, marginTop(8))

        logout = MaterialButton(this).apply {
            text = getString(R.string.profile_sign_out)
            isAllCaps = false
            cornerRadius = dp(16)
            backgroundTintList = ColorStateList.valueOf(primary)
            setTextColor(Color.WHITE)
            setOnClickListener {
                if (auth.state.value?.loading != true) {
                    isEnabled = false
                    text = getString(R.string.profile_signing_out)
                    auth.logout()
                }
            }
        }
        content.addView(logout, marginTop(26))

        content.addView(
            label(getString(R.string.profile_footer), 11f, muted, false)
                .apply { gravity = Gravity.CENTER }
                .withTop(20)
        )

        auth.state.observe(this) { state ->
            state.user?.let { user ->
                name.text = user.fullName
                email.text = user.email
                university.text = user.university

                initials.text = user.fullName.trim()
                    .split(Regex("\\s+"))
                    .filter { it.isNotBlank() }
                    .take(2)
                    .map { it.take(1).uppercase() }
                    .joinToString("")
                    .ifBlank { "S" }

                status.text = getString(R.string.profile_up_to_date)
                retry.visibility = View.GONE
                logout.isEnabled = true
                logout.text = getString(R.string.profile_sign_out)
            }

            if (state.loading && state.user == null) {
                status.text = getString(R.string.profile_loading_account)
            } else if (state.error != null && state.user == null) {
                status.text = state.error
                retry.visibility = View.VISIBLE
            }

            if (state.loggedOut && !leaving) {
                leaving = true
                state.error?.let {
                    Toast.makeText(this, it, Toast.LENGTH_LONG).show()
                }

                startActivity(
                    Intent(this, LoginActivity::class.java)
                        .addFlags(Intent.FLAG_ACTIVITY_NEW_TASK or Intent.FLAG_ACTIVITY_CLEAR_TASK)
                )
                finish()
            }
        }

        withNetworkAccess { auth.loadProfile() }
    }


    private fun showLanguagePicker() {
        val tags = arrayOf("ru", "kk", "en")
        val labels = arrayOf(
            getString(R.string.language_russian),
            getString(R.string.language_kazakh),
            getString(R.string.language_english)
        )
        val selected = tags.indexOf(AppLanguage.currentTag(this)).coerceAtLeast(0)

        MaterialAlertDialogBuilder(this)
            .setTitle(R.string.profile_language_title)
            .setSingleChoiceItems(labels, selected) { dialog, which ->
                dialog.dismiss()
                if (tags[which] != AppLanguage.currentTag(this)) {
                    AppLanguage.setLanguage(tags[which])
                }
            }
            .setNegativeButton(R.string.common_cancel, null)
            .show()
    }

    private fun vertical() = LinearLayout(this).apply {
        orientation = LinearLayout.VERTICAL
    }

    private fun card() = MaterialCardView(this).apply {
        radius = dp(22).toFloat()
        cardElevation = 0f
        setCardBackgroundColor(Color.WHITE)
        strokeWidth = dp(1)
        setStrokeColor(ColorStateList.valueOf(Color.rgb(232, 236, 245)))
    }

    private fun label(value: String, size: Float, color: Int, bold: Boolean) =
        TextView(this).apply {
            text = value
            textSize = size
            setTextColor(color)
            typeface = Typeface.create(
                "sans-serif",
                if (bold) Typeface.BOLD else Typeface.NORMAL
            )
        }

    private fun TextView.withTop(top: Int): TextView {
        layoutParams = LinearLayout.LayoutParams(-1, -2).apply {
            topMargin = dp(top)
        }
        return this
    }

    private fun marginTop(top: Int) =
        LinearLayout.LayoutParams(-1, -2).apply {
            topMargin = dp(top)
        }

    private fun addDetail(parent: LinearLayout, title: String, value: String): TextView {
        val block = vertical().apply {
            setPadding(0, dp(12), 0, dp(12))
            addView(label(title, 12f, muted, false))
        }
        val valueView = label(value, 15f, ink, true).withTop(5)
        block.addView(valueView)
        parent.addView(block)
        return valueView
    }

    private fun addStaticDetail(parent: LinearLayout, title: String, value: String) {
        val block = vertical().apply {
            setPadding(0, dp(12), 0, dp(12))
            addView(label(title, 12f, muted, false))
            addView(label(value, 15f, ink, true).withTop(5))
        }
        parent.addView(block)
    }

    private fun addDivider(parent: LinearLayout) {
        parent.addView(View(this).apply {
            setBackgroundColor(Color.rgb(237, 240, 247))
        }, LinearLayout.LayoutParams(-1, dp(1)))
    }

    private fun dp(value: Int): Int =
        (value * resources.displayMetrics.density + 0.5f).toInt()

    private object ViewCompatInsets {
        fun apply(view: View, horizontal: Int, vertical: Int) {
            androidx.core.view.ViewCompat.setOnApplyWindowInsetsListener(view) { target, insets ->
                val bars = insets.getInsets(
                    androidx.core.view.WindowInsetsCompat.Type.systemBars() or
                        androidx.core.view.WindowInsetsCompat.Type.displayCutout()
                )
                target.setPadding(
                    horizontal + bars.left,
                    vertical + bars.top,
                    horizontal + bars.right,
                    vertical + bars.bottom
                )
                insets
            }
            androidx.core.view.ViewCompat.requestApplyInsets(view)
        }
    }
}
