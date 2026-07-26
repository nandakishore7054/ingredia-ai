import sqlite3

db_path = 'database/recipes.db'
conn = sqlite3.connect(db_path)
conn.row_factory = sqlite3.Row
cur = conn.cursor()

# --- All recipes with full data ---
print('=== ALL RECIPES (full data) ===')
cur.execute('SELECT id, name, cuisine, diet, cooking_time, calories, protein, carbs, fats, instructions FROM recipes ORDER BY id')
recipes = cur.fetchall()
for r in recipes:
    has_instructions = 'YES' if r['instructions'] and len(r['instructions']) > 10 else 'NO/EMPTY'
    print(f'  [{r["id"]}] {r["name"]} | cuisine={r["cuisine"]} | diet={r["diet"]} | time={r["cooking_time"]}min | cal={r["calories"]} | protein={r["protein"]}g | carbs={r["carbs"]}g | fat={r["fats"]}g | instructions={has_instructions}')

# --- Missing nutrition ---
print('\n=== RECIPES WITH MISSING NUTRITION ===')
cur.execute('SELECT id, name FROM recipes WHERE calories IS NULL OR protein IS NULL OR carbs IS NULL OR fats IS NULL')
missing_nutrition = cur.fetchall()
print(f'  Count: {len(missing_nutrition)}')
for r in missing_nutrition:
    print(f'  [{r["id"]}] {r["name"]}')

# --- Missing instructions ---
print('\n=== RECIPES WITH MISSING INSTRUCTIONS ===')
cur.execute("SELECT id, name FROM recipes WHERE instructions IS NULL OR instructions = ''")
missing_instr = cur.fetchall()
print(f'  Count: {len(missing_instr)}')
for r in missing_instr:
    print(f'  [{r["id"]}] {r["name"]}')

# --- All ingredients ---
print('\n=== ALL INGREDIENTS ===')
cur.execute('SELECT id, name FROM ingredients ORDER BY name')
for i in cur.fetchall():
    print(f'  [{i["id"]}] {i["name"]}')

# --- Recipes with ingredient counts ---
print('\n=== RECIPE INGREDIENT COUNTS ===')
cur.execute('''
    SELECT r.id, r.name, COUNT(ri.ingredient_id) as ing_count
    FROM recipes r
    LEFT JOIN recipe_ingredients ri ON r.id = ri.recipe_id
    GROUP BY r.id
    ORDER BY ing_count DESC
''')
for row in cur.fetchall():
    print(f'  [{row["id"]}] {row["name"]}: {row["ing_count"]} ingredients')

# --- Orphan recipes (no ingredients linked) ---
print('\n=== RECIPES WITH ZERO INGREDIENTS LINKED ===')
cur.execute('''
    SELECT r.id, r.name
    FROM recipes r
    LEFT JOIN recipe_ingredients ri ON r.id = ri.recipe_id
    WHERE ri.recipe_id IS NULL
''')
orphans = cur.fetchall()
print(f'  Count: {len(orphans)}')
for r in orphans:
    print(f'  [{r["id"]}] {r["name"]}')

# --- Duplicate favorite entries ---
print('\n=== DUPLICATE FAVORITES CHECK ===')
cur.execute('''
    SELECT user_id, recipe_id, COUNT(*) as cnt
    FROM favorites
    GROUP BY user_id, recipe_id
    HAVING cnt > 1
''')
dupes = cur.fetchall()
print(f'  Duplicate favorites: {len(dupes)}')

# --- Users info (no passwords) ---
print('\n=== USERS ===')
cur.execute("SELECT id, name, email, is_active, created_at FROM users")
for u in cur.fetchall():
    print(f'  [{u["id"]}] {u["name"]} | {u["email"]} | active={u["is_active"]} | created={u["created_at"]}')

# --- User preferences ---
print('\n=== USER PREFERENCES ===')
cur.execute("SELECT * FROM user_preferences")
for p in cur.fetchall():
    print(f'  user_id={p["user_id"]} | diet={p["diet"]} | allergies={p["allergies"]} | dislikes={p["disliked_ingredients"]} | cal_limit={p["calorie_limit"]}')

# --- Cuisine diversity ---
print('\n=== CUISINE DISTRIBUTION ===')
cur.execute("SELECT cuisine, COUNT(*) as cnt FROM recipes GROUP BY cuisine ORDER BY cnt DESC")
for row in cur.fetchall():
    print(f'  {row["cuisine"]}: {row["cnt"]} recipes')

# --- Diet distribution ---
print('\n=== DIET DISTRIBUTION ===')
cur.execute("SELECT diet, COUNT(*) as cnt FROM recipes GROUP BY diet ORDER BY cnt DESC")
for row in cur.fetchall():
    print(f'  {row["diet"]}: {row["cnt"]} recipes')

conn.close()
