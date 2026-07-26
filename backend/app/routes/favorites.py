from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.db.database import SessionLocal
from app.db.models import Favorite
from app.utils.auth_dependency import get_current_user

router = APIRouter(prefix="/favorites", tags=["Favorites"])

@router.post("/{recipe_id}")
def toggle_favorite(recipe_id: int, current_user=Depends(get_current_user)):
    """
    Atomic Favorites Toggle Endpoint:
    - If recipe is not favorited -> Add to favorites (favorited: True)
    - If recipe is already favorited -> Remove from favorites (favorited: False)
    """
    db: Session = SessionLocal()
    try:
        existing_fav = db.query(Favorite).filter(
            Favorite.user_id == current_user.id,
            Favorite.recipe_id == recipe_id
        ).first()

        if existing_fav:
            db.delete(existing_fav)
            db.commit()
            return {
                "success": True,
                "favorited": False,
                "message": "Recipe removed from favorites"
            }
        else:
            fav = Favorite(user_id=current_user.id, recipe_id=recipe_id)
            db.add(fav)
            db.commit()
            return {
                "success": True,
                "favorited": True,
                "message": "Recipe added to favorites"
            }
    except IntegrityError:
        db.rollback()
        # Handle race condition if unique constraint triggers
        return {
            "success": True,
            "favorited": True,
            "message": "Recipe is already in favorites"
        }
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to update favorite: {str(e)}")
    finally:
        db.close()

@router.delete("/{recipe_id}")
def remove_favorite(recipe_id: int, current_user=Depends(get_current_user)):
    """Idempotent delete endpoint for removing a favorite."""
    db: Session = SessionLocal()
    try:
        existing_fav = db.query(Favorite).filter(
            Favorite.user_id == current_user.id,
            Favorite.recipe_id == recipe_id
        ).first()

        if existing_fav:
            db.delete(existing_fav)
            db.commit()

        return {
            "success": True,
            "favorited": False,
            "message": "Recipe removed from favorites"
        }
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to remove favorite: {str(e)}")
    finally:
        db.close()

@router.get("/")
def list_favorites(current_user=Depends(get_current_user)):
    """Fetch all favorited recipes for the current user."""
    db: Session = SessionLocal()
    try:
        favorites = db.query(Favorite).filter(
            Favorite.user_id == current_user.id
        ).all()
        return favorites
    finally:
        db.close()

