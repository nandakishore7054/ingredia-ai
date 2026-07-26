"use client";

import React, { createContext, useContext, useState } from "react";

export type Recipe = {
  id: number;
  name: string;
  cuisine?: string;
  diet?: string;
  cooking_time?: number;
  prep_time?: number;
  total_time?: number;
  servings?: number;
  difficulty?: string;
  calories?: number;
  protein?: number;
  carbs?: number;
  fats?: number;
  instructions?: string;
  ingredients?: string[];
  is_favorite?: boolean;
};

type AppContextType = {
  ingredients: string[];
  setIngredients: (v: string[]) => void;

  recipes: Recipe[];
  setRecipes: (v: Recipe[]) => void;

  loading: boolean;
  setLoading: (v: boolean) => void;

  error: string | null;
  setError: (v: string | null) => void;
};

const AppContext = createContext<AppContextType | null>(null);

export function AppProvider({ children }: { children: React.ReactNode }) {
  const [ingredients, setIngredients] = useState<string[]>([]);
  const [recipes, setRecipes] = useState<Recipe[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  return (
    <AppContext.Provider
      value={{
        ingredients,
        setIngredients,
        recipes,
        setRecipes,
        loading,
        setLoading,
        error,
        setError,
      }}
    >
      {children}
    </AppContext.Provider>
  );
}

export function useAppContext() {
  const ctx = useContext(AppContext);
  if (!ctx) throw new Error("useAppContext must be used inside AppProvider");
  return ctx;
}
