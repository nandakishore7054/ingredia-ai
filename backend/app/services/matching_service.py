from app.db.database import SessionLocal
from app.db.models import Recipe, Ingredient, RecipeIngredient
from app.services.llm_service import llm_service
from collections import defaultdict
import logging

logger = logging.getLogger(__name__)

async def find_matching_recipes(detected_ingredients: list, limit: int = 10):
    db = SessionLocal()
    detected_set = set(i.lower().strip() for i in detected_ingredients if i)

    results = []

    try:
        # OPTIMIZATION: Single JOIN query to fetch all recipes and their linked ingredient names.
        # Eliminates N+1 query bottleneck (previously fired 2 queries per recipe inside a loop).
        rows = db.query(Recipe, Ingredient.name)\
            .join(RecipeIngredient, Recipe.id == RecipeIngredient.recipe_id)\
            .join(Ingredient, Ingredient.id == RecipeIngredient.ingredient_id)\
            .all()

        # Group ingredients by recipe
        recipe_ingredients_map = defaultdict(lambda: {"recipe": None, "ingredients": set()})
        for recipe, ingredient_name in rows:
            recipe_ingredients_map[recipe.id]["recipe"] = recipe
            recipe_ingredients_map[recipe.id]["ingredients"].add(ingredient_name.lower().strip())

        for entry in recipe_ingredients_map.values():
            recipe = entry["recipe"]
            recipe_ingredients = entry["ingredients"]

            if not recipe_ingredients:
                continue

            matched = recipe_ingredients & detected_set
            if not matched:
                continue

            match_percentage = int((len(matched) / len(recipe_ingredients)) * 100)

            results.append({
                "id": recipe.id,
                "name": recipe.name,
                "cuisine": recipe.cuisine,
                "diet": recipe.diet,
                "cooking_time": recipe.cooking_time,
                "instructions": recipe.instructions,
                "calories": recipe.calories,
                "protein": recipe.protein,
                "carbs": recipe.carbs,
                "fats": recipe.fats,
                "match_percentage": match_percentage,
                "matched_ingredients": list(matched),
            })

    except Exception as e:
        logger.error(f"Error executing recipe matching query: {e}")
    finally:
        db.close()

    results.sort(key=lambda x: x["match_percentage"], reverse=True)
    db_results = results[:limit]

    # --- HYBRID AI LOGIC ---
    # If the database returns fewer than 3 good matches, supplement with AI
    if len(db_results) < 3 and detected_ingredients:
        logger.info(f"Database only found {len(db_results)} matches. Falling back to AI for dynamic generation.")
        try:
            ai_recipes = await llm_service.generate_dynamic_recipe(detected_ingredients)
            # Combine, re-sort by match percentage, and enforce limit
            db_results.extend(ai_recipes)
            db_results.sort(key=lambda x: x.get("match_percentage", 0), reverse=True)
            db_results = db_results[:limit]
        except Exception as e:
            logger.error(f"Failed to fetch AI supplemental recipes: {e}")

    return db_results

