import os
import sys
import time
import logging
import sqlite3

# Ensure we can import app modules
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.db.database import SessionLocal, DATABASE_URL
from app.db.models import Recipe, Ingredient, RecipeIngredient
from app.services.instruction_service import generate_instructions

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def migrate_schema():
    """Adds the new columns to the SQLite database if they don't exist."""
    db_path = DATABASE_URL.replace("sqlite:///", "")
    
    # Simple check and alter
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        
        columns_to_add = [
            ("prep_time", "INTEGER"),
            ("total_time", "INTEGER"),
            ("servings", "INTEGER"),
            ("difficulty", "TEXT"),
            ("meal_type", "TEXT")
        ]
        
        for col_name, col_type in columns_to_add:
            try:
                cursor.execute(f"ALTER TABLE recipes ADD COLUMN {col_name} {col_type}")
                logger.info(f"Added column {col_name} to recipes table.")
            except sqlite3.OperationalError as e:
                if "duplicate column name" in str(e):
                    logger.info(f"Column {col_name} already exists.")
                else:
                    raise e
        conn.commit()

def enrich_database():
    """Iterates through all recipes and enriches them via LLM."""
    db = SessionLocal()
    
    recipes = db.query(Recipe).all()
    logger.info(f"Found {len(recipes)} recipes to enrich.")
    
    for recipe in recipes:
        # Check if it needs enrichment. If it has all the new fields, skip.
        if (recipe.instructions and recipe.calories and recipe.prep_time 
            and recipe.total_time and recipe.servings and recipe.difficulty and recipe.meal_type):
            logger.info(f"Recipe '{recipe.name}' is already fully enriched. Skipping.")
            continue
            
        logger.info(f"Enriching recipe: {recipe.name}...")
        
        # Fetch ingredients
        ingredient_rows = db.query(Ingredient.name).join(
            RecipeIngredient, Ingredient.id == RecipeIngredient.ingredient_id
        ).filter(
            RecipeIngredient.recipe_id == recipe.id
        ).all()
        ingredients_list = [row[0] for row in ingredient_rows]
        
        try:
            ai_data = generate_instructions(
                recipe_name=recipe.name,
                ingredients=ingredients_list,
                cuisine=recipe.cuisine,
            )
            
            # Update fields
            recipe.instructions = ai_data.get("instructions", recipe.instructions)
            recipe.calories = ai_data.get("calories", recipe.calories)
            recipe.protein = ai_data.get("protein", recipe.protein)
            recipe.carbs = ai_data.get("carbs", recipe.carbs)
            recipe.fats = ai_data.get("fats", recipe.fats)
            
            recipe.prep_time = ai_data.get("prep_time", recipe.prep_time)
            if ai_data.get("cooking_time"):
                recipe.cooking_time = ai_data.get("cooking_time")
            recipe.total_time = ai_data.get("total_time", recipe.total_time)
            recipe.servings = ai_data.get("servings", recipe.servings)
            recipe.difficulty = ai_data.get("difficulty", recipe.difficulty)
            recipe.meal_type = ai_data.get("meal_type", recipe.meal_type)
            
            db.commit()
            logger.info(f"Successfully enriched '{recipe.name}'.")
            
            # Avoid rate limits
            time.sleep(2)
        except Exception as e:
            logger.error(f"Failed to enrich '{recipe.name}': {e}")
            db.rollback()

    db.close()
    logger.info("Database enrichment complete!")

if __name__ == "__main__":
    logger.info("Starting Recipe Database Enrichment...")
    migrate_schema()
    enrich_database()
