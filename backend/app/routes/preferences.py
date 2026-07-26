from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import SessionLocal
from app.db.models import UserPreference
from app.utils.auth_dependency import get_current_user

router = APIRouter(prefix="/preferences", tags=["Preferences"])


from typing import Optional
from pydantic import BaseModel

class PreferenceSchema(BaseModel):
    diet: Optional[str] = None
    allergies: Optional[str] = None
    disliked_ingredients: Optional[str] = None
    preferred_cuisines: Optional[str] = None
    calorie_limit: Optional[int] = None
    spice_level: Optional[str] = None

@router.post("/")
def save_preferences(
    data: PreferenceSchema,
    current_user=Depends(get_current_user)
):
    db: Session = SessionLocal()

    pref = db.query(UserPreference).filter(
        UserPreference.user_id == current_user.id
    ).first()

    if not pref:
        pref = UserPreference(user_id=current_user.id)

    pref.diet = data.diet
    pref.allergies = data.allergies
    pref.disliked_ingredients = data.disliked_ingredients
    pref.preferred_cuisines = data.preferred_cuisines
    pref.calorie_limit = data.calorie_limit
    pref.spice_level = data.spice_level

    db.add(pref)
    db.commit()
    db.refresh(pref)
    db.close()

    return {"message": "Preferences saved successfully", "preferences": pref}


@router.get("/")
def get_preferences(current_user=Depends(get_current_user)):
    db: Session = SessionLocal()

    pref = db.query(UserPreference).filter(
        UserPreference.user_id == current_user.id
    ).first()

    db.close()
    return pref
