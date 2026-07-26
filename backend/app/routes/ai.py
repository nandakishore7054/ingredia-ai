from fastapi import APIRouter, HTTPException
from typing import List, Dict, Any
from pydantic import BaseModel
from app.services.llm_service import llm_service

router = APIRouter(prefix="/ai", tags=["AI Integration"])

class PromptRequest(BaseModel):
    prompt: str

class SubsRequest(BaseModel):
    recipe_name: str
    ingredients: List[str]

class ChatRequest(BaseModel):
    messages: List[Dict[str, str]]

@router.post("/generate-prompt")
async def generate_from_prompt(request: PromptRequest):
    recipes = await llm_service.generate_from_prompt(request.prompt)
    if not recipes:
        raise HTTPException(status_code=500, detail="Failed to generate AI recipes.")
    return {"recipes": recipes}

@router.post("/substitutions")
async def get_substitutions(request: SubsRequest):
    data = await llm_service.analyze_nutrition_and_subs(request.recipe_name, request.ingredients)
    if not data:
        raise HTTPException(status_code=500, detail="Failed to analyze nutrition.")
    return data

@router.post("/chat")
async def chat_assistant(request: ChatRequest):
    response_text = await llm_service.chat(request.messages)
    return {"reply": response_text}
