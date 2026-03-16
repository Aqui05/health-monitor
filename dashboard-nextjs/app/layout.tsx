import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Health Monitor — Dashboard",
  description: "Système distribué de surveillance des maladies chroniques",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="fr">
      <body className="min-h-screen bg-[#0a0f1e] text-slate-200">
        {children}
      </body>
    </html>
  );
}
