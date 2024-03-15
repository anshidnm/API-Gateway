from fastapi import Request, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt
from datetime import datetime, timedelta
from utils import raise_exception

import os
import time


class JwtAuthentication:
    """
    Class for utilies of jwt authentication.
    By default the expirey times are in seconds,
    Please use appropriate methods if need to
    convert to minutes, hours and days.
    """

    def __init__(self) -> None:
        self.__access_expiry = self.days(1)
        self.__refresh_expiry = self.days(5)
        self.__algorithm = os.getenv("JWT_ALGORITHM")
        self.__access_secret = os.getenv("ACCESS_SECRET")
        self.__refresh_secret = os.getenv("REFRESH_SECRET")

    def minutes(self, minutes: int):
        """
        Convert minutes to seconds
        """
        return minutes * 60

    def hours(self, hours: int):
        """
        Convert hours to seconds
        """
        return hours * 60 * 60

    def days(self, days: int):
        """
        Convert days to seconds
        """
        return days * 60 * 60 * 24

    def create_access_token(self, data: dict):
        """
        Return access token for user
        """
        expiry = datetime.utcnow() + timedelta(seconds=self.__access_expiry)
        data.update({"exp": expiry, "token_type": "access"})
        return jwt.encode(data, self.__access_secret, self.__algorithm)

    def create_refresh_token(self, data: dict):
        """
        Return refresh token for user
        """
        expiry = datetime.utcnow() + timedelta(seconds=self.__refresh_expiry)
        data.update({"exp": expiry, "token_type": "refresh"})
        return jwt.encode(data, self.__refresh_secret, self.__algorithm)
    
    def decode_access_token(self, token: str):
        """
        decode the jwt access token and return data
        """
        return jwt.decode(token, self.__access_secret, self.__algorithm)

    def decode_refresh_token(self, token: str):
        """
        decode the jwt refresh token and return data
        """
        return jwt.decode(token, self.__refresh_secret, self.__algorithm)


class JwtBearer(HTTPBearer):

    def __init__(self, auto_error: bool = True):
        super().__init__(auto_error=auto_error)
    
    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super().__call__(request)
        if credentials:
            if not credentials.scheme == "Bearer":
                raise_exception(
                    "Invalid authentication scheme",
                    status=status.HTTP_401_UNAUTHORIZED
                )
            if not self.verify_jwt(credentials.credentials):
                raise_exception(
                    "Invalid token or expired token",
                    status=status.HTTP_401_UNAUTHORIZED
                )
            return self.verify_jwt(credentials.credentials)
        else:           
            raise_exception(
                "Authentication credentials not provided",
                status=status.HTTP_401_UNAUTHORIZED
            )
    
    def verify_jwt(self, token):
        result = None
        try:
            data = JwtAuthentication().decode_access_token(token)
            is_valid = (data["exp"] >= time.time() and data["token_type"]=="access")
            if is_valid:
                result = data["user_id"]
        except:
            pass
        return result
