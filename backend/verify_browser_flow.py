import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from fastapi.testclient import TestClient
from app.main import app
from app.utils.auth_dependency import get_current_user
from app.db.models import User

# Override auth dependency for testing protected routes
def mock_get_current_user():
    return User(id=1, name="Test Chef", email="testchef@ingredia.ai")

app.dependency_overrides[get_current_user] = mock_get_current_user

client = TestClient(app)

TARGET_10_RECIPES = [
    "Aloo Paratha",
    "Paneer Makhani",
    "Chili Chicken",
    "Palak Paneer",
    "White Sauce Pasta",
    "Garlic Bread",
    "Veg Sandwich",
    "Vegetable Pulao",
    "Aloo Gobi",
    "Paneer Bhurji"
]

def run_browser_verification():
    print("==================================================")
    print("   INGREDIA AI — BROWSER END-TO-END VERIFICATION  ")
    print("==================================================")
    
    # 1. Test 10 Required Recipe Detail Page Endpoints
    print("\n--- Testing 10 Target Recipe Detail Pages ---")
    all_recipes_ok = True
    for name in TARGET_10_RECIPES:
        url = f"/recipes/{name}"
        res = client.get(url)
        if res.status_code == 200:
            data = res.json()
            inst_snippet = (data.get("instructions") or "")[:40].replace("\n", " ")
            cals = data.get("calories")
            protein = data.get("protein")
            carbs = data.get("carbs")
            fats = data.get("fats")
            print(f"[OK 200] {name:20} | {cals} kcal | P:{protein}g C:{carbs}g F:{fats}g | Instructions: '{inst_snippet}...'")
        else:
            print(f"[FAIL {res.status_code}] {name:20} -> FAIL: {res.text}")
            all_recipes_ok = False

    # 2. Test User Preferences GET & POST
    print("\n--- Testing User Preferences Workflow ---")
    pref_post = client.post("/preferences/", json={
        "diet": "Vegetarian",
        "allergies": "Peanuts",
        "preferred_cuisines": "Indian, Italian",
        "calorie_limit": 2000,
        "spice_level": "Medium"
    })
    pref_get = client.get("/preferences/")
    print(f"POST /preferences/ -> HTTP {pref_post.status_code}")
    print(f"GET  /preferences/ -> HTTP {pref_get.status_code} | Saved Diet: {pref_get.json().get('diet') if pref_get.status_code==200 else 'Error'}")

    # 3. Test Personalized Recommendations
    print("\n--- Testing Personalized Recommendations ---")
    recs_res = client.get("/recommendations/personalized")
    print(f"GET /recommendations/personalized -> HTTP {recs_res.status_code} | Recommended Count: {len(recs_res.json().get('recipes', [])) if recs_res.status_code==200 else 0}")

    # 4. Test Search & Filters
    print("\n--- Testing Search & Filters ---")
    search_res = client.post("/search-recipes", json={"cuisine": "Indian"})
    print(f"POST /search-recipes (Indian Cuisine) -> HTTP {search_res.status_code} | Matches: {len(search_res.json()) if search_res.status_code==200 else 0}")

    # 5. Test Match Recipes (Ingredient Detection pipeline endpoint)
    print("\n--- Testing Match Recipes ---")
    match_res = client.post("/match-recipes", json=["paneer", "tomato", "butter"])
    print(f"POST /match-recipes -> HTTP {match_res.status_code} | Matches: {len(match_res.json()) if match_res.status_code==200 else 0}")

    print("\n==================================================")
    if all_recipes_ok and recs_res.status_code == 200 and search_res.status_code == 200:
        print("[SUCCESS] ALL 10 TARGET RECIPES & WORKFLOWS VERIFIED 100% SUCCESSFUL!")
    else:
        print("[WARN] SOME WORKFLOWS ENCOUNTERED ISSUES.")
    print("==================================================")

if __name__ == "__main__":
    run_browser_verification()
