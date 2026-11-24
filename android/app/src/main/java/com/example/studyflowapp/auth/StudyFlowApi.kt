package com.example.studyflowapp.auth

import com.google.gson.JsonObject
import okhttp3.OkHttpClient
import retrofit2.Call
import retrofit2.Retrofit
import retrofit2.converter.gson.GsonConverterFactory
import retrofit2.http.Body
import retrofit2.http.GET
import retrofit2.http.Header
import retrofit2.http.Headers
import retrofit2.http.POST
import retrofit2.http.Path
import java.util.concurrent.TimeUnit

interface StudyFlowApi {

    @Headers("Accept: application/json")
    @GET("{path}")
    fun get(
        @Path(value = "path", encoded = true) path: String,
        @Header("Authorization") authorization: String?
    ): Call<JsonObject>

    @Headers("Accept: application/json")
    @POST("{path}")
    fun post(
        @Path(value = "path", encoded = true) path: String,
        @Header("Authorization") authorization: String?,
        @Body body: JsonObject
    ): Call<JsonObject>
}

object StudyFlowApiFactory {

    fun create(baseUrl: String): StudyFlowApi {
        val client = OkHttpClient.Builder()
            .connectTimeout(15, TimeUnit.SECONDS)
            .readTimeout(15, TimeUnit.SECONDS)
            .writeTimeout(15, TimeUnit.SECONDS)
            .followRedirects(false)
            .followSslRedirects(false)
            .build()

        return Retrofit.Builder()
            .baseUrl(baseUrl)
            .client(client)
            .addConverterFactory(GsonConverterFactory.create())
            .build()
            .create(StudyFlowApi::class.java)
    }
}
