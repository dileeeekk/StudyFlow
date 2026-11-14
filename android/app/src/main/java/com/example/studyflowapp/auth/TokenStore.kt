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
