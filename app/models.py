from database import Base
from datetime import datetime
import sqlalchemy as sa


class BaseModel(Base):
    __abstract__ = True
    is_active = sa.Column(sa.Boolean(), default=True)
    created_at = sa.Column(sa.DateTime(), default=datetime.utcnow)
    updated_at = sa.Column(
        sa.DateTime(),
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )


class User(BaseModel):
    __tablename__ = "user"
    id = sa.Column(sa.Integer, primary_key=True, unique=True)
    username = sa.Column(sa.String(200))
    name = sa.Column(sa.String(200), nullable=False)
    email = sa.Column(sa.String(200), unique=True)
    mobile = sa.Column(sa.String(10), unique=True)
    profile_pic = sa.Column(sa.String(200), nullable=True)
    password = sa.Column(sa.String(64))
    is_superuser = sa.Column(sa.Boolean(), default=False)
    is_staff = sa.Column(sa.Boolean(), default=False)