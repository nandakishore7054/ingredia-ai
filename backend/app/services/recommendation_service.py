from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from app.db.database import SessionLocal
from app.db.models import Recipe, Ingredient, RecipeIngredient


def recommend_recipes_ml(detected_ingredients: list):
    db = SessionLocal()

    # normalize input
    detected_ingredients = [i.lower().strip() for i in detected_ingredients]
    user_text = " ".join(detected_ingredients)

    recipes = db.query(Recipe).all()

    recipe_texts = []
    recipe_names = []

    for recipe in recipes:
        links = (
            db.query(RecipeIngredient)
            .filter(RecipeIngredient.recipe_id == recipe.id)
            .all()
        )

        if not links:
            continue

        ingredient_ids = [l.ingredient_id for l in links]

        ingredients = (
            db.query(Ingredient)
            .filter(Ingredient.id.in_(ingredient_ids))
            .all()
        )

        ingredient_names = [i.name for i in ingredients]

        recipe_texts.append(" ".join(ingredient_names))
        recipe_names.append(recipe.name)

    db.close()

    if not recipe_texts:
        return []

    # TF-IDF
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(recipe_texts + [user_text])

    similarities = cosine_similarity(
        tfidf_matrix[-1],
        tfidf_matrix[:-1]
    )[0]

    results = []

    for idx, score in enumerate(similarities):
        if score > 0:
            results.append({
                "recipe_name": recipe_names[idx],
                "similarity_score": round(float(score), 3)
            })

    results.sort(key=lambda x: x["similarity_score"], reverse=True)

    return results[:10]  # top 10