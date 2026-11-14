package com.example.studyflowapp.auth

import android.app.Application
import android.os.Handler
import android.os.Looper
import androidx.lifecycle.AndroidViewModel
import androidx.lifecycle.LiveData
import androidx.lifecycle.MutableLiveData
import java.util.concurrent.Executors

data class AuthState(val loading: Boolean = false, val user: AccountUser? = null,
    val error: String? = null, val expired: Boolean = false, val loggedOut: Boolean = false)

/** Retains the request across rotation, without retaining an Activity or password. */
class AuthViewModel(application: Application) : AndroidViewModel(application) {
    private val repository = AuthRepository.get(application)
    private val executor = Executors.newSingleThreadExecutor()
    private val main = Handler(Looper.getMainLooper())
    private val mutable = MutableLiveData(AuthState())
    val state: LiveData<AuthState> = mutable
    @Volatile private var cleared = false
    private var profileStarted = false

    fun login(email: String, password: String) = submit { repository.login(email, password) }
    fun register(name: String, email: String, password: String, university: String, accepted: Boolean) =
        submit { repository.register(name, email, password, university, accepted) }

    fun loadProfile(retry: Boolean = false) {
        if (profileStarted && !retry) return
        profileStarted = true
        submit { repository.profile() }
    }

    fun consumeResult() { mutable.value = AuthState() }

    private fun submit(work: () -> AccountUser) {
        if (mutable.value?.loading == true) return
        mutable.value = AuthState(loading = true)
        executor.execute {
            val result = try { AuthState(user = work()) }
            catch (error: AuthFailure) { AuthState(error = error.message, expired = error.expired) }
            catch (_: Exception) { AuthState(error = "Could not complete sign-in securely. Please try again.") }
            main.post { if (!cleared) mutable.value = result }
        }
    }

    fun logout() {
        if (mutable.value?.loading == true) return
        mutable.value = AuthState(loading = true)
        executor.execute {
            var warning: String? = null
            try { repository.logout() } catch (_: Exception) {
                warning = "Signed out on this device. The server could not be reached to revoke the session."
            }
            main.post { if (!cleared) mutable.value = AuthState(loggedOut = true, error = warning) }
        }
    }

    override fun onCleared() {
        cleared = true
        executor.shutdownNow()
        super.onCleared()
    }
}
