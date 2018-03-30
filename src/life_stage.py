from abc import ABCMeta, abstractmethod


class AbstractLifeStage(metaclass=ABCMeta):
    """Life stage base abstract superclass."""

    def __init__(self):
        self.stage = None
        self._start = None
        self._end = None
        self._span = list(range(0, 0))

    def __hash__(self):
        return 1

    def __eq__(self, other):
        """Override the default Equals behavior"""
        return self.stage == other.stage

    def __ne__(self, other):
        """Override the default Unequal behavior"""
        return self.stage != other.stage

    def __str__(self):
        return self.stage

    @property
    def start(self):
        return self._start

    @property
    def end(self):
        return self._end

    @property
    def span(self):
        return self._span

    @property
    @abstractmethod
    def next_stage(self):
        raise NotImplementedError


class Baby(AbstractLifeStage):
    """Baby life stage base class."""

    def __init__(self):
        super().__init__()
        self.stage = "Baby"
        self._start = 0
        self._end = 3
        self._span = list(range(self._start, self._end + 1))

    @property
    def next_stage(self):
        return Child()


class Child(AbstractLifeStage):
    """Child life stage base class."""

    def __init__(self):
        super().__init__()
        self.stage = "Child"
        self._start = 4
        self._end = 12
        self._span = list(range(self._start, self._end + 1))

    @property
    def next_stage(self):
        return Teen()


class Teen(AbstractLifeStage):
    """Teen life stage base class."""

    def __init__(self):
        super().__init__()
        self.stage = "Teen"
        self._start = 13
        self._end = 17
        self._span = list(range(self._start, self._end + 1))

    @property
    def next_stage(self):
        return YoungAdult()


class YoungAdult(AbstractLifeStage):
    """YoungAdult life stage base class."""

    def __init__(self):
        super().__init__()
        self.stage = "Young Adult"
        self._start = 18
        self._end = 39
        self._span = list(range(self._start, self._end + 1))

    @property
    def next_stage(self):
        return Adult()


class Adult(AbstractLifeStage):
    """Adult life stage base class."""

    def __init__(self):
        super().__init__()
        self.stage = "Adult"
        self._start = 40
        self._end = 59
        self._span = list(range(self._start, self._end + 1))

    @property
    def next_stage(self):
        return Senior()


class Senior(AbstractLifeStage):
    """Senior life stage base class."""

    def __init__(self):
        super().__init__()
        self.stage = "Senior"
        self._start = 60
        self._end = 79
        self._span = list(range(self._start, self._end + 1))

    @property
    def next_stage(self):
        return False
