package com.example.helmetdetectionv2.network

import android.app.Service
import android.app.Notification
import android.app.NotificationChannel
import android.app.NotificationManager
import android.content.Intent
import android.os.Build
import android.os.IBinder
import androidx.core.app.NotificationCompat
import com.example.helmetdetectionv2.R

class WebSocketService : Service() {

    override fun onCreate() {
        super.onCreate()
        WebSocketManager.start(applicationContext)
        createNotificationChannel()
        startForeground(1, buildNotification())
    }

    override fun onStartCommand(intent: Intent?, flags: Int, startId: Int): Int {
        // Service tetap berjalan
        return START_STICKY
    }

    override fun onDestroy() {
        super.onDestroy()
        // Opsional: close WebSocket jika ingin
    }

    override fun onBind(intent: Intent?): IBinder? = null

    private fun createNotificationChannel() {
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
            val channel = NotificationChannel(
                "ws_service",
                "WebSocket Service",
                NotificationManager.IMPORTANCE_LOW
            )
            getSystemService(NotificationManager::class.java).createNotificationChannel(channel)
        }
    }

    private fun buildNotification(): Notification {
        return NotificationCompat.Builder(this, "ws_service")
            .setContentTitle("Helmet Detection Aktif")
            .setContentText("Monitoring pelanggaran berjalan...")
            .setSmallIcon(R.drawable.logo)
            .build()
    }
}