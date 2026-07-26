import axios from "axios";

export const api = axios.create({
  baseURL: process.env.NEXT_PUBLIC_API_URL || "https://ingredia-ai.onrender.com",
});

/* 🔐 Attach JWT automatically */
api.interceptors.request.use((config) => {
  const token = localStorage.getItem("token");
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

/* 🚨 Handle 401 Unauthorized globally (Expired/Invalid JWT) */
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response && error.response.status === 401) {
      if (typeof window !== "undefined") {
        localStorage.removeItem("token");
        localStorage.removeItem("user");
        window.location.href = "/login";
      }
    }
    return Promise.reject(error);
  }
);

/* =========================
   IMAGE ANALYSIS
========================= */
export async function analyzeImage(file: File) {
  const formData = new FormData();
  formData.append("file", file);

  const response = await api.post("/analyze-and-match", formData, {
    headers: {
      "Content-Type": "multipart/form-data",
    },
  });

  return response.data;
}

/* =========================
   SEARCH RECIPES
========================= */
export async function searchRecipes(filters: any) {
  const response = await api.post("/search-recipes", filters);
  return response.data;
}

/* =========================
   GENERATE INSTRUCTIONS
========================= */
export async function generateInstructions(data: {
  recipe_name: string;
  ingredients: string[];
  cuisine?: string;
}) {
  const response = await api.post("/generate-instructions", data);
  return response.data;
}

/* =========================
   AUTH / RECOMMENDATIONS
========================= */
export async function getPersonalizedRecipes(token: string) {
  const response = await api.get("/recommendations/personalized", {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  });

  return response.data.recipes;
}

/* =========================
   🕒 COOKING HISTORY
========================= */
export async function addToHistory(recipeId: number, token: string) {
  const response = await api.post(
    `/history/${recipeId}`,
    {},
    {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    }
  );

  return response.data;
}

export async function getHistory(token: string) {
  const response = await api.get("/history/", {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  });

  return response.data;
}

/* =========================
   ✅ MATCH RECIPES (FIXED)
========================= */
export async function matchRecipes(ingredients: string[]) {
  const response = await api.post("/match-recipes", ingredients);
  return response.data; // ✅ FIX HERE
}

/* =========================
   ❤️ FAVORITES
========================= */
export async function addFavorite(recipeId: number) {
  const res = await api.post(`/favorites/${recipeId}`);
  return res.data;
}

export async function removeFavorite(recipeId: number) {
  const res = await api.delete(`/favorites/${recipeId}`);
  return res.data;
}

export async function getFavorites() {
  const res = await api.get("/favorites/");
  return res.data;
}
