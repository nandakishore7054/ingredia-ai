"use client";

import RecipeCard from "./RecipeCard";

export default function RecipeGrid({
  recipes,
  loading,
}: {
  recipes: any;
  loading: boolean;
}) {
  if (loading) {
    return <p className="text-center mt-6">Loading recipes...</p>;
  }

  if (!Array.isArray(recipes) || recipes.length === 0) {
    return (
      <p className="text-center mt-6 text-gray-500">
        No recipes found 🍽️
      </p>
    );
  }

  return (
    <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6 mt-6">
      {recipes.map((recipe: any) => (
        <RecipeCard key={recipe.id || recipe.name} recipe={recipe} />
      ))}
    </div>
  );
}
