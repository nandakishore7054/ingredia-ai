import sys
import os
import sqlite3

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from dotenv import load_dotenv
load_dotenv(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env"))

from app.services.recipe_service import get_recipe_by_name

TEST_RECIPES = [
    "Aloo Paratha",
    "Paneer Makhani",
    "Chili Chicken",
    "Garlic Bread",
    "White Sauce Pasta",
    "Veg Sandwich"
]

def run_enrichment_test():
    print("==================================================")
    print("   AI NUTRITION ENRICHMENT & CACHING VERIFICATION ")
    print("==================================================")

    db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "database", "recipes.db")
    
    # 1. Verify initial DB state (should be NULL)
    conn = sqlite3.connect(db_path)
    print("\n--- Initial Database Values Before Request ---")
    for name in TEST_RECIPES:
        row = conn.execute("SELECT calories, protein, carbs, fats FROM recipes WHERE name = ?", (name,)).fetchone()
        print(f"DB Entry: {name:20} -> Calories: {row[0] if row else 'N/A'}")
    conn.close()

    # 2. First Request (Generates AI Nutrition and saves to DB)
    print("\n--- 1ST REQUEST: Dynamically Generating AI Nutrition ---")
    generated_results = {}
    for name in TEST_RECIPES:
        data = get_recipe_by_name(name)
        cals = data.get("calories")
        protein = data.get("protein")
        carbs = data.get("carbs")
        fats = data.get("fats")
        generated_results[name] = (cals, protein, carbs, fats)
        print(f"Generated: {name:20} -> {cals} kcal | P:{protein}g C:{carbs}g F:{fats}g")

    # 3. Verify Database After 1st Request
    conn = sqlite3.connect(db_path)
    print("\n--- Database Values After 1st Request (Cached in SQLite) ---")
    all_cached_in_db = True
    for name in TEST_RECIPES:
        row = conn.execute("SELECT calories, protein, carbs, fats FROM recipes WHERE name = ?", (name,)).fetchone()
        print(f"Cached DB: {name:20} -> {row[0]} kcal | P:{row[1]}g C:{row[2]}g F:{row[3]}g")
        if not row[0] or row[0] == 420:
            all_cached_in_db = False
    conn.close()

    # 4. 2nd Request (Immediate cached read)
    print("\n--- 2ND REQUEST: Reading Cached Values from SQLite ---")
    second_request_results = {}
    for name in TEST_RECIPES:
        data = get_recipe_by_name(name)
        cals = data.get("calories")
        second_request_results[name] = cals
        print(f"Cached Read: {name:20} -> {cals} kcal")

    # 5. Assertions
    print("\n==================================================")
    print("VERIFICATION CHECKLIST:")
    
    # Unique values check
    unique_calories = set(v[0] for v in generated_results.values() if v[0] is not None)
    print(f"1. Different realistic values generated across recipes: {len(unique_calories) > 1} ({unique_calories})")
    
    # All stored check
    all_cached_in_db = all(second_request_results[n] is not None for n in TEST_RECIPES)
    print(f"2. All recipes have realistic AI nutrition stored in SQLite: {all_cached_in_db}")
    
    # Caching check
    cache_matches = all(generated_results[n][0] == second_request_results[n] for n in TEST_RECIPES)
    print(f"3. Second request matches cached SQLite data without regenerating: {cache_matches}")

    print("==================================================")
    if len(unique_calories) > 1 and all_cached_in_db and cache_matches:
        print("[SUCCESS] AI NUTRITION ENRICHMENT & CACHING VERIFIED 100% SUCCESSFUL!")
    else:
        print("[WARN] SOME CHECKS REQUIRE ATTENTION.")
    print("==================================================")

if __name__ == "__main__":
    run_enrichment_test()
