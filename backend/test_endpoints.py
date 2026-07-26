import sys
import os

# Ensure backend directory is in path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from fastapi.testclient import TestClient
from app.main import app
from app.utils.auth_dependency import get_current_user
from app.db.models import User

# Override auth dependency for testing protected routes
def mock_get_current_user():
    return User(id=1, name="Test User", email="test@example.com")

app.dependency_overrides[get_current_user] = mock_get_current_user

client = TestClient(app)

def run_api_tests():
    print("==========================================")
    print("    FASTAPI ENDPOINT VERIFICATION SUITE   ")
    print("==========================================")

    endpoints_to_test = [
        ("GET", "/", None),
        ("POST", "/search-recipes", {}),
        ("GET", "/recipes/Pasta", None),
        ("GET", "/preferences/", None),
        ("POST", "/preferences/", {"diet": "Vegetarian", "calorie_limit": 2000}),
        ("GET", "/recommendations/personalized", None),
        ("POST", "/match-recipes", ["tomato", "onion"]),
    ]

    failed = False
    for method, path, payload in endpoints_to_test:
        try:
            if method == "GET":
                res = client.get(path)
            else:
                res = client.post(path, json=payload)

            print(f"[{method}] {path:35} -> HTTP {res.status_code}")
            if res.status_code >= 500:
                print(f"   [FAIL] Server Error ({res.status_code}): {res.text}")
                failed = True
            elif res.status_code not in (200, 201, 404):
                print(f"   [WARN] Unexpected Status ({res.status_code}): {res.text}")
        except Exception as e:
            print(f"[{method}] {path:35} -> EXCEPTION: {e}")
            failed = True

    print("==========================================")
    if not failed:
        print("[SUCCESS] ALL ENDPOINTS PASSED WITHOUT 500 ERRORS!")
    else:
        print("[FAIL] SOME ENDPOINTS FAILED WITH 500 ERRORS.")
    print("==========================================")

if __name__ == "__main__":
    run_api_tests()
