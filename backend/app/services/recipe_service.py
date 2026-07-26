from app.db.database import SessionLocal
from app.db.models import Recipe, Ingredient, RecipeIngredient
from app.services.instruction_service import generate_instructions, generate_nutrition

def ensure_recipe_nutrition(recipe: Recipe, db=None, ingredients_list=None):
    """
    Ensures a recipe has valid nutrition data cached in SQLite.
    If calories/protein/carbs/fats are NULL or 0:
      - Calls AI generate_nutrition()
      - Saves generated values to SQLite DB
      - Commits once
    Returns updated recipe.
    """
    if recipe.calories and recipe.calories > 0:
        return recipe

    if ingredients_list is None:
        if db:
            ingredient_rows = db.query(Ingredient.name).join(
                RecipeIngredient, Ingredient.id == RecipeIngredient.ingredient_id
            ).filter(
                RecipeIngredient.recipe_id == recipe.id
            ).all()
            ingredients_list = [row[0] for row in ingredient_rows]
        else:
            ingredients_list = []

    try:
        nutrition_data = generate_nutrition(recipe.name, ingredients_list)
        if nutrition_data and nutrition_data.get("calories"):
            recipe.calories = nutrition_data["calories"]
            recipe.protein = nutrition_data["protein"]
            recipe.carbs = nutrition_data["carbs"]
            recipe.fats = nutrition_data["fats"]
            if db:
                db.commit()
                db.refresh(recipe)
    except Exception as e:
        print(f"Error ensuring nutrition for '{recipe.name}': {e}")
        if db:
            db.rollback()

    return recipe

def get_recipe_by_name(name: str):
    db = SessionLocal()
    clean_name = name.strip()

    recipe = db.query(Recipe).filter(
        Recipe.name.ilike(clean_name)
    ).first()

    # Fallback to partial match if exact case-insensitive match is not found
    if not recipe:
        recipe = db.query(Recipe).filter(
            Recipe.name.ilike(f"%{clean_name}%")
        ).first()

    if not recipe:
        db.close()
        return None

    # Fetch ingredients
    ingredient_rows = db.query(Ingredient.name).join(
        RecipeIngredient, Ingredient.id == RecipeIngredient.ingredient_id
    ).filter(
        RecipeIngredient.recipe_id == recipe.id
    ).all()
    ingredients_list = [row[0] for row in ingredient_rows]

    db_updated = False

    # 1️⃣ GENERATE INSTRUCTIONS IF MISSING
    if not recipe.instructions:
        try:
            ai_data = generate_instructions(
                recipe_name=recipe.name,
                ingredients=ingredients_list,
                cuisine=recipe.cuisine or "",
            )
            recipe.instructions = ai_data.get("instructions")
            recipe.prep_time = recipe.prep_time or ai_data.get("prep_time")
            recipe.cooking_time = recipe.cooking_time or ai_data.get("cooking_time")
            recipe.total_time = recipe.total_time or ai_data.get("total_time")
            recipe.servings = recipe.servings or ai_data.get("servings")
            recipe.difficulty = recipe.difficulty or ai_data.get("difficulty")
            recipe.meal_type = recipe.meal_type or ai_data.get("meal_type")
            db_updated = True
        except Exception as e:
            print(f"Error updating instructions for '{recipe.name}': {e}")

    # 2️⃣ ENSURE NUTRITION EXISTS
    if not recipe.calories or recipe.calories == 0:
        ensure_recipe_nutrition(recipe, db=db, ingredients_list=ingredients_list)
    elif db_updated:
        try:
            db.commit()
            db.refresh(recipe)
        except Exception as e:
            db.rollback()

    result = {
        "id": recipe.id,
        "name": recipe.name,
        "cuisine": recipe.cuisine or "General",
        "diet": recipe.diet or "Omnivore",
        "cooking_time": recipe.cooking_time or 20,
        "prep_time": recipe.prep_time or 10,
        "total_time": recipe.total_time or ((recipe.cooking_time or 20) + (recipe.prep_time or 10)),
        "servings": recipe.servings or 4,
        "difficulty": recipe.difficulty or "Easy",
        "meal_type": recipe.meal_type or "Dinner",
        "calories": recipe.calories,
        "protein": recipe.protein,
        "carbs": recipe.carbs,
        "fats": recipe.fats,
        "instructions": recipe.instructions or f"1. Prepare fresh ingredients for {recipe.name}.\n2. Cook over medium flame until tender.\n3. Season and serve hot.",
        "ingredients": ingredients_list
    }

    db.close()
    return result
