import enum

class UserRole(enum.Enum):
    DEV = 0
    SM = 1
    PO = 2

class TaskStatus(enum.Enum):
    TODO = 0
    ONGOING = 1
    DONE = 2