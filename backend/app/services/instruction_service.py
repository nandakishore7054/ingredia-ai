import os
import json
from openai import OpenAI

def generate_instructions(recipe_name: str, ingredients: list, cuisine: str = ""):
    """
    Generates step-by-step instructions and macro details for a recipe.
    Uses OpenAI or Groq API with robust fallback defaults if keys are missing/fail.
    """
    api_key = os.getenv("OPENAI_API_KEY") or os.getenv("GROQ_API_KEY")
    
    if api_key:
        try:
            if os.getenv("GROQ_API_KEY") and not os.getenv("OPENAI_API_KEY"):
                client = OpenAI(api_key=api_key, base_url="https://api.groq.com/openai/v1")
                model = "llama-3.3-70b-versatile"
            else:
                client = OpenAI(api_key=api_key)
                model = "gpt-4o-mini"

            prompt = f"""
You are a professional chef and nutritionist.

Recipe name: {recipe_name}
Cuisine: {cuisine or "General"}
Ingredients: {", ".join(ingredients) if ingredients else "Standard ingredients"}

Return STRICT JSON only in this format:
{{
  "instructions": "1. Prepare ingredients.\\n2. Cook on medium heat for 15 minutes.\\n3. Serve warm.",
  "calories": 450,
  "protein": 18,
  "carbs": 52,
  "fats": 14,
  "prep_time": 10,
  "cooking_time": 20,
  "total_time": 30,
  "servings": 4,
  "difficulty": "Easy",
  "meal_type": "Dinner"
}}
"""
            response = client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.4,
            )
            content = response.choices[0].message.content.strip()
            if content.startswith("```"):
                content = content.split("\n", 1)[-1].rsplit("```", 1)[0].strip()
            return json.loads(content)
        except Exception as e:
            print(f"Instruction service fallback used for '{recipe_name}': {e}")

    # Fallback default object when API key is missing or call fails
    return {
        "instructions": f"1. Prepare fresh ingredients for {recipe_name}.\n2. Heat pan or pot over medium heat with oil.\n3. Sauté and combine ingredients until thoroughly cooked.\n4. Season to taste and serve hot.",
        "calories": None,
        "protein": None,
        "carbs": None,
        "fats": None,
        "prep_time": 10,
        "cooking_time": 20,
        "total_time": 30,
        "servings": 4,
        "difficulty": "Easy",
        "meal_type": "Dinner"
    }

def generate_nutrition(recipe_name: str, ingredients: list):
    """
    Generates realistic nutritional data for a recipe.
    Returns STRICT JSON: {"calories": int, "protein": int, "carbs": int, "fats": int}
    Returns None if LLM is unavailable or fails.
    """
    api_key = os.getenv("OPENAI_API_KEY") or os.getenv("GROQ_API_KEY")
    if not api_key:
        return None

    try:
        if os.getenv("GROQ_API_KEY") and not os.getenv("OPENAI_API_KEY"):
            client = OpenAI(api_key=api_key, base_url="https://api.groq.com/openai/v1")
            model = "llama-3.3-70b-versatile"
        else:
            client = OpenAI(api_key=api_key)
            model = "gpt-4o-mini"

        prompt = f"""
You are a professional chef and nutritionist. Calculate realistic nutritional values for 1 serving of this recipe:

Recipe name: {recipe_name}
Ingredients: {", ".join(ingredients) if ingredients else "Standard ingredients"}

Return STRICT JSON only in this format:
{{
  "calories": 480,
  "protein": 18,
  "carbs": 55,
  "fats": 20
}}

No explanations. No markdown. No extra text.
"""
        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
        )
        content = response.choices[0].message.content.strip()
        if content.startswith("```"):
            content = content.split("\n", 1)[-1].rsplit("```", 1)[0].strip()
        data = json.loads(content)
        return {
            "calories": int(data.get("calories", 0)),
            "protein": int(data.get("protein", 0)),
            "carbs": int(data.get("carbs", 0)),
            "fats": int(data.get("fats", 0)),
        }
    except Exception as e:
        print(f"Error generating nutrition for '{recipe_name}': {e}")
        return None
