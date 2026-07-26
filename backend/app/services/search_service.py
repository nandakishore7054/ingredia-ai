from app.db.database import SessionLocal
from app.db.models import Recipe, Ingredient, RecipeIngredient
from app.services.recipe_service import ensure_recipe_nutrition
from typing import List, Optional
import math

def search_recipes(
    query: Optional[str] = None,
    ingredients: Optional[List[str]] = None,
    cuisine: Optional[str] = None,
    diet: Optional[str] = None,
    max_cooking_time: Optional[int] = None,
    sort_by: str = "name",
    page: int = 1,
    limit: int = 10,
):
    db = SessionLocal()

    try:
        recipes_query = db.query(Recipe)

        if query:
            recipes_query = recipes_query.filter(
                Recipe.name.ilike(f"%{query}%")
            )

        if cuisine:
            recipes_query = recipes_query.filter(
                Recipe.cuisine.ilike(f"%{cuisine}%")
            )

        if diet:
            recipes_query = recipes_query.filter(
                Recipe.diet == diet
            )

        if max_cooking_time is not None:
            recipes_query = recipes_query.filter(
                Recipe.cooking_time <= max_cooking_time
            )

        recipes = recipes_query.all()
        results = []

        for recipe in recipes:
            links = (
                db.query(RecipeIngredient)
                .filter(RecipeIngredient.recipe_id == recipe.id)
                .all()
            )

            ingredient_ids = [l.ingredient_id for l in links]

            recipe_ingredients = (
                db.query(Ingredient)
                .filter(Ingredient.id.in_(ingredient_ids))
                .all()
            )

            ingredient_names = [i.name for i in recipe_ingredients]

            match_count = 0
            if ingredients:
                matched = set(ingredients).intersection(set(ingredient_names))
                if not matched:
                    continue
                match_count = len(matched)

            ensure_recipe_nutrition(recipe, db=db, ingredients_list=ingredient_names)

            results.append({
                "id": recipe.id,
                "name": recipe.name,
                "cuisine": recipe.cuisine,
                "diet": recipe.diet,
                "cooking_time": recipe.cooking_time,
                "calories": recipe.calories,
                "protein": recipe.protein,
                "carbs": recipe.carbs,
                "fats": recipe.fats,
                "instructions": recipe.instructions,
                "ingredients": ingredient_names,
                "match_count": match_count
            })

        if sort_by == "name":
            results.sort(key=lambda x: x["name"])

        elif sort_by == "fastest":
            results.sort(key=lambda x: x["cooking_time"])

        elif sort_by == "best_match":
            results.sort(key=lambda x: x["match_count"], reverse=True)

        total_results = len(results)
        total_pages = math.ceil(total_results / limit) if limit else 1

        start = (page - 1) * limit
        end = start + limit
        paginated_results = results[start:end]

        return {
            "page": page,
            "limit": limit,
            "total_results": total_results,
            "total_pages": total_pages,
            "recipes": paginated_results
        }

    finally:
        db.close()
