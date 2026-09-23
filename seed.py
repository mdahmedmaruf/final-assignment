from auth import hash_password
from database import Base, SessionLocal, engine
from models import User, UserRole

Base.metadata.create_all(bind=engine)


def seed_demo_user():
    db = SessionLocal()

    try:
        demo_user = [
            {
                "full_name": "Demo Admin",
                "email": "admin@example.com",
                "phone": "+8801914642486",
                "password": "password123",
                "role": UserRole.ADMIN,
            },
            {
                "full_name": "Demo Rider",
                "email": "rider@example.com",
                "phone": "+8801682664379",
                "password": "password123",
                "role": UserRole.RIDER,
            },
            {
                "full_name": "Demo Customer",
                "email": "customer@example.com",
                "phone": "+8801821740717",
                "password": "password123",
                "role": UserRole.CUSTOMER,
            },
        ]

        for user_data in demo_user:
            existing_user = (
                db.query(User).filter(User.email == user_data["email"]).first()
            )
            if not existing_user:
                new_user = User(
                    full_name=user_data["full_name"],
                    email=user_data["email"],
                    phone=user_data["phone"],
                    hashed_password=hash_password(user_data["password"]),
                    role=user_data["role"],
                )
                db.add(new_user)
                print(f"Created: {user_data['full_name']} {user_data['role'].value}")
            else:
                print(f"Skipped: {user_data['email']} already exists")

        db.commit()
        print("\nDemo users seeded successfully!")
    except Exception as e:
        db.rollback()
        print(f"Error seeding users: {e}")
    finally:
        db.close()


if __name__ == "__main__":
    seed_demo_user()
