"use client";
import { Gauge, Disc, Image as ImageIcon, MessageSquare, BarChart2, FlaskConical, Calculator, Sun, Languages } from "lucide-react";

export default function BottomBar() {
  const icons = [Gauge, Disc, ImageIcon, MessageSquare, BarChart2, FlaskConical, Calculator, Sun, Languages];
  return (
    <div className="w-full max-w-[1200px] mx-auto px-18 pt-0 relative z-20">
      {/* 🔥 hud-panel-curved aur side padding */}
      <div className="hud-panel-curved w-[90%] max-w-7xl flex items-center justify-center gap-10 px-8 py-3">
        {icons.map((Icon, idx) => (
          <div key={idx} className="p-1.5 rounded-full hover:bg-cyan-900/50 cursor-pointer transition group">
             <Icon className="w-5 h-5 text-cyan-400 group-hover:text-cyan-100 icon-glow" />
          </div>
        ))}
      </div>
    </div>
  );
}