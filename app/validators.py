from sqlalchemy.orm import Session
from responses import bad_request


class BaseValidator:
    """
    Basic class for validation.
    _validation_mapping method should be 
    oveeride in each child class and return
    a dictionary
    """
    def __init__(
            self, db: Session,
            data: object,
            fields: list|None = None
        ) -> None:
        self._db = db
        self._data = data
        self.__fields = fields

    def _validation_mapping(self):
        """
        Return validation handler mapping
        """
        pass

    def __validation_field_mapping(self, field):
        """
        Return appropriate validation according fields
        """
        if field in self._validation_mapping():
            return self._validation_mapping()[field]        
    
    def validate(self):
        """
        Return Json response with 400 status
        code if any validation error occures
        """
        fields = (
            self.__fields
            if self.__fields or self.__fields.__class__.__name__!="NoneType"
            else self._validation_mapping().keys()
        )
        errors = {}
        for field in fields:
            handler = self.__validation_field_mapping(field)
            exc = handler()
            if exc:
                errors.update(exc)
        if errors:
            return bad_request(message="Invalid input", errors=errors)
   