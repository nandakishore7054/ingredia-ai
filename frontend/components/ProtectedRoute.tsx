"use client";

import { useEffect } from "react";
import { useRouter } from "next/navigation";
import { useAuth } from "@/context/AuthContext";
import toast from "react-hot-toast";

export default function ProtectedRoute({ children }: { children: React.ReactNode }) {
  const { user, loading } = useAuth();
  const router = useRouter();

  useEffect(() => {
    if (!loading && !user) {
      // Deduplicate toast notifications to prevent repetitive alert spams (Problem 6 & 7)
      toast.error("Please login to access this page", {
        id: "protected-route-unauthorized",
      });
      router.push("/login");
    }
  }, [user, loading, router]);

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-50/50">
        <div className="flex flex-col items-center gap-3">
          <div className="w-10 h-10 border-4 border-green-600 border-t-transparent rounded-full animate-spin" />
          <p className="text-sm font-medium text-gray-500 animate-pulse">Authenticating...</p>
        </div>
      </div>
    );
  }

  if (!user) {
    return null; // Prevent children layout render while routing redirects
  }

  return <>{children}</>;
}
