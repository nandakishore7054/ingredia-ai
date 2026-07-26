import os
import sqlite3

def migrate_database(db_path):
    if not os.path.exists(db_path):
        print(f"Database file not found at {db_path}, skipping.")
        return

    print(f"Migrating database schema for: {db_path}")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # 1️⃣ Check & add columns to `recipes`
    cursor.execute("PRAGMA table_info(recipes)")
    existing_recipe_cols = {row[1] for row in cursor.fetchall()}

    recipe_columns_to_add = [
        ("prep_time", "INTEGER"),
        ("total_time", "INTEGER"),
        ("servings", "INTEGER"),
        ("difficulty", "VARCHAR"),
        ("meal_type", "VARCHAR"),
    ]

    for col_name, col_type in recipe_columns_to_add:
        if col_name not in existing_recipe_cols:
            try:
                cursor.execute(f"ALTER TABLE recipes ADD COLUMN {col_name} {col_type}")
                print(f"  [+] Added column '{col_name}' ({col_type}) to table 'recipes'")
            except sqlite3.OperationalError as e:
                print(f"  [!] Exception adding {col_name}: {e}")

    # Set default values for NULL fields in recipes if recipes table exists
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='recipes'")
    if cursor.fetchone():
        cursor.execute("UPDATE recipes SET prep_time = 10 WHERE prep_time IS NULL")
        cursor.execute("UPDATE recipes SET total_time = cooking_time + 10 WHERE total_time IS NULL")
        cursor.execute("UPDATE recipes SET servings = 4 WHERE servings IS NULL")
        cursor.execute("UPDATE recipes SET difficulty = 'Easy' WHERE difficulty IS NULL")
        cursor.execute("UPDATE recipes SET meal_type = 'Dinner' WHERE meal_type IS NULL")

    # 2️⃣ Check & add columns to `user_preferences`
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='user_preferences'")
    if cursor.fetchone():
        cursor.execute("PRAGMA table_info(user_preferences)")
        existing_pref_cols = {row[1] for row in cursor.fetchall()}

        pref_columns_to_add = [
            ("preferred_cuisines", "VARCHAR"),
            ("spice_level", "VARCHAR"),
        ]

        for col_name, col_type in pref_columns_to_add:
            if col_name not in existing_pref_cols:
                try:
                    cursor.execute(f"ALTER TABLE user_preferences ADD COLUMN {col_name} {col_type}")
                    print(f"  [+] Added column '{col_name}' ({col_type}) to table 'user_preferences'")
                except sqlite3.OperationalError as e:
                    print(f"  [!] Exception adding {col_name}: {e}")

    conn.commit()
    conn.close()
    print(f"Schema migration completed successfully for {db_path}!\n")

if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.abspath(__file__))
    migrate_database(os.path.join(base_dir, "database", "recipes.db"))
    migrate_database(os.path.join(base_dir, "recipes.db"))
