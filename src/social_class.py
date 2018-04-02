from abc import ABCMeta


class AbstractSocialClass(metaclass=ABCMeta):
    """Abstract base class for social class."""


    def __init__(self):
        self.name = ""
        self.rank = -1
        self.avg_salary_min = 0

    def is_belonged_to(self, avg_salary):
        if avg_salary >= self.avg_salary_min:
            return True
        else:
            return False



class UpperClass(AbstractSocialClass):
    """Rich people."""

    def __init__(self):
        super().__init__()
        self.name = "Upper class"
        self.rank = 3
        self.avg_salary_min= 60000


class MiddleClass(AbstractSocialClass):
    """Average / Working class."""

    def __init__(self):
        super().__init__()
        self.name = "Middle class"
        self.rank = 2
        self.avg_salary_min = 35000

class LowerClass(AbstractSocialClass):
    """Poor people."""

    def __init__(self):
        super().__init__()
        self.name = "Lower class"
        self.rank = 1
        self.avg_salary_min = 0
