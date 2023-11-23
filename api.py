from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, Column, BigInteger, DateTime, Text
from sqlalchemy.orm import declarative_base, sessionmaker
from cachetools import cached, TTLCache
from pydantic import BaseModel
from typing import Optional

# Create a FastAPI app
app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create a SQLAlchemy engine and session
SQLALCHEMY_DATABASE_URI = (
    "mysql+pymysql://sql12647981:XM51KVKzDA@sql12.freemysqlhosting.net:3306/sql12647981"
)
engine = create_engine(SQLALCHEMY_DATABASE_URI)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


# Define the User model
class User(Base):
    __tablename__ = "users"
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    deleted_at = Column(DateTime, index=True)
    name = Column(Text(collation="latin1_swedish_ci"))
    email = Column(Text(collation="latin1_swedish_ci"))
    password = Column(Text(collation="latin1_swedish_ci"))
    college_name = Column(Text(collation="latin1_swedish_ci"))
    phone_number = Column(Text(collation="latin1_swedish_ci"))
    gender = Column(Text(collation="latin1_swedish_ci"))
    course = Column(Text(collation="latin1_swedish_ci"))
    specialization = Column(Text(collation="latin1_swedish_ci"))
    skills = Column(Text(collation="latin1_swedish_ci"))
    linkedin = Column(Text(collation="latin1_swedish_ci"))
    github = Column(Text(collation="latin1_swedish_ci"))
    behance = Column(Text(collation="latin1_swedish_ci"))


# Pydantic model for request data
class UserProfileUpdate(BaseModel):
    email: str
    name: Optional[str] = None
    phone_number: Optional[str] = None
    college_name: Optional[str] = None
    gender: Optional[str] = None
    course: Optional[str] = None
    specialization: Optional[str] = None
    skills: Optional[str] = None
    linkedin: Optional[str] = None
    github: Optional[str] = None
    behance: Optional[str] = None


# Cache configuration
cache = TTLCache(maxsize=100, ttl=60)  # Adjust ttl as needed


# Cached function to get user profile
@cached(cache)
def get_user_profile(email: str):
    # Fetch user from the database
    user = SessionLocal().query(User).filter_by(email=email).first()
    if user:
        return {
            "id": user.id,
            "created_at": user.created_at,
            "name": user.name,
            "email": user.email,
            "phone_number": user.phone_number,
            "gender": user.gender,
            "course": user.course,
            "specialization": user.specialization,
            "skills": user.skills,
            "linkedin": user.linkedin,
            "github": user.github,
            "behance": user.behance,
        }
    else:
        raise HTTPException(status_code=404, detail="User not found")


# FastAPI endpoint for user profile
@app.get("/profile")
async def get_profile(email: str):
    return get_user_profile(email)


# FastAPI endpoint for updating user profile
@app.post("/profile")
async def update_profile(data: UserProfileUpdate):
    user = SessionLocal().query(User).filter_by(email=data.email).first()
    if user:
        if data.name:
            user.name = data.name
        if data.phone_number:
            user.phone_number = data.phone_number
        if data.college_name:
            user.college_name = data.college_name
        if data.gender:
            user.gender = data.gender
        if data.course:
            user.course = data.course
        if data.specialization:
            user.specialization = data.specialization
        if data.skills:
            user.skills = data.skills
        if data.linkedin:
            user.linkedin = data.linkedin
        if data.github:
            user.github = data.github
        if data.behance:
            user.behance = data.behance

        # Commit changes to the database
        SessionLocal().commit()

        # Clear the cache for the updated user
        cache.pop(data.email, None)

        return {"message": "Profile updated successfully"}
    else:
        raise HTTPException(status_code=404, detail="User not found")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=5000)
