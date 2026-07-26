import "./globals.css";
import Navbar from "@/components/Navbar";
import Chatbot from "@/components/Chatbot";
import { AuthProvider } from "@/context/AuthContext";
import { AppProvider } from "@/context/AppContext";
import { Toaster } from "react-hot-toast";

import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "Ingredia AI - Intelligent Recipe & Nutrition Assistant",
  description: "Computer Vision ingredient detection, AI-powered recipe matching, personalized nutrition insights, and dietary planning.",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body suppressHydrationWarning>
        <AuthProvider>
          <AppProvider>
            <Toaster position="top-right" />
            <Navbar />
            {children}
            <Chatbot />
          </AppProvider>
        </AuthProvider>
      </body>
    </html>
  );
}
