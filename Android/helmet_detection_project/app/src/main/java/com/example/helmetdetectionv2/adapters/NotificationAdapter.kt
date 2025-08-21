package com.example.helmetdetectionv2.adapters

import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.TextView
import androidx.recyclerview.widget.RecyclerView
import com.example.helmetdetectionv2.R
import com.example.helmetdetectionv2.models.LogModel

class NotificationAdapter(private val list: List<LogModel>) :
    RecyclerView.Adapter<NotificationAdapter.ViewHolder>() {

    class ViewHolder(view: View) : RecyclerView.ViewHolder(view) {
        val txtNotif: TextView = view.findViewById(R.id.txtNotif)
    }

    override fun onCreateViewHolder(parent: ViewGroup, viewType: Int): ViewHolder {
        val view = LayoutInflater.from(parent.context)
            .inflate(R.layout.item_notification, parent, false)
        return ViewHolder(view)
    }

    override fun onBindViewHolder(holder: ViewHolder, position: Int) {
        val data = list[position]
        holder.txtNotif.text = "${data.waktu} - Pengendara tidak menggunakan helm!"
    }

    override fun getItemCount(): Int = list.size
}