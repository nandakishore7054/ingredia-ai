"use client";

import { useParams, useRouter } from "next/navigation";
import { useEffect, useState } from "react";
import { ArrowLeft, Clock, Flame, Heart, Sparkles, ChefHat, Users, CheckCircle2, Share2, Printer } from "lucide-react";
import { useAppContext } from "@/context/AppContext";
import { useAuth } from "@/context/AuthContext";
import { api } from "@/services/api";
import toast from "react-hot-toast";

const MacroRing = ({ value, max, color, label }: { value: number | null, max: number, color: string, label: string }) => {
  const safeValue = value || 0;
  const safeMax = max || 100; // prevent divide by zero
  const radius = 30;
  const circumference = 2 * Math.PI * radius;
  const percent = Math.min(safeValue / safeMax, 1);
  const strokeDashoffset = circumference - percent * circumference;
  
  return (
    <div className="flex flex-col items-center">
      <div className="relative flex items-center justify-center w-20 h-20">
        <svg className="w-full h-full transform -rotate-90">
          <circle cx="40" cy="40" r="30" stroke="currentColor" strokeWidth="6" fill="transparent" className="text-gray-100" />
          <circle cx="40" cy="40" r="30" stroke="currentColor" strokeWidth="6" fill="transparent"
            strokeDasharray={circumference} strokeDashoffset={strokeDashoffset}
            className={`transition-all duration-1000 ease-out ${color}`} strokeLinecap="round" />
        </svg>
        <span className="absolute text-sm font-bold text-gray-700">{value != null && value > 0 ? `${value}g` : "—"}</span>
      </div>
      <span className="text-xs text-gray-500 font-medium uppercase mt-1">{label}</span>
    </div>
  );
};

export default function RecipeDetailPage() {
  const { name } = useParams();
  const router = useRouter();
  const { recipes, setRecipes } = useAppContext();
  const { token } = useAuth();

  const decodedName = decodeURIComponent(name as string);
  const [recipe, setRecipe] = useState<any | null>(null);
  const [loading, setLoading] = useState(true);
  const [analyzing, setAnalyzing] = useState(false);
  const [aiInsights, setAiInsights] = useState<string | null>(null);

  useEffect(() => {
    // 1️⃣ Try from context first
    const fromContext = recipes.find(
      (r) => r.name.toLowerCase() === decodedName.toLowerCase()
    );

    if (fromContext) {
      setRecipe(fromContext);
      // Even if found in context, fetch from backend to get ingredients if missing
      if (!fromContext.ingredients || fromContext.ingredients.length === 0) {
        fetchRecipe();
      } else {
        setLoading(false);
      }
      return;
    }

    // 2️⃣ Fallback → fetch from backend
    async function fetchRecipe() {
      try {
        const res = await api.get(`/recipes/${encodeURIComponent(decodedName)}`);
        setRecipe(res.data);
      } catch {
        setRecipe(null);
      } finally {
        setLoading(false);
      }
    }

    fetchRecipe();
  }, [decodedName, recipes]);

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-50">
        <div className="animate-pulse flex flex-col items-center">
          <div className="h-12 w-12 border-4 border-green-500 border-t-transparent rounded-full animate-spin mb-4"></div>
          <p className="text-gray-500 font-medium">Loading recipe details...</p>
        </div>
      </div>
    );
  }

  if (!recipe) {
    return (
      <div className="min-h-screen flex flex-col items-center justify-center bg-gray-50">
        <p className="text-gray-500 mb-4 text-xl font-medium">
          Recipe not found 😕
        </p>
        <button
          onClick={() => router.push("/recipes")}
          className="px-6 py-2 bg-green-600 text-white rounded-full font-medium hover:bg-green-700 transition"
        >
          ← Back to Recipes
        </button>
      </div>
    );
  }

  const toggleFavorite = async () => {
    if (!token) return toast.error("Please login to save favorites");

    try {
      const res = await api.post(`/favorites/${recipe.id}`);
      const isFav = res.data?.favorited !== undefined ? res.data.favorited : !recipe.is_favorite;

      setRecipe({ ...recipe, is_favorite: isFav });

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

  const getAiInsights = async () => {
    if (!token) return toast.error("Please login to use AI features");
    setAnalyzing(true);
    try {
      const res = await api.post("/ai/substitutions", { 
        recipe_name: recipe.name, 
        ingredients: recipe.ingredients || [] 
      });
      setAiInsights(res.data.nutrition_insights || "Healthy and balanced.");
      toast.success("AI Analysis Complete!");
    } catch (err) {
      toast.error("Analysis failed");
    } finally {
      setAnalyzing(false);
    }
  };

  // Mocked/calculated values for rich display
  const prepTime = 10;
  const cookingTime = recipe.cooking_time || 20;
  const totalTime = prepTime + cookingTime;
  const difficulty = cookingTime > 40 ? "Hard" : cookingTime > 20 ? "Medium" : "Easy";
  const servings = 4;
  const ingredientsList = recipe.ingredients || [];
  
  // Parse instructions into steps if it's a single block of text
  const rawInstructions = recipe.instructions || "";
  const instructionSteps = rawInstructions.split(/\n+/).filter((s: string) => s.trim().length > 0);

  return (
    <div className="min-h-screen bg-gray-50 pb-20">
      {/* Hero Image Section */}
      <div className="relative h-72 md:h-96 w-full bg-gray-900">
        <img 
          src="https://images.unsplash.com/photo-1546069901-ba9599a7e63c?auto=format&fit=crop&w=1200&q=80" 
          alt={recipe.name}
          className="w-full h-full object-cover opacity-60"
        />
        <div className="absolute top-6 left-6">
          <button
            onClick={() => router.push("/recipes")}
            className="flex items-center gap-2 bg-white/20 hover:bg-white/40 backdrop-blur-md text-white px-4 py-2 rounded-full transition font-medium"
          >
            <ArrowLeft size={18} /> Back
          </button>
        </div>
      </div>

      {/* Main Content Container */}
      <div className="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 -mt-24 relative z-10">
        
        {/* Header Card */}
        <div className="bg-white rounded-3xl shadow-xl p-8 mb-8 border border-gray-100">
          <div className="flex justify-between items-start mb-4">
            <div>
              <div className="flex flex-wrap gap-2 mb-3">
                {recipe.cuisine && <span className="px-3 py-1 bg-green-50 text-green-700 rounded-full text-sm font-semibold">{recipe.cuisine}</span>}
                {recipe.diet && <span className="px-3 py-1 bg-blue-50 text-blue-700 rounded-full text-sm font-semibold">{recipe.diet}</span>}
                <span className="px-3 py-1 bg-orange-50 text-orange-700 rounded-full text-sm font-semibold">{difficulty}</span>
              </div>
              <h1 className="text-4xl md:text-5xl font-extrabold text-gray-900 mb-4">{recipe.name}</h1>
            </div>
            <div className="flex items-center gap-2">
              <button
                onClick={() => {
                  if (typeof window !== "undefined") {
                    navigator.clipboard.writeText(window.location.href);
                    toast.success("Recipe link copied to clipboard! 📋");
                  }
                }}
                className="p-2.5 bg-gray-50 rounded-full hover:bg-gray-100 text-gray-600 transition"
                title="Copy Link"
                aria-label="Copy Link"
              >
                <Share2 size={20} />
              </button>
              <button
                onClick={() => {
                  if (typeof window !== "undefined") {
                    window.print();
                  }
                }}
                className="p-2.5 bg-gray-50 rounded-full hover:bg-gray-100 text-gray-600 transition hidden sm:block"
                title="Print Recipe"
                aria-label="Print Recipe"
              >
                <Printer size={20} />
              </button>
              <button
                onClick={toggleFavorite}
                className="p-3 bg-gray-50 rounded-full hover:bg-red-50 transition group"
                aria-label="Favorite Recipe"
              >
                <Heart size={26} className={recipe.is_favorite ? "text-red-500" : "text-gray-400 group-hover:text-red-400 transition"} fill={recipe.is_favorite ? "currentColor" : "none"} />
              </button>
            </div>
          </div>

          <div className="flex flex-wrap items-center gap-6 md:gap-10 text-gray-600 font-medium">
            <div className="flex items-center gap-2"><Clock className="text-gray-400" size={20} /> Prep: {prepTime}m</div>
            <div className="flex items-center gap-2"><Flame className="text-orange-400" size={20} /> Cook: {cookingTime}m</div>
            <div className="flex items-center gap-2"><ChefHat className="text-purple-400" size={20} /> Total: {totalTime}m</div>
            <div className="flex items-center gap-2"><Users className="text-blue-400" size={20} /> Serves: {servings}</div>
          </div>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          
          {/* Left Column: Ingredients & AI */}
          <div className="lg:col-span-1 space-y-8">
            
            {/* Ingredients Card */}
            <div className="bg-white rounded-3xl shadow p-6 border border-gray-100">
              <h2 className="text-2xl font-bold mb-4 text-gray-900 flex items-center gap-2">
                Ingredients <span className="text-sm font-normal text-gray-500 bg-gray-100 px-2 py-1 rounded-full">{ingredientsList.length} items</span>
              </h2>
              {ingredientsList.length > 0 ? (
                <ul className="space-y-3">
                  {ingredientsList.map((ing: string, i: number) => (
                    <li key={i} className="flex items-start gap-3 group">
                      <div className="mt-0.5 text-green-500 bg-green-50 rounded-full p-1"><CheckCircle2 size={16} /></div>
                      <span className="text-gray-700 capitalize font-medium group-hover:text-gray-900 transition">{ing}</span>
                    </li>
                  ))}
                </ul>
              ) : (
                <p className="text-gray-500 italic">No specific ingredients listed.</p>
              )}
            </div>

            {/* AI Nutrition & Subs */}
            <div className="bg-gradient-to-br from-green-50 to-emerald-100 rounded-3xl shadow p-6 border border-green-200">
              <h2 className="text-xl font-bold mb-3 text-green-900 flex items-center gap-2">
                <Sparkles className="text-green-600" /> AI Nutrition & Subs
              </h2>
              <p className="text-green-800 text-sm mb-4">
                Get personalized ingredient substitutions and deeper nutrition insights using AI.
              </p>
              {aiInsights ? (
                <div className="bg-white/80 p-4 rounded-xl text-sm text-gray-800 leading-relaxed border border-green-200">
                  {aiInsights}
                </div>
              ) : (
                <button 
                  onClick={getAiInsights}
                  disabled={analyzing}
                  className="w-full py-3 bg-green-600 text-white font-semibold rounded-xl hover:bg-green-700 transition flex items-center justify-center gap-2 shadow-sm disabled:opacity-70 disabled:cursor-not-allowed"
                >
                  {analyzing ? (
                    <><div className="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin"></div> Analyzing...</>
                  ) : (
                    <>Analyze Recipe</>
                  )}
                </button>
              )}
            </div>

          </div>

          {/* Right Column: Instructions & Nutrition Macros */}
          <div className="lg:col-span-2 space-y-8">
            
            {/* Nutrition Macros Card */}
            <div className="bg-white rounded-3xl shadow p-6 border border-gray-100">
              <h2 className="text-2xl font-bold mb-6 text-gray-900">Nutrition per serving</h2>
              
              <div className="flex flex-wrap justify-around items-center gap-4">
                <div className="text-center mb-4 md:mb-0">
                  <p className="text-4xl font-extrabold text-gray-900">{recipe.calories ? `${recipe.calories} kcal` : "Nutrition unavailable"}</p>
                  <p className="text-sm font-medium text-gray-500 uppercase mt-1">Calories</p>
                </div>
                
                <div className="hidden md:block w-px h-16 bg-gray-200"></div>

                <MacroRing value={recipe.protein} max={50} color="text-red-500" label="Protein" />
                <MacroRing value={recipe.carbs} max={100} color="text-blue-500" label="Carbs" />
                <MacroRing value={recipe.fats} max={50} color="text-yellow-500" label="Fats" />
              </div>
            </div>

            {/* Instructions Card */}
            <div className="bg-white rounded-3xl shadow p-6 md:p-8 border border-gray-100">
              <h2 className="text-2xl font-bold mb-6 text-gray-900 flex items-center gap-2">
                Instructions 👨‍🍳
              </h2>
              
              <div className="space-y-6">
                {instructionSteps.map((step: string, index: number) => {
                  // Clean up step text (remove prefix numbers if they exist like "1. ", "Step 1:")
                  const cleanStep = step.replace(/^(Step\s*\d+:?|\d+\.\s*)/i, '').trim();
                  
                  return (
                    <div key={index} className="flex gap-4">
                      <div className="flex-shrink-0">
                        <div className="w-8 h-8 rounded-full bg-gray-900 text-white flex items-center justify-center font-bold text-sm">
                          {index + 1}
                        </div>
                      </div>
                      <p className="text-gray-700 leading-relaxed pt-1">
                        {cleanStep}
                      </p>
                    </div>
                  );
                })}
              </div>
            </div>

          </div>
        </div>
      </div>
    </div>
  );
}
