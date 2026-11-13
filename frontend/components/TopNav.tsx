"use client";
import { Folder, Settings, Video, Search, Mail, Globe, Radio, Tv } from "lucide-react";

const waveHeights = [40, 70, 30, 90, 50, 100, 60, 80, 20, 50, 90, 40, 70, 100, 50, 30, 80, 60, 90, 40];

export default function TopNav() {
  return (
    <div className="w-full max-w-[1200px] mx-auto px-18 pt-0 relative z-20">
      <div className="top-bar-wrapper">
        <div className="top-bar-inner w-full h-full flex items-center">
          <div className="grid grid-cols-3 w-full h-full items-start pt-4">
            
            {/* LEFT ICONS: Responsive gap aur padding */}
            <div className="flex items-center justify-start gap-4 lg:gap-8 pl-4 md:pl-16 mt-1">
              <Folder className="w-5 h-5 shrink-0 text-cyan-300 icon-glow cursor-pointer hover:text-white transition" />
              <Settings className="w-5 h-5 shrink-0 text-cyan-300 icon-glow cursor-pointer hover:text-white transition" />
              <Video className="w-5 h-5 shrink-0 text-cyan-300 icon-glow cursor-pointer hover:text-white transition" />
              <Search className="w-5 h-5 shrink-0 text-cyan-300 icon-glow cursor-pointer hover:text-white transition" />
            </div>
            
            {/* CENTER WAVEFORM */}
            <div className="flex items-center justify-center gap-1 h-8 mt-4 overflow-hidden">
              {waveHeights.map((height, i) => (
                <div 
                  key={i} 
                  className="w-1 shrink-0 bg-cyan-400 rounded-full animate-[pulse_1s_ease-in-out_infinite]" 
                  style={{ height: `${height}%`, animationDelay: `${i * 0.05}s`, boxShadow: '0 0 8px #00E5FF' }} 
                />
              ))}
            </div>

            {/* RIGHT ICONS: Responsive gap aur padding */}
            <div className="flex items-center justify-end gap-4 lg:gap-8 pr-4 md:pr-16 mt-1">
              <Mail className="w-5 h-5 shrink-0 text-cyan-300 icon-glow cursor-pointer hover:text-white transition" />
              <Globe className="w-5 h-5 shrink-0 text-cyan-300 icon-glow cursor-pointer hover:text-white transition" />
              <Radio className="w-5 h-5 shrink-0 text-cyan-300 icon-glow cursor-pointer hover:text-white transition" />
              <Tv className="w-5 h-5 shrink-0 text-cyan-300 icon-glow cursor-pointer hover:text-white transition" />
            </div>

          </div>
        </div>
      </div>
    </div>
  );
}