from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app import models
from app.auth import (
    hash_password, verify_password, create_access_token,
    require_admin, require_volunteer
)
from app.email import send_signup_email, send_approval_email
from pydantic import BaseModel
from typing import Optional

router = APIRouter()

# --- Pydantic Schemas ---

class VolunteerSignup(BaseModel):
    full_name: str
    email: str
    phone: str
    city: str
    skills: Optional[str] = None
    password: str
    wants_to_contribute: Optional[bool] = False

class VolunteerLogin(BaseModel):
    email: str
    password: str

class AdminLogin(BaseModel):
    username: str
    password: str

# --- Volunteer Routes ---

@router.post("/volunteer/signup")
async def volunteer_signup(data: VolunteerSignup, db: Session = Depends(get_db)):
    existing = db.query(models.Volunteer).filter(models.Volunteer.email == data.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    new_volunteer = models.Volunteer(
        full_name=data.full_name,
        email=data.email,
        phone=data.phone,
        city=data.city,
        skills=data.skills,
        password=hash_password(data.password),
        wants_to_contribute=data.wants_to_contribute
    )
    db.add(new_volunteer)
    db.commit()
    db.refresh(new_volunteer)
    try:
        await send_signup_email(data.email, data.full_name)
    except Exception as e:
        print(f"Email error: {e}")
    return {"message": "Thank you for joining ActionMysuru! Your application is under review."}

@router.post("/volunteer/login")
def volunteer_login(data: VolunteerLogin, db: Session = Depends(get_db)):
    volunteer = db.query(models.Volunteer).filter(models.Volunteer.email == data.email).first()
    if not volunteer or not verify_password(data.password, volunteer.password):
        raise HTTPException(status_code=401, detail="Invalid email or password")
    if not volunteer.is_approved:
        raise HTTPException(status_code=403, detail="Your application is pending approval")
    token = create_access_token({"sub": volunteer.email, "role": "volunteer"})
    return {"access_token": token, "token_type": "bearer"}

@router.get("/volunteer/me")
def volunteer_dashboard(current_user: dict = Depends(require_volunteer), db: Session = Depends(get_db)):
    volunteer = db.query(models.Volunteer).filter(models.Volunteer.email == current_user["sub"]).first()
    return {
        "full_name": volunteer.full_name,
        "email": volunteer.email,
        "city": volunteer.city,
        "skills": volunteer.skills,
        "is_approved": volunteer.is_approved,
        "wants_to_contribute": volunteer.wants_to_contribute
    }

# --- Admin Routes ---

@router.post("/admin/login")
def admin_login(data: AdminLogin, db: Session = Depends(get_db)):
    admin = db.query(models.Admin).filter(models.Admin.username == data.username).first()
    if not admin or not verify_password(data.password, admin.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_access_token({"sub": admin.username, "role": "admin"})
    return {"access_token": token, "token_type": "bearer"}

@router.get("/admin/volunteers")
def get_all_volunteers(
    current_user: dict = Depends(require_admin),
    db: Session = Depends(get_db)
):
    volunteers = db.query(models.Volunteer).all()
    return volunteers

@router.get("/admin/contributors")
def get_contributors(
    current_user: dict = Depends(require_admin),
    db: Session = Depends(get_db)
):
    contributors = db.query(models.Volunteer).filter(models.Volunteer.wants_to_contribute == True).all()
    return contributors

@router.patch("/admin/volunteers/{volunteer_id}/approve")
async def approve_volunteer(
    volunteer_id: int,
    current_user: dict = Depends(require_admin),
    db: Session = Depends(get_db)
):
    volunteer = db.query(models.Volunteer).filter(models.Volunteer.id == volunteer_id).first()
    if not volunteer:
        raise HTTPException(status_code=404, detail="Volunteer not found")
    volunteer.is_approved = True
    db.commit()
    try:
        await send_approval_email(volunteer.email, volunteer.full_name)
    except Exception as e:
        print(f"Email error: {e}")
    return {"message": f"{volunteer.full_name} has been approved"}

@router.patch("/admin/volunteers/{volunteer_id}/revoke")
async def revoke_volunteer(
    volunteer_id: int,
    current_user: dict = Depends(require_admin),
    db: Session = Depends(get_db)
):
    volunteer = db.query(models.Volunteer).filter(models.Volunteer.id == volunteer_id).first()
    if not volunteer:
        raise HTTPException(status_code=404, detail="Volunteer not found")
    volunteer.is_approved = False
    db.commit()
    return {"message": f"{volunteer.full_name}'s approval has been revoked"}

@router.delete("/admin/volunteers/{volunteer_id}")
def delete_volunteer(
    volunteer_id: int,
    current_user: dict = Depends(require_admin),
    db: Session = Depends(get_db)
):
    volunteer = db.query(models.Volunteer).filter(models.Volunteer.id == volunteer_id).first()
    if not volunteer:
        raise HTTPException(status_code=404, detail="Volunteer not found")
    db.delete(volunteer)
    db.commit()
    return {"message": "Volunteer deleted successfully"}