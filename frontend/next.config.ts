import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  output: "standalone",
  // 🔥 Yeh naya block add karo
  images: {
    remotePatterns: [
      {
        protocol: 'https',
        hostname: 'images.unsplash.com',
      },
    ],
  },
};

export default nextConfig;