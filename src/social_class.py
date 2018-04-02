from abc import ABCMeta


class AbstractSocialClass(metaclass=ABCMeta):
    """Abstract base class for social class."""

    def __init__(self):
        self.name = ""
        self.rank = -1
        self.total_salary_min = 0
        self.total_salary_max = 0

    def belongs_to(self, total_salary):
        """Returns the social class that belongs to given salary."""
        return total_salary in range(self.total_salary_min, self.total_salary_max + 1)


class UpperClass(AbstractSocialClass):
    """Rich people."""

    def __init__(self):
        super().__init__()
        self.name = "Upper class"
        self.rank = 3
        self.total_salary_min = 389436
        self.total_salary_max = 99999999


class MiddleClass(AbstractSocialClass):
    """Average / Working class."""

    def __init__(self):
        super().__init__()
        self.name = "Middle class"
        self.rank = 2
        self.total_salary_min = 162354
        self.total_salary_max = 389435


class LowerClass(AbstractSocialClass):
    """Poor people."""

    def __init__(self):
        super().__init__()
        self.name = "Lower class"
        self.rank = 1
        self.total_salary_min = 0
        self.total_salary_max = 162353
