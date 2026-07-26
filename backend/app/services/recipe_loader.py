import requests
from app.db.database import SessionLocal
from app.db.models import Recipe, Ingredient, RecipeIngredient

API_URL = "https://www.themealdb.com/api/json/v1/1/search.php?s="

NON_VEG_KEYWORDS = {
    "chicken", "beef", "pork", "fish",
    "mutton", "lamb", "seafood", "shrimp"
}

def clean_text(text):
    return text.lower().strip()

def detect_diet(ingredient_names):
    for ing in ingredient_names:
        for nonveg in NON_VEG_KEYWORDS:
            if nonveg in ing:
                return "non-vegetarian"
    return "vegetarian"

def save_recipes_to_db():
    db = SessionLocal()

    response = requests.get(API_URL)
    data = response.json()

    if not data.get("meals"):
        return

    for meal in data["meals"]:
        ingredient_names = set()

        for i in range(1, 21):
            ing = meal.get(f"strIngredient{i}")
            if ing and ing.strip():
                ingredient_names.add(clean_text(ing))

        diet = detect_diet(ingredient_names)

        recipe = Recipe(
            name=clean_text(meal["strMeal"]),
            cuisine=clean_text(meal["strArea"] or "unknown"),
            diet=diet,
            cooking_time=30,
            instructions=meal["strInstructions"]
        )

        db.add(recipe)
        db.commit()
        db.refresh(recipe)

        for ing_name in ingredient_names:
            ingredient = (
                db.query(Ingredient)
                .filter(Ingredient.name == ing_name)
                .first()
            )

            if not ingredient:
                ingredient = Ingredient(name=ing_name)
                db.add(ingredient)
                db.commit()
                db.refresh(ingredient)

            exists = (
                db.query(RecipeIngredient)
                .filter_by(
                    recipe_id=recipe.id,
                    ingredient_id=ingredient.id
                )
                .first()
            )

            if not exists:
                db.add(
                    RecipeIngredient(
                        recipe_id=recipe.id,
                        ingredient_id=ingredient.id
                    )
                )

        db.commit()

    db.close()

if __name__ == "__main__":
    save_recipes_to_db()