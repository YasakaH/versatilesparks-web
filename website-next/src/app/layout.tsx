import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Browser Engineering Knowledge System — Versatile Sparks",
  description: "An interactive database and dependency map for production-grade browser automation, anti-detection, and session recovery.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" className="h-full antialiased dark">
      <body className="min-h-full flex flex-col bg-[#090909] text-[#f2f2f2]">
        {children}
      </body>
    </html>
  );
}
