package com.example.helmetdetectionv2.network

import android.content.Context
import android.util.Log
import com.example.helmetdetectionv2.utils.NotificationUtils
import kotlinx.coroutines.CoroutineScope
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.Job
import kotlinx.coroutines.delay
import kotlinx.coroutines.launch
import okhttp3.OkHttpClient
import okhttp3.Request
import okhttp3.Response
import okhttp3.WebSocket
import okhttp3.WebSocketListener
import org.json.JSONObject

object WebSocketManager : WebSocketListener() {

    private const val TAG = "WebSocketManager"
    private const val WS_URL = "ws://192.168.0.100:8080"
    private val client = OkHttpClient()
    private var webSocket: WebSocket? = null
    private var appContext: Context? = null

    private var reconnectJob: Job? = null

    private var eventListener: WebSocketEventListener? = null

    fun setEventListener(listener: WebSocketEventListener?) {
        eventListener = listener
    }

    fun start(context: Context) {
        appContext = context.applicationContext
        connect()
    }

    private fun connect() {
        val request = Request.Builder().url(WS_URL).build()
        webSocket = client.newWebSocket(request, this)
        Log.d(TAG, "Connecting to $WS_URL")
    }

    /* ---------- WebSocketListener callbacks ---------- */

    override fun onOpen(ws: WebSocket, response: Response) {
        Log.d(TAG, "WebSocket opened")
    }

    override fun onMessage(ws: WebSocket, text: String) {
        Log.d(TAG, "Message: $text")
        try {
            val json = JSONObject(text)
            val title = json.optString("title")
            val body = json.optString("message")

            Log.d(TAG, "Show notification: $title - $body")
            NotificationUtils.show(appContext!!, title, body)
            // Trigger UI refresh
            eventListener?.onLogUpdateReceived()

        } catch (e: Exception) {
            Log.e(TAG, "Gagal parse pesan", e)
        }
    }


    override fun onClosing(ws: WebSocket, code: Int, reason: String) {
        ws.close(1000, null)
        Log.d(TAG, "Closing: $code / $reason")
    }

    override fun onFailure(ws: WebSocket, t: Throwable, r: Response?) {
        Log.e(TAG, "Failure: ${t.message}")
        scheduleReconnect()
    }

    override fun onClosed(ws: WebSocket, code: Int, reason: String) {
        Log.d(TAG, "Closed: $code / $reason")
        scheduleReconnect()
    }

    /* ---------- Helpers ---------- */

    private fun scheduleReconnect() {
        if (reconnectJob?.isActive == true) return

        reconnectJob = CoroutineScope(Dispatchers.IO).launch {
            delay(5_000)
            connect()
        }
    }

    private fun parseJson(json: String): Pair<String, String> {
        val obj = JSONObject(json)
        return obj.optString("title", "Notifikasi") to obj.optString("body", "")
    }
}