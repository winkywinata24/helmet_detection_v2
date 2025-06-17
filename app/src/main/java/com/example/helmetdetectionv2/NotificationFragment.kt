package com.example.helmetdetectionv2

import android.content.Context
import android.os.Bundle
import androidx.fragment.app.Fragment
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.Toast
import androidx.recyclerview.widget.LinearLayoutManager
import androidx.recyclerview.widget.RecyclerView
import com.example.helmetdetectionv2.adapters.NotificationAdapter
import com.example.helmetdetectionv2.models.LogResponse
import com.example.helmetdetectionv2.network.RetrofitClient
import com.example.helmetdetectionv2.utils.NotificationUtils
import retrofit2.Call
import retrofit2.Callback
import retrofit2.Response

class NotificationFragment : Fragment() {
    private lateinit var rvNotification: RecyclerView

    override fun onCreateView(
        inflater: LayoutInflater, container: ViewGroup?,
        savedInstanceState: Bundle?
    ): View? {
        val view = inflater.inflate(R.layout.fragment_notification, container, false)
        rvNotification = view.findViewById(R.id.rvNotification)
        rvNotification.layoutManager = LinearLayoutManager(requireContext())
        getNotifikasi()
        return view
    }

    private fun getNotifikasi() {
        RetrofitClient.instance.getLog().enqueue(object : Callback<LogResponse> {
            override fun onResponse(call: Call<LogResponse>, response: Response<LogResponse>) {
                if (response.isSuccessful) {
                    val allLog = response.body()?.log ?: emptyList()
                    val filtered = allLog.filter { it.status_helm == 0 }
                    rvNotification.adapter = NotificationAdapter(filtered)

                    val latest = filtered.maxByOrNull { it.id }
                    val storedLogId = getLastLogId()

                    if (latest != null && latest.id > storedLogId) {
                        NotificationUtils.showNotification(requireContext(), "Deteksi orang tanpa helm pada ${latest.waktu}")
                        saveLastLogId(latest.id)
                    }
                }
            }

            override fun onFailure(call: Call<LogResponse>, t: Throwable) {
                Toast.makeText(requireContext(), "Gagal ambil notifikasi", Toast.LENGTH_SHORT).show()
            }
        })
    }

    private fun getLastLogId(): Int {
        val prefs = requireContext().getSharedPreferences("helmet_prefs", Context.MODE_PRIVATE)
        return prefs.getInt("last_log_id", -1)
    }

    private fun saveLastLogId(id: Int) {
        val prefs = requireContext().getSharedPreferences("helmet_prefs", Context.MODE_PRIVATE)
        prefs.edit().putInt("last_log_id", id).apply()
    }
}