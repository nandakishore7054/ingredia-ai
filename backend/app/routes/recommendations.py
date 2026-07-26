from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import SessionLocal
from app.db.models import Recipe, Ingredient, RecipeIngredient, User, UserPreference
from app.services.recipe_service import ensure_recipe_nutrition
from app.utils.auth_dependency import get_current_user

router = APIRouter(
    prefix="/recommendations",
    tags=["Recommendations"]
)


@router.get("/personalized")
def personalized_recommendations(
    current_user: User = Depends(get_current_user)
):
    db: Session = SessionLocal()

    # 1️⃣ Fetch user preferences
    prefs = db.query(UserPreference).filter(
        UserPreference.user_id == current_user.id
    ).first()

    allergies = set(filter(None, (prefs.allergies.lower() if prefs and prefs.allergies else "").split(",")))
    dislikes = set(filter(None, (prefs.disliked_ingredients.lower() if prefs and prefs.disliked_ingredients else "").split(",")))
    preferred_cuisines = set(filter(None, (prefs.preferred_cuisines.lower() if prefs and prefs.preferred_cuisines else "").split(",")))
    target_diet = (prefs.diet.lower() if prefs and prefs.diet else None)
    calorie_limit = prefs.calorie_limit if prefs and prefs.calorie_limit else 2500

    # 2️⃣ Fetch all recipes & score them
    all_recipes = db.query(Recipe).all()
    scored_recipes = []

    for r in all_recipes:
        score = 80 # base score

        # Diet matching
        if target_diet and target_diet != "omnivore":
            if r.diet and r.diet.lower() == target_diet:
                score += 15
            else:
                score -= 30

        # Calorie target
        if r.calories:
            if r.calories <= calorie_limit:
                score += 10
            else:
                score -= 15

        # Preferred cuisine match
        if preferred_cuisines and r.cuisine:
            if any(c.strip().lower() in r.cuisine.lower() for c in preferred_cuisines):
                score += 15

        # Ingredient checks (allergies & dislikes)
        ingredients = (
            db.query(Ingredient.name)
            .join(RecipeIngredient)
            .filter(RecipeIngredient.recipe_id == r.id)
            .all()
        )
        ing_names = {i[0].lower() for i in ingredients}

        if ing_names & allergies:
            continue # Strict exclude

        if ing_names & dislikes:
            score -= 20

        match_pct = max(50, min(99, score))

        ensure_recipe_nutrition(r, db=db, ingredients_list=list(ing_names))
        
        scored_recipes.append({
            "id": r.id,
            "name": r.name,
            "cuisine": r.cuisine,
            "diet": r.diet,
            "cooking_time": r.cooking_time,
            "prep_time": r.prep_time,
            "total_time": r.total_time,
            "servings": r.servings,
            "difficulty": r.difficulty,
            "calories": r.calories,
            "protein": r.protein,
            "carbs": r.carbs,
            "fats": r.fats,
            "instructions": r.instructions,
            "match_percentage": match_pct,
            "ingredients": list(ing_names)
        })

    db.close()

    scored_recipes.sort(key=lambda x: x["match_percentage"], reverse=True)

    return {
        "user": current_user.email,
        "recommended_count": len(scored_recipes),
        "recipes": scored_recipes[:8]
    }
