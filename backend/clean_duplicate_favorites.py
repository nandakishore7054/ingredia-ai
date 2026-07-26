import sqlite3
import os

db_path = os.path.join(os.path.dirname(__file__), "database", "recipes.db")

def clean_duplicates():
    if not os.path.exists(db_path):
        print(f"Database file not found at {db_path}")
        return

    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    print("Cleaning duplicate favorites...")

    # Find duplicates
    cur.execute("""
        SELECT user_id, recipe_id, COUNT(*) as cnt
        FROM favorites
        GROUP BY user_id, recipe_id
        HAVING cnt > 1
    """)
    duplicates = cur.fetchall()
    print(f"Found {len(duplicates)} duplicate (user_id, recipe_id) combinations.")

    deleted_count = 0
    for user_id, recipe_id, count in duplicates:
        # Keep the record with min(id), delete the rest
        cur.execute("""
            DELETE FROM favorites
            WHERE user_id = ? AND recipe_id = ? AND id NOT IN (
                SELECT MIN(id)
                FROM favorites
                WHERE user_id = ? AND recipe_id = ?
            )
        """, (user_id, recipe_id, user_id, recipe_id))
        deleted_count += cur.rowcount

    print(f"Deleted {deleted_count} duplicate rows.")

    # Create unique index to enforce unique constraints at database level
    print("Creating unique index `uq_user_recipe_favorite`...")
    cur.execute("""
        CREATE UNIQUE INDEX IF NOT EXISTS uq_user_recipe_favorite
        ON favorites(user_id, recipe_id)
    """)

    conn.commit()
    conn.close()
    print("Clean duplicate favorites completed successfully!")

if __name__ == "__main__":
    clean_duplicates()
