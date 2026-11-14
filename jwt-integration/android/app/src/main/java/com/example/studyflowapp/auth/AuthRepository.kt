package com.example.studyflowapp.auth

import android.content.Context
import com.example.studyflowapp.BuildConfig
import org.json.JSONArray
import org.json.JSONObject
import java.io.IOException
import java.io.InterruptedIOException
import java.net.HttpURLConnection
import java.net.URI
import java.util.Locale

data class AccountUser(val id: Long, val email: String, val fullName: String, val university: String) {
    companion object {
        fun from(json: JSONObject) = AccountUser(json.getLong("id"), json.getString("email"),
            json.getString("full_name"), json.getString("university"))
    }
}

class AuthFailure(message: String, val status: Int = 0, val expired: Boolean = false) : Exception(message)

class AuthRepository private constructor(context: Context) {
    private val store = TokenStore(context.applicationContext)

    // One lock serializes refresh rotation, logout and new login across all screens.
    @Synchronized fun hasSession(): Boolean = store.read() != null

    @Synchronized fun login(email: String, password: String): AccountUser = establish(
        request("auth/login/", JSONObject().put("email", email.trim().lowercase(Locale.ROOT)).put("password", password)))

    @Synchronized fun register(name: String, email: String, password: String, university: String, accepted: Boolean): AccountUser = establish(
        request("auth/register/", JSONObject().put("full_name", name.trim()).put("email", email.trim().lowercase(Locale.ROOT))
            .put("password", password).put("university", university.trim()).put("terms_accepted", accepted)))

    private fun establish(json: JSONObject): AccountUser {
        val user = AccountUser.from(json.getJSONObject("user"))
        val tokens = Tokens(json.getString("access"), json.getString("refresh"))
        require(tokens.access.isNotBlank() && tokens.refresh.isNotBlank())
        if (Thread.currentThread().isInterrupted) throw InterruptedIOException()
        store.save(tokens)
        return user
    }

    @Synchronized fun profile(): AccountUser {
        var tokens = store.read() ?: throw AuthFailure("Please log in to continue.", expired = true)
        val response = try {
            request("auth/me/", access = tokens.access)
        } catch (failure: AuthFailure) {
            if (failure.status != 401) throw failure
            tokens = refresh(tokens)
            try { request("auth/me/", access = tokens.access) } catch (retry: AuthFailure) {
                if (retry.status == 401) expire()
                throw retry
            }
        }
        return AccountUser.from(response)
    }

    private fun refresh(old: Tokens): Tokens {
        val response = try {
            request("auth/refresh/", JSONObject().put("refresh", old.refresh))
        } catch (failure: AuthFailure) {
            if (failure.status in listOf(400, 401, 403)) expire()
            throw failure // Offline/5xx must not destroy a valid saved session.
        }
        val tokens = Tokens(response.getString("access"), response.optString("refresh", old.refresh))
        require(tokens.access.isNotBlank() && tokens.refresh.isNotBlank())
        store.save(tokens) // Persist both rotated tokens together, before retrying the request.
        return tokens
    }

    @Synchronized fun logout() {
        val tokens = store.read()
        try {
            if (tokens != null) request("auth/logout/", JSONObject().put("refresh", tokens.refresh))
        } catch (failure: AuthFailure) {
            if (failure.status !in listOf(400, 401)) throw failure
        } finally {
            store.clear() // Local logout also works when the network is unavailable.
        }
    }

    private fun expire(): Nothing {
        store.clear()
        throw AuthFailure("Your session has expired. Please log in again.", expired = true)
    }

    private fun request(path: String, body: JSONObject? = null, access: String? = null): JSONObject {
        val base = try { URI(BuildConfig.API_BASE_URL) } catch (_: Exception) { throw AuthFailure("API address is not configured.") }
        val localDebug = BuildConfig.DEBUG && base.host in setOf("10.0.2.2", "127.0.0.1", "localhost")
        if ((base.scheme != "https" && !(localDebug && base.scheme == "http")) || base.host.isNullOrBlank() ||
            base.userInfo != null || base.query != null || base.fragment != null || !base.path.endsWith("/")) {
            throw AuthFailure("Configure a valid HTTPS API address for this build.")
        }
        val connection = base.resolve(path).toURL().openConnection() as HttpURLConnection
        try {
            connection.requestMethod = if (body == null) "GET" else "POST"
            connection.instanceFollowRedirects = false // Never forward credentials to another URL.
            connection.connectTimeout = 15000
            connection.readTimeout = 15000
            connection.useCaches = false
            connection.setRequestProperty("Accept", "application/json")
            if (access != null) connection.setRequestProperty("Authorization", "Bearer $access")
            if (body != null) {
                val bytes = body.toString().toByteArray(Charsets.UTF_8)
                connection.doOutput = true
                connection.setRequestProperty("Content-Type", "application/json; charset=utf-8")
                connection.setFixedLengthStreamingMode(bytes.size)
                connection.outputStream.use { it.write(bytes) }
            }
            val status = connection.responseCode
            val stream = if (status in 200..299) connection.inputStream else connection.errorStream
            val text = stream?.bufferedReader(Charsets.UTF_8)?.use { reader ->
                val result = StringBuilder(); val buffer = CharArray(4096)
                while (true) {
                    val count = reader.read(buffer); if (count < 0) break
                    result.append(buffer, 0, count)
                    if (result.length > 262144) throw AuthFailure("The server response is too large.")
                }
                result.toString()
            }.orEmpty()
            val json = try { JSONObject(text.ifBlank { "{}" }) } catch (_: Exception) { JSONObject() }
            if (status !in 200..299) {
                val message = when {
                    status == 429 -> "Too many attempts. Please wait a minute and try again."
                    status >= 500 -> "The server is temporarily unavailable. Please try again."
                    status in 300..399 -> "The API address returned a redirect. Check the server configuration."
                    else -> errorMessage(json).ifBlank { "The request failed. Please try again." }
                }
                throw AuthFailure(message, status)
            }
            return json
        } catch (error: IOException) {
            throw AuthFailure("Cannot reach the server. Check your connection and try again.")
        } catch (_: SecurityException) {
            throw AuthFailure("Network access is not allowed. Check the app permissions.")
        } finally { connection.disconnect() }
    }

    private fun errorMessage(json: JSONObject): String {
        val labels = mapOf("email" to "Email", "password" to "Password", "full_name" to "Full name",
            "university" to "University", "terms_accepted" to "Agreement", "detail" to "", "non_field_errors" to "")
        return labels.mapNotNull { (key, label) ->
            if (!json.has(key)) return@mapNotNull null
            val value = json.get(key)
            val text = if (value is JSONArray) (0 until value.length()).joinToString(" ") { value.optString(it) } else value.toString()
            if (label.isBlank()) text else "$label: $text"
        }.joinToString("\n").take(700)
    }

    companion object {
        @Volatile private var instance: AuthRepository? = null
        fun get(context: Context): AuthRepository = instance ?: synchronized(this) {
            instance ?: AuthRepository(context).also { instance = it }
        }
    }
}
