from enum import Enum


class Status(Enum):
    A = 'active'
    I = 'inactive'
    D = 'deleted'
    P = 'pending'
    S = 'suspended'
    T = 'terminated'
