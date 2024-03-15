import hashlib
import config
import os
import shutil

from fastapi import HTTPException, Request, UploadFile


class PasswordHashing:
    """
    Utility class for hashing passwords using
    SHA256 and salt
    """

    def __init__(self, password) -> None:
        self.__password: str = password
        self.__salt: str = config.SECRET_KEY

    def __create_sha256_hash(self):
        """
        create 64 characters SHA256 hash value 
        represented in hexadecimal format
        """
        hash_obj = hashlib.sha256(
            (self.__salt + self.__password).encode()
        )
        return hash_obj.hexdigest()
    
    def get_password(self):
        """
        Return hashed password
        """
        return self.__create_sha256_hash()
    
    def check_password(self, hashed_password):
        """
        Return True if provided hash value
        mathes the hash value of excisting password.
        """
        return self.get_password() == hashed_password


def raise_exception(content: dict|str, status: int = 400):
    """
    Function for raise custom exceptions
    """
    raise HTTPException(
        detail=content,
        status_code=status
    )


def convert_host_url(request: Request):
    """
    This function converts the full request
    url to scheme://host:port/ format
    """
    scheme = request.url.scheme
    port = request.url.port
    host = request.url.hostname
    url = f"{scheme}://{host}{':'+str(port) if port else ''}"
    return url


def get_absolute_url(request: Request, file_name: str = None):
    """
    Return absolute url of the file
    """
    if not file_name:
        return None
    url = f"/{config.MEDIA_URL.strip('/')}/"
    media_url = convert_host_url(request=request) + url + file_name
    return media_url


class FileSystem:
    """
    Utility class for manage uploading
    files
    """

    def __init__(
        self,
        file: UploadFile,
        location: str = "",
        custom_name: str = ""
    ):
        self._file = file
        self._file_name = self._file.filename
        self._location = f"{location.strip('/')}/" if location else location
        self._root = f"/{config.MEDIA_ROOT.strip('/')}/"
        self._custom_name = custom_name
        self._is_checked = False
        if self._custom_name:
            ext = self._file.filename.split(".")[-1]
            self._file_name =  f"{self._custom_name}.{ext}"

    @property
    def _get_file_location(self):
        """
        return file path which is combination
        of location and root
        """
        return self._root + self._location
        
    @property
    def _get_destination(self):
        """
        return full path of file
        """
        return self._get_file_location + self._file_name

    @property
    def _get_file_path(self):
        """
        return file location and file name
        added together
        """
        return self._location + self._file_name
    
    def _create_location(self):
        """
        Check the provided location exist
        in media root. if not exists create
        that location in root
        """
        if not os.path.exists(self._get_file_location):
            os.makedirs(self._get_file_location, exist_ok=True)

    def _rename_file_if_already_exist(self):
        """
        rename file if the same file name
        already exists
        """
        count = 1
        while os.path.exists(self._get_destination):
            file_name, ext = self._file_name.split(".")
            self._file_name = f"{file_name}_{count}.{ext}"
            count += 1
    
    def check_for_save(self):
        """
        return the latest name available for file.
        This method should be called before calling save.
        """
        self._create_location()
        self._rename_file_if_already_exist()
        self._is_checked = True
        return self._get_file_path
    
    def save(self):
        """
        Save the file in to the file system
        """
        if self._is_checked:
            with open(self._get_destination, 'wb') as buffer:
                shutil.copyfileobj(self._file.file, buffer)
        else:
            raise_exception("Please call check_for_save method before save")

    @classmethod
    def remove_file(cls, filename):
        """
        Remove file from file system.
        """
        path = f"/{config.MEDIA_ROOT.strip('/')}/" + filename
        if os.path.exists(path) and os.path.isfile(path):
            os.remove(path)
