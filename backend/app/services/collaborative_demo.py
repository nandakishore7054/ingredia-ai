import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

# =========================
# STEP 1: FAKE USER DATA
# =========================
ratings = [
    {"user": 1, "recipe": "pasta", "rating": 5},
    {"user": 1, "recipe": "pizza", "rating": 4},
    {"user": 1, "recipe": "garlic bread", "rating": 5},

    {"user": 2, "recipe": "pasta", "rating": 5},
    {"user": 2, "recipe": "pizza", "rating": 4},

    {"user": 3, "recipe": "biryani", "rating": 5},
    {"user": 3, "recipe": "pulao", "rating": 4},
]

# =========================
# STEP 2: DATAFRAME
# =========================
df = pd.DataFrame(ratings)

# =========================
# STEP 3: USER–RECIPE MATRIX
# =========================
user_recipe_matrix = df.pivot_table(
    index="user",
    columns="recipe",
    values="rating"
).fillna(0)

# =========================
# STEP 4: USER SIMILARITY
# =========================
user_similarity = cosine_similarity(user_recipe_matrix)

similarity_df = pd.DataFrame(
    user_similarity,
    index=user_recipe_matrix.index,
    columns=user_recipe_matrix.index
)

# =========================
# STEP 5: SIMPLE RECOMMENDER
# =========================
def recommend_for_user(user_id):
    # find most similar user (excluding self)
    similar_users = similarity_df[user_id].sort_values(ascending=False)
    similar_users = similar_users.drop(user_id)

    most_similar_user = similar_users.index[0]

    # recipes rated by similar user
    similar_user_ratings = user_recipe_matrix.loc[most_similar_user]

    # recipes not rated by target user
    target_user_ratings = user_recipe_matrix.loc[user_id]

    recommendations = []

    for recipe in user_recipe_matrix.columns:
        if target_user_ratings[recipe] == 0 and similar_user_ratings[recipe] > 0:
            recommendations.append(recipe)

    return recommendations


# =========================
# DEMO RUN
# =========================
if __name__ == "__main__":
    print("User-Recipe Matrix:")
    print(user_recipe_matrix)

    print("\nUser Similarity Matrix:")
    print(similarity_df)

    print("\nRecommendations for User 2:")
    print(recommend_for_user(2))