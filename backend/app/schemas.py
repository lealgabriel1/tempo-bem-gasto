from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List

class UserBase(BaseModel):
    username: str = Field(..., max_length=50)

class UserCreate(UserBase):
    password: str = Field(..., min_length=6)
    is_ngo: bool = Field(False, description="Escolher ONG (true) ou Voluntário (false)")

class User(UserBase):
    id: int
    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str

class NGOProfileBase(BaseModel):
    name: str
    description: Optional[str]

class TokenResponse(BaseModel):
    access_token: str
    token_type: str
    is_ngo: bool

class NGOProfileCreate(NGOProfileBase):
    pass

class NGOProfile(NGOProfileBase):
    id: int
    user_id: int
    class Config:
        orm_mode = True

class OpportunityBase(BaseModel):
    title: str
    description: Optional[str]
    location: Optional[str]

class OpportunityCreate(OpportunityBase):
    pass

class Opportunity(OpportunityBase):
    id: int
    ngo_id: int
    created_at: datetime
    class Config:
        orm_mode = True

class VolunteerProfileBase(BaseModel):
    full_name: str
    bio: Optional[str]

class VolunteerProfileCreate(VolunteerProfileBase):
    pass

class VolunteerProfile(VolunteerProfileBase):
    id: int
    user_id: int
    class Config:
        orm_mode = True

class ApplicationBase(BaseModel):
    opportunity_id: int

class ApplicationCreate(ApplicationBase):
    pass

class ApplicationStatusUpdate(BaseModel):
    status: str

class Application(ApplicationBase):
    id: int
    user_id: int
    status: str
    applied_at: datetime
    opportunity: Opportunity
    class Config:
        orm_mode = True
