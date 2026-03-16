/** @type {import('next').NextConfig} */
const nextConfig = {
  async rewrites() {
    return [
      {
        source: "/api/gateway/:path*",
        destination: "http://api-gateway:5000/:path*",
      },
    ];
  },
};

export default nextConfig;
