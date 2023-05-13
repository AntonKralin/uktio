from enum import Enum

class UserType(Enum):
    SUPERUSER = 1
    REGIONADMIN = 2
    ORGADMIN = 3
    REGIONVIEW = 4
    ORGVIEW = 5