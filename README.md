# 📦 Courier Service API (FastAPI)

A comprehensive backend API for a modern Courier and Parcel Delivery Management Service built with **FastAPI**, **SQLAlchemy**, and **SQLite/PostgreSQL**.

---

## 🌟 Key Features

- 🔐 **Authentication & Authorization:** JWT-based OAuth2 authentication (using Email as login identity).
- 👥 **Role-Based Access Control (RBAC):**
    - **Admin:** Full user management (CRUD) and parcel assignment to riders.
    - **Rider:** View assigned delivery tasks and update delivery status.
    - **Customer:** Create parcel delivery requests and track their own parcels.
- 🚚 **Parcel Management:** Automated tracking number generation (`TRK-XXXXXXXX`) and real-time status updates (`PENDING` ➔ `APPROVED` ➔ `ASSIGNED` ➔ `ACCEPTED` ➔ `PICKED_UP` ➔ `OUT_FOR_DELIVERY` ➔ `DELIVERED` / `FAILED`).
- 🛠️ **Modular Architecture:** Clean file organization using `APIRouter` for scalable development.

---

## 🏗️ Project Structure

```text
.
├── auth.py                  # Core Authentication utilities (JWT, Password Hashing)
├── database.py              # Database connection and session setup
├── models.py                # SQLAlchemy ORM Models (User, Parcel)
├── schemas.py               # Pydantic Schemas for Request/Response validation
├── seed.py                  # Seeder script to populate initial demo data
├── main.py                  # FastAPI Application Entry Point
├── routers/
│   ├── authentication.py    # Public endpoints (Register, Login)
│   ├── admin.py             # Secured endpoints for Admin management
│   └── parcels.py           # Parcel creation, tracking, assignment & status updates
├── .env                     # Environment Variables
└── README.md
```
