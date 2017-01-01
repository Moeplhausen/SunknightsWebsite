from enum import IntEnum,unique

@unique
class AjaxAction(IntEnum):
    GETTOURNAMENTS=1
    CREATETOURNAMENT=2
    EDITTOURNAMENT=3
    DELETETOURNAMENT=4

