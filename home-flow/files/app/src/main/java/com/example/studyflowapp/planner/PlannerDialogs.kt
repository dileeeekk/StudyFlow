package com.example.studyflowapp.planner

import android.content.Context
import android.graphics.Color
import android.graphics.drawable.GradientDrawable
import com.example.studyflowapp.R
import com.google.android.material.dialog.MaterialAlertDialogBuilder

internal fun plannerDialog(context: Context): MaterialAlertDialogBuilder =
    MaterialAlertDialogBuilder(context, R.style.StudyFlow_PlannerDialog).setBackground(
        GradientDrawable().apply {
            setColor(Color.WHITE)
            cornerRadius = 24f * context.resources.displayMetrics.density
        }
    )
