"use client";
import { Wrench, ShoppingBag, MessageCircle, Search, MoreHorizontal } from "lucide-react";

const tools = [
  { name: "Daraz", icon: ShoppingBag, color: "text-orange-400" },
  { name: "WhatsApp", icon: MessageCircle, color: "text-green-400" },
  { name: "Web Search", icon: Search, color: "text-blue-400" },
  { name: "Other Tools", icon: MoreHorizontal, color: "text-purple-400" },
];

export default function LeftPanel() {
  return (
    <div className="hud-panel-left-wrapper mt-4">
      
      {/* Inner Container */}
      <div className="hud-panel-left-inner p-4 flex flex-col gap-3">
        
        {/* Header */}
        <div className="flex items-center gap-2 border-b border-cyan-500/30 pb-3 mb-1 shrink-0">
          <Wrench className="w-5 h-5 text-cyan-400 icon-glow" />
          <h2 className="text-sm font-bold tracking-widest text-white">TOOLS</h2>
        </div>

        {/* Tools List */}
        <div className="flex flex-col gap-3 overflow-y-auto custom-scrollbar pr-1 max-h-[60vh]">
          {tools.map((tool, idx) => (
            <div 
              key={idx} 
              // 🔥 Cards ki border par strong cyan glow add kiya hai
              className="flex items-center gap-3 p-2.5 rounded-full border border-cyan-400 bg-[#003A91]/80 
                         shadow-[0_0_15px_rgba(0,229,255,0.3),inset_0_0_10px_rgba(0,229,255,0.2)] 
                         hover:shadow-[0_0_25px_rgba(0,229,255,0.8),inset_0_0_15px_rgba(0,229,255,0.4)] 
                         hover:bg-[#0050C0] hover:border-cyan-200 transition-all duration-300 cursor-pointer group shrink-0"
            >
              <div className="p-1.5 rounded-full bg-cyan-950/50 group-hover:scale-110 transition shrink-0">
                <tool.icon className={`w-4 h-4 ${tool.color}`} />
              </div>
              <span className="text-xs font-semibold tracking-wide text-white transition">{tool.name}</span>
            </div>
          ))}
        </div>

      </div>
    </div>
  );
}