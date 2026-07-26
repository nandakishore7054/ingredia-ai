from dotenv import load_dotenv
load_dotenv()  # Load .env before any service reads os.getenv()

from fastapi import FastAPI, UploadFile, File, Depends
from fastapi.middleware.cors import CORSMiddleware
import shutil
import os
from typing import List, Dict

from app.services.roboflow_service import roboflow_service
from app.services.matching_service import find_matching_recipes
from app.services.recommendation_service import recommend_recipes_ml
from app.services.search_service import search_recipes
from app.services.instruction_service import generate_instructions

from app.routes import auth, favorites, preferences, history, recommendations
from app.utils.auth_dependency import get_current_user

app = FastAPI(title="Intelligent Recipe Generator")

# Initialize database tables
from app.db.database import engine, Base
from app.db.seed_data import seed

Base.metadata.create_all(bind=engine)
seed() # Ensures initial recipes exist on Render

# -------------------- CORS --------------------
# CORSMiddleware should be added before routes to ensure preflight requests are handled correctly
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:3001",
        "https://ingredia-ai-steel.vercel.app",
    ],
    allow_origin_regex=r"https://.*\.vercel\.app", # Allow all Vercel preview deployments
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------------------- ROUTERS --------------------
app.include_router(auth.router)
app.include_router(favorites.router)
app.include_router(preferences.router)
app.include_router(history.router)
app.include_router(recommendations.router)

from app.routes import ai, recipes
app.include_router(ai.router)
app.include_router(recipes.router)

UPLOAD_DIR = "temp_uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# -------------------- PUBLIC ENDPOINTS --------------------

@app.post("/analyze")
async def analyze_image(file: UploadFile = File(...)):
    """
    Detect ingredients using Roboflow Hosted Inference.
    Returns structured results with confidence scores and bounding boxes.
    """
    image_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(image_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    detections = await roboflow_service.detect(image_path)

    # Extract unique ingredient names for backward compatibility
    ingredient_names = list(set(d["ingredient"] for d in detections))

    return {
        "detected_ingredients": ingredient_names,
        "detections": detections,  # Rich data: ingredient, confidence, bbox
    }


@app.post("/match-recipes")
async def match_recipes(ingredients: List[str]):
    return await find_matching_recipes(ingredients)


@app.post("/analyze-and-match")
async def analyze_and_match(file: UploadFile = File(...)):
    """
    Full pipeline: Detect ingredients via Roboflow, then run hybrid matching.
    Returns both rich detection data and recipe matches.
    """
    image_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(image_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    detections = await roboflow_service.detect(image_path)
    ingredient_names = list(set(d["ingredient"] for d in detections))

    if not ingredient_names:
        return {"detected_ingredients": [], "detections": [], "matches": []}

    matches = await find_matching_recipes(ingredient_names)
    return {
        "detected_ingredients": ingredient_names,
        "detections": detections,
        "matches": matches,
    }


# -------------------- PROTECTED --------------------

@app.post("/recommend-ml")
async def recommend_ml(
    ingredients: List[str],
    current_user=Depends(get_current_user)
):
    return recommend_recipes_ml(ingredients)


@app.post("/search-recipes")
async def search_and_filter(filters: Dict = {}):
    return search_recipes(**filters)


@app.post("/generate-instructions")
async def generate_recipe_instructions(
    data: Dict,
    current_user=Depends(get_current_user)
):
    ai_data = generate_instructions(
        recipe_name=data.get("recipe_name"),
        ingredients=data.get("ingredients", []),
        cuisine=data.get("cuisine", "")
    )
    return ai_data


@app.get("/")
def root():
    return {"status": "API running successfully"}

