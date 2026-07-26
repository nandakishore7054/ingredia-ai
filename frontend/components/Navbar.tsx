"use client";

import Link from "next/link";
import { useAuth } from "@/context/AuthContext";
import { motion } from "framer-motion";
import { ChefHat, LogOut, User as UserIcon } from "lucide-react";

export default function Navbar() {
  const { user, logout, loading } = useAuth();

  return (
    <nav className="sticky top-0 z-50 bg-white/80 backdrop-blur-md border-b border-gray-100 shadow-sm transition-all">
      <div className="max-w-7xl mx-auto px-6 h-16 flex justify-between items-center">
        
        {/* LOGO */}
        <Link href="/" className="flex items-center gap-2 group">
          <div className="bg-green-600 p-1.5 rounded-lg text-white group-hover:bg-green-700 transition">
            <ChefHat size={22} />
          </div>
          <span className="text-xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-green-700 to-emerald-500">
            Ingredia AI
          </span>
        </Link>

        {/* DESKTOP LINKS */}
        <div className="hidden md:flex items-center gap-8">
          <Link href="/upload" className="text-gray-600 hover:text-green-600 font-medium transition">
            Scan & Detect
          </Link>
          <Link href="/recipes" className="text-gray-600 hover:text-green-600 font-medium transition">
            Recipes
          </Link>
          {user && (
            <>
              <Link href="/favorites" className="text-gray-600 hover:text-green-600 font-medium transition">
                Favorites
              </Link>
              <Link href="/preferences" className="text-gray-600 hover:text-green-600 font-medium transition">
                Preferences
              </Link>
            </>
          )}
        </div>

        {/* AUTH ACTIONS */}
        <div className="flex items-center gap-4">
          {loading ? (
            <div className="w-24 h-9 bg-gray-200 rounded-full animate-pulse" />
          ) : !user ? (
            <div className="flex items-center gap-3">
              <Link href="/login" className="text-gray-600 hover:text-gray-900 font-medium px-2">
                Login
              </Link>
              <Link
                href="/register"
                className="px-5 py-2 rounded-full bg-black text-white text-sm font-medium hover:bg-gray-800 transition shadow-md"
              >
                Sign Up Free
              </Link>
            </div>
          ) : (
            <UserBadge name={user.name} onLogout={logout} />
          )}
        </div>
      </div>
    </nav>
  );
}

/* 👤 USER BADGE */
function UserBadge({ name, onLogout }: { name: string; onLogout: () => void }) {
  return (
    <div className="flex items-center gap-4">
      <Link href="/profile" className="flex items-center gap-2 hover:bg-gray-50 px-3 py-1.5 rounded-full transition border border-gray-100">
        <div className="w-7 h-7 rounded-full bg-green-100 text-green-700 flex items-center justify-center font-bold text-sm">
          {name.charAt(0).toUpperCase()}
        </div>
        <span className="text-sm font-medium text-gray-700 hidden sm:block">{name}</span>
      </Link>
      
      <button
        onClick={onLogout}
        className="text-gray-400 hover:text-red-500 transition p-1"
        title="Logout"
      >
        <LogOut size={20} />
      </button>
    </div>
  );
}
