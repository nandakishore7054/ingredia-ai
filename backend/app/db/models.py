from sqlalchemy import Column, Integer, String, ForeignKey, Text, Boolean, UniqueConstraint
from sqlalchemy.sql import func
from sqlalchemy.types import DateTime

from app.db.database import Base


class Recipe(Base):
    __tablename__ = "recipes"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    cuisine = Column(String)
    diet = Column(String)
    cooking_time = Column(Integer)
    prep_time = Column(Integer)
    total_time = Column(Integer)
    servings = Column(Integer)
    difficulty = Column(String)
    meal_type = Column(String)
    calories = Column(Integer)
    protein = Column(Integer)
    carbs = Column(Integer)
    fats = Column(Integer)

    instructions = Column(Text)


class Ingredient(Base):
    __tablename__ = "ingredients"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)


class RecipeIngredient(Base):
    __tablename__ = "recipe_ingredients"

    recipe_id = Column(Integer, ForeignKey("recipes.id"), primary_key=True)
    ingredient_id = Column(Integer, ForeignKey("ingredients.id"), primary_key=True)


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)

    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class Favorite(Base):
    __tablename__ = "favorites"
    __table_args__ = (
        UniqueConstraint("user_id", "recipe_id", name="uq_user_recipe_favorite"),
    )

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    recipe_id = Column(Integer, ForeignKey("recipes.id"), nullable=False)

class UserPreference(Base):
    __tablename__ = "user_preferences"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True)

    diet = Column(String)                     # veg, vegan, keto
    allergies = Column(String)                # peanuts, milk
    disliked_ingredients = Column(String)     # onion, garlic
    preferred_cuisines = Column(String)       # Italian, Indian, Mexican
    calorie_limit = Column(Integer)           # 2000
    spice_level = Column(String)             # Mild, Medium, Spicy

class CookingHistory(Base):
    __tablename__ = "cooking_history"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    recipe_id = Column(Integer, ForeignKey("recipes.id"))

    cooked_at = Column(DateTime(timezone=True), server_default=func.now())
