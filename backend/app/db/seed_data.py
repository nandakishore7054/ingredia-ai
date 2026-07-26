from app.db.database import SessionLocal
from app.db.models import Recipe, Ingredient, RecipeIngredient

db = SessionLocal()

# -----------------------------
# INGREDIENTS (25)
# -----------------------------
ingredients = [
    "Onion", "Tomato", "Potato", "Capsicum", "Carrot", "Spinach",
    "Garlic", "Ginger", "Chicken", "Egg", "Paneer",
    "Rice", "Wheat Flour", "Pasta", "Bread",
    "Milk", "Cheese", "Butter",
    "Oil", "Salt", "Chili Powder", "Turmeric",
    "Soy Sauce", "Oregano", "Lentils"
]

ingredient_map = {}

for name in ingredients:
    ingredient = db.query(Ingredient).filter_by(name=name).first()
    if not ingredient:
        ingredient = Ingredient(name=name)
        db.add(ingredient)
        db.commit()
        db.refresh(ingredient)
    ingredient_map[name] = ingredient.id


# -----------------------------
# RECIPES (30)
# -----------------------------
recipes = [
    # Indian
    ("Butter Chicken", "Indian", "Non-Veg", 45,
     ["Chicken", "Tomato", "Onion", "Butter", "Milk", "Garlic", "Ginger", "Chili Powder"]),
    ("Paneer Makhani", "Indian", "Vegetarian", 40,
     ["Paneer", "Tomato", "Onion", "Butter", "Milk", "Garlic", "Ginger"]),
    ("Aloo Gobi", "Indian", "Vegan", 30,
     ["Potato", "Onion", "Tomato", "Turmeric", "Chili Powder"]),
    ("Egg Curry", "Indian", "Eggetarian", 30,
     ["Egg", "Onion", "Tomato", "Garlic", "Ginger", "Turmeric"]),
    ("Palak Paneer", "Indian", "Vegetarian", 35,
     ["Spinach", "Paneer", "Onion", "Garlic", "Ginger", "Milk"]),
    ("Vegetable Pulao", "Indian", "Vegan", 25,
     ["Rice", "Carrot", "Capsicum", "Potato", "Onion"]),
    ("Dal Tadka", "Indian", "Vegan", 25,
     ["Lentils", "Onion", "Tomato", "Garlic", "Turmeric"]),
    ("Paneer Bhurji", "Indian", "Vegetarian", 20,
     ["Paneer", "Onion", "Tomato", "Capsicum"]),
    ("Jeera Rice", "Indian", "Vegan", 15,
     ["Rice", "Oil", "Salt"]),
    ("Aloo Paratha", "Indian", "Vegetarian", 30,
     ["Potato", "Wheat Flour", "Onion"]),

    # Italian / Western
    ("Arrabbiata Pasta", "Italian", "Vegan", 25,
     ["Pasta", "Tomato", "Garlic", "Chili Powder"]),
    ("White Sauce Pasta", "Italian", "Vegetarian", 30,
     ["Pasta", "Milk", "Butter", "Cheese", "Oregano"]),
    ("Grilled Cheese Sandwich", "Western", "Vegetarian", 10,
     ["Bread", "Cheese", "Butter"]),
    ("Spanish Omelette", "Western", "Eggetarian", 20,
     ["Egg", "Potato", "Onion"]),
    ("Garlic Bread", "Western", "Vegetarian", 15,
     ["Bread", "Butter", "Garlic", "Oregano"]),
    ("Tomato Soup", "Western", "Vegan", 20,
     ["Tomato", "Garlic", "Oil"]),
    ("Veg Sandwich", "Western", "Vegetarian", 10,
     ["Bread", "Tomato", "Onion", "Capsicum"]),
    ("Scrambled Eggs", "Western", "Eggetarian", 10,
     ["Egg", "Butter"]),

    # Indo-Chinese
    ("Chili Chicken", "Indo-Chinese", "Non-Veg", 35,
     ["Chicken", "Capsicum", "Onion", "Soy Sauce", "Garlic", "Ginger"]),
    ("Veg Fried Rice", "Indo-Chinese", "Vegan", 25,
     ["Rice", "Carrot", "Capsicum", "Onion", "Soy Sauce"]),
    ("Egg Fried Rice", "Indo-Chinese", "Eggetarian", 25,
     ["Rice", "Egg", "Carrot", "Soy Sauce"]),
    ("Gobi Manchurian", "Indo-Chinese", "Vegan", 40,
     ["Potato", "Garlic", "Soy Sauce", "Chili Powder"]),
    ("Paneer Chili", "Indo-Chinese", "Vegetarian", 30,
     ["Paneer", "Capsicum", "Onion", "Soy Sauce"]),
    ("Garlic Noodles", "Indo-Chinese", "Vegan", 20,
     ["Pasta", "Garlic", "Soy Sauce"]),
    ("Veg Manchow Soup", "Indo-Chinese", "Vegan", 25,
     ["Carrot", "Capsicum", "Garlic", "Soy Sauce"]),
    ("Stir Fry Veggies", "Indo-Chinese", "Vegan", 20,
     ["Carrot", "Capsicum", "Onion", "Spinach"]),

    # Smart Logic
    ("One Pot Veg Meal", "Fusion", "Vegan", 30,
     ["Rice", "Potato", "Carrot", "Onion"]),
    ("High Protein Bowl", "Fusion", "Protein", 20,
     ["Chicken", "Paneer", "Spinach"]),
    ("Emergency Meal", "Quick", "Vegetarian", 5,
     ["Bread", "Butter"])
]


# -----------------------------
# INSERT RECIPES & MAPPING
# -----------------------------
for name, cuisine, diet, time, ing_list in recipes:
    recipe = db.query(Recipe).filter_by(name=name).first()
    if not recipe:
        recipe = Recipe(
            name=name,
            cuisine=cuisine,
            diet=diet,
            cooking_time=time
        )
        db.add(recipe)
        db.commit()
        db.refresh(recipe)

    for ing in ing_list:
        exists = db.query(RecipeIngredient).filter_by(
            recipe_id=recipe.id,
            ingredient_id=ingredient_map[ing]
        ).first()
        if not exists:
            db.add(
                RecipeIngredient(
                    recipe_id=recipe.id,
                    ingredient_id=ingredient_map[ing]
                )
            )
    db.commit()

db.close()
print("✅ Database seeded successfully with 30 recipes!")
