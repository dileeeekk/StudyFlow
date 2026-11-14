package com.example.studyflowapp.auth

import android.content.pm.PackageManager
import android.content.Intent
import android.net.Uri
import android.os.Build
import android.provider.Settings
import androidx.activity.result.contract.ActivityResultContracts
import androidx.appcompat.app.AppCompatActivity
import androidx.core.content.ContextCompat
import com.example.studyflowapp.BuildConfig
import com.example.studyflowapp.R
import com.google.android.material.dialog.MaterialAlertDialogBuilder
import java.net.URI

/** The local-network permission is declared only in the debug manifest. */
open class NetworkActivity : AppCompatActivity() {
    private var pendingNetworkAction: (() -> Unit)? = null
    private var retryAfterSettings: (() -> Unit)? = null
    private val permission = registerForActivityResult(ActivityResultContracts.RequestPermission()) { granted ->
        val action = pendingNetworkAction; pendingNetworkAction = null
        if (granted) action?.invoke()
        else showPermissionHelp(action)
    }

    private fun showPermissionHelp(action: (() -> Unit)?) {
        MaterialAlertDialogBuilder(this).setMessage(R.string.auth_local_permission).setCancelable(false)
            .setPositiveButton(R.string.auth_open_settings) { _, _ ->
                retryAfterSettings = action
                startActivity(Intent(Settings.ACTION_APPLICATION_DETAILS_SETTINGS, Uri.parse("package:$packageName")))
            }.setNegativeButton(R.string.auth_cancel) { _, _ -> finish() }.show()
    }

    override fun onResume() {
        super.onResume()
        retryAfterSettings?.let { action ->
            retryAfterSettings = null
            if (ContextCompat.checkSelfPermission(this, "android.permission.ACCESS_LOCAL_NETWORK") == PackageManager.PERMISSION_GRANTED) action()
            else showPermissionHelp(action)
        }
    }

    protected fun withNetworkAccess(action: () -> Unit) {
        val local = BuildConfig.DEBUG && runCatching { URI(BuildConfig.API_BASE_URL).host }.getOrNull() in
            setOf("10.0.2.2", "127.0.0.1", "localhost")
        val permissionName = "android.permission.ACCESS_LOCAL_NETWORK"
        if (local && Build.VERSION.SDK_INT >= 37 && ContextCompat.checkSelfPermission(this, permissionName) != PackageManager.PERMISSION_GRANTED) {
            if (pendingNetworkAction == null) {
                pendingNetworkAction = action
                permission.launch(permissionName)
            }
        } else action()
    }
}
