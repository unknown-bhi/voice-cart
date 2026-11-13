"use client";
import { Mic, MicOff, Loader2 } from "lucide-react";
import { useVoiceAssistant, BarVisualizer, useLocalParticipant } from "@livekit/components-react";

interface CenterDisplayProps {
  onStart: () => void;
  isConnected: boolean;
  isConnecting: boolean;
}

export default function CenterDisplay({ onStart, isConnected, isConnecting }: CenterDisplayProps) {
  return (
    <div className="flex flex-col items-center justify-center w-full h-full relative z-10 pt-4">
      
      {/* 🟢 AVATAR SECTION */}
      {isConnected ? (
        <ConnectedAvatar />
      ) : (
        <div className="relative w-[280px] h-[280px] md:w-[360px] md:h-[360px] flex items-center justify-center mb-6 shrink-0 animate-float opacity-50 grayscale">
          <AvatarSVG state="idle" />
        </div>
      )}

      {/* 🔥 CONDITIONAL RENDERING: Mic Section */}
      {isConnected ? (
        <ConnectedMicSection />
      ) : (
        <DisconnectedMicSection onStart={onStart} isConnecting={isConnecting} />
      )}
    </div>
  );
}

// ==========================================
// 🟢 1. CUSTOM SVG AVATAR COMPONENT
// ==========================================
function AvatarSVG({ state }: { state: string }) {
  const isTalking = state === "speaking";
  const isThinking = state === "thinking";

  return (
    <div className="relative w-[280px] h-[280px] md:w-[360px] md:h-[360px] flex items-center justify-center">
      
      {/* Glowing Rings */}
      <div className={`absolute inset-0 rounded-full border border-[#00E5FF] transition-all duration-300 ${isTalking ? 'shadow-[0_0_80px_rgba(0,229,255,0.8)] animate-pulse-ring' : 'shadow-[0_0_50px_rgba(0,229,255,0.3)]'}`} />
      <div className="absolute inset-[-12px] rounded-full border border-dashed border-cyan-500/30 animate-[spin_10s_linear_infinite]" />
      <div className="absolute inset-[-24px] rounded-full border border-cyan-300/10 animate-[spin_15s_linear_infinite_reverse]" />

      {/* Main SVG Face Container */}
      <div className={`relative w-[230px] h-[230px] md:w-[300px] md:h-[300px] rounded-full overflow-hidden border-[3px] border-cyan-400 shadow-[0_0_30px_rgba(0,229,255,0.6)] z-10 bg-[#001a4d] flex items-center justify-center ${isThinking ? 'animate-pulse' : 'animate-float'}`}>
        
        <svg viewBox="0 0 200 200" className="w-[180px] h-[180px] drop-shadow-[0_0_15px_#00E5FF]">
          {/* Head Outline */}
          <path d="M100 10 C140 10 170 40 170 90 C170 140 140 180 100 180 C60 180 30 140 30 90 C30 40 60 10 100 10 Z" fill="none" stroke="#00E5FF" strokeWidth="2" />
          
          {/* Internal Circuitry Details */}
          <path d="M50 70 L70 70 M130 70 L150 70 M60 130 L80 130 M120 130 L140 130" stroke="#00E5FF" strokeWidth="1" opacity="0.5" />
          <circle cx="100" cy="160" r="3" fill="#00E5FF" />

          {/* Eyes */}
          <g className="animate-blink">
            {/* Left Eye */}
            <ellipse cx="70" cy="85" rx="12" ry="6" fill="#00E5FF" opacity="0.8" />
            <ellipse cx="70" cy="85" rx="4" ry="4" fill="#FFF" />
            {/* Right Eye */}
            <ellipse cx="130" cy="85" rx="12" ry="6" fill="#00E5FF" opacity="0.8" />
            <ellipse cx="130" cy="85" rx="4" ry="4" fill="#FFF" />
          </g>

          {/* Mouth */}
          <g className={isTalking ? "animate-talk" : ""}>
            {isTalking ? (
              // Open Mouth (Talking)
              <ellipse cx="100" cy="125" rx="15" ry="8" fill="#00E5FF" opacity="0.9" />
            ) : (
              // Closed Mouth (Idle)
              <path d="M85 125 Q100 135 115 125" fill="none" stroke="#00E5FF" strokeWidth="3" strokeLinecap="round" />
            )}
          </g>
        </svg>

        {/* Audio Reactivity Glow inside Avatar */}
        {isTalking && (
          <div className="absolute bottom-4 left-1/2 -translate-x-1/2 w-16 h-4 bg-cyan-400/50 blur-lg rounded-full animate-pulse" />
        )}
      </div>
    </div>
  );
}

// ==========================================
// 🟢 2. CONNECTED WRAPPER (Passes state to Avatar)
// ==========================================
function ConnectedAvatar() {
  const { state } = useVoiceAssistant();
  return <AvatarSVG state={state} />;
}

// ==========================================
// 🎤 3. CONNECTED MIC SECTION
// ==========================================
function ConnectedMicSection() {
  const { state, audioTrack } = useVoiceAssistant();
  const { localParticipant } = useLocalParticipant();

  const getStatusText = () => {
    if (state === "listening") return "LISTENING...";
    if (state === "thinking") return "PROCESSING...";
    if (state === "speaking") return "SPEAKING...";
    return "CONNECTED";
  };

  const getSubText = () => {
    if (state === "listening") return "Speak now";
    if (state === "thinking") return "Please wait...";
    if (state === "speaking") return "AI is responding";
    return "Ready";
  };

  const isMuted = !localParticipant?.isMicrophoneEnabled;

  return (
    <div className="relative w-full flex items-center justify-center gap-2 md:gap-6 mt-2 shrink-0">
      <div className="flex items-center justify-center gap-1 h-12 w-[80px] md:w-[120px]">
         {audioTrack && <BarVisualizer state={state} barCount={5} trackRef={audioTrack} className="h-full w-full" />}
      </div>

      <button 
        onClick={() => localParticipant?.setMicrophoneEnabled(isMuted)}
        className="hud-panel flex items-center gap-3 md:gap-4 px-4 md:px-6 py-2 w-[260px] md:w-[320px] shrink-0 justify-center border border-cyan-400 shadow-[0_0_30px_rgba(0,229,255,0.4)] bg-[#003A91] transition-all duration-300 hover:scale-105 hover:shadow-[0_0_40px_rgba(0,229,255,0.6)]"
      >
        <div className="w-8 h-8 md:w-10 md:h-10 shrink-0 rounded-full flex items-center justify-center shadow-[0_0_15px_#00E5FF] bg-cyan-500 text-[#003A91]">
          {isMuted ? <MicOff className="w-5 h-5" /> : <Mic className="w-5 h-5" />}
        </div>
        <div className="flex flex-col items-start">
          <span className="text-xs md:text-sm font-bold text-white tracking-widest uppercase">
            {isMuted ? "MUTED" : getStatusText()}
          </span>
          <span className="text-[10px] md:text-xs text-cyan-200 tracking-wider">
            {isMuted ? "Tap to unmute" : getSubText()}
          </span>
        </div>
      </button>

      <div className="flex items-center justify-center gap-1 h-12 w-[80px] md:w-[120px]">
         {audioTrack && <BarVisualizer state={state} barCount={5} trackRef={audioTrack} className="h-full w-full" />}
      </div>
    </div>
  );
}

// ==========================================
// 🎤 4. DISCONNECTED MIC SECTION
// ==========================================
function DisconnectedMicSection({ onStart, isConnecting }: { onStart: () => void, isConnecting: boolean }) {
  return (
    <div className="relative w-full flex items-center justify-center gap-2 md:gap-6 mt-2 shrink-0">
      <div className="w-[80px] md:w-[120px] h-12 flex items-center justify-center opacity-30">
        <div className="flex gap-1">---</div>
      </div>

      <button 
        onClick={onStart}
        disabled={isConnecting}
        className="hud-panel flex items-center gap-3 md:gap-4 px-4 md:px-6 py-2 w-[260px] md:w-[320px] shrink-0 justify-center border border-cyan-500/50 shadow-[0_0_20px_rgba(0,229,255,0.2)] bg-[#002A6B] transition-all duration-300 hover:scale-105 hover:shadow-[0_0_30px_rgba(0,229,255,0.5)] hover:border-cyan-400"
      >
        <div className="w-8 h-8 md:w-10 md:h-10 shrink-0 rounded-full flex items-center justify-center shadow-[0_0_15px_#00E5FF] bg-cyan-600 text-white">
          {isConnecting ? <Loader2 className="w-5 h-5 animate-spin" /> : <Mic className="w-5 h-5" />}
        </div>
        <div className="flex flex-col items-start">
          <span className="text-xs md:text-sm font-bold text-white tracking-widest uppercase">
            {isConnecting ? "CONNECTING..." : "CLICK TO START"}
          </span>
          <span className="text-[10px] md:text-xs text-cyan-200 tracking-wider">
            {isConnecting ? "Please wait" : "Tap mic to talk"}
          </span>
        </div>
      </button>

      <div className="w-[80px] md:w-[120px] h-12 flex items-center justify-center opacity-30">
        <div className="flex gap-1">---</div>
      </div>
    </div>
  );
}