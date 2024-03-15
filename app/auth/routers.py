from dependencies import get_db
from fastapi import (
    APIRouter,
    Depends,
    status,
    UploadFile,
    Form,
    Request
)
from pydantic import EmailStr
from sqlalchemy import or_
from sqlalchemy.orm import Session
from responses import bad_request
from typing_extensions import Annotated
from utils import PasswordHashing, FileSystem, get_absolute_url
from dependencies import get_current_user
from .jwt_authentication import JwtAuthentication
from models import User
from .schemas import (
    UserCreateSchema,
    UserSchema,
    UserPasswordLoginSchema,
    RefreshTokenSchema
)
from .validators import UserValidator
import time


router = APIRouter(tags=["Authentication"])


@router.post("/refresh", status_code=status.HTTP_200_OK)
def create_access_from_refresh(body: RefreshTokenSchema):
    try:
        jwt_obj = JwtAuthentication()
        data = jwt_obj.decode_refresh_token(body.refresh)
        is_valid = (
            data["exp"] >= time.time()
            and data["token_type"]=="refresh"
        )
        if is_valid:
            data = {"user_id": data["user_id"]}
            return {"access": jwt_obj.create_access_token(data)}
        return bad_request(
            "Invalid token or expired token",
            status.HTTP_401_UNAUTHORIZED
        )
    except Exception as e:
        return bad_request(str(e))


@router.get("/profile", response_model=UserSchema)
def profile(
    user_id: Annotated[int, Depends(get_current_user)],
    db: Annotated[Session, Depends(get_db)],
    request: Request
):
    try:
        user = db.query(User).filter(User.id==user_id).first()
        if user.profile_pic:
            user.profile_pic = get_absolute_url(request, user.profile_pic)
        return user
    except Exception as e:
        return bad_request(str(e))


@router.post("/register", response_model=UserSchema)
def register(
    *,
    username: Annotated[str, Form(...)],
    name: str = Form(...),
    email: EmailStr = Form(...),
    mobile: str = Form(min_length=10, max_length=10),
    password: str = Form(min_length=8),
    profile_pic: UploadFile = None,
    db: Session = Depends(get_db),
    request: Request
):
    try:
        data = UserCreateSchema(
            username=username,
            name=name,
            email=email,
            mobile=mobile,
            password=password,
        )
        password = data.password
        pw = PasswordHashing(password)
        hashed = pw.get_password()
        data.password = hashed
        data.username = data.username.lower()
        errors = UserValidator(db, data).validate()
        if errors:
            return errors
        if profile_pic:
            fs = FileSystem(profile_pic, "profiles")
            file_name = fs.check_for_save()
            data.profile_pic = file_name
        user = User(**data.model_dump())
        db.add(user)
        db.commit()
        if profile_pic:
            fs.save()
        db.refresh(user)
        if user.profile_pic:
            user.profile_pic = get_absolute_url(request, user.profile_pic)
        return user
    except Exception as e:
        return bad_request(str(e))


@router.post("/password-login", status_code=status.HTTP_200_OK)
def login(data: UserPasswordLoginSchema, db: Session = Depends(get_db)):
    try:
        password = data.password
        pw = PasswordHashing(password)
        hashed_password = pw.get_password()
        user = db.query(User).filter(
            or_(User.username==data.username, User.email==data.username),
            User.password==hashed_password
        ).first()
        if user:
            data = {"user_id": user.id}
            jwt_obj = JwtAuthentication()
            response = {
                "access": jwt_obj.create_access_token(data),
                "refresh": jwt_obj.create_refresh_token(data)
            }
            return response
        return bad_request("Invalid Credentials")
    except Exception as e:
        return bad_request(str(e))