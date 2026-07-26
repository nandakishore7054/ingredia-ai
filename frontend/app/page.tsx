"use client";

import Link from "next/link";
import { useEffect, useState } from "react";
import { motion } from "framer-motion";
import { Camera, Sparkles, ChefHat, ArrowRight, Zap, Star, Sliders, Heart, Clock, Utensils } from "lucide-react";
import { useAuth } from "@/context/AuthContext";
import { api } from "@/services/api";
import RecipeCard from "@/components/RecipeCard";
import RecipeSkeleton from "@/components/RecipeSkeleton";

export default function LandingOrDashboardPage() {
  const { user } = useAuth();
  const [recommendations, setRecommendations] = useState<any[]>([]);
  const [loadingRecs, setLoadingRecs] = useState<boolean>(true);

  useEffect(() => {
    if (user) {
      async function fetchRecs() {
        try {
          const res = await api.get("/recommendations/personalized");
          if (res.data && res.data.recipes) {
            setRecommendations(res.data.recipes);
          }
        } catch (err) {
          console.error("Failed to load recommendations", err);
        } finally {
          setLoadingRecs(false);
        }
      }
      fetchRecs();
    }
  }, [user]);

  // ==========================================
  // 1️⃣ LOGGED-IN DASHBOARD VIEW
  // ==========================================
  if (user) {
    return (
      <div className="min-h-screen bg-gray-50 pb-20">
        {/* WELCOME HEADER */}
        <div className="bg-gradient-to-r from-gray-900 via-gray-800 to-green-950 text-white py-12 px-6 sm:px-12 shadow-lg mb-10">
          <div className="max-w-7xl mx-auto flex flex-col md:flex-row justify-between items-start md:items-center gap-6">
            <div>
              <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-green-500/20 text-green-300 text-xs font-semibold uppercase tracking-wider mb-3">
                <Sparkles size={14} /> Personal Dashboard
              </div>
              <h1 className="text-3xl md:text-5xl font-extrabold tracking-tight">
                Welcome back, <span className="text-transparent bg-clip-text bg-gradient-to-r from-green-400 to-emerald-300">{user.name}</span>! 👋
              </h1>
              <p className="text-gray-300 mt-2 text-base max-w-xl">
                Ready to turn your fresh ingredients into healthy, tailored recipes?
              </p>
            </div>

            <div className="flex gap-3">
              <Link
                href="/upload"
                className="px-5 py-3 bg-green-600 hover:bg-green-700 text-white font-bold rounded-2xl transition shadow-md flex items-center gap-2"
              >
                <Camera size={18} /> Scan Ingredients
              </Link>
              <Link
                href="/preferences"
                className="px-5 py-3 bg-white/10 hover:bg-white/20 text-white font-semibold rounded-2xl transition backdrop-blur-md flex items-center gap-2"
              >
                <Sliders size={18} /> Preferences
              </Link>
            </div>
          </div>
        </div>

        <div className="max-w-7xl mx-auto px-6 space-y-12">
          
          {/* QUICK ACTIONS GRID */}
          <div className="grid grid-cols-1 sm:grid-cols-3 gap-6">
            <Link
              href="/upload"
              className="bg-white p-6 rounded-3xl shadow-sm border border-gray-100 hover:shadow-md transition group flex flex-col justify-between"
            >
              <div className="w-12 h-12 rounded-2xl bg-green-50 text-green-600 flex items-center justify-center mb-4 group-hover:scale-110 transition-transform">
                <Camera size={24} />
              </div>
              <div>
                <h3 className="text-lg font-bold text-gray-900 mb-1">Upload & Detect</h3>
                <p className="text-gray-500 text-sm">Snap a photo of your fridge or pantry to auto-detect items.</p>
              </div>
              <div className="mt-4 flex items-center gap-1 text-green-600 font-semibold text-sm">
                Start Detection <ArrowRight size={16} />
              </div>
            </Link>

            <Link
              href="/recipes"
              className="bg-white p-6 rounded-3xl shadow-sm border border-gray-100 hover:shadow-md transition group flex flex-col justify-between"
            >
              <div className="w-12 h-12 rounded-2xl bg-blue-50 text-blue-600 flex items-center justify-center mb-4 group-hover:scale-110 transition-transform">
                <Utensils size={24} />
              </div>
              <div>
                <h3 className="text-lg font-bold text-gray-900 mb-1">Browse Recipes</h3>
                <p className="text-gray-500 text-sm">Explore filtered recipes by cuisine, meal type, or max cook time.</p>
              </div>
              <div className="mt-4 flex items-center gap-1 text-blue-600 font-semibold text-sm">
                View All <ArrowRight size={16} />
              </div>
            </Link>

            <Link
              href="/favorites"
              className="bg-white p-6 rounded-3xl shadow-sm border border-gray-100 hover:shadow-md transition group flex flex-col justify-between"
            >
              <div className="w-12 h-12 rounded-2xl bg-red-50 text-red-500 flex items-center justify-center mb-4 group-hover:scale-110 transition-transform">
                <Heart size={24} />
              </div>
              <div>
                <h3 className="text-lg font-bold text-gray-900 mb-1">Saved Favorites</h3>
                <p className="text-gray-500 text-sm">Quickly access your saved collection of favorite meals.</p>
              </div>
              <div className="mt-4 flex items-center gap-1 text-red-500 font-semibold text-sm">
                Open Favorites <ArrowRight size={16} />
              </div>
            </Link>
          </div>

          {/* RECOMMENDED FOR YOU */}
          <div>
            <div className="flex justify-between items-center mb-6">
              <div>
                <h2 className="text-2xl font-extrabold text-gray-900 flex items-center gap-2">
                  <Sparkles className="text-green-600" /> Recommended For You
                </h2>
                <p className="text-gray-500 text-sm">Tailored based on your diet, allergies, and calorie goals.</p>
              </div>
              <Link href="/preferences" className="text-sm font-semibold text-green-600 hover:underline">
                Edit Preferences
              </Link>
            </div>

            {loadingRecs ? (
              <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
                {[...Array(4)].map((_, i) => (
                  <RecipeSkeleton key={i} />
                ))}
              </div>
            ) : recommendations.length > 0 ? (
              <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
                {recommendations.map((recipe) => (
                  <RecipeCard key={recipe.id} recipe={recipe} />
                ))}
              </div>
            ) : (
              <div className="bg-white p-8 rounded-3xl border border-gray-100 text-center">
                <p className="text-gray-500">Configure your preferences to unlock hyper-personalized recipe picks.</p>
                <Link href="/preferences" className="mt-4 inline-block px-6 py-2 bg-green-600 text-white rounded-full text-sm font-bold">
                  Set Preferences
                </Link>
              </div>
            )}
          </div>

        </div>
      </div>
    );
  }

  // ==========================================
  // 2️⃣ PUBLIC MARKETING LANDING PAGE VIEW
  // ==========================================
  return (
    <div className="min-h-screen bg-white">
      {/* HERO SECTION */}
      <section className="relative pt-24 pb-32 overflow-hidden">
        <div className="absolute inset-0 bg-[linear-gradient(to_right,#80808012_1px,transparent_1px),linear-gradient(to_bottom,#80808012_1px,transparent_1px)] bg-[size:24px_24px]"></div>
        
        <div className="max-w-7xl mx-auto px-6 relative z-10 text-center">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6 }}
            className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-green-50 text-green-700 border border-green-200 text-sm font-medium mb-8"
          >
            <Sparkles size={16} />
            Ingredia AI — Intelligent Culinary & Nutrition Assistant
          </motion.div>

          <motion.h1
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 0.1 }}
            className="text-5xl md:text-7xl font-extrabold text-gray-900 tracking-tight mb-8"
          >
            Snap your ingredients.<br />
            <span className="text-transparent bg-clip-text bg-gradient-to-r from-green-600 to-emerald-400">
              Cook something amazing.
            </span>
          </motion.h1>

          <motion.p
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 0.2 }}
            className="text-lg md:text-xl text-gray-600 max-w-2xl mx-auto mb-10"
          >
            Stop wondering what to cook. Ingredia AI uses Computer Vision and LLM intelligence to instantly detect pantry items and recommend healthy recipes.
          </motion.p>

          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 0.3 }}
            className="flex flex-col sm:flex-row items-center justify-center gap-4"
          >
            <Link
              href="/upload"
              className="px-8 py-4 bg-black text-white rounded-full font-medium text-lg hover:bg-gray-800 transition flex items-center gap-2 shadow-xl shadow-black/10"
            >
              Try Detection Demo <ArrowRight size={20} />
            </Link>
            <Link
              href="/recipes"
              className="px-8 py-4 bg-white text-gray-900 border-2 border-gray-200 rounded-full font-medium text-lg hover:border-gray-300 transition"
            >
              Browse Recipes
            </Link>
          </motion.div>
        </div>
      </section>

      {/* HOW IT WORKS */}
      <section className="py-24 bg-gray-50 border-t border-gray-100">
        <div className="max-w-7xl mx-auto px-6">
          <div className="text-center mb-16">
            <h2 className="text-3xl md:text-4xl font-bold text-gray-900 mb-4">How It Works</h2>
            <p className="text-gray-600 max-w-xl mx-auto">Three simple steps to transform your raw ingredients into a culinary masterpiece.</p>
          </div>

          <div className="grid md:grid-cols-3 gap-8">
            {[
              { icon: Camera, title: "1. Snap a Photo", desc: "Take a picture of ingredients in your fridge or kitchen pantry." },
              { icon: Zap, title: "2. Computer Vision Analysis", desc: "Our YOLO vision model detects and identifies your exact food items." },
              { icon: ChefHat, title: "3. AI Recipe Match", desc: "Get matched with balanced recipes tailored to your dietary goals." },
            ].map((step, i) => (
              <motion.div
                key={i}
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ delay: i * 0.2 }}
                className="bg-white p-8 rounded-2xl shadow-sm border border-gray-100 text-center"
              >
                <div className="w-16 h-16 bg-green-50 text-green-600 rounded-full flex items-center justify-center mx-auto mb-6">
                  <step.icon size={32} />
                </div>
                <h3 className="text-xl font-bold text-gray-900 mb-3">{step.title}</h3>
                <p className="text-gray-600 leading-relaxed">{step.desc}</p>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* FOOTER */}
      <footer className="bg-gray-900 text-white py-12 border-t border-gray-800">
        <div className="max-w-7xl mx-auto px-6 flex flex-col md:flex-row justify-between items-center">
          <div className="flex items-center gap-2 mb-4 md:mb-0">
            <ChefHat className="text-green-500" />
            <span className="text-xl font-bold">Ingredia AI</span>
          </div>
          <p className="text-gray-400 text-sm">© {new Date().getFullYear()} Ingredia AI. Developed for Infosys Springboard Virtual Internship.</p>
        </div>
      </footer>
    </div>
  );
}
