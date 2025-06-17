package com.example.helmetdetectionv2

import android.os.Bundle
import android.util.Log
import androidx.fragment.app.Fragment
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.TextView
import android.widget.Toast
import androidx.annotation.OptIn
import androidx.media3.common.MediaItem
import androidx.media3.common.util.UnstableApi
import androidx.media3.exoplayer.ExoPlayer
import androidx.media3.exoplayer.rtsp.RtspMediaSource
import androidx.media3.ui.PlayerView
import androidx.recyclerview.widget.LinearLayoutManager
import androidx.recyclerview.widget.RecyclerView
import com.example.helmetdetectionv2.adapters.LogAdapter
import com.example.helmetdetectionv2.models.LogResponse
import com.example.helmetdetectionv2.network.RetrofitClient
import com.example.helmetdetectionv2.network.WebSocketEventListener
import com.example.helmetdetectionv2.network.WebSocketManager
import retrofit2.Call
import retrofit2.Callback
import retrofit2.Response

class HomeFragment : Fragment(), WebSocketEventListener {
    private lateinit var rvLog: RecyclerView
    private lateinit var txtNoHelm: TextView
    private lateinit var txtNoStrap: TextView
    private lateinit var playerView: PlayerView
    private var player: ExoPlayer? = null

    override fun onCreateView(
        inflater: LayoutInflater, container: ViewGroup?,
        savedInstanceState: Bundle?
    ): View? {
        return inflater.inflate(R.layout.fragment_home, container, false)
    }

    @OptIn(UnstableApi::class)
    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        super.onViewCreated(view, savedInstanceState)

        rvLog = view.findViewById(R.id.rvLog)
        txtNoHelm = view.findViewById(R.id.txtNoHelm)
        txtNoStrap = view.findViewById(R.id.txtNoStrap)
        playerView = view.findViewById(R.id.player_view)

        val rtspUrl = "rtsp://admin123:admin123@192.168.0.10/stream1"
        val mediaItem = MediaItem.fromUri(rtspUrl)
        val mediaSource = RtspMediaSource.Factory().createMediaSource(mediaItem)
        player = ExoPlayer.Builder(requireContext()).build()
        playerView.player = player
        player!!.volume = 0f
        player!!.setMediaSource(mediaSource)
        player!!.prepare()
        player!!.playWhenReady = true

        getLogData()
        WebSocketManager.setEventListener(this)
    }

    override fun onLogUpdateReceived() {
        activity?.runOnUiThread {
            getLogData() // Refresh log saat notifikasi masuk
        }
    }

    override fun onDestroyView() {
        super.onDestroyView()
        WebSocketManager.setEventListener(null)
    }

    private fun getLogData() {
        RetrofitClient.instance.getLog().enqueue(object : Callback<LogResponse> {
            override fun onResponse(call: Call<LogResponse>, response: Response<LogResponse>) {
                if (response.isSuccessful) {
                    val data = response.body()
                    rvLog.layoutManager = LinearLayoutManager(requireContext())
                    rvLog.adapter = LogAdapter(data!!.log)

                    txtNoHelm.text = data.totalHelm.toString()
                    txtNoStrap.text = data.totalStrap.toString()
                }
            }

            override fun onFailure(call: Call<LogResponse>, t: Throwable) {
                Log.e("API_ERROR", "Gagal ambil data: ${t.message}", t)
                Toast.makeText(requireContext(), "Gagal ambil data: ${t.message}", Toast.LENGTH_LONG).show()
            }
        })
    }
}