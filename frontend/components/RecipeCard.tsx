"use client";

import { motion } from "framer-motion";
import { Clock, Flame, Heart, Sparkles } from "lucide-react";
import { useRouter } from "next/navigation";
import { useAuth } from "@/context/AuthContext";
import { useAppContext } from "@/context/AppContext";
import { api } from "@/services/api";
import toast from "react-hot-toast";

export default function RecipeCard({ recipe }: { recipe: any }) {
  const router = useRouter();
  const { token } = useAuth();
  const { recipes, setRecipes } = useAppContext();

  const toggleFavorite = async (e: React.MouseEvent) => {
    e.stopPropagation();
    if (!token) return toast.error("Please login to save favorites");

    try {
      const res = await api.post(`/favorites/${recipe.id}`);
      const isFav = res.data?.favorited !== undefined ? res.data.favorited : !recipe.is_favorite;

      setRecipes(
        recipes.map((r) =>
          r.id === recipe.id
            ? { ...r, is_favorite: isFav }
            : r
        )
      );

      if (isFav) {
        toast.success("Added to favorites ❤️");
      } else {
        toast.success("Removed from favorites");
      }
    } catch (err) {
      toast.error("Failed to update favorites");
    }
  };

  return (
    <motion.div
      onClick={() =>
        router.push(`/recipes/${encodeURIComponent(recipe.name)}`)
      }
      whileHover={{ scale: 1.02 }}
      className="relative bg-white rounded-3xl shadow p-6 cursor-pointer border border-gray-100 flex flex-col h-full"
    >
      {/* ❤️ Favorite */}
      <button
        onClick={toggleFavorite}
        className={`absolute top-4 right-4 ${
          recipe.is_favorite ? "text-red-500" : "text-gray-300 hover:text-red-400 transition"
        }`}
      >
        <Heart fill={recipe.is_favorite ? "currentColor" : "none"} />
      </button>

      <h3 className="text-xl font-bold mb-3 pr-8">{recipe.name}</h3>

      <div className="flex gap-2 mb-4 flex-wrap">
        <span className="px-3 py-1 bg-green-50 text-green-700 rounded-full text-xs font-medium border border-green-100">
          {recipe.cuisine || "Fusion"}
        </span>
        <span className="px-3 py-1 bg-blue-50 text-blue-700 rounded-full text-xs font-medium border border-blue-100">
          {recipe.diet || "Any"}
        </span>
      </div>

      <div className="flex gap-4 text-sm text-gray-600 mb-4">
        <span className="flex items-center gap-1 font-medium">
          <Clock size={14} className="text-gray-400" /> {recipe.cooking_time}m
        </span>
        <span className="flex items-center gap-1 font-medium">
          <Flame size={14} className="text-orange-400" /> {recipe.calories ? `${recipe.calories} kcal` : "Nutrition unavailable"}
        </span>
      </div>

      <div className="mt-auto pt-4 border-t border-gray-100">
        <button
          onClick={async (e) => {
            e.stopPropagation();
            toast.loading("Analyzing nutrition...", { id: "ai-subs" });
            try {
              const res = await api.post("/ai/substitutions", { 
                recipe_name: recipe.name, 
                ingredients: recipe.matched_ingredients || [] 
              });
              toast.success(
                <div>
                  <p className="font-bold mb-1">AI Insights:</p>
                  <p className="text-sm">{res.data.nutrition_insights || "Healthy and balanced."}</p>
                </div>, 
                { id: "ai-subs", duration: 5000 }
              );
            } catch (err) {
              toast.error("Analysis failed", { id: "ai-subs" });
            }
          }}
          className="w-full py-2 bg-green-50 text-green-700 text-sm font-semibold rounded-xl hover:bg-green-100 transition flex items-center justify-center gap-2"
        >
          <Sparkles size={16} /> AI Nutrition & Subs
        </button>
      </div>
    </motion.div>
  );
}
