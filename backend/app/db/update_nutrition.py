from app.db.database import SessionLocal
from app.db.models import Recipe

# Example nutrition data (you can expand later)
NUTRITION_DATA = {
    "flan": {"calories": 250, "protein": 6, "carbs": 30, "fats": 12},
    "hummus": {"calories": 180, "protein": 8, "carbs": 14, "fats": 10},
    "falafel": {"calories": 320, "protein": 12, "carbs": 35, "fats": 15},
    "paella": {"calories": 400, "protein": 20, "carbs": 45, "fats": 14},
}

def update_nutrition():
    db = SessionLocal()

    for recipe_name, nutrition in NUTRITION_DATA.items():
        recipe = db.query(Recipe).filter(Recipe.name == recipe_name).first()
        if recipe:
            recipe.calories = nutrition["calories"]
            recipe.protein = nutrition["protein"]
            recipe.carbs = nutrition["carbs"]
            recipe.fats = nutrition["fats"]
            print(f"✅ Updated nutrition for {recipe_name}")
        else:
            print(f"⚠ Recipe not found: {recipe_name}")

    db.commit()
    db.close()
    print("🎉 Nutrition update completed")

if __name__ == "__main__":
    update_nutrition()
