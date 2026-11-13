"use client";
import { FileText, MessageSquare, Bot, User } from "lucide-react";
import { useTranscriptions } from "@livekit/components-react";
import { useEffect, useRef } from "react";

interface RightPanelProps {
  isConnected: boolean;
}

export default function RightPanel({ isConnected }: RightPanelProps) {
  return (
    <div className="hud-panel-right-wrapper w-full mt-4">
      <div className="hud-panel-right-inner p-4 flex flex-col gap-4 h-[500px] max-h-[60vh]">
        
        {/* Header */}
        <div className="flex items-center justify-between border-b border-cyan-500/30 pb-3 mb-1 shrink-0">
          <div className="flex items-center gap-2">
            <FileText className="w-5 h-5 text-cyan-400 icon-glow" />
            <h2 className="text-sm font-bold tracking-widest text-white">TRANSCRIPT</h2>
          </div>
          
          {/* Live Indicator */}
          <div className={`flex items-center gap-1.5 px-2.5 py-1 rounded-full border shadow-[0_0_10px_rgba(34,197,94,0.3)] transition-colors ${isConnected ? 'bg-green-500/10 border-green-500/50' : 'bg-gray-500/10 border-gray-500/50'}`}>
            <div className={`w-1.5 h-1.5 rounded-full animate-pulse ${isConnected ? 'bg-green-400 shadow-[0_0_5px_#4ade80]' : 'bg-gray-400'}`} />
            <span className={`text-[10px] font-bold ${isConnected ? 'text-green-400' : 'text-gray-400'}`}>
              {isConnected ? "LIVE" : "OFFLINE"}
            </span>
          </div>
        </div>

        {/* Transcript List */}
        {isConnected ? (
          <ConnectedTranscripts />
        ) : (
          <div className="flex-1 flex flex-col items-center justify-center text-center opacity-50">
            <MessageSquare className="w-8 h-8 text-cyan-300 mb-2" />
            <p className="text-xs text-cyan-100">Connect to start conversation.<br/>Transcript will appear here.</p>
          </div>
        )}

      </div>
    </div>
  );
}

// 🔥 Live Transcript Component (Sirf connected state mein chalega)
function ConnectedTranscripts() {
  const transcriptions = useTranscriptions();
  const scrollRef = useRef<HTMLDivElement>(null);

  // Jab bhi naya text aaye, automatically neeche scroll ho jaye
  useEffect(() => {
    if (scrollRef.current) {
      scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
    }
  }, [transcriptions]);

  if (transcriptions.length === 0) {
    return (
      <div className="flex-1 flex flex-col items-center justify-center text-center opacity-50">
        <div className="w-6 h-6 border-2 border-cyan-400 border-t-transparent rounded-full animate-spin mb-3"></div>
        <p className="text-xs text-cyan-200">Listening... Start speaking.</p>
      </div>
    );
  }

  return (
    <div 
      ref={scrollRef}
      className="flex-1 overflow-y-auto custom-scrollbar pr-2 flex flex-col gap-4"
    >
      {transcriptions.map((t, idx) => {
        // Check karo message user ka hai ya AI ka
        const isUser = t.participantInfo?.identity === 'user' || t.participantInfo?.identity?.startsWith('user-');

        return (
          <div key={idx} className={`flex flex-col ${isUser ? 'items-end' : 'items-start'}`}>
            
            {/* Sender Name */}
            <div className="flex items-center gap-1 mb-1">
              {isUser ? <User className="w-3 h-3 text-cyan-400" /> : <Bot className="w-3 h-3 text-green-400" />}
              <span className="text-[10px] text-cyan-200 uppercase tracking-wider">
                {isUser ? "You" : "VoxLive"}
              </span>
            </div>

            {/* Message Bubble */}
            <div className={`p-3 rounded-xl max-w-[90%] text-xs leading-relaxed border ${
              isUser 
                ? 'bg-[#003A91] border-cyan-400/50 text-white rounded-tr-sm' 
                : 'bg-[#00E5FF]/10 border-[#00E5FF]/40 text-cyan-100 rounded-tl-sm shadow-[0_0_10px_rgba(0,229,255,0.1)]'
            }`}>
              {t.text}
            </div>
            
          </div>
        );
      })}
    </div>
  );
}