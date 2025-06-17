package com.example.helmetdetectionv2.adapters

import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.TextView
import androidx.core.content.ContextCompat
import androidx.recyclerview.widget.RecyclerView
import com.example.helmetdetectionv2.R
import com.example.helmetdetectionv2.models.LogModel

class LogAdapter(private val list: List<LogModel>) :
    RecyclerView.Adapter<LogAdapter.ViewHolder>() {

    class ViewHolder(itemView: View) : RecyclerView.ViewHolder(itemView) {
        val waktu: TextView = itemView.findViewById(R.id.txtWaktu)
        val helm: TextView = itemView.findViewById(R.id.txtHelm)
        val strap: TextView = itemView.findViewById(R.id.txtStrap)
    }

    override fun onCreateViewHolder(parent: ViewGroup, viewType: Int): ViewHolder {
        val view = LayoutInflater.from(parent.context)
            .inflate(R.layout.item_log, parent, false)
        return ViewHolder(view)
    }

    override fun onBindViewHolder(holder: ViewHolder, position: Int) {
        val data = list[position]
        holder.waktu.text = data.waktu
        holder.helm.text = if (data.status_helm == 1) "TRUE" else "FALSE"
        holder.strap.text = if (data.status_strap == 1) "TRUE" else "FALSE"

        val context = holder.itemView.context
        holder.helm.background = ContextCompat.getDrawable(
            context,
            if (data.status_helm == 1) R.drawable.bg_true else R.drawable.bg_false
        )
        holder.strap.background = ContextCompat.getDrawable(
            context,
            if (data.status_strap == 1) R.drawable.bg_true else R.drawable.bg_false
        )
    }

    override fun getItemCount() = list.size
}