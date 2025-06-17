package com.example.helmetdetectionv2.models

import com.google.gson.annotations.SerializedName

data class LogResponse(
    @SerializedName("log_history") val log: List<LogModel>,
    @SerializedName("total_helm_false") val totalHelm: Int,
    @SerializedName("total_strap_false") val totalStrap: Int
)