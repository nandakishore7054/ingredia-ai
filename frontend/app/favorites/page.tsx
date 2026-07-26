"use client";

import { useAppContext } from "@/context/AppContext";
import RecipeGrid from "@/components/RecipeGrid";
import ProtectedRoute from "@/components/ProtectedRoute";

export default function FavoritesPage() {
  const { recipes, loading } = useAppContext();

  const favorites = recipes.filter((r) => r.is_favorite);

  return (
    <ProtectedRoute>
      <div className="max-w-6xl mx-auto p-6">
        <h1 className="text-3xl font-bold mb-6 text-center">
          Your Favorites ❤️
        </h1>

        <RecipeGrid recipes={favorites} loading={loading} />
      </div>
    </ProtectedRoute>
  );
}
