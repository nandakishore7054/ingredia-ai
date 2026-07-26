import sqlite3
conn = sqlite3.connect('database/recipes.db')
conn.row_factory = sqlite3.Row
cur = conn.cursor()

cur.execute('''
    SELECT recipe_id, ingredient_id, COUNT(*) as cnt 
    FROM recipe_ingredients 
    GROUP BY recipe_id, ingredient_id 
    HAVING cnt > 1
''')
print(f'Duplicate mappings: {len(cur.fetchall())}')

cur.execute('''
    SELECT i.name, COUNT(ri.recipe_id) as count
    FROM ingredients i
    LEFT JOIN recipe_ingredients ri ON i.id = ri.ingredient_id
    GROUP BY i.id
    ORDER BY count DESC
''')
print('Usage:')
for r in cur.fetchall():
    print(f'{r["name"]}: {r["count"]}')
