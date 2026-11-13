"use client";

import { useState } from "react";
import { LiveKitRoom, RoomAudioRenderer } from "@livekit/components-react"; // 🔥 RoomAudioRenderer import kiya
import TopNav from "@/components/TopNav";
import BottomBar from "@/components/BottomBar";
import LeftPanel from "@/components/LeftPanel";
import RightPanel from "@/components/RightPanel";
import CenterDisplay from "@/components/CenterDisplay";
import { createSession } from "@/lib/api"; 

export default function Home() {
  const [token, setToken] = useState<string>("");
  const [connecting, setConnecting] = useState(false);

  const startConversation = async () => {
    setConnecting(true);
    try {
      // Backend se token mango
      const data = await createSession(`user-${Math.floor(Math.random() * 1000)}`);
      setToken(data.token);
    } catch (error) {
      console.error("Failed to connect:", error);
      alert("Backend se connect nahi ho paya. Check karo ke server chal raha hai ya nahi.");
    } finally {
      setConnecting(false);
    }
  };

  const endConversation = () => {
    setToken("");
  };

  // Dashboard ka layout
  const DashboardContent = (
    <main className="h-screen w-full flex flex-col overflow-hidden bg-[#00122e]">
      
      {/* TOP NAVIGATION */}
      <div className="shrink-0 w-full z-20">
        <TopNav />
      </div>

      {/* MAIN CONTENT AREA */}
      <div className="flex-1 w-full flex px-4 gap-2 lg:gap-6 justify-center items-center overflow-hidden relative z-10">
        
        {/* LEFT SIDE (Tools) */}
        <div className="flex items-center justify-center shrink-0 w-[180px] md:w-[220px] lg:w-[240px]">
          <LeftPanel />
        </div>

        {/* CENTER SECTION (Avatar & Mic) */}
        <div className="flex-1 h-full flex items-center justify-center min-w-0">
          <CenterDisplay 
            onStart={startConversation} 
            isConnected={!!token} 
            isConnecting={connecting} 
          />
        </div>

        {/* RIGHT SIDE (Activity Log / Transcript) */}
        <div className="flex items-center justify-center shrink-0 w-[220px] md:w-[260px] lg:w-[300px]">
          <RightPanel isConnected={!!token} />
        </div>

      </div>

      {/* BOTTOM TOOLBAR */}
      <div className="shrink-0 w-full z-20">
        <BottomBar />
      </div>
      
    </main>
  );

  // Agar token mil gaya hai, toh LiveKitRoom ke andar Dashboard dikhao
  if (token) {
    return (
      <LiveKitRoom
        token={token}
        serverUrl={process.env.NEXT_PUBLIC_LIVEKIT_URL}
        connect={true}
        audio={true}
        video={false}
        onDisconnected={endConversation}
      >
        {/* 🔥 YEH SABSE ZAROORI HAI: AI ki awaz speakers par play karega */}
        <RoomAudioRenderer />
        
        {DashboardContent}
      </LiveKitRoom>
    );
  }

  // Agar token nahi hai, toh normal Dashboard dikhao (Start button ke sath)
  return DashboardContent;
}