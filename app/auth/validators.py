from validators import BaseValidator
from models import User


class UserValidator(BaseValidator):
    """
    Class for validate data during user creation
    or updation
    """

    def _validation_mapping(self):
        """
        Return validation handler mapping
        """
        validations = {
            "email": self.__is_email_exist,
            "username": self.__is_username_exist,
            "mobile": self.__is_mobile_exist,
        }
        return validations

    def __is_email_exist(self):
        """
        Verify the email already exist in db
        """
        if self._db.query(User).filter(User.email.ilike(self._data.email)).first():
            return {"email": "This email already exists"}
        
    def __is_username_exist(self):
        """
        Verify the username already exist in db
        """
        if self._db.query(User).filter(User.username.ilike(self._data.username)).first():
            return {"username": "This username already exists"}

    def __is_mobile_exist(self):
        """
        Verify the mobile already exist in db
        """
        if self._db.query(User).filter(User.mobile==self._data.mobile).first():
            return {"mobile": "This mobile already exists"}
    