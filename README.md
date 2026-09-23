---

### `README.md`

```markdown
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

---

## 🚀 Getting Started

### 1. Prerequisites

- Python 3.9+
- Virtual Environment tool (`venv`)

### 2. Installation & Setup

1. **Clone the repository:**

```bash
git clone [https://github.com/your-username/courier-service-api.git](https://github.com/your-username/courier-service-api.git)
cd courier-service-api

```

2. **Create and activate a virtual environment:**

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux / macOS
python3 -m venv venv
source venv/bin/activate

```

3. **Install dependencies:**

```bash
pip install fastapi uvicorn sqlalchemy passlib[bcrypt] python-jose[cryptography] python-dotenv pydantic[email]

```

4. **Set up Environment Variables (`.env`):**
   Create a `.env` file in the root directory:

```env
DATABASE_URL=sqlite:///./courier.db
SECRET_KEY=your_super_secret_jwt_key_here
ACCESS_TOKEN_EXPIRE_MINUTES=30

```

---

## 🗄️ Database Seeding (Demo Users)

Run the `seed.py` script to generate pre-configured demo users for all three roles (`ADMIN`, `RIDER`, `CUSTOMER`):

```bash
python seed.py

```

### 🔑 Demo Credentials:

| Role         | Email                  | Password      |
| ------------ | ---------------------- | ------------- |
| **Admin**    | `admin@example.com`    | `password123` |
| **Rider**    | `rider@example.com`    | `password123` |
| **Customer** | `customer@example.com` | `password123` |

---

## 🏃 Running the Application

Start the Uvicorn development server:

```bash
uvicorn main:app --reload

```

The API will be running at: **`http://127.0.0.1:8000`**

---

## 📖 API Documentation (Swagger UI)

FastAPI automatically generates interactive API documentation:

- **Interactive OpenAPI Documentation:** [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs?utm_source=gemini)
- **Alternative ReDoc Documentation:** [http://127.0.0.1:8000/redoc](https://www.google.com/search?q=http://127.0.0.1:8000/redoc&utm_source=gemini)

---

## 📌 API Endpoints Overview

### 🔑 Authentication

- `POST /auth/register` — Register a new Customer account.
- `POST /auth/login` — Login with Email & Password to receive a JWT Bearer Token.

### 👑 Admin Management

- `GET /api/admin/users/` — Get a list of all registered users.
- `POST /api/admin/users/` — Create new users with specific roles (Rider/Admin).
- `PUT /api/admin/users/{user_id}` — Update user profile or role.
- `DELETE /api/admin/users/{user_id}` — Remove a user account.

### 📦 Parcel Management

- `GET /api/parcels/` — Get parcels (Filtered automatically based on user role).
- `POST /api/parcels/` — Create a new parcel request (Customers only).
- `PUT /api/parcels/{parcel_id}/assign` — Assign a rider to a parcel (Admin only).
- `PUT /api/parcels/{parcel_id}/status` — Update delivery status (Assigned Rider only).

```

```
