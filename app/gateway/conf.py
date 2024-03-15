from dataclasses import dataclass


@dataclass
class Services:
    """
    Parent class for store all information
    abount each services included in system
    """

    name: str
    api_url: str