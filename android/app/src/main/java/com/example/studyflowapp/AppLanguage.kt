package com.example.studyflowapp

import android.content.Context
import androidx.appcompat.app.AppCompatDelegate
import androidx.core.os.LocaleListCompat

object AppLanguage {
    private val supported = setOf("ru", "kk", "en")

    fun currentTag(context: Context): String {
        val appLocales = AppCompatDelegate.getApplicationLocales()
        val locale = if (!appLocales.isEmpty) {
            appLocales[0]
        } else {
            context.resources.configuration.locales[0]
        }
        val language = locale?.language ?: "en"
        return if (language in supported) language else "en"
    }

    fun displayName(context: Context, tag: String): String {
        return when (tag) {
            "ru" -> context.getString(R.string.language_russian)
            "kk" -> context.getString(R.string.language_kazakh)
            else -> context.getString(R.string.language_english)
        }
    }

    fun setLanguage(tag: String) {
        val safeTag = if (tag in supported) tag else "en"
        AppCompatDelegate.setApplicationLocales(
            LocaleListCompat.forLanguageTags(safeTag)
        )
    }
}
