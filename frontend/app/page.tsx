"use client";

import { useState } from "react";
import {
  LiveKitRoom,
  RoomAudioRenderer,
  useVoiceAssistant,
  BarVisualizer,
  useTranscriptions,
} from "@livekit/components-react";
import "@livekit/components-styles";
import { createSession, endSession } from "@/lib/api";
import { Mic, PhoneOff, Sparkles, User, Bot, Loader2 } from "lucide-react";

export default function Home() {
  const [sessionData, setSessionData] = useState<{ token: string; roomName: string; sessionId: string } | null>(null);
  const [connecting, setConnecting] = useState(false);
  const [error, setError] = useState("");

  const startConversation = async () => {
    setConnecting(true);
    setError("");
    try {
      const userId = `user-${Math.floor(Math.random() * 1000)}`;
      const data = await createSession(userId);
      setSessionData({
        token: data.token,
        roomName: data.room_name,
        sessionId: data.session_id,
      });
    } catch (err: any) {
      setError(err.message);
    } finally {
      setConnecting(false);
    }
  };

  const handleDisconnect = async () => {
    if (sessionData?.sessionId) {
      await endSession(sessionData.sessionId);
    }
    setSessionData(null);
  };

  // ================= LANDING SCREEN =================
  if (!sessionData) {
    return (
      <main className="relative flex min-h-screen flex-col items-center justify-center bg-slate-950 text-white overflow-hidden">
        {/* Background Gradients */}
        <div className="absolute top-[-20%] left-[-10%] w-[500px] h-[500px] bg-blue-600/20 rounded-full blur-[120px]" />
        <div className="absolute bottom-[-20%] right-[-10%] w-[500px] h-[500px] bg-purple-600/20 rounded-full blur-[120px]" />

        <div className="relative z-10 flex flex-col items-center gap-6">
          <div className="p-4 bg-white/5 rounded-full border border-white/10 mb-4 animate-bounce shadow-[0_0_30px_rgba(59,130,246,0.3)]">
            <Sparkles className="w-12 h-12 text-blue-400" />
          </div>
          
          <h1 className="text-6xl md:text-7xl font-extrabold tracking-tight text-gradient">
            VoxLive
          </h1>
          <p className="text-lg md:text-xl text-slate-400 font-light max-w-md text-center">
            Sub-800ms Voice AI Agent with real-time e-commerce data integration.
          </p>

          {error && <p className="text-red-400 bg-red-900/20 px-4 py-2 rounded-lg border border-red-800">{error}</p>}

          <button
            onClick={startConversation}
            disabled={connecting}
            className="group relative mt-8 px-10 py-5 bg-blue-600 hover:bg-blue-500 rounded-full text-lg font-semibold transition-all duration-300 hover:scale-105 hover:shadow-[0_0_40px_rgba(59,130,246,0.6)] disabled:opacity-50 disabled:hover:scale-100 flex items-center gap-3"
          >
            {connecting ? (
              <Loader2 className="w-6 h-6 animate-spin" />
            ) : (
              <Mic className="w-6 h-6 group-hover:animate-pulse" />
            )}
            {connecting ? "Initializing..." : "Start Conversation"}
          </button>
        </div>
      </main>
    );
  }

  // ================= ACTIVE CALL SCREEN =================
  return (
    <main className="min-h-screen bg-slate-950 text-white p-4 md:p-8 flex justify-center items-center">
      <LiveKitRoom
        token={sessionData.token}
        serverUrl={process.env.NEXT_PUBLIC_LIVEKIT_URL}
        connect={true}
        audio={true}
        video={false}
        onDisconnected={handleDisconnect}
        className="w-full max-w-6xl h-[85vh] grid grid-cols-1 md:grid-cols-12 gap-6"
      >
        <RoomAudioRenderer />
        
        {/* Left Side: Orb & Visualizer (Glassmorphism) */}
        <div className="md:col-span-5 bg-white/5 border border-white/10 rounded-3xl p-8 flex flex-col items-center justify-center relative overflow-hidden backdrop-blur-xl">
          <div className="absolute top-0 left-0 w-full h-1 bg-gradient-to-r from-blue-500 via-purple-500 to-pink-500" />
          
          <h2 className="text-sm font-medium text-slate-400 uppercase tracking-widest mb-12">
            {sessionData.roomName}
          </h2>

          <div className="relative flex items-center justify-center w-48 h-48 rounded-full bg-slate-900 border border-slate-700 animate-glow">
            <AgentVisualizer />
          </div>

          <div className="mt-16 w-full flex justify-center">
            <button
              onClick={handleDisconnect}
              className="flex items-center gap-2 px-8 py-3 bg-red-500/10 hover:bg-red-500/20 text-red-400 border border-red-500/30 rounded-full font-medium transition-all duration-300 hover:scale-105"
            >
              <PhoneOff className="w-5 h-5" />
              End Call
            </button>
          </div>
        </div>

        {/* Right Side: Live Transcript (Glassmorphism) */}
        <div className="md:col-span-7 bg-white/5 border border-white/10 rounded-3xl p-6 flex flex-col relative overflow-hidden backdrop-blur-xl">
           <div className="flex items-center gap-2 mb-6 border-b border-white/10 pb-4">
             <div className="w-3 h-3 bg-green-500 rounded-full animate-pulse" />
             <h3 className="text-lg font-semibold text-slate-200">Live Transcript</h3>
           </div>
           <TranscriptPanel />
        </div>

      </LiveKitRoom>
    </main>
  );
}

// ================= COMPONENTS =================

function AgentVisualizer() {
  const { state, audioTrack } = useVoiceAssistant();
  
  const getStatusColor = () => {
    if (state === "listening") return "text-green-400";
    if (state === "thinking") return "text-yellow-400";
    return "text-blue-400";
  };

  return (
    <div className="flex flex-col items-center w-full z-10">
      <BarVisualizer
        state={state}
        barCount={7}
        trackRef={audioTrack}
        className="h-20 w-32"
      />
      <p className={`mt-6 text-sm font-bold tracking-widest uppercase ${getStatusColor()}`}>
        {state === "listening" ? "Listening" : state === "thinking" ? "Processing" : "Speaking"}
      </p>
    </div>
  );
}

function TranscriptPanel() {
  const transcriptions = useTranscriptions();

  return (
    <div className="flex-1 overflow-y-auto flex flex-col gap-4 pr-2 custom-scrollbar">
      {transcriptions.length === 0 ? (
        <div className="h-full flex flex-col items-center justify-center text-slate-500 gap-3">
          <Mic className="w-8 h-8 opacity-50" />
          <p className="text-sm">Speak to start the conversation...</p>
        </div>
      ) : (
        transcriptions.map((t, idx) => {
          const isUser = t.participantInfo?.identity === 'user';
          return (
            <div key={idx} className={`flex gap-3 max-w-[85%] ${isUser ? 'self-end flex-row-reverse' : 'self-start'}`}>
              
              {/* Avatar */}
              <div className={`w-8 h-8 rounded-full flex items-center justify-center shrink-0 ${isUser ? 'bg-blue-600' : 'bg-purple-600'}`}>
                {isUser ? <User className="w-4 h-4 text-white" /> : <Bot className="w-4 h-4 text-white" />}
              </div>

              {/* Message Bubble */}
              <div className={`p-3 rounded-2xl text-sm ${isUser ? 'bg-blue-600/20 border border-blue-500/30 rounded-tr-sm' : 'bg-slate-800/80 border border-slate-700 rounded-tl-sm'}`}>
                <p className="text-slate-200 leading-relaxed">{t.text}</p>
              </div>

            </div>
          );
        })
      )}
    </div>
  );
}