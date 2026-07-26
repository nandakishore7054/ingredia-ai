"use client";

import { useEffect, useState } from "react";
import ProtectedRoute from "@/components/ProtectedRoute";
import { api } from "@/services/api";
import toast from "react-hot-toast";
import { Sliders, Save, Check, Flame, ShieldAlert, Utensils } from "lucide-react";

const DIET_OPTIONS = ["Omnivore", "Vegetarian", "Vegan", "Keto", "Gluten-Free"];
const ALLERGY_OPTIONS = ["Peanuts", "Milk", "Eggs", "Soy", "Nuts", "Shellfish"];
const CUISINE_OPTIONS = ["Indian", "Italian", "Mexican", "Asian", "Mediterranean", "American"];
const SPICE_OPTIONS = ["Mild", "Medium", "Spicy", "Extra Hot"];

export default function PreferencesPage() {
  const [diet, setDiet] = useState<string>("Omnivore");
  const [allergies, setAllergies] = useState<string[]>([]);
  const [disliked, setDisliked] = useState<string>("");
  const [preferredCuisines, setPreferredCuisines] = useState<string[]>([]);
  const [calorieLimit, setCalorieLimit] = useState<number>(2000);
  const [spiceLevel, setSpiceLevel] = useState<string>("Medium");

  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);

  useEffect(() => {
    async function fetchPreferences() {
      try {
        const res = await api.get("/preferences/");
        if (res.data) {
          if (res.data.diet) setDiet(res.data.diet);
          if (res.data.allergies) setAllergies(res.data.allergies.split(",").filter(Boolean));
          if (res.data.disliked_ingredients) setDisliked(res.data.disliked_ingredients);
          if (res.data.preferred_cuisines) setPreferredCuisines(res.data.preferred_cuisines.split(",").filter(Boolean));
          if (res.data.calorie_limit) setCalorieLimit(res.data.calorie_limit);
          if (res.data.spice_level) setSpiceLevel(res.data.spice_level);
        }
      } catch (err) {
        console.error("Failed to load preferences", err);
      } finally {
        setLoading(false);
      }
    }
    fetchPreferences();
  }, []);

  const toggleArrayItem = (item: string, current: string[], setter: (val: string[]) => void) => {
    if (current.includes(item)) {
      setter(current.filter((i) => i !== item));
    } else {
      setter([...current, item]);
    }
  };

  const handleSave = async (e: React.FormEvent) => {
    e.preventDefault();
    setSaving(true);
    try {
      await api.post("/preferences/", {
        diet,
        allergies: allergies.join(","),
        disliked_ingredients: disliked,
        preferred_cuisines: preferredCuisines.join(","),
        calorie_limit: calorieLimit,
        spice_level: spiceLevel,
      });
      toast.success("Preferences updated successfully! 🎉");
    } catch (err) {
      toast.error("Failed to save preferences.");
    } finally {
      setSaving(false);
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-50">
        <div className="animate-spin rounded-full h-10 w-10 border-4 border-green-600 border-t-transparent"></div>
      </div>
    );
  }

  return (
    <ProtectedRoute>
      <div className="min-h-screen bg-gray-50 py-10 px-4 sm:px-6 lg:px-8">
        <div className="max-w-3xl mx-auto bg-white rounded-3xl shadow-sm border border-gray-100 p-8">
          
          <div className="flex items-center gap-3 mb-6 pb-6 border-b border-gray-100">
            <div className="p-3 bg-green-50 text-green-700 rounded-2xl">
              <Sliders size={28} />
            </div>
            <div>
              <h1 className="text-3xl font-extrabold text-gray-900">Dietary Preferences</h1>
              <p className="text-gray-500 text-sm">Personalize AI recipe recommendations and nutritional targets.</p>
            </div>
          </div>

          <form onSubmit={handleSave} className="space-y-8">
            
            {/* 1️⃣ DIET TYPE */}
            <div>
              <label className="block text-sm font-bold text-gray-800 mb-3 flex items-center gap-2">
                <Utensils size={18} className="text-green-600" /> Dietary Pattern
              </label>
              <div className="flex flex-wrap gap-2">
                {DIET_OPTIONS.map((option) => (
                  <button
                    key={option}
                    type="button"
                    onClick={() => setDiet(option)}
                    className={`px-4 py-2 rounded-full text-sm font-semibold transition border ${
                      diet === option
                        ? "bg-green-600 text-white border-green-600 shadow-sm"
                        : "bg-gray-50 text-gray-700 border-gray-200 hover:bg-gray-100"
                    }`}
                  >
                    {option}
                  </button>
                ))}
              </div>
            </div>

            {/* 2️⃣ ALLERGIES & RESTRICTIONS */}
            <div>
              <label className="block text-sm font-bold text-gray-800 mb-3 flex items-center gap-2">
                <ShieldAlert size={18} className="text-red-500" /> Allergies & Intolerances
              </label>
              <div className="flex flex-wrap gap-2 mb-3">
                {ALLERGY_OPTIONS.map((item) => {
                  const active = allergies.includes(item);
                  return (
                    <button
                      key={item}
                      type="button"
                      onClick={() => toggleArrayItem(item, allergies, setAllergies)}
                      className={`px-4 py-2 rounded-full text-sm font-semibold transition border flex items-center gap-1.5 ${
                        active
                          ? "bg-red-50 text-red-700 border-red-200"
                          : "bg-gray-50 text-gray-600 border-gray-200 hover:bg-gray-100"
                      }`}
                    >
                      {active && <Check size={14} />} {item}
                    </button>
                  );
                })}
              </div>
            </div>

            {/* 3️⃣ PREFERRED CUISINES */}
            <div>
              <label className="block text-sm font-bold text-gray-800 mb-3">
                Favorite Cuisines
              </label>
              <div className="flex flex-wrap gap-2">
                {CUISINE_OPTIONS.map((cuisine) => {
                  const active = preferredCuisines.includes(cuisine);
                  return (
                    <button
                      key={cuisine}
                      type="button"
                      onClick={() => toggleArrayItem(cuisine, preferredCuisines, setPreferredCuisines)}
                      className={`px-4 py-2 rounded-full text-sm font-semibold transition border flex items-center gap-1.5 ${
                        active
                          ? "bg-emerald-600 text-white border-emerald-600 shadow-sm"
                          : "bg-gray-50 text-gray-600 border-gray-200 hover:bg-gray-100"
                      }`}
                    >
                      {active && <Check size={14} />} {cuisine}
                    </button>
                  );
                })}
              </div>
            </div>

            {/* 4️⃣ CALORIE LIMIT & SPICE */}
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-6 pt-4 border-t border-gray-100">
              <div>
                <label className="block text-sm font-bold text-gray-800 mb-2">
                  Daily Calorie Target: <span className="text-green-600 font-extrabold">{calorieLimit} kcal</span>
                </label>
                <input
                  type="range"
                  min={1200}
                  max={3500}
                  step={50}
                  value={calorieLimit}
                  onChange={(e) => setCalorieLimit(Number(e.target.value))}
                  className="w-full accent-green-600 cursor-pointer"
                />
                <div className="flex justify-between text-xs text-gray-400 mt-1">
                  <span>1200 kcal</span>
                  <span>3500 kcal</span>
                </div>
              </div>

              <div>
                <label className="block text-sm font-bold text-gray-800 mb-2 flex items-center gap-1.5">
                  <Flame size={16} className="text-orange-500" /> Spice Level
                </label>
                <select
                  value={spiceLevel}
                  onChange={(e) => setSpiceLevel(e.target.value)}
                  className="w-full bg-gray-50 border border-gray-200 rounded-xl px-3 py-2 text-sm font-medium focus:ring-2 focus:ring-green-500 outline-none"
                >
                  {SPICE_OPTIONS.map((spice) => (
                    <option key={spice} value={spice}>
                      {spice}
                    </option>
                  ))}
                </select>
              </div>
            </div>

            {/* 5️⃣ DISLIKED INGREDIENTS */}
            <div>
              <label className="block text-sm font-bold text-gray-800 mb-2">
                Disliked Ingredients (Comma Separated)
              </label>
              <input
                type="text"
                value={disliked}
                onChange={(e) => setDisliked(e.target.value)}
                placeholder="e.g. mushrooms, cilantro, eggplant"
                className="w-full bg-gray-50 border border-gray-200 rounded-xl px-4 py-2.5 text-sm focus:ring-2 focus:ring-green-500 outline-none"
              />
            </div>

            {/* SAVE BUTTON */}
            <div className="pt-4 border-t border-gray-100 flex justify-end">
              <button
                type="submit"
                disabled={saving}
                className="px-8 py-3 bg-green-600 text-white rounded-full font-bold shadow-md hover:bg-green-700 transition flex items-center gap-2 disabled:opacity-50"
              >
                <Save size={18} /> {saving ? "Saving..." : "Save Preferences"}
              </button>
            </div>

          </form>
        </div>
      </div>
    </ProtectedRoute>
  );
}
