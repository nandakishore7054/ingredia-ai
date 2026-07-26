from app.db.database import engine, Base

# IMPORTING ALL MODELS HERE
from app.db.models import (
    User,
    Recipe,
    Ingredient,
    RecipeIngredient,
    Favorite,
    UserPreference,
    CookingHistory
)

def init():
    Base.metadata.create_all(bind=engine)
    print("✅ Database tables created successfully")

if __name__ == "__main__":
    init()
