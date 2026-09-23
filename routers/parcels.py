import uuid
from typing import Annotated, List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from auth import get_current_user
from database import get_db
from models import Parcel, ParcelStatus, User, UserRole
from schemas import (
    ParcelAssign,
    ParcelCreate,
    ParcelResponse,
    ParcelStatusUpdate,
)

router = APIRouter(prefix="/api/parcels", tags=["parcel Management"])

db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[User, Depends(get_current_user)]


@router.get("", response_model=List[ParcelResponse])
def get_all_parcels(db: db_dependency, current_user: user_dependency):
    if UserRole(current_user.role) == UserRole.ADMIN:
        return db.query(Parcel).all()
    if UserRole(current_user.role) == UserRole.RIDER:
        return (
            db.query(Parcel).filter(Parcel.assigned_rider_id == current_user.id).all()
        )
    if UserRole(current_user.role) == UserRole.CUSTOMER:
        return db.query(Parcel).filter(Parcel.sender_id == current_user.id).all()

    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="User role not authorized to view parcels",
    )


@router.post("", response_model=ParcelResponse, status_code=status.HTTP_201_CREATED)
def create_parcel(
    parcel_data: ParcelCreate, db: db_dependency, current_user: user_dependency
):
    if UserRole(current_user.role) != UserRole.CUSTOMER:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only customers can request parcel delivery",
        )

    tracking_code = f"TRK-{uuid.uuid4().hex[:8].upper()}"
    new_parcel = Parcel(
        tracking_number=tracking_code,
        sender_id=current_user.id,
        receiver_name=parcel_data.receiver_name,
        receiver_phone=parcel_data.receiver_phone,
        delivery_address=parcel_data.delivery_address,
        description=parcel_data.description,
        weight_kg=parcel_data.weight_kg,
        status=ParcelStatus.PENDING,
    )

    db.add(new_parcel)
    db.commit()
    db.refresh(new_parcel)

    return new_parcel


@router.put("/{parcel_id}/approve", response_model=ParcelResponse)
def approve_parcel(parcel_id: int, db: db_dependency, current_user: user_dependency):
    if UserRole(current_user.role) != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admin can approve parcels",
        )

    parcel = db.query(Parcel).filter(Parcel.id == parcel_id).first()

    if not parcel:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Parcel not found"
        )

    if parcel.status is not ParcelStatus.PENDING:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"cannot approve parcel in status : [parcel.status]",
        )

    setattr(parcel, "status", ParcelStatus.APPROVED)
    db.commit()
    db.refresh(parcel)

    return parcel


@router.put("/{parcel_id}/assign", response_model=ParcelResponse)
def assign_rider(
    parcel_id: int, data: ParcelAssign, db: db_dependency, current_user: user_dependency
):
    if UserRole(current_user.role) != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Only admin can assign rider"
        )

    parcel = db.query(Parcel).filter(Parcel.id == parcel_id).first()
    if not parcel:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Parcel not found"
        )

    if parcel.status is not ParcelStatus.APPROVED:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only approved parcels can be assigned to rider",
        )

    rider = (
        db.query(User)
        .filter(User.id == data.rider_id, User.role == UserRole.RIDER)
        .first()
    )

    if not rider:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid rider id"
        )

    setattr(parcel, "assigned_rider_id", rider.id)
    setattr(parcel, "status", ParcelStatus.ASSIGNED)

    db.commit()
    db.refresh(parcel)

    return parcel


@router.put("/{parcel_id}/status", response_model=ParcelResponse)
def update_parcel_status(
    parcel_id: int,
    status_data: ParcelStatusUpdate,
    db: db_dependency,
    current_user: user_dependency,
):
    if UserRole(current_user.role) != UserRole.RIDER:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only riders can update delivery status",
        )

    parcel = (
        db.query(Parcel)
        .filter(Parcel.id == parcel_id, Parcel.assigned_rider_id == current_user.id)
        .first()
    )

    if not parcel:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Parcel not assign to you"
        )

    allowed_rider_statuses = [
        ParcelStatus.ACCEPTED,
        ParcelStatus.REJECTED,
        ParcelStatus.PICKED_UP,
        ParcelStatus.OUT_FOR_DELIVERY,
        ParcelStatus.DELIVERED,
        ParcelStatus.FAILED,
    ]

    if status_data.status not in allowed_rider_statuses:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid status update. Rider can only update status to: {[s.value for s in allowed_rider_statuses]}",
        )

    setattr(parcel, "status", status_data.status)

    db.commit()
    db.refresh(parcel)

    return parcel
