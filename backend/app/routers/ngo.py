from fastapi import APIRouter, Depends, HTTPException, status
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from typing import List
from app.core.config import settings
from app.database import SessionLocal
from app import models, schemas
from app.routers.auth import oauth2_scheme, get_db

router = APIRouter(prefix="/ngo")

async def get_current_ngo(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username: str = payload.get("sub")
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    user = db.query(models.User).filter(models.User.username == username, models.User.is_ngo == 1).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not an NGO user")
    return user

@router.post("/profile", response_model=schemas.NGOProfile)
def upsert_profile(profile: schemas.NGOProfileCreate,
                   user: models.User = Depends(get_current_ngo),
                   db: Session = Depends(get_db)):
    existing = db.query(models.NGOProfile).filter(models.NGOProfile.user_id == user.id).first()
    if existing:
        existing.name, existing.description = profile.name, profile.description
    else:
        existing = models.NGOProfile(user_id=user.id, **profile.dict())
        db.add(existing)
    db.commit(); db.refresh(existing)
    return existing

@router.post("/opportunities", response_model=schemas.Opportunity)
def create_opportunity(opp: schemas.OpportunityCreate,
                       user: models.User = Depends(get_current_ngo),
                       db: Session = Depends(get_db)):
    prof = db.query(models.NGOProfile).filter(models.NGOProfile.user_id == user.id).first()
    if not prof:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Set up NGO profile first")
    new_opp = models.Opportunity(ngo_id=prof.id, **opp.dict())
    db.add(new_opp); db.commit(); db.refresh(new_opp)
    return new_opp

@router.get("/opportunities", response_model=List[schemas.Opportunity])
def list_opps(user: models.User = Depends(get_current_ngo), db: Session = Depends(get_db)):
    prof = db.query(models.NGOProfile).filter(models.NGOProfile.user_id == user.id).first()
    return db.query(models.Opportunity).filter(models.Opportunity.ngo_id == prof.id).all()

@router.get("/opportunities/{opp_id}/candidates", response_model=List[schemas.Application])
def list_candidates(opp_id: int,
                    user: models.User = Depends(get_current_ngo),
                    db: Session = Depends(get_db)):
    opp = db.query(models.Opportunity).filter(
        models.Opportunity.id == opp_id,
        models.Opportunity.ngo_id == db.query(models.NGOProfile.id).filter(models.NGOProfile.user_id == user.id)
    ).first()
    if not opp:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
    return db.query(models.Application).filter(models.Application.opportunity_id == opp_id).all()

@router.post("/opportunities/{opp_id}/candidates/{app_id}", response_model=schemas.Application)
def update_status(opp_id: int,
                  app_id: int,
                  update: schemas.ApplicationStatusUpdate,
                  user: models.User = Depends(get_current_ngo),
                  db: Session = Depends(get_db)):
    app_obj = db.query(models.Application).join(models.Opportunity).filter(
        models.Application.id == app_id,
        models.Opportunity.id == opp_id,
        models.Opportunity.ngo.has(user_id=user.id)
    ).first()
    if not app_obj:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Application not found")
    app_obj.status = update.status; db.commit(); db.refresh(app_obj)
    return app_obj
