"use client";

import { useState, useRef, useEffect } from "react";
import { api, matchRecipes } from "@/services/api";
import { useAppContext } from "@/context/AppContext";
import RecipeGrid from "@/components/RecipeGrid";
import toast from "react-hot-toast";
import { Camera, Upload, Scan, X, Plus, ChefHat, Keyboard } from "lucide-react";

type Detection = {
  ingredient: string;
  confidence: number;
  bbox: { x: number; y: number; width: number; height: number };
};

const normalizeRecipes = (list: any[]) =>
  list.map((r: any, index: number) => ({
    id: r.id ?? index,
    name: r.name ?? "Unnamed Recipe",
    cuisine: r.cuisine ?? "Unknown",
    diet: r.diet ?? "Unknown",
    cooking_time: r.cooking_time ?? 30,
    is_favorite: r.is_favorite ?? false,
    instructions: r.instructions ?? null,
    calories: r.calories ?? null,
    protein: r.protein ?? null,
    carbs: r.carbs ?? null,
    fats: r.fats ?? null,
  }));

/** Returns a Tailwind color class based on the confidence score */
function confidenceColor(conf: number) {
  if (conf >= 0.8) return "bg-green-100 text-green-700 border-green-200";
  if (conf >= 0.5) return "bg-yellow-100 text-yellow-700 border-yellow-200";
  return "bg-red-100 text-red-700 border-red-200";
}

export default function UploadPage() {
  const [file, setFile] = useState<File | null>(null);
  const [preview, setPreview] = useState<string | null>(null);
  const [manualInput, setManualInput] = useState("");
  const [inputError, setInputError] = useState("");
  const [manualMode, setManualMode] = useState(false);
  const [mounted, setMounted] = useState(false);
  const [detections, setDetections] = useState<Detection[]>([]);
  const [detecting, setDetecting] = useState(false);

  const {
    ingredients,
    setIngredients,
    recipes,
    setRecipes,
    loading,
    setLoading,
    setError,
  } = useAppContext();

  const videoRef = useRef<HTMLVideoElement>(null);
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);

  useEffect(() => setMounted(true), []);
  if (!mounted) return null;

  /* ---------------- CAMERA ---------------- */
  const openCamera = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({
        video: { facingMode: "environment" },
      });
      if (videoRef.current) {
        videoRef.current.srcObject = stream;
        videoRef.current.play();
      }
    } catch {
      toast.error("Camera permission denied");
    }
  };

  const capturePhoto = () => {
    const video = videoRef.current;
    const canvas = canvasRef.current;
    if (!video || !canvas) return;

    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    const ctx = canvas.getContext("2d");
    if (!ctx) return;

    ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
    canvas.toBlob((blob) => {
      if (!blob) return;
      const imageFile = new File([blob], "camera.jpg", { type: "image/jpeg" });
      setFile(imageFile);
      setPreview(URL.createObjectURL(blob));
      setDetections([]);
      setRecipes([]);
    }, "image/jpeg");
  };

  /* ---------------- FILE UPLOAD ---------------- */
  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const selected = e.target.files?.[0];
    if (!selected) return;
    setFile(selected);
    setPreview(URL.createObjectURL(selected));
    setIngredients([]);
    setDetections([]);
    setRecipes([]);
  };

  /* ----- STEP 1: DETECT (returns detections only, NO recipes yet) ----- */
  const detectIngredients = async () => {
    if (!file) return toast.error("No image selected");

    setDetecting(true);
    setError(null);
    setIngredients([]);
    setDetections([]);
    setRecipes([]);

    try {
      const formData = new FormData();
      formData.append("file", file);
      const { data } = await api.post("/analyze", formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });

      const dets: Detection[] = data.detections || [];
      setDetections(dets);
      setIngredients(data.detected_ingredients || []);

      if (dets.length === 0) {
        toast.error("No ingredients detected. Try adding manually.");
      } else {
        toast.success(`Detected ${dets.length} item(s)! Review below.`);
      }
    } catch {
      setError("Failed to analyze image");
      toast.error("Detection failed. Please try again.");
    } finally {
      setDetecting(false);
    }
  };

  /* ----- STEP 2: USER EDITS INGREDIENTS ----- */
  const removeIngredient = (ing: string) => {
    setIngredients(ingredients.filter((i) => i !== ing));
    setDetections(detections.filter((d) => d.ingredient !== ing));
  };

  const addIngredient = () => {
    const value = manualInput.trim().toLowerCase();
    
    if (!value) {
      setInputError("Please enter an ingredient.");
      return;
    }
    
    if (ingredients.includes(value)) {
      setInputError(`"${value}" is already in your list.`);
      return;
    }

    setIngredients([...ingredients, value]);
    setDetections([...detections, { ingredient: value, confidence: 1.0, bbox: { x: 0, y: 0, width: 0, height: 0 } }]);
    setManualInput("");
    setInputError("");
  };

  /* ----- STEP 3: GENERATE RECIPES (explicit user action) ----- */
  const generateRecipes = async () => {
    if (!ingredients.length) return;

    setLoading(true);
    setError(null);
    setRecipes([]);

    try {
      const response = await matchRecipes(ingredients);
      const recipesArray = Array.isArray(response) ? response : response.matches || [];
      setRecipes(normalizeRecipes(recipesArray));
      toast.success("Recipes generated!");
    } catch {
      setError("Failed to fetch recipes");
      toast.error("Recipe generation failed.");
    } finally {
      setLoading(false);
    }
  };

  /* ---------------- UI ---------------- */
  return (
    <div className="min-h-screen max-w-5xl mx-auto p-6">

      {/* HEADER */}
      <div className="text-center mb-10">
        <h1 className="text-4xl font-extrabold text-gray-900 mb-2">
          Ingredient Detection
        </h1>
        <p className="text-gray-500">Upload a photo of your ingredients and let AI identify them.</p>
      </div>

      {/* CAMERA + UPLOAD SECTION */}
      <div className="bg-white rounded-2xl shadow-sm border border-gray-100 p-8 flex flex-col items-center">
        <video ref={videoRef} className="w-80 rounded-xl border border-gray-200 mb-4" playsInline />
        <canvas ref={canvasRef} className="hidden" />

        <div className="flex gap-3 mb-6 flex-wrap justify-center">
          <button onClick={openCamera} className="flex items-center gap-2 px-5 py-2.5 bg-blue-600 text-white rounded-full font-medium hover:bg-blue-700 transition shadow-sm">
            <Camera size={18} /> Open Camera
          </button>
          <button onClick={capturePhoto} className="flex items-center gap-2 px-5 py-2.5 bg-purple-600 text-white rounded-full font-medium hover:bg-purple-700 transition shadow-sm">
            <Scan size={18} /> Capture
          </button>
          <button onClick={() => fileInputRef.current?.click()} className="flex items-center gap-2 px-5 py-2.5 bg-green-600 text-white rounded-full font-medium hover:bg-green-700 transition shadow-sm">
            <Upload size={18} /> Upload Image
          </button>
          <button onClick={() => setManualMode(true)} className="flex items-center gap-2 px-5 py-2.5 bg-orange-600 text-white rounded-full font-medium hover:bg-orange-700 transition shadow-sm">
            <Keyboard size={18} /> Type Manually
          </button>
        </div>

        <input ref={fileInputRef} type="file" accept="image/*" className="hidden" onChange={handleFileChange} />

        {preview && (
          <div className="flex flex-col items-center">
            <img src={preview} alt="Preview" className="w-72 rounded-2xl border border-gray-200 shadow-sm" />
            <button
              onClick={detectIngredients}
              disabled={detecting}
              className="mt-5 px-8 py-3 bg-black text-white rounded-full font-semibold text-lg hover:bg-gray-800 transition shadow-lg disabled:opacity-60 flex items-center gap-2"
            >
              {detecting ? (
                <>
                  <div className="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin" />
                  Analyzing...
                </>
              ) : (
                <><Scan size={20} /> Detect Ingredients</>
              )}
            </button>
          </div>
        )}
      </div>

      {/* DETECTION RESULTS — STEP 2: Review & Edit */}
      {(detections.length > 0 || ingredients.length > 0 || manualMode) && (
        <div className="mt-8 bg-white rounded-2xl shadow-sm border border-gray-100 p-8">
          <h2 className="text-xl font-bold text-gray-900 mb-1">Review Detected Ingredients</h2>
          <p className="text-sm text-gray-500 mb-5">Remove incorrect items or add missing ones before generating recipes.</p>

          {/* CONFIDENCE BADGES */}
          <div className="flex flex-wrap gap-3 mb-6">
            {detections.map((det, i) => (
              <div
                key={`${det.ingredient}-${i}`}
                className={`flex items-center gap-2 px-4 py-2 rounded-full border text-sm font-medium ${confidenceColor(det.confidence)}`}
              >
                <span className="capitalize">{det.ingredient}</span>
                <span className="text-xs opacity-75">{Math.round(det.confidence * 100)}%</span>
                <button
                  onClick={() => removeIngredient(det.ingredient)}
                  className="ml-1 opacity-50 hover:opacity-100 transition"
                >
                  <X size={14} />
                </button>
              </div>
            ))}
          </div>

          {/* MANUAL ADD */}
          <div className="mb-6">
            <div className="flex gap-2">
              <input
                value={manualInput}
                onChange={(e) => {
                  setManualInput(e.target.value);
                  if (inputError) setInputError("");
                }}
                onKeyDown={(e) => {
                  if (e.key === "Enter") {
                    e.preventDefault();
                    addIngredient();
                  }
                }}
                placeholder="Add missing ingredient..."
                className={`flex-1 border rounded-full px-4 py-2.5 text-sm outline-none transition ${inputError ? "border-red-400 focus:border-red-500" : "border-gray-200 focus:border-green-500"}`}
              />
              <button onClick={addIngredient} className="bg-green-600 text-white px-5 py-2.5 rounded-full font-medium hover:bg-green-700 transition flex items-center gap-1">
                <Plus size={16} /> Add
              </button>
            </div>
            {inputError && <p className="text-red-500 text-sm mt-2 ml-4">{inputError}</p>}
          </div>

          {/* STEP 3: GENERATE */}
          {ingredients.length > 0 && (
            <button
              onClick={generateRecipes}
              disabled={loading}
              className="w-full py-3.5 bg-black text-white rounded-full font-semibold text-lg hover:bg-gray-800 transition shadow-lg disabled:opacity-60 flex items-center justify-center gap-2"
            >
              {loading ? (
                <>
                  <div className="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin" />
                  Generating...
                </>
              ) : (
                <><ChefHat size={22} /> Generate Recipes from {ingredients.length} Ingredient{ingredients.length > 1 ? "s" : ""}</>
              )}
            </button>
          )}
        </div>
      )}

      {/* CONFIDENCE LEGEND */}
      {detections.length > 0 && (
        <div className="mt-4 flex items-center gap-4 text-xs text-gray-500 justify-center">
          <span className="flex items-center gap-1"><span className="w-3 h-3 rounded-full bg-green-500 inline-block" /> High (≥80%)</span>
          <span className="flex items-center gap-1"><span className="w-3 h-3 rounded-full bg-yellow-500 inline-block" /> Medium (50-79%)</span>
          <span className="flex items-center gap-1"><span className="w-3 h-3 rounded-full bg-red-500 inline-block" /> Low (&lt;50%)</span>
        </div>
      )}

      {/* RECIPE RESULTS */}
      <div className="mt-8">
        <RecipeGrid recipes={recipes} loading={loading} />
      </div>
    </div>
  );
}
