package com.example.helmetdetectionv2.network

import com.example.helmetdetectionv2.models.LogResponse
import retrofit2.Call
import retrofit2.http.GET

interface ApiService {
    @GET("get_log.php")
    fun getLog(): Call<LogResponse>
}