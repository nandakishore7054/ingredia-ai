import os
import sys
import sqlite3
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from dotenv import load_dotenv
load_dotenv(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env"))

from app.services.instruction_service import generate_nutrition

def enrich_all_nutrition():
    db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "database", "recipes.db")
    print(f"Connecting to SQLite database: {db_path}")

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # 1. Fetch all recipes
    cursor.execute("SELECT id, name, calories, protein, carbs, fats FROM recipes")
    recipes = cursor.fetchall()

    print(f"Total recipes in database: {len(recipes)}")
    print("--------------------------------------------------")

    updated_count = 0
    skipped_count = 0
    updated_summary = []

    for r_id, r_name, r_cal, r_prot, r_carbs, r_fats in recipes:
        # Skip if valid nutrition already exists (and not 0 / null / legacy 420)
        if r_cal and r_cal > 0 and r_cal != 420:
            print(f"[SKIP] '{r_name:22}' already has valid nutrition: {r_cal} kcal | P:{r_prot}g C:{r_carbs}g F:{r_fats}g")
            skipped_count += 1
            continue

        print(f"[ENRICHING] Generating AI nutrition for: '{r_name}'...")

        # Fetch ingredients for this recipe
        cursor.execute("""
            SELECT i.name FROM ingredients i
            JOIN recipe_ingredients ri ON i.id = ri.ingredient_id
            WHERE ri.recipe_id = ?
        """, (r_id,))
        ing_rows = cursor.fetchall()
        ingredients_list = [row[0] for row in ing_rows]

        nutrition = generate_nutrition(r_name, ingredients_list)

        if nutrition and nutrition.get("calories"):
            cal = nutrition["calories"]
            prot = nutrition["protein"]
            carbs = nutrition["carbs"]
            fats = nutrition["fats"]

            cursor.execute("""
                UPDATE recipes
                SET calories = ?, protein = ?, carbs = ?, fats = ?
                WHERE id = ?
            """, (cal, prot, carbs, fats, r_id))
            conn.commit()

            updated_count += 1
            updated_summary.append((r_name, cal, prot, carbs, fats))
            print(f"  --> SUCCESS: Saved -> {cal} kcal | P:{prot}g C:{carbs}g F:{fats}g")
        else:
            print(f"  --> FAILED to generate nutrition for '{r_name}'")

        # Brief delay to prevent rate-limiting
        time.sleep(1)

    conn.close()

    print("\n==================================================")
    print("        ENRICHMENT SUMMARY REPORT                 ")
    print("==================================================")
    print(f"Total Recipes Processed: {len(recipes)}")
    print(f"Recipes Already Enriched: {skipped_count}")
    print(f"Recipes Newly Enriched  : {updated_count}")
    print("--------------------------------------------------")
    print("Summary of Updated Recipes:")
    for item in updated_summary:
        print(f" - {item[0]:25}: {item[1]} kcal | P:{item[2]}g C:{item[3]}g F:{item[4]}g")
    print("==================================================")

if __name__ == "__main__":
    enrich_all_nutrition()
