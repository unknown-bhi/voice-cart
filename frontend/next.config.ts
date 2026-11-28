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
  allowedDevOrigins: ['172.26.240.1']
};

export default nextConfig;