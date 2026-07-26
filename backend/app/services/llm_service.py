import os
import json
from openai import AsyncOpenAI
import logging

logger = logging.getLogger(__name__)

class LLMService:
    def __init__(self):
        # We use the OpenAI client but point it to Groq's base URL.
        # This provides the OpenAI-compatible architecture requested.
        self.api_key = os.getenv("GROQ_API_KEY", os.getenv("OPENAI_API_KEY"))
        
        if not self.api_key:
            logger.warning("No GROQ_API_KEY found. AI features will fallback/fail.")
            
        self.client = AsyncOpenAI(
            api_key=self.api_key,
            base_url="https://api.groq.com/openai/v1"
        )
        # Primary model is llama-3.3-70b-versatile
        self.model = "llama-3.3-70b-versatile"
        
        # Standard pantry assumptions
        self.pantry_staples = "salt, oil, water, pepper, turmeric, sugar"

    async def _safe_json_call(self, prompt: str, system_prompt: str = "") -> dict:
        """Helper to make an LLM call and safely parse the JSON output with graceful fallback."""
        if not self.api_key:
            return {}
            
        try:
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.4,
                response_format={"type": "json_object"}
            )
            content = response.choices[0].message.content
            return json.loads(content)
        except Exception as e:
            logger.error(f"LLM API Error: {str(e)}")
            # Attempt fallback to llama3-70b-8192 if versatile fails
            try:
                logger.info("Attempting fallback to llama3-70b-8192...")
                response = await self.client.chat.completions.create(
                    model="llama3-70b-8192",
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.4,
                    response_format={"type": "json_object"}
                )
                return json.loads(response.choices[0].message.content)
            except Exception as fallback_err:
                logger.error(f"Fallback LLM API Error: {str(fallback_err)}")
                return {}

    async def generate_dynamic_recipe(self, ingredients: list) -> list:
        """Generates recipes dynamically based on detected ingredients."""
        system_prompt = "You are a master chef AI. Output strictly valid JSON."
        prompt = f"""
        I have the following ingredients: {', '.join(ingredients)}.
        You may also assume I have basic pantry staples: {self.pantry_staples}.
        
        Generate 3 delicious recipes using these ingredients. 
        Format your response EXACTLY like this JSON object:
        {{
            "recipes": [
                {{
                    "name": "Recipe Name",
                    "cuisine": "Italian/Mexican/etc",
                    "diet": "Vegan/Omnivore/etc",
                    "cooking_time": 30,
                    "instructions": "Step 1... Step 2...",
                    "calories": 400,
                    "protein": 20,
                    "carbs": 50,
                    "fats": 15,
                    "match_percentage": 95,
                    "matched_ingredients": ["item1", "item2"]
                }}
            ]
        }}
        """
        result = await self._safe_json_call(prompt, system_prompt)
        return result.get("recipes", [])

    async def generate_from_prompt(self, user_prompt: str) -> list:
        """Generates recipes based on a natural language prompt."""
        system_prompt = "You are a master chef AI. Output strictly valid JSON."
        prompt = f"""
        User request: "{user_prompt}"
        You may assume basic pantry staples are available: {self.pantry_staples}.
        
        Generate 3 recipes fulfilling this request.
        Format your response EXACTLY like this JSON object:
        {{
            "recipes": [
                {{
                    "name": "Recipe Name",
                    "cuisine": "...",
                    "diet": "...",
                    "cooking_time": 30,
                    "instructions": "...",
                    "calories": 400,
                    "protein": 20,
                    "carbs": 50,
                    "fats": 15,
                    "match_percentage": 100,
                    "matched_ingredients": []
                }}
            ]
        }}
        """
        result = await self._safe_json_call(prompt, system_prompt)
        return result.get("recipes", [])

    async def analyze_nutrition_and_subs(self, recipe_name: str, ingredients: list) -> dict:
        """Provides deep dive nutrition and substitution analysis."""
        system_prompt = "You are an expert nutritionist and chef. Output strictly valid JSON."
        prompt = f"""
        Analyze this recipe: "{recipe_name}"
        Current ingredients: {', '.join(ingredients)}
        Pantry staples available: {self.pantry_staples}

        Provide smart substitutions for missing ingredients, and a detailed nutritional breakdown.
        Format EXACTLY like this JSON:
        {{
            "substitutions": [
                {{"ingredient": "Missing item", "substitute": "Suggested substitute", "reason": "Why it works"}}
            ],
            "nutrition_insights": "A short 2-sentence summary of the health benefits.",
            "macros": {{ "calories": 450, "protein": 25, "carbs": 40, "fats": 20 }}
        }}
        """
        return await self._safe_json_call(prompt, system_prompt)

    async def chat(self, messages: list) -> str:
        """Handles conversational cooking assistant queries."""
        if not self.api_key:
            return "AI Chat is currently unavailable due to missing API keys."
            
        try:
            # Inject system prompt at the beginning
            formatted_messages = [
                {"role": "system", "content": f"You are Ingredia AI, a helpful, friendly, expert culinary and nutrition assistant. You know the user has these pantry staples: {self.pantry_staples}. Keep answers concise and formatting clean."}
            ]
            
            # Append user history
            for msg in messages:
                formatted_messages.append({
                    "role": msg.get("role", "user"),
                    "content": msg.get("content", "")
                })

            response = await self.client.chat.completions.create(
                model=self.model,
                messages=formatted_messages,
                temperature=0.7,
            )
            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"Chat Error: {str(e)}")
            return "I'm sorry, I'm having trouble thinking right now. Please try again later."

llm_service = LLMService()
