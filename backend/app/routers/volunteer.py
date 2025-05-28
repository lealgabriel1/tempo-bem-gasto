from fastapi import APIRouter, Depends, HTTPException, status
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from typing import List, Optional
from app.core.config import settings
from app.database import SessionLocal
from app import models, schemas
from app.routers.auth import oauth2_scheme, get_db

router = APIRouter(prefix="/volunteer")

async def get_current_volunteer(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username: str = payload.get("sub")
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    user = db.query(models.User).filter(models.User.username == username, models.User.is_ngo == 0).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not a volunteer user")
    return user

@router.post("/profile", response_model=schemas.VolunteerProfile)
def upsert_volunteer(profile: schemas.VolunteerProfileCreate,
                     user: models.User = Depends(get_current_volunteer),
                     db: Session = Depends(get_db)):
    existing = db.query(models.VolunteerProfile).filter(models.VolunteerProfile.user_id == user.id).first()
    if existing:
        existing.full_name, existing.bio = profile.full_name, profile.bio
    else:
        existing = models.VolunteerProfile(user_id=user.id, **profile.dict())
        db.add(existing)
    db.commit(); db.refresh(existing)
    return existing

@router.get("/opportunities", response_model=List[schemas.Opportunity])
def feed(q: Optional[str] = None, user: models.User = Depends(get_current_volunteer), db: Session = Depends(get_db)):
    query = db.query(models.Opportunity)
    if q:
        query = query.filter(
            models.Opportunity.title.ilike(f"%{q}%") |
            models.Opportunity.location.ilike(f"%{q}%")
        )
    return query.order_by(models.Opportunity.created_at.desc()).all()

@router.get("/opportunities/{opp_id}", response_model=schemas.Opportunity)
def detail(opp_id: int, user: models.User = Depends(get_current_volunteer), db: Session = Depends(get_db)):
    opp = db.query(models.Opportunity).get(opp_id)
    if not opp:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
    return opp

@router.post("/opportunities/{opp_id}/apply", response_model=schemas.Application)
def apply(opp_id: int, user: models.User = Depends(get_current_volunteer), db: Session = Depends(get_db)):
    exists = db.query(models.Application).filter(
        models.Application.user_id == user.id,
        models.Application.opportunity_id == opp_id
    ).first()
    if exists:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Already applied")
    app_obj = models.Application(user_id=user.id, opportunity_id=opp_id)
    db.add(app_obj); db.commit(); db.refresh(app_obj)
    return app_obj

@router.get("/applications", response_model=List[schemas.Application])
def my_apps(user: models.User = Depends(get_current_volunteer), db: Session = Depends(get_db)):
    return db.query(models.Application).filter(models.Application.user_id == user.id).all()

@router.get("/applications/accepted", response_model=List[schemas.Application])
def accepted(user: models.User = Depends(get_current_volunteer), db: Session = Depends(get_db)):
    return db.query(models.Application).filter(
        models.Application.user_id == user.id,
        models.Application.status == "approved"
    ).all()
