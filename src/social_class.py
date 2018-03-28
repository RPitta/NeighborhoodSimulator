from abc import ABCMeta, abstractmethod


class AbstractSocialClass(metaclass=ABCMeta):
    """Abstract base class for social class."""

    def __init__(self):
        self.name = ""
        self.rank = -1


class UpperClass(AbstractSocialClass):
    """Rich people."""

    def __init__(self):
        super().__init__()
        self.name = "Upper class"
        self.rank = 3


class MiddleClass(AbstractSocialClass):
    """Average / Working class."""

    def __init__(self):
        super().__init__()
        self.name = "Middle class"
        self.rank = 2


class LowerClass(AbstractSocialClass):
    """Poor people."""

    def __init__(self):
        super().__init__()
        self.name = "Lower class"
        self.rank = 1

