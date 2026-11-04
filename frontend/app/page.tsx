"use client";

import { useState } from "react";
import {
  LiveKitRoom,
  RoomAudioRenderer,
  useVoiceAssistant,
  BarVisualizer,
} from "@livekit/components-react";
import "@livekit/components-styles";
import { createSession, endSession } from "@/lib/api"; // 🔥 Yahan se import kiya

export default function Home() {
  const [sessionData, setSessionData] = useState<{ token: string; roomName: string; sessionId: string } | null>(null);
  const [connecting, setConnecting] = useState(false);
  const [error, setError] = useState("");

  const startConversation = async () => {
    setConnecting(true);
    setError("");
    try {
      const userId = `user-${Math.floor(Math.random() * 1000)}`;
      
      // 🔥 API call ab sirf ek line mein
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
      // Backend par session end karo (DB status update + Redis count decrement)
      await endSession(sessionData.sessionId);
    }
    setSessionData(null);
  };

  if (!sessionData) {
    return (
      <main className="flex min-h-screen flex-col items-center justify-center bg-gray-900 text-white p-4">
        <h1 className="text-4xl font-bold mb-4">VoxLive</h1>
        <p className="text-gray-400 mb-8">Real-Time Voice AI Agent</p>
        
        {error && <p className="text-red-500 mb-4">{error}</p>}

        <button
          onClick={startConversation}
          disabled={connecting}
          className="px-8 py-4 bg-blue-600 hover:bg-blue-700 disabled:bg-gray-600 rounded-full text-lg font-semibold transition-all"
        >
          {connecting ? "Connecting..." : "Start Conversation"}
        </button>
      </main>
    );
  }

  return (
    <main className="flex min-h-screen flex-col items-center justify-center bg-gray-900 text-white p-4">
      <LiveKitRoom
        token={sessionData.token}
        serverUrl={process.env.NEXT_PUBLIC_LIVEKIT_URL}
        connect={true}
        audio={true}
        video={false}
        onDisconnected={handleDisconnect}
        className="w-full max-w-md flex flex-col items-center gap-6"
      >
        <h2 className="text-2xl font-bold">Connected to: {sessionData.roomName}</h2>
        
        <RoomAudioRenderer />
        <AgentVisualizer />
        
        <button 
          onClick={handleDisconnect}
          className="px-6 py-2 bg-red-600 hover:bg-red-700 rounded-full text-sm font-semibold mt-4"
        >
          End Call
        </button>
      </LiveKitRoom>
    </main>
  );
}

function AgentVisualizer() {
  const { state, audioTrack } = useVoiceAssistant();
  
  return (
    <div className="flex flex-col items-center w-full mt-8">
      <BarVisualizer 
        state={state} 
        barCount={5} 
        trackRef={audioTrack} 
        className="h-16 w-full" 
      />
      <p className="mt-4 text-sm text-gray-400">
        Status: {state === "listening" ? "Listening..." : state === "thinking" ? "Thinking..." : "Speaking..."}
      </p>
    </div>
  );
}