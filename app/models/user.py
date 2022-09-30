from typing import Optional
from sqlmodel import Field
from .base import Base
from sqlalchemy import UniqueConstraint
from pydantic import EmailStr, validator


class UserBase(Base):
    email: EmailStr
    description: Optional[str] = None


class UserCreate(UserBase):
    pass


class User(UserBase, table=True):
    __tablename__ = "users"
    __table_args__ = (UniqueConstraint("email"),)

    id: int = Field(default=None, primary_key=True)

    @validator("email")
    def validate_email(cls, value):
        return value

    @validator("description")
    def validate_description(cls, value):
        return value


if __name__ == "__main__":
    print("test User")

    test_user = User(
        email="jdoe",  # oops this should be an email address
        description="John Doe",
    )

    print("User test_user: ", test_user)

    test_user_1 = User(
        email="jdoe@gmail.com",  # oops this should be an email address
        description="John Doe",
    )

    print("User test_user_1: ", test_user_1)

    test_user_2 = User.validate(
        {
            "email": "jdoe",
            "description": "John Doe",

        }
    )
    print("User test_user_2: ", test_user_2)
