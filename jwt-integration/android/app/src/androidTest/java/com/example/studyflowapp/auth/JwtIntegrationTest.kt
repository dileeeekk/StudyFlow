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
