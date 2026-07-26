from fastapi import APIRouter, HTTPException
from app.services.recipe_service import get_recipe_by_name

router = APIRouter(prefix="/recipes", tags=["Recipes"])

@router.get("/{name}")
def recipe_detail(name: str):
    recipe = get_recipe_by_name(name)
    if not recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")
    return recipe
