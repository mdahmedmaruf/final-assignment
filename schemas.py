from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, EmailStr, Field

from models import ParcelStatus, UserRole


class UserCreate(BaseModel):
    full_name: str
    email: EmailStr
    phone: str
    password: str
    role: UserRole


class UserUpdate(BaseModel):
    full_name: Optional[str] = Field(default=None)
    email: Optional[EmailStr] = Field(default=None)
    phone: Optional[str] = Field(default=None)
    password: Optional[str] = Field(default=None)
    role: Optional[UserRole] = Field(default=None)


class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    full_name: str
    email: str
    phone: str
    role: UserRole
    created_at: datetime


class UserRegistration(BaseModel):
    full_name: str
    email: EmailStr
    phone: str
    password: str


class ParcelCreate(BaseModel):
    receiver_name: str
    receiver_phone: str
    delivery_address: str
    description: str
    weight_kg: float


class ParcelAssign(BaseModel):
    rider_id: int


class ParcelStatusUpdate(BaseModel):
    status: ParcelStatus


class SenderResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    full_name: str
    phone: str


class ParcelResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    tracking_number: str
    sender_id: int
    receiver_name: str
    receiver_phone: str
    delivery_address: str
    description: str
    weight_kg: float
    status: ParcelStatus
    assigned_rider_id: Optional[int]
    created_at: datetime
    updated_at: datetime
    sender: Optional[SenderResponse] = None
