# StudyFlow — Django и JWT

Код уже добавлен в существующий Android-проект. Django-бэкенд создан в отдельной папке. Переносить код вручную на этом компьютере не требуется.

## 1. Что теперь работает

Login и Register отправляют данные в Django и переходят на Home только после успешного ответа. Django хранит аккаунты и хеши паролей в SQLite. Сервер выдаёт JWT access на 5 минут и refresh на 7 дней. Android использует access для защищённого профиля, а при ответе 401 один раз обновляет пару токенов и повторяет запрос. Если refresh недействителен, приложение очищает сессию и возвращает Login. При временной недоступности сервера сессия сохраняется и доступна кнопка Try again.

Токены зашифрованы AES-GCM; ключ находится в Android Keystore, файл не включается в резервное копирование. Пароль на устройстве не сохраняется. После перезапуска приложения действующая сессия восстанавливается через защищённый запрос к серверу. Имя приветствия берётся из аккаунта. Вкладка Profile временно открывает данные аккаунта и кнопку Log Out. Выход отзывает refresh и удаляет локальные токены.

XML-разметка существующих экранов, изображения и шрифты не изменялись. Даты, задачи, расписание и проценты на Home пока взяты из макета. Забытый пароль и подтверждение email ещё не подключены. Сервер локальный; публичное развёртывание не выполнялось.

## 2. Где находятся файлы

- Android: `C:\Users\admin\AndroidStudioProjects\StudyFlowApp`.
- Django: `C:\Users\admin\OneDrive\Documents\ChatGPT\Приложение StudyFlow\studyflow-backend`.
- Резервные копии изменённых Android-файлов: папка `backup` рядом с этой инструкцией.
- Архив `StudyFlow-JWT.zip`: папка `android` содержит только дополнения и изменения Android; папка `studyflow-backend` — исходный код сервера. База, секреты и виртуальное окружение в архив не включены.

## 3. Пошаговый запуск

1. Сервер оставлен работающим локально после проверки. Если компьютер перезапущен или сервер остановлен, открой **Terminal** в Android Studio и выполни:

```powershell
Set-Location -LiteralPath 'C:\Users\admin\OneDrive\Documents\ChatGPT\Приложение StudyFlow\studyflow-backend'
& '.\.venv\Scripts\python.exe' manage.py runserver 127.0.0.1:8000
```

2. Оставь терминал с сервером открытым. Если указано, что порт уже занят, проверь, не работает ли уже StudyFlow-сервер; второй экземпляр не нужен.
3. В Android Studio открой существующий **StudyFlowApp**, выбери **app**, свой эмулятор и нажми **Run ▶**.
4. Открой **Create an account**. Введи имя, email, университет и свой пароль. Нужны минимум 8 символов; Django также отклоняет очень простые, полностью цифровые и похожие на имя/email пароли. Установи согласие и нажми **Create Account**.
5. Если Android 17 запросит доступ к устройствам поблизости, разреши его для соединения с локальным тестовым сервером. В release-сборке это разрешение отсутствует.
6. Должен открыться Home с твоим именем. **Profile → Log Out** возвращает пустой Login. Теперь войди с теми же email и паролем. Неверный пароль должен показать ошибку.

Полная настройка нового компьютера, USB-телефона, адреса API, административного доступа и release-сборки находится в `studyflow-backend/README.md`.

## 4. Файлы и готовый код

Ниже приведены полные версии всех добавленных и изменённых файлов. При ручном переносе замени содержимое существующих файлов полностью. Для новых файлов создай указанные папки и файлы с точно такими именами. Kotlin-файлы создаются через **New → Kotlin Class/File → File**. XML — через **New → Android Resource File**, тип соответствует папке `res/xml` или `res/values`. Файлы Python и PowerShell — обычные текстовые файлы с расширениями `.py` и `.ps1`. Папка `src/debug` применяется только к debug-сборке, `src/androidTest` — к тестам на устройстве.


### `C:\Users\admin\AndroidStudioProjects\StudyFlowApp\app\build.gradle.kts`

Действие: Изменить существующий файл.

```kotlin
plugins {
    alias(libs.plugins.android.application)
}

android {
    namespace = "com.example.studyflowapp"
    compileSdk {
        version = release(37)
    }

    defaultConfig {
        applicationId = "com.example.studyflowapp"
        minSdk = 24
        targetSdk = 37
        versionCode = 1
        versionName = "1.0"

        testInstrumentationRunner = "androidx.test.runner.AndroidJUnitRunner"
    }

    buildFeatures { buildConfig = true }
    buildTypes {
        debug {
            val api = providers.gradleProperty("STUDYFLOW_API_URL").orElse("http://10.0.2.2:8000/api/").get()
            buildConfigField("String", "API_BASE_URL", "\"${api.replace("\\", "\\\\").replace("\"", "\\\"")}\"")
        }
        release {
            val api = providers.gradleProperty("STUDYFLOW_RELEASE_API_URL").orElse("").get()
            buildConfigField("String", "API_BASE_URL", "\"${api.replace("\\", "\\\\").replace("\"", "\\\"")}\"")
            optimization {
                enable = true
                packageScope = setOf("androidx.**", "kotlin.**", "kotlinx.**")
            }
        }
    }
    compileOptions {
        sourceCompatibility = JavaVersion.VERSION_11
        targetCompatibility = JavaVersion.VERSION_11
    }
}

dependencies {
    implementation("androidx.lifecycle:lifecycle-viewmodel:2.11.0")
    implementation("androidx.lifecycle:lifecycle-livedata-core:2.11.0")
    implementation(libs.androidx.activity.ktx)
    implementation(libs.androidx.appcompat)
    implementation(libs.androidx.constraintlayout)
    implementation(libs.androidx.core.ktx)
    implementation(libs.material)
    testImplementation(libs.junit)
    androidTestImplementation(libs.androidx.espresso.core)
    androidTestImplementation(libs.androidx.junit)
}
```

### `C:\Users\admin\AndroidStudioProjects\StudyFlowApp\app\src\androidTest\java\com\example\studyflowapp\auth\JwtIntegrationTest.kt`

Действие: Создать файл.

```kotlin
package com.example.studyflowapp.auth

import android.content.Context
import androidx.test.ext.junit.runners.AndroidJUnit4
import androidx.test.platform.app.InstrumentationRegistry
import org.junit.Assert.*
import org.junit.Test
import org.junit.runner.RunWith
import java.io.File
import java.util.concurrent.Callable
import java.util.concurrent.Executors

/** Runs against the local Django server. Never prints tokens or passwords. */
@RunWith(AndroidJUnit4::class)
class JwtIntegrationTest {
    @Test fun jwtRoundTripRefreshConcurrencyEncryptedStorageAndRevocation() {
        val context = InstrumentationRegistry.getInstrumentation().targetContext
        val repository = AuthRepository.get(context)
        val store = TokenStore(context)
        store.clear()
        assertFalse(repository.hasSession())
        val email = "jwt-test-${System.currentTimeMillis()}@example.com"
        val password = "StudyFlow!94Orbit"
        val user = repository.register("JWT Test", email, password, "Test University", true)
        assertEquals(email, user.email)
        assertEquals(user.id, repository.profile().id)
        val first = store.read()!!
        val encrypted = File(context.noBackupFilesDir, "auth-session.bin").readBytes().toString(Charsets.ISO_8859_1)
        assertFalse(encrypted.contains(first.access))
        assertFalse(encrypted.contains(first.refresh))
        assertFalse(encrypted.contains(password))

        // Invalid access triggers a real 401, then one refresh for all concurrent callers.
        store.save(Tokens("expired.access.token", first.refresh))
        val pool = Executors.newFixedThreadPool(4)
        try {
            val results = pool.invokeAll((1..4).map { Callable { repository.profile().id } })
            results.forEach { assertEquals(user.id, it.get()) }
        } finally { pool.shutdownNow() }
        val rotated = store.read()!!
        assertNotEquals(first.refresh, rotated.refresh)
        assertNotEquals("expired.access.token", rotated.access)

        // The rotated-away refresh cannot be reused and must clear the local session.
        store.save(Tokens("expired.access.token", first.refresh))
        try { repository.profile(); fail("Revoked refresh was accepted") }
        catch (error: AuthFailure) { assertTrue(error.expired) }
        assertFalse(repository.hasSession())

        repository.login(email.uppercase(), password)
        val beforeLogout = store.read()!!
        repository.logout()
        assertFalse(repository.hasSession())
        store.save(Tokens("expired.access.token", beforeLogout.refresh))
        try { repository.profile(); fail("Logout did not revoke refresh") }
        catch (error: AuthFailure) { assertTrue(error.expired) }

        try { repository.login(email, "WrongPassword!"); fail("Wrong password accepted") }
        catch (error: AuthFailure) { assertEquals(401, error.status) }
        assertFalse(repository.hasSession())

        repository.login(email, password)
        File(context.noBackupFilesDir, "auth-session.bin").writeText("corrupted-data")
        assertFalse(repository.hasSession())
        repository.login(email, password) // Recover with a fresh Keystore key.
        assertEquals(email, repository.profile().email)
        repository.logout()
    }
}
```

### `C:\Users\admin\AndroidStudioProjects\StudyFlowApp\app\src\debug\AndroidManifest.xml`

Действие: Создать файл.

```xml
<?xml version="1.0" encoding="utf-8"?>
<manifest xmlns:android="http://schemas.android.com/apk/res/android">
    <uses-permission android:name="android.permission.ACCESS_LOCAL_NETWORK" />
    <application android:networkSecurityConfig="@xml/debug_network_security" />
</manifest>
```

### `C:\Users\admin\AndroidStudioProjects\StudyFlowApp\app\src\debug\res\xml\debug_network_security.xml`

Действие: Создать файл.

```xml
<?xml version="1.0" encoding="utf-8"?>
<network-security-config>
    <base-config cleartextTrafficPermitted="false" />
    <domain-config cleartextTrafficPermitted="true">
        <domain includeSubdomains="false">10.0.2.2</domain>
        <domain includeSubdomains="false">127.0.0.1</domain>
        <domain includeSubdomains="false">localhost</domain>
    </domain-config>
</network-security-config>
```

### `C:\Users\admin\AndroidStudioProjects\StudyFlowApp\app\src\main\AndroidManifest.xml`

Действие: Изменить существующий файл.

```xml
<?xml version="1.0" encoding="utf-8"?>
<manifest xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:tools="http://schemas.android.com/tools">

    <uses-permission android:name="android.permission.INTERNET" />

    <application
        android:allowBackup="true"
        android:usesCleartextTraffic="false"
        android:dataExtractionRules="@xml/data_extraction_rules"
        android:fullBackupContent="@xml/backup_rules"
        android:icon="@mipmap/ic_launcher"
        android:label="@string/app_name"
        android:roundIcon="@mipmap/ic_launcher_round"
        android:supportsRtl="true"
        android:theme="@style/Theme.StudyFlowApp">
        <activity
            android:name=".MainActivity"
            android:theme="@style/Theme.StudyFlowApp.Splash"
            android:exported="true"
            android:windowSoftInputMode="adjustResize">
            <intent-filter>
                <action android:name="android.intent.action.MAIN" />

                <category android:name="android.intent.category.LAUNCHER" />
            </intent-filter>
        </activity>
        <activity
            android:name=".OnboardingActivity"
            android:exported="false"
            android:theme="@style/Theme.StudyFlowApp.Onboarding" />
        <activity
            android:name=".LoginActivity"
            android:exported="false"
            android:theme="@style/Theme.StudyFlowApp.Login"
            android:windowSoftInputMode="adjustResize|stateAlwaysHidden" />
        <activity
            android:name=".RegisterActivity"
            android:exported="false"
            android:theme="@style/Theme.StudyFlowApp.Register"
            android:windowSoftInputMode="adjustResize|stateAlwaysHidden" />
        <activity
            android:name=".HomeActivity"
            android:exported="false"
            android:theme="@style/Theme.StudyFlowApp.Home" />
    </application>

</manifest>
```

### `C:\Users\admin\AndroidStudioProjects\StudyFlowApp\app\src\main\java\com\example\studyflowapp\auth\AuthRepository.kt`

Действие: Создать файл.

```kotlin
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
```

### `C:\Users\admin\AndroidStudioProjects\StudyFlowApp\app\src\main\java\com\example\studyflowapp\auth\AuthViewModel.kt`

Действие: Создать файл.

```kotlin
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
```

### `C:\Users\admin\AndroidStudioProjects\StudyFlowApp\app\src\main\java\com\example\studyflowapp\auth\NetworkActivity.kt`

Действие: Создать файл.

```kotlin
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
```

### `C:\Users\admin\AndroidStudioProjects\StudyFlowApp\app\src\main\java\com\example\studyflowapp\auth\TokenStore.kt`

Действие: Создать файл.

```kotlin
package com.example.studyflowapp.auth

import android.content.Context
import android.security.keystore.KeyGenParameterSpec
import android.security.keystore.KeyProperties
import android.util.AtomicFile
import com.example.studyflowapp.BuildConfig
import org.json.JSONObject
import java.io.File
import java.io.FileNotFoundException
import java.security.KeyStore
import javax.crypto.Cipher
import javax.crypto.KeyGenerator
import javax.crypto.SecretKey
import javax.crypto.spec.GCMParameterSpec

// No generated toString(): tokens must never appear in logs.
internal class Tokens(val access: String, val refresh: String)

internal class TokenStore(context: Context) {
    private val file = AtomicFile(File(context.noBackupFilesDir, "auth-session.bin"))
    private val alias = "studyflow.auth.aes.v1"

    private fun key(): SecretKey {
        val store = KeyStore.getInstance("AndroidKeyStore").apply { load(null) }
        (store.getKey(alias, null) as? SecretKey)?.let { return it }
        return KeyGenerator.getInstance(KeyProperties.KEY_ALGORITHM_AES, "AndroidKeyStore").apply {
            init(KeyGenParameterSpec.Builder(alias, KeyProperties.PURPOSE_ENCRYPT or KeyProperties.PURPOSE_DECRYPT)
                .setBlockModes(KeyProperties.BLOCK_MODE_GCM)
                .setEncryptionPaddings(KeyProperties.ENCRYPTION_PADDING_NONE)
                .setKeySize(256).build())
        }.generateKey()
    }

    fun read(): Tokens? {
        val bytes = try { file.openRead().use { it.readBytes() } } catch (_: FileNotFoundException) { return null }
        return try {
            require(bytes.size in 30..65536 && bytes[0] == 1.toByte())
            val cipher = Cipher.getInstance("AES/GCM/NoPadding")
            cipher.init(Cipher.DECRYPT_MODE, key(), GCMParameterSpec(128, bytes.copyOfRange(1, 13)))
            val json = JSONObject(String(cipher.doFinal(bytes.copyOfRange(13, bytes.size)), Charsets.UTF_8))
            if (json.getString("server") != BuildConfig.API_BASE_URL) { clear(); return null }
            Tokens(json.getString("access"), json.getString("refresh")).also {
                require(it.access.isNotBlank() && it.refresh.isNotBlank())
            }
        } catch (_: Exception) {
            clear()
            // A lost/invalidated device key requires a fresh login, never plaintext fallback.
            KeyStore.getInstance("AndroidKeyStore").apply { load(null); deleteEntry(alias) }
            null
        }
    }

    fun save(tokens: Tokens) {
        val plain = JSONObject().put("server", BuildConfig.API_BASE_URL)
            .put("access", tokens.access).put("refresh", tokens.refresh).toString().toByteArray(Charsets.UTF_8)
        val cipher = Cipher.getInstance("AES/GCM/NoPadding")
        cipher.init(Cipher.ENCRYPT_MODE, key()) // Keystore generates a fresh random IV each time.
        val encrypted = byteArrayOf(1) + cipher.iv + cipher.doFinal(plain)
        val stream = file.startWrite()
        try {
            stream.write(encrypted)
            file.finishWrite(stream)
        } catch (error: Exception) {
            file.failWrite(stream)
            throw error
        }
    }

    fun clear() { file.delete() }
}
```

### `C:\Users\admin\AndroidStudioProjects\StudyFlowApp\app\src\main\java\com\example\studyflowapp\HomeActivity.kt`

Действие: Изменить существующий файл.

```kotlin
package com.example.studyflowapp

import android.content.Intent
import android.widget.TextView
import android.widget.Toast
import android.graphics.Color
import android.graphics.Rect
import android.os.Bundle
import android.view.TouchDelegate
import android.view.View
import android.view.ViewGroup
import androidx.activity.SystemBarStyle
import androidx.activity.enableEdgeToEdge
import androidx.lifecycle.ViewModelProvider
import com.example.studyflowapp.auth.AuthViewModel
import com.example.studyflowapp.auth.NetworkActivity
import com.google.android.material.dialog.MaterialAlertDialogBuilder
import androidx.core.view.ViewCompat
import androidx.core.view.WindowInsetsCompat
import androidx.core.view.updateLayoutParams
import androidx.core.view.updatePadding

/** Authenticated account; task and schedule cards still contain Figma preview data. */
class HomeActivity : NetworkActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        enableEdgeToEdge(
            statusBarStyle = SystemBarStyle.light(Color.TRANSPARENT, Color.TRANSPARENT),
            navigationBarStyle = SystemBarStyle.light(Color.TRANSPARENT, Color.rgb(23, 36, 67))
        )
        setContentView(R.layout.activity_home)
        val root = findViewById<View>(R.id.home_root)
        val auth = ViewModelProvider(this)[AuthViewModel::class.java]
        root.visibility = View.INVISIBLE
        fun returnToLogin() {
            startActivity(Intent(this, LoginActivity::class.java)
                .addFlags(Intent.FLAG_ACTIVITY_NEW_TASK or Intent.FLAG_ACTIVITY_CLEAR_TASK))
            finish()
        }
        auth.state.observe(this) { state ->
            if (state.expired || state.loggedOut) {
                state.error?.let { Toast.makeText(this, it, Toast.LENGTH_LONG).show() }
                returnToLogin()
            } else if (state.user != null) {
                root.visibility = View.VISIBLE
                val user = state.user
                val firstName = user.fullName.trim().split(Regex("\\s+"), limit = 2).first()
                findViewById<TextView>(R.id.home_greeting).text = getString(R.string.auth_greeting, firstName)
                findViewById<View>(R.id.home_tab_profile).setOnClickListener {
                    if (auth.state.value?.loading == true) return@setOnClickListener
                    MaterialAlertDialogBuilder(this).setTitle(R.string.auth_account)
                        .setMessage("${user.fullName}\n${user.email}\n${user.university}")
                        .setNegativeButton(R.string.auth_cancel, null)
                        .setPositiveButton(R.string.auth_logout) { _, _ -> auth.logout() }.show()
                }
            } else if (state.error != null) {
                MaterialAlertDialogBuilder(this).setTitle(R.string.auth_offline_title)
                    .setMessage(state.error).setCancelable(false)
                    .setPositiveButton(R.string.auth_retry) { _, _ -> withNetworkAccess { auth.loadProfile(retry = true) } }
                    .setNegativeButton(R.string.auth_logout) { _, _ -> auth.logout() }.show()
            }
        }
        withNetworkAccess { auth.loadProfile() }

        val scroll = findViewById<View>(R.id.home_scroll)
        val navigation = findViewById<View>(R.id.home_navigation)
        val add = findViewById<View>(R.id.home_add_container)
        ViewCompat.setOnApplyWindowInsetsListener(root) { _, insets ->
            val safe = insets.getInsets(WindowInsetsCompat.Type.systemBars() or WindowInsetsCompat.Type.displayCutout())
            scroll.updatePadding(left = safe.left, top = maxOf(safe.top, dp(44)) + dp(16), right = safe.right)
            navigation.updatePadding(left = safe.left, right = safe.right, bottom = maxOf(safe.bottom, dp(34)))
            add.updateLayoutParams<ViewGroup.MarginLayoutParams> { marginEnd = dp(24) + safe.right }
            insets
        }
        ViewCompat.requestApplyInsets(root)
        findViewById<View>(R.id.home_tab_home).isSelected = true
        // Enlarge small visual controls without changing the Figma layout.
        for (id in listOf(R.id.home_check_problem, R.id.home_check_diagram,
                R.id.home_notifications, R.id.home_see_all, R.id.home_class_count)) {
            val target = findViewById<View>(id)
            val parent = target.parent as View
            parent.post {
                val rect = Rect()
                target.getHitRect(rect)
                rect.inset(-maxOf(0, (dp(48) - rect.width()) / 2), -maxOf(0, (dp(48) - rect.height()) / 2))
                parent.touchDelegate = TouchDelegate(rect, target)
            }
        }
    }

    private fun dp(value: Int): Int = (value * resources.displayMetrics.density + 0.5f).toInt()
}
```

### `C:\Users\admin\AndroidStudioProjects\StudyFlowApp\app\src\main\java\com\example\studyflowapp\LoginActivity.kt`

Действие: Изменить существующий файл.

```kotlin
package com.example.studyflowapp

import android.content.Intent
import android.graphics.Color
import android.os.Bundle
import android.text.method.HideReturnsTransformationMethod
import android.text.method.PasswordTransformationMethod
import android.view.View
import android.view.ViewGroup
import androidx.core.widget.doAfterTextChanged
import android.view.inputmethod.EditorInfo
import android.widget.EditText
import android.widget.ImageButton
import androidx.activity.SystemBarStyle
import androidx.activity.enableEdgeToEdge
import androidx.lifecycle.ViewModelProvider
import com.example.studyflowapp.auth.AuthViewModel
import com.example.studyflowapp.auth.NetworkActivity
import com.google.android.material.button.MaterialButton
import com.google.android.material.dialog.MaterialAlertDialogBuilder
import androidx.core.view.ViewCompat
import androidx.core.view.WindowInsetsCompat
import androidx.core.view.WindowInsetsControllerCompat
import androidx.core.view.updatePadding
import androidx.core.widget.NestedScrollView

class LoginActivity : NetworkActivity() {
    private var openingHome = false
    private var authBusy = false
    private var openingRegistration = false
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        enableEdgeToEdge(
            statusBarStyle = SystemBarStyle.light(Color.TRANSPARENT, Color.TRANSPARENT),
            navigationBarStyle = SystemBarStyle.light(Color.TRANSPARENT, Color.rgb(23, 36, 67))
        )
        setContentView(R.layout.activity_login)
        val auth = ViewModelProvider(this)[AuthViewModel::class.java]
        val scroll = findViewById<NestedScrollView>(R.id.login_scroll)
        findViewById<View>(R.id.login_content).requestFocus()
        fun revealFocusedField() {
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
        var previousImeBottom = 0
        ViewCompat.setOnApplyWindowInsetsListener(scroll) { view, insets ->
            val bars = insets.getInsets(WindowInsetsCompat.Type.systemBars())
            val cutout = insets.getInsets(WindowInsetsCompat.Type.displayCutout())
            val ime = insets.getInsets(WindowInsetsCompat.Type.ime())
            view.updatePadding(
                left = maxOf(bars.left, cutout.left),
                top = maxOf(bars.top, cutout.top, dp(44)) + dp(42),
                right = maxOf(bars.right, cutout.right),
                bottom = maxOf(bars.bottom, cutout.bottom, ime.bottom, dp(34))
            )
            if (ime.bottom > previousImeBottom) {
                revealFocusedField()
            }
            previousImeBottom = ime.bottom
            insets
        }
        ViewCompat.requestApplyInsets(scroll)

        findViewById<View>(R.id.login_create_account).setOnClickListener {
            if (!openingRegistration) {
                openingRegistration = true
                startActivity(Intent(this, RegisterActivity::class.java))
            }
        }

        val password = findViewById<EditText>(R.id.login_password)
        val email = findViewById<EditText>(R.id.login_email)
        val passwordError = findViewById<View>(R.id.login_password_error)
        val submit = findViewById<View>(R.id.login_submit)
        val buttonContainer = findViewById<ViewGroup>(R.id.login_button_container)
        fun formIsValid(): Boolean = email.text.isNotBlank() && password.text.isNotBlank() &&
            Character.codePointCount(password.text, 0, password.text.length) >= 8
        fun updateFormState() {
            val length = Character.codePointCount(password.text, 0, password.text.length)
            passwordError.visibility = if (length in 1..7) View.VISIBLE else View.INVISIBLE
            val enabled = formIsValid() && !authBusy
            submit.isEnabled = enabled
            for (index in 0 until buttonContainer.childCount) {
                buttonContainer.getChildAt(index).alpha = if (enabled) 1f else 0.45f
            }
        }
        for (field in listOf(email, password)) {
            field.doAfterTextChanged { updateFormState() }
            field.setOnClickListener {
                field.requestFocus()
                WindowInsetsControllerCompat(window, field).show(WindowInsetsCompat.Type.ime())
            }
            field.setOnFocusChangeListener { _, focused ->
                if (focused && previousImeBottom > 0) revealFocusedField()
            }
        }
        updateFormState()
        val toggle = findViewById<ImageButton>(R.id.login_password_toggle)
        toggle.setOnClickListener {
            val start = password.selectionStart
            val end = password.selectionEnd
            val show = password.transformationMethod is PasswordTransformationMethod
            password.transformationMethod = if (show) HideReturnsTransformationMethod.getInstance()
                else PasswordTransformationMethod.getInstance()
            if (start >= 0 && end >= 0) password.setSelection(start, end)
            toggle.setImageResource(if (show) R.drawable.ic_login_eye else R.drawable.ic_login_eye_off)
            toggle.setContentDescription(getString(if (show) R.string.login_hide_password else R.string.login_show_password))
        }
        fun closeKeyboard() {
            WindowInsetsControllerCompat(window, scroll).hide(WindowInsetsCompat.Type.ime())
            findViewById<View>(R.id.login_content).requestFocus()
        }
        // Credentials are sent only to Django; Home opens only after a successful response.
        submit.setOnClickListener {
            if (formIsValid() && !authBusy && !openingHome) {
                withNetworkAccess {
                    closeKeyboard()
                    auth.login(email.text.toString(), password.text.toString())
                }
            }
        }
        auth.state.observe(this) { state ->
            authBusy = state.loading
            for (field in listOf(email, password)) field.isEnabled = !state.loading
            toggle.isEnabled = !state.loading
            findViewById<View>(R.id.login_create_account).isEnabled = !state.loading
            (submit as MaterialButton).setText(if (state.loading) R.string.auth_signing_in else R.string.login_submit)
            updateFormState()
            if (state.user != null && !openingHome) {
                openingHome = true
                password.text.clear()
                auth.consumeResult()
                startActivity(Intent(this, HomeActivity::class.java)
                    .addFlags(Intent.FLAG_ACTIVITY_NEW_TASK or Intent.FLAG_ACTIVITY_CLEAR_TASK))
                finish()
            } else if (state.error != null) {
                val message = state.error
                auth.consumeResult()
                MaterialAlertDialogBuilder(this).setTitle(R.string.auth_error_title)
                    .setMessage(message).setPositiveButton(android.R.string.ok, null).show()
            }
        }
        password.setOnEditorActionListener { _, actionId, _ ->
            if (actionId == EditorInfo.IME_ACTION_DONE) { closeKeyboard(); true } else false
        }
    }

    override fun onResume() {
        super.onResume()
        openingHome = false
        openingRegistration = false
    }

    private fun dp(value: Int): Int = (value * resources.displayMetrics.density + 0.5f).toInt()
}
```

### `C:\Users\admin\AndroidStudioProjects\StudyFlowApp\app\src\main\java\com\example\studyflowapp\MainActivity.kt`

Действие: Изменить существующий файл.

```kotlin
package com.example.studyflowapp

import com.example.studyflowapp.auth.AuthRepository
import android.content.Intent
import android.graphics.Color
import android.os.Build
import android.os.Bundle
import android.os.Handler
import android.os.Looper
import android.view.View
import androidx.activity.SystemBarStyle
import androidx.activity.enableEdgeToEdge
import androidx.appcompat.app.AppCompatActivity
import androidx.core.view.doOnPreDraw

class MainActivity : AppCompatActivity() {
    private val handler = Handler(Looper.getMainLooper())
    private var activityStarted = false
    private var contentDrawn = false
    private var systemSplashDismissed = Build.VERSION.SDK_INT < Build.VERSION_CODES.S

    private val openOnboarding = Runnable {
        if (activityStarted && contentDrawn && systemSplashDismissed) {
            val signedIn = runCatching { AuthRepository.get(this).hasSession() }.getOrDefault(false)
            val destination = if (signedIn) HomeActivity::class.java else OnboardingActivity::class.java
            startActivity(Intent(this, destination))
            finish()
        }
    }

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        enableEdgeToEdge(
            statusBarStyle = SystemBarStyle.dark(Color.TRANSPARENT),
            navigationBarStyle = SystemBarStyle.dark(Color.TRANSPARENT)
        )
        setContentView(R.layout.activity_main)
        val content = findViewById<View>(R.id.main)

        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.S) {
            splashScreen.setOnExitAnimationListener { systemSplash ->
                systemSplash.remove()
                content.postOnAnimation {
                    systemSplashDismissed = true
                    scheduleOnboardingIfVisible()
                }
            }
        }

        content.doOnPreDraw {
            content.postOnAnimation {
                contentDrawn = true
                scheduleOnboardingIfVisible()
            }
        }
    }

    override fun onStart() {
        super.onStart()
        activityStarted = true
        scheduleOnboardingIfVisible()
    }

    override fun onStop() {
        activityStarted = false
        handler.removeCallbacks(openOnboarding)
        super.onStop()
    }

    private fun scheduleOnboardingIfVisible() {
        handler.removeCallbacks(openOnboarding)
        if (activityStarted && contentDrawn && systemSplashDismissed) {
            // UI preview duration; real data loading has not been connected yet.
            handler.postDelayed(openOnboarding, 1_500L)
        }
    }
}
```

### `C:\Users\admin\AndroidStudioProjects\StudyFlowApp\app\src\main\java\com\example\studyflowapp\RegisterActivity.kt`

Действие: Изменить существующий файл.

```kotlin
package com.example.studyflowapp

import android.content.Intent
import android.graphics.Color
import android.graphics.Rect
import android.view.TouchDelegate
import android.os.Bundle
import android.text.method.HideReturnsTransformationMethod
import android.text.method.PasswordTransformationMethod
import android.view.View
import android.view.ViewGroup
import android.view.inputmethod.EditorInfo
import android.widget.CheckBox
import androidx.core.widget.doAfterTextChanged
import android.widget.EditText
import android.widget.ImageButton
import androidx.activity.SystemBarStyle
import androidx.activity.enableEdgeToEdge
import androidx.lifecycle.ViewModelProvider
import com.example.studyflowapp.auth.AuthViewModel
import com.example.studyflowapp.auth.NetworkActivity
import com.google.android.material.button.MaterialButton
import com.google.android.material.dialog.MaterialAlertDialogBuilder
import androidx.core.view.ViewCompat
import androidx.core.view.WindowInsetsCompat
import androidx.core.view.WindowInsetsControllerCompat
import androidx.core.view.updatePadding
import androidx.core.widget.NestedScrollView

class RegisterActivity : NetworkActivity() {
    private var openingHome = false
    private var authBusy = false
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        enableEdgeToEdge(
            statusBarStyle = SystemBarStyle.light(Color.TRANSPARENT, Color.TRANSPARENT),
            navigationBarStyle = SystemBarStyle.light(Color.TRANSPARENT, Color.rgb(23, 36, 67))
        )
        setContentView(R.layout.activity_register)
        val auth = ViewModelProvider(this)[AuthViewModel::class.java]
        val scroll = findViewById<NestedScrollView>(R.id.register_scroll)
        findViewById<View>(R.id.register_content).requestFocus()
        fun revealFocusedField() {
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
        var previousImeBottom = 0
        ViewCompat.setOnApplyWindowInsetsListener(scroll) { view, insets ->
            val bars = insets.getInsets(WindowInsetsCompat.Type.systemBars())
            val cutout = insets.getInsets(WindowInsetsCompat.Type.displayCutout())
            val ime = insets.getInsets(WindowInsetsCompat.Type.ime())
            view.updatePadding(
                left = maxOf(bars.left, cutout.left),
                top = maxOf(bars.top, cutout.top, dp(44)) + dp(16),
                right = maxOf(bars.right, cutout.right),
                bottom = maxOf(bars.bottom, cutout.bottom, ime.bottom, dp(34))
            )
            if (ime.bottom > previousImeBottom) {
                revealFocusedField()
            }
            previousImeBottom = ime.bottom
            insets
        }
        ViewCompat.requestApplyInsets(scroll)

        findViewById<View>(R.id.register_back).setOnClickListener { finish() }
        findViewById<View>(R.id.register_login).setOnClickListener { finish() }
        val memberRow = findViewById<View>(R.id.register_member_row)
        val loginLink = findViewById<View>(R.id.register_login)
        memberRow.post {
            val area = Rect()
            loginLink.getHitRect(area)
            area.inset(-dp(12), 0)
            memberRow.touchDelegate = TouchDelegate(area, loginLink)
        }
        val headerRow = findViewById<View>(R.id.register_header_row)
        val back = findViewById<View>(R.id.register_back)
        headerRow.post {
            val area = Rect()
            back.getHitRect(area)
            area.inset(-dp(2), -dp(2))
            headerRow.touchDelegate = TouchDelegate(area, back)
        }

        val name = findViewById<EditText>(R.id.register_name)
        val email = findViewById<EditText>(R.id.register_email)
        val password = findViewById<EditText>(R.id.register_password)
        val university = findViewById<EditText>(R.id.register_university)
        val fields = listOf(name, email, password, university)
        val passwordError = findViewById<View>(R.id.register_password_error)
        val agreement = findViewById<CheckBox>(R.id.register_agreement)
        val submit = findViewById<View>(R.id.register_submit)
        val buttonContainer = findViewById<ViewGroup>(R.id.register_button_container)
        fun formIsValid(): Boolean = agreement.isChecked && fields.all { it.text.isNotBlank() } &&
            Character.codePointCount(password.text, 0, password.text.length) >= 8
        fun updateFormState() {
            val length = Character.codePointCount(password.text, 0, password.text.length)
            passwordError.visibility = if (length in 1..7) View.VISIBLE else View.INVISIBLE
            val enabled = formIsValid() && !authBusy
            submit.isEnabled = enabled
            for (index in 0 until buttonContainer.childCount) {
                buttonContainer.getChildAt(index).alpha = if (enabled) 1f else 0.45f
            }
        }
        agreement.setOnCheckedChangeListener { _, _ -> updateFormState() }
        for (field in fields) {
            field.doAfterTextChanged { updateFormState() }
            field.setOnClickListener {
                field.requestFocus()
                WindowInsetsControllerCompat(window, field).show(WindowInsetsCompat.Type.ime())
            }
            field.setOnFocusChangeListener { _, focused ->
                if (focused && previousImeBottom > 0) revealFocusedField()
            }
        }
        updateFormState()
        val toggle = findViewById<ImageButton>(R.id.register_password_toggle)
        toggle.setOnClickListener {
            val start = password.selectionStart
            val end = password.selectionEnd
            val show = password.transformationMethod is PasswordTransformationMethod
            password.transformationMethod = if (show) HideReturnsTransformationMethod.getInstance()
                else PasswordTransformationMethod.getInstance()
            if (start >= 0 && end >= 0) password.setSelection(start, end)
            toggle.setImageResource(if (show) R.drawable.ic_login_eye else R.drawable.ic_login_eye_off)
            toggle.setContentDescription(getString(if (show) R.string.login_hide_password else R.string.login_show_password))
        }
        fun closeKeyboard() {
            WindowInsetsControllerCompat(window, scroll).hide(WindowInsetsCompat.Type.ime())
            findViewById<View>(R.id.register_content).requestFocus()
        }
        // Credentials are sent only to Django; Home opens only after a successful response.
        submit.setOnClickListener {
            if (formIsValid() && !authBusy && !openingHome) {
                withNetworkAccess {
                    closeKeyboard()
                    auth.register(name.text.toString(), email.text.toString(), password.text.toString(), university.text.toString(), agreement.isChecked)
                }
            }
        }
        auth.state.observe(this) { state ->
            authBusy = state.loading
            for (field in fields) field.isEnabled = !state.loading
            toggle.isEnabled = !state.loading
            agreement.isEnabled = !state.loading
            findViewById<View>(R.id.register_login).isEnabled = !state.loading
            (submit as MaterialButton).setText(if (state.loading) R.string.auth_registering else R.string.register_submit)
            updateFormState()
            if (state.user != null && !openingHome) {
                openingHome = true
                password.text.clear()
                auth.consumeResult()
                startActivity(Intent(this, HomeActivity::class.java)
                    .addFlags(Intent.FLAG_ACTIVITY_NEW_TASK or Intent.FLAG_ACTIVITY_CLEAR_TASK))
                finish()
            } else if (state.error != null) {
                val message = state.error
                auth.consumeResult()
                MaterialAlertDialogBuilder(this).setTitle(R.string.auth_error_title)
                    .setMessage(message).setPositiveButton(android.R.string.ok, null).show()
            }
        }
        university.setOnEditorActionListener { _, actionId, _ ->
            if (actionId == EditorInfo.IME_ACTION_DONE) { closeKeyboard(); true } else false
        }
    }

    override fun onResume() {
        super.onResume()
        openingHome = false
    }

    private fun dp(value: Int): Int = (value * resources.displayMetrics.density + 0.5f).toInt()
}
```

### `C:\Users\admin\AndroidStudioProjects\StudyFlowApp\app\src\main\res\values\auth_strings.xml`

Действие: Создать файл.

```xml
<?xml version="1.0" encoding="utf-8"?>
<resources>
    <string name="auth_signing_in">Logging in…</string>
    <string name="auth_registering">Creating account…</string>
    <string name="auth_error_title">Unable to continue</string>
    <string name="auth_retry">Try again</string>
    <string name="auth_logout">Log Out</string>
    <string name="auth_account">Your account</string>
    <string name="auth_greeting">Hi, %1$s ✦</string>
    <string name="auth_local_permission">Allow Nearby devices access in the app settings to connect to the local development server, then try again.</string>
    <string name="auth_offline_title">Cannot load your account</string>
    <string name="auth_cancel">Cancel</string>
    <string name="auth_open_settings">Open settings</string>
</resources>
```

### `C:\Users\admin\OneDrive\Documents\ChatGPT\Приложение StudyFlow\studyflow-backend\.gitignore`

Действие: создать файл.

```text
.venv/
__pycache__/
*.py[cod]
db.sqlite3*
.local-settings.json
*.log
.env
```

### `C:\Users\admin\OneDrive\Documents\ChatGPT\Приложение StudyFlow\studyflow-backend\accounts\__init__.py`

Действие: создать файл.

```python

```

### `C:\Users\admin\OneDrive\Documents\ChatGPT\Приложение StudyFlow\studyflow-backend\accounts\admin.py`

Действие: создать файл.

```python
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


@admin.register(User)
class AccountAdmin(UserAdmin):
    ordering = ('email',)
    list_display = ('email', 'full_name', 'university', 'is_active', 'is_staff')
    search_fields = ('email', 'full_name', 'university')
    readonly_fields = ('terms_accepted_at', 'last_login', 'date_joined')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Profile', {'fields': ('full_name', 'university', 'terms_accepted_at')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = ((None, {'classes': ('wide',), 'fields': ('email', 'full_name', 'university', 'password1', 'password2')}),)
```

### `C:\Users\admin\OneDrive\Documents\ChatGPT\Приложение StudyFlow\studyflow-backend\accounts\migrations\0001_initial.py`

Действие: создать файл.

```python
# Generated by Django 5.2.19 on 2026-11-06 19:04

import accounts.models
import django.db.models.functions.text
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('full_name', models.CharField(max_length=150)),
                ('university', models.CharField(max_length=200)),
                ('terms_accepted_at', models.DateTimeField(blank=True, null=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'constraints': [models.UniqueConstraint(django.db.models.functions.text.Lower('email'), name='user_email_case_insensitive_unique')],
            },
            managers=[
                ('objects', accounts.models.UserManager()),
            ],
        ),
    ]
```

### `C:\Users\admin\OneDrive\Documents\ChatGPT\Приложение StudyFlow\studyflow-backend\accounts\migrations\__init__.py`

Действие: создать файл.

```python

```

### `C:\Users\admin\OneDrive\Documents\ChatGPT\Приложение StudyFlow\studyflow-backend\accounts\models.py`

Действие: создать файл.

```python
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.db.models.functions import Lower


class UserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Email is required.')
        user = self.model(email=email.strip().lower(), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        if not extra_fields['is_staff'] or not extra_fields['is_superuser']:
            raise ValueError('Superuser must have is_staff=True and is_superuser=True.')
        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=150)
    university = models.CharField(max_length=200)
    terms_accepted_at = models.DateTimeField(null=True, blank=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name', 'university']
    objects = UserManager()

    class Meta:
        constraints = [models.UniqueConstraint(Lower('email'), name='user_email_case_insensitive_unique')]
```

### `C:\Users\admin\OneDrive\Documents\ChatGPT\Приложение StudyFlow\studyflow-backend\accounts\serializers.py`

Действие: создать файл.

```python
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError as DjangoValidationError
from django.db import IntegrityError, transaction
from django.utils import timezone
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'full_name', 'university')


class RegisterSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=254)
    full_name = serializers.CharField(max_length=150)
    university = serializers.CharField(max_length=200)
    password = serializers.CharField(write_only=True, trim_whitespace=False, min_length=8, max_length=128)
    terms_accepted = serializers.BooleanField()

    def validate_email(self, value):
        value = value.strip().lower()
        if User.objects.filter(email__iexact=value).exists():
            raise serializers.ValidationError('An account with this email already exists.')
        return value

    def validate_terms_accepted(self, value):
        if not value:
            raise serializers.ValidationError('Please accept the Terms of Service and Privacy Policy.')
        return value

    def validate(self, attrs):
        password = attrs['password']
        if not password.strip():
            raise serializers.ValidationError({'password': ['Enter a password with at least 8 characters.']})
        user = User(email=attrs['email'], full_name=attrs['full_name'], university=attrs['university'])
        try:
            validate_password(password, user)
        except DjangoValidationError as exc:
            raise serializers.ValidationError({'password': exc.messages}) from exc
        return attrs

    def create(self, validated_data):
        validated_data.pop('terms_accepted')
        try:
            with transaction.atomic():
                return User.objects.create_user(**validated_data, terms_accepted_at=timezone.now())
        except IntegrityError as exc:
            raise serializers.ValidationError({'email': ['An account with this email already exists.']}) from exc


class LoginSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        attrs['email'] = attrs['email'].strip().lower()
        data = super().validate(attrs)
        data['user'] = UserSerializer(self.user).data
        return data
```

### `C:\Users\admin\OneDrive\Documents\ChatGPT\Приложение StudyFlow\studyflow-backend\accounts\tests.py`

Действие: создать файл.

```python
from datetime import timedelta
from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.utils import timezone
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import AccessToken


class AuthenticationTests(APITestCase):
    def setUp(self):
        cache.clear()
        self.data = {'email': 'student@example.com', 'full_name': 'Test Student',
                     'university': 'Test University', 'password': 'StudyFlow!94Orbit', 'terms_accepted': True}

    def register(self):
        response = self.client.post('/api/auth/register/', self.data, format='json')
        self.assertEqual(response.status_code, 201, response.data)
        return response.data

    def test_register_hashes_password_returns_profile_and_protects_me(self):
        data = self.register()
        user = get_user_model().objects.get(email=self.data['email'])
        self.assertTrue(user.check_password(self.data['password']))
        self.assertNotEqual(user.password, self.data['password'])
        self.assertIsNotNone(user.terms_accepted_at)
        self.assertNotIn('password', data['user'])
        self.assertEqual(self.client.get('/api/auth/me/').status_code, 401)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + data['access'])
        self.assertEqual(self.client.get('/api/auth/me/').data['email'], self.data['email'])
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + data['refresh'])
        self.assertEqual(self.client.get('/api/auth/me/').status_code, 401)

    def test_login_case_insensitive_and_invalid_credentials(self):
        self.register()
        response = self.client.post('/api/auth/login/', {'email': 'STUDENT@EXAMPLE.COM', 'password': self.data['password']}, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertIn('refresh', response.data)
        self.assertEqual(self.client.post('/api/auth/login/', {'email': self.data['email'], 'password': 'WrongPassword!'}, format='json').status_code, 401)

    def test_required_fields_consent_password_and_duplicate(self):
        for field in ['email', 'full_name', 'university', 'password', 'terms_accepted']:
            cache.clear()
            bad = self.data.copy(); bad.pop(field)
            self.assertEqual(self.client.post('/api/auth/register/', bad, format='json').status_code, 400)
        for field, value in [('terms_accepted', False), ('password', 'short'), ('password', '        '), ('full_name', '  '), ('university', '  '), ('email', 'not-email')]:
            cache.clear()
            bad = {**self.data, field: value}
            self.assertEqual(self.client.post('/api/auth/register/', bad, format='json').status_code, 400)
        cache.clear(); self.register()
        self.assertEqual(self.client.post('/api/auth/register/', {**self.data, 'email': 'STUDENT@EXAMPLE.COM'}, format='json').status_code, 400)

    def test_refresh_rotates_and_old_refresh_is_rejected(self):
        data = self.register()
        result = self.client.post('/api/auth/refresh/', {'refresh': data['refresh']}, format='json')
        self.assertEqual(result.status_code, 200)
        self.assertNotEqual(result.data['refresh'], data['refresh'])
        self.assertEqual(self.client.post('/api/auth/refresh/', {'refresh': data['refresh']}, format='json').status_code, 401)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + result.data['access'])
        self.assertEqual(self.client.get('/api/auth/me/').status_code, 200)

    def test_expired_or_modified_access_is_rejected(self):
        data = self.register()
        token = AccessToken(data['access']); token.set_exp(from_time=timezone.now() - timedelta(minutes=10), lifetime=timedelta(seconds=1))
        for access in [str(token), data['access'][:-10] + 'invalidXYZ']:
            self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + access)
            self.assertEqual(self.client.get('/api/auth/me/').status_code, 401)

    def test_logout_revokes_refresh(self):
        data = self.register()
        self.assertEqual(self.client.post('/api/auth/logout/', {'refresh': data['refresh']}, format='json').status_code, 200)
        self.assertEqual(self.client.post('/api/auth/refresh/', {'refresh': data['refresh']}, format='json').status_code, 401)

    def test_inactive_user_cannot_login_refresh_or_use_access(self):
        data = self.register()
        user = get_user_model().objects.get(email=self.data['email']); user.is_active = False; user.save()
        self.assertEqual(self.client.post('/api/auth/login/', {'email': self.data['email'], 'password': self.data['password']}, format='json').status_code, 401)
        self.assertEqual(self.client.post('/api/auth/refresh/', {'refresh': data['refresh']}, format='json').status_code, 401)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + data['access'])
        self.assertEqual(self.client.get('/api/auth/me/').status_code, 401)

    def test_login_throttling(self):
        for _ in range(10):
            self.client.post('/api/auth/login/', {'email': 'unknown@example.com', 'password': 'WrongPassword!'}, format='json')
        self.assertEqual(self.client.post('/api/auth/login/', {'email': 'unknown@example.com', 'password': 'WrongPassword!'}, format='json').status_code, 429)
```

### `C:\Users\admin\OneDrive\Documents\ChatGPT\Приложение StudyFlow\studyflow-backend\accounts\urls.py`

Действие: создать файл.

```python
from django.urls import path
from .views import LoginView, LogoutView, MeView, RefreshView, RegisterView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('refresh/', RefreshView.as_view(), name='refresh'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('me/', MeView.as_view(), name='me'),
]
```

### `C:\Users\admin\OneDrive\Documents\ChatGPT\Приложение StudyFlow\studyflow-backend\accounts\views.py`

Действие: создать файл.

```python
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenBlacklistView
from .serializers import LoginSerializer, RegisterSerializer, UserSerializer


class RegisterView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []
    throttle_scope = 'register'

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        return Response({'access': str(refresh.access_token), 'refresh': str(refresh),
                         'user': UserSerializer(user).data}, status=status.HTTP_201_CREATED)


class LoginView(TokenObtainPairView):
    serializer_class = LoginSerializer
    throttle_scope = 'login'


class RefreshView(TokenRefreshView):
    throttle_scope = 'refresh'


class LogoutView(TokenBlacklistView):
    throttle_scope = 'logout'


class MeView(APIView):
    throttle_scope = 'profile'

    def get(self, request):
        return Response(UserSerializer(request.user).data)
```

### `C:\Users\admin\OneDrive\Documents\ChatGPT\Приложение StudyFlow\studyflow-backend\bootstrap.py`

Действие: создать файл.

```python
"""Create private local development keys once. Never print them or ship them to Android."""
import json
import secrets
from pathlib import Path

path = Path(__file__).resolve().parent / '.local-settings.json'
if not path.exists():
    with path.open('x', encoding='utf-8') as stream:
        json.dump({'SECRET_KEY': secrets.token_urlsafe(64),
                   'JWT_SIGNING_KEY': secrets.token_urlsafe(64)}, stream)
    print('Local development keys created (excluded from Git).')
else:
    print('Existing local keys preserved.')
```

### `C:\Users\admin\OneDrive\Documents\ChatGPT\Приложение StudyFlow\studyflow-backend\config\__init__.py`

Действие: создать файл.

```python

```

### `C:\Users\admin\OneDrive\Documents\ChatGPT\Приложение StudyFlow\studyflow-backend\config\settings.py`

Действие: создать файл.

```python
import json
import os
from datetime import timedelta
from pathlib import Path
from django.core.exceptions import ImproperlyConfigured

BASE_DIR = Path(__file__).resolve().parent.parent
DEBUG = os.environ.get('DJANGO_DEBUG', '1') == '1'
local_file = BASE_DIR / '.local-settings.json'
local = json.loads(local_file.read_text(encoding='utf-8')) if DEBUG and local_file.exists() else {}
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY') or local.get('SECRET_KEY')
JWT_SIGNING_KEY = os.environ.get('JWT_SIGNING_KEY') or local.get('JWT_SIGNING_KEY')
if not SECRET_KEY or not JWT_SIGNING_KEY:
    raise ImproperlyConfigured('Run python bootstrap.py for local development; set DJANGO_SECRET_KEY and JWT_SIGNING_KEY for deployment.')
host_setting = os.environ.get('DJANGO_ALLOWED_HOSTS', 'localhost,127.0.0.1,10.0.2.2' if DEBUG else '')
ALLOWED_HOSTS = [host.strip() for host in host_setting.split(',') if host.strip()]
if not ALLOWED_HOSTS:
    raise ImproperlyConfigured('DJANGO_ALLOWED_HOSTS is required for deployment.')

INSTALLED_APPS = [
    'django.contrib.admin', 'django.contrib.auth', 'django.contrib.contenttypes',
    'django.contrib.sessions', 'django.contrib.messages', 'django.contrib.staticfiles',
    'rest_framework', 'rest_framework_simplejwt.token_blacklist', 'accounts',
]
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware', 'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware', 'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware', 'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
ROOT_URLCONF = 'config.urls'
TEMPLATES = [{'BACKEND': 'django.template.backends.django.DjangoTemplates', 'DIRS': [], 'APP_DIRS': True,
              'OPTIONS': {'context_processors': ['django.template.context_processors.request',
                                                'django.contrib.auth.context_processors.auth',
                                                'django.contrib.messages.context_processors.messages']}}]
WSGI_APPLICATION = 'config.wsgi.application'
DATABASES = {'default': {'ENGINE': 'django.db.backends.sqlite3', 'NAME': BASE_DIR / 'db.sqlite3'}}
AUTH_USER_MODEL = 'accounts.User'
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
     'OPTIONS': {'user_attributes': ['email', 'full_name']}},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator', 'OPTIONS': {'min_length': 8}},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Qyzylorda'
USE_I18N = True
USE_TZ = True
STATIC_URL = 'static/'
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
DATA_UPLOAD_MAX_MEMORY_SIZE = 32 * 1024

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': ['rest_framework_simplejwt.authentication.JWTAuthentication'],
    'DEFAULT_PERMISSION_CLASSES': ['rest_framework.permissions.IsAuthenticated'],
    'DEFAULT_RENDERER_CLASSES': ['rest_framework.renderers.JSONRenderer'],
    'DEFAULT_PARSER_CLASSES': ['rest_framework.parsers.JSONParser'],
    'DEFAULT_THROTTLE_CLASSES': ['rest_framework.throttling.ScopedRateThrottle'],
    'DEFAULT_THROTTLE_RATES': {'login': '10/min', 'register': '5/min', 'refresh': '30/min',
                             'logout': '30/min', 'profile': '60/min'},
}
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=5),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
    'SIGNING_KEY': JWT_SIGNING_KEY,
    'ALGORITHM': 'HS256',
    'AUTH_HEADER_TYPES': ('Bearer',),
    'ISSUER': 'studyflow',
    'AUDIENCE': 'studyflow-android',
}
SECURE_SSL_REDIRECT = not DEBUG
SESSION_COOKIE_SECURE = not DEBUG
CSRF_COOKIE_SECURE = not DEBUG
SECURE_HSTS_SECONDS = 31536000 if not DEBUG else 0
SECURE_HSTS_INCLUDE_SUBDOMAINS = not DEBUG
SECURE_HSTS_PRELOAD = not DEBUG
```

### `C:\Users\admin\OneDrive\Documents\ChatGPT\Приложение StudyFlow\studyflow-backend\config\urls.py`

Действие: создать файл.

```python
from django.contrib import admin
from django.urls import include, path

urlpatterns = [path('admin/', admin.site.urls), path('api/auth/', include('accounts.urls'))]
```

### `C:\Users\admin\OneDrive\Documents\ChatGPT\Приложение StudyFlow\studyflow-backend\config\wsgi.py`

Действие: создать файл.

```python
import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
application = get_wsgi_application()
```

### `C:\Users\admin\OneDrive\Documents\ChatGPT\Приложение StudyFlow\studyflow-backend\manage.py`

Действие: создать файл.

```python
#!/usr/bin/env python
import os
import sys

if __name__ == '__main__':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
    from django.core.management import execute_from_command_line
    execute_from_command_line(sys.argv)
```

### `C:\Users\admin\OneDrive\Documents\ChatGPT\Приложение StudyFlow\studyflow-backend\requirements.txt`

Действие: создать файл.

```text
asgiref==3.13.0
Django==5.2.19
djangorestframework==3.16.1
djangorestframework_simplejwt==5.5.1
PyJWT==2.15.1
sqlparse==0.6.1
tzdata==2026.6
```

### `C:\Users\admin\OneDrive\Documents\ChatGPT\Приложение StudyFlow\studyflow-backend\start-backend.ps1`

Действие: создать файл.

```powershell
$ErrorActionPreference = 'Stop'
Set-Location -LiteralPath $PSScriptRoot
$backendPython = Join-Path $PSScriptRoot '.venv\Scripts\python.exe'
if (-not (Test-Path -LiteralPath $backendPython)) {
    python -m venv .venv
    if ($LASTEXITCODE -ne 0) { throw 'Could not create Python environment.' }
    & $backendPython -m pip install -r requirements.txt
    if ($LASTEXITCODE -ne 0) { throw 'Could not install backend dependencies.' }
}
& $backendPython bootstrap.py
if ($LASTEXITCODE -ne 0) { throw 'Could not prepare local settings.' }
& $backendPython manage.py migrate
if ($LASTEXITCODE -ne 0) { throw 'Database migration failed.' }
& $backendPython manage.py runserver 127.0.0.1:8000
```

## 5. Результаты проверки

- Django: 8 тестов прошли — создание аккаунта, хеширование пароля, обязательные поля и согласие, повторный email, вход, защищённый профиль, просроченный/изменённый access, ротация и отзыв refresh, неактивный пользователь, лимит попыток.
- Android: assembleDebug, assembleDebugAndroidTest и lintDebug прошли; ошибок Lint нет. Манифест release проверен отдельно: локальное сетевое разрешение и HTTP-конфигурация debug туда не попадают.
- Интеграционный тест в эмуляторе: настоящий Django, шифрование файла токенов, четыре одновременных запроса после недействительного access, ротация refresh, отказ при повторном использовании старого refresh, отзыв при выходе, неверный пароль, восстановление после повреждённого хранилища.
- Интерфейс: регистрация, имя на Home, сохранение сессии после остановки процесса, Profile / Log Out, пустые поля после выхода, ошибка неверного пароля и успешный вход.
- Недоступность сервера: сервер временно остановлен; токены сохранились. После запуска сервера Try again восстановила Home. Сервер снова работает, тестовая сессия на устройстве завершена.
- Все существующие XML-разметки сохранены без изменений.

Скриншоты проверки находятся рядом с инструкцией: JWT-register-home.png, JWT-account-dialog.png, JWT-invalid-password.png, JWT-offline-retry.png.

Для повторной проверки backend: из папки сервера выполни `.\.venv\Scripts\python.exe manage.py test accounts`. Android-тест `JwtIntegrationTest` запускается из Android Studio при работающем локальном сервере и разрешённом доступе к локальной сети. Тест использует отдельный временный аккаунт `@example.com` и завершает сессию; запускай его на тестовом устройстве.

Ключевые особенности: после выхода уже выданный access остаётся действительным до истечения, максимум 5 минут; при выходе без сети Android удаляет локальные токены, но не может немедленно отозвать refresh на сервере. Публичный сервер и публикация приложения требуют отдельного этапа развёртывания, описанного в README.

Документация: [Simple JWT](https://django-rest-framework-simplejwt.readthedocs.io/en/stable/getting_started.html), [настройки JWT](https://django-rest-framework-simplejwt.readthedocs.io/en/stable/settings.html), [Android Keystore](https://developer.android.com/privacy-and-security/keystore).
