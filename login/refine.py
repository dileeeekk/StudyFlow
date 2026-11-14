from pathlib import Path
HERE=Path(__file__).resolve().parent
main=HERE/'StudyFlowApp-login/app/src/main'
p=main/'java/com/example/studyflowapp/LoginActivity.kt'
t=p.read_text(encoding='utf-8').replace('import android.graphics.Rect\n','').replace('import androidx.core.view.updatePadding','import androidx.core.view.updatePadding\nimport androidx.core.widget.NestedScrollView')
t=t.replace('val scroll = findViewById<View>(R.id.login_scroll)','val scroll = findViewById<NestedScrollView>(R.id.login_scroll)')
t=t.replace('        var previousImeBottom = 0','''        fun revealFocusedField() {
            val field = currentFocus as? EditText ?: return
            scroll.post {
                val fieldPosition = IntArray(2)
                val scrollPosition = IntArray(2)
                field.getLocationOnScreen(fieldPosition)
                scroll.getLocationOnScreen(scrollPosition)
                val visibleBottom = scrollPosition[1] + scroll.height - scroll.paddingBottom - dp(12)
                val overlap = fieldPosition[1] + field.height - visibleBottom
                if (overlap > 0) scroll.smoothScrollBy(0, overlap)
            }
        }
        var previousImeBottom = 0''')
t=t.replace('''                currentFocus?.takeIf { it is EditText }?.let { field ->
                    field.post { field.requestRectangleOnScreen(Rect(0, 0, field.width, field.height), false) }
                }''','''                revealFocusedField()''')
t=t.replace('''        val toggle = findViewById<ImageButton>''','''        val email = findViewById<EditText>(R.id.login_email)
        for (field in listOf(email, password)) {
            field.setOnFocusChangeListener { _, focused ->
                if (focused && previousImeBottom > 0) revealFocusedField()
            }
        }
        val toggle = findViewById<ImageButton>''')
p.write_text(t,encoding='utf-8')
p=main/'res/layout/activity_login.xml'
t=p.read_text(encoding='utf-8').replace('android:fillViewport="true" android:clipToPadding="false"','android:fillViewport="true" android:clipToPadding="true"')
p.write_text(t,encoding='utf-8')
print('Refined keyboard scrolling and system-bar clipping.')
