from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import SessionLocal
from app.db.models import CookingHistory
from app.utils.auth_dependency import get_current_user

router = APIRouter(prefix="/history", tags=["Cooking History"])


@router.post("/{recipe_id}")
def add_to_history(
    recipe_id: int,
    current_user=Depends(get_current_user)
):
    db: Session = SessionLocal()

    entry = CookingHistory(
        user_id=current_user.id,
        recipe_id=recipe_id
    )

    db.add(entry)
    db.commit()
    db.close()

    return {"message": "Recipe added to cooking history"}


@router.get("/")
def get_history(current_user=Depends(get_current_user)):
    db: Session = SessionLocal()

    history = db.query(CookingHistory).filter(
        CookingHistory.user_id == current_user.id
    ).all()

    db.close()
    return history
