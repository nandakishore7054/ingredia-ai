"use client";

import { useState, useEffect, useCallback } from "react";
import { useAppContext } from "@/context/AppContext";
import RecipeCard from "@/components/RecipeCard";
import { api, searchRecipes } from "@/services/api";
import toast from "react-hot-toast";
import { Sparkles, Search, Filter, RotateCcw, Clock, Utensils, Leaf } from "lucide-react";

export default function RecipesPage() {
  const { recipes, setRecipes } = useAppContext();
  const [loading, setLoading] = useState(false);

  // Search & Filter State
  const [query, setQuery] = useState("");
  const [cuisine, setCuisine] = useState("");
  const [diet, setDiet] = useState("");
  const [maxCookingTime, setMaxCookingTime] = useState("");
  const [totalResults, setTotalResults] = useState(0);

  // AI Prompt State (Preserved)
  const [prompt, setPrompt] = useState("");
  const [aiLoading, setAiLoading] = useState(false);
  const [showAiBox, setShowAiBox] = useState(false);

  /* ---------------- FETCH & FILTER RECIPES ---------------- */
  const fetchFilteredRecipes = useCallback(async () => {
    setLoading(true);
    try {
      const filters: any = {};
      if (query.trim()) filters.query = query.trim();
      if (cuisine) filters.cuisine = cuisine;
      if (diet) filters.diet = diet;
      if (maxCookingTime) filters.max_cooking_time = parseInt(maxCookingTime);

      const res = await searchRecipes(filters);
      const items = res.recipes || [];
      setRecipes(items);
      setTotalResults(res.total_results || items.length);
    } catch (err) {
      toast.error("Failed to load recipes.");
    } finally {
      setLoading(false);
    }
  }, [query, cuisine, diet, maxCookingTime, setRecipes]);

  useEffect(() => {
    fetchFilteredRecipes();
  }, [fetchFilteredRecipes]);

  /* ---------------- CLEAR FILTERS ---------------- */
  const handleClearFilters = () => {
    setQuery("");
    setCuisine("");
    setDiet("");
    setMaxCookingTime("");
  };

  /* ---------------- AI GENERATE PROMPT (PRESERVED) ---------------- */
  const handleAiSearch = async () => {
    if (!prompt.trim()) return;
    setAiLoading(true);
    try {
      const res = await api.post("/ai/generate-prompt", { prompt });
      if (res.data.recipes) {
        setRecipes(res.data.recipes);
        setTotalResults(res.data.recipes.length);
        toast.success("AI generated your recipes!");
      }
    } catch (err) {
      toast.error("Failed to generate AI recipes.");
    } finally {
      setAiLoading(false);
    }
  };

  return (
    <div className="max-w-7xl mx-auto p-6">
      
      {/* HEADER */}
      <div className="text-center mb-8">
        <h1 className="text-4xl font-extrabold text-gray-900 mb-2">
          Explore Recipes
        </h1>
        <p className="text-gray-500 max-w-xl mx-auto">
          Search by name, filter by cuisine, diet, and cooking time, or let AI craft custom recipes for you.
        </p>
      </div>

      {/* AI GENERATOR TOGGLE / BOX (PRESERVED) */}
      <div className="max-w-3xl mx-auto mb-8">
        {!showAiBox ? (
          <button
            onClick={() => setShowAiBox(true)}
            className="w-full py-3 px-6 bg-gradient-to-r from-green-50 to-emerald-50 text-green-700 rounded-2xl border border-green-200 font-medium hover:border-green-300 transition flex items-center justify-center gap-2 shadow-sm"
          >
            <Sparkles size={18} /> Want AI to generate custom recipes from a text prompt? Click here
          </button>
        ) : (
          <div className="bg-white p-2 rounded-2xl shadow-sm border border-gray-200 flex items-center gap-2">
            <div className="pl-3 text-green-500">
              <Sparkles size={20} />
            </div>
            <input 
              type="text" 
              value={prompt}
              onChange={(e) => setPrompt(e.target.value)}
              onKeyDown={(e) => e.key === "Enter" && handleAiSearch()}
              placeholder='e.g. "I have chicken and rice, make it spicy"'
              className="flex-1 px-3 py-2.5 outline-none text-gray-700 text-sm bg-transparent"
            />
            <button 
              onClick={handleAiSearch}
              disabled={aiLoading}
              className="bg-black text-white px-5 py-2.5 rounded-xl font-medium text-sm hover:bg-gray-800 transition disabled:opacity-70 flex items-center gap-2"
            >
              {aiLoading ? "Thinking..." : "Generate AI"}
            </button>
            <button 
              onClick={() => setShowAiBox(false)}
              className="text-gray-400 hover:text-gray-600 px-2 text-sm"
            >
              ✕
            </button>
          </div>
        )}
      </div>

      {/* SEARCH AND FILTERS BAR */}
      <div className="bg-white rounded-2xl shadow-sm border border-gray-100 p-6 mb-8">
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
          
          {/* SEARCH INPUT */}
          <div className="relative">
            <Search className="absolute left-3.5 top-3 text-gray-400" size={18} />
            <input
              type="text"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              placeholder="Search recipe name..."
              className="w-full pl-10 pr-4 py-2.5 bg-gray-50 border border-gray-200 rounded-xl text-sm outline-none focus:border-green-500 transition"
            />
          </div>

          {/* CUISINE FILTER */}
          <div className="relative">
            <Utensils className="absolute left-3.5 top-3 text-gray-400" size={16} />
            <select
              value={cuisine}
              onChange={(e) => setCuisine(e.target.value)}
              className="w-full pl-10 pr-4 py-2.5 bg-gray-50 border border-gray-200 rounded-xl text-sm outline-none focus:border-green-500 transition appearance-none cursor-pointer"
            >
              <option value="">All Cuisines</option>
              <option value="Indian">Indian</option>
              <option value="Italian">Italian</option>
              <option value="Western">Western</option>
              <option value="Indo-Chinese">Indo-Chinese</option>
              <option value="Fusion">Fusion</option>
            </select>
          </div>

          {/* DIET FILTER */}
          <div className="relative">
            <Leaf className="absolute left-3.5 top-3 text-gray-400" size={16} />
            <select
              value={diet}
              onChange={(e) => setDiet(e.target.value)}
              className="w-full pl-10 pr-4 py-2.5 bg-gray-50 border border-gray-200 rounded-xl text-sm outline-none focus:border-green-500 transition appearance-none cursor-pointer"
            >
              <option value="">All Diets</option>
              <option value="Vegan">Vegan</option>
              <option value="Vegetarian">Vegetarian</option>
              <option value="Eggetarian">Eggetarian</option>
              <option value="Non-Veg">Non-Veg</option>
            </select>
          </div>

          {/* MAX COOKING TIME FILTER */}
          <div className="relative">
            <Clock className="absolute left-3.5 top-3 text-gray-400" size={16} />
            <select
              value={maxCookingTime}
              onChange={(e) => setMaxCookingTime(e.target.value)}
              className="w-full pl-10 pr-4 py-2.5 bg-gray-50 border border-gray-200 rounded-xl text-sm outline-none focus:border-green-500 transition appearance-none cursor-pointer"
            >
              <option value="">Any Time</option>
              <option value="15">Under 15 mins</option>
              <option value="30">Under 30 mins</option>
              <option value="45">Under 45 mins</option>
              <option value="60">Under 60 mins</option>
            </select>
          </div>
        </div>

        {/* ACTIVE FILTERS SUMMARY & CLEAR */}
        {(query || cuisine || diet || maxCookingTime) && (
          <div className="mt-4 pt-4 border-t border-gray-100 flex items-center justify-between text-xs text-gray-500 flex-wrap gap-2">
            <span>
              Found <strong className="text-gray-900 font-semibold">{totalResults}</strong> recipe(s) matching your active filters.
            </span>
            <button
              onClick={handleClearFilters}
              className="flex items-center gap-1 text-red-600 hover:text-red-700 font-medium transition"
            >
              <RotateCcw size={13} /> Reset Filters
            </button>
          </div>
        )}
      </div>

      {/* RESULTS DISPLAY */}
      {loading || aiLoading ? (
        <div className="flex flex-col items-center justify-center py-20">
          <div className="w-10 h-10 border-4 border-green-600 border-t-transparent rounded-full animate-spin mb-4" />
          <p className="text-gray-500 text-sm">Searching recipes...</p>
        </div>
      ) : !recipes.length ? (
        <div className="text-center py-20 bg-white rounded-2xl border border-gray-100 p-8 shadow-sm">
          <Search className="mx-auto text-gray-300 mb-4" size={48} />
          <h3 className="text-xl font-bold text-gray-800 mb-2">No matching recipes found</h3>
          <p className="text-gray-500 max-w-md mx-auto mb-6 text-sm">
            Try adjusting your search criteria, clearing some filters, or using the AI Recipe Generator above.
          </p>
          <button
            onClick={handleClearFilters}
            className="px-6 py-2.5 bg-black text-white rounded-full font-medium text-sm hover:bg-gray-800 transition"
          >
            Clear All Filters
          </button>
        </div>
      ) : (
        <div>
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
            {recipes.map((r, i) => (
              <RecipeCard key={r.id || i} recipe={r} />
            ))}
          </div>
        </div>
      )}
    </div>
  );
}