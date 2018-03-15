
from abc import ABCMeta, abstractmethod, abstractproperty


class AbstractLifeStage:

    @property
    @abstractmethod
    def start(self):
        return

    @property
    @abstractmethod
    def end(self):
        return

    @property
    @abstractmethod
    def span(self):
        return

    @property
    @abstractmethod
    def is_of_age(self):
        return

    @property
    @abstractmethod
    def next_stage(self):
        return


class Baby(AbstractLifeStage):

    def __init__(self):
        self._name = "Baby"
        self._start = 1
        self._end = 3
        self._span = range(self._start, self._end)
        # Other baby specific attributes

    def __str__(self):
        return self._name

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
    def is_of_age(self):
        return False

    @property
    def next_stage(self):
        return Child()


class Child(AbstractLifeStage):

    def __init__(self):
        self._name = "Child"
        self._start = 4
        self._end = 12
        self._span = range(self._start, self._end)
        # Other child specific attributes

    def __str__(self):
        return self._name

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
    def is_of_age(self):
        return False

    @property
    def next_stage(self):
        return Teen()


class Teen(AbstractLifeStage):

    def __init__(self):
        self._name = "Teen"
        self._start = 13
        self._end = 17
        self._span = range(self._start, self._end)
        # Other teen specific attributes

    def __str__(self):
        return self._name

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
    def is_of_age(self):
        return False

    @property
    def next_stage(self):
        return YoungAdult()


class YoungAdult(AbstractLifeStage):

    def __init__(self):
        self._name = "Young Adult"
        self._start = 18
        self._end = 39
        self._span = range(self._start, self._end)
        # Other young adult specific attributes

    def __str__(self):
        return self._name

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
    def is_of_age(self):
        return True

    @property
    def next_stage(self):
        return Adult()


class Adult(AbstractLifeStage):

    def __init__(self):
        self._name = "Adult"
        self._start = 40
        self._end = 59
        self._span = range(self._start, self._end)
        # Other adult specific attributes

    def __str__(self):
        return self._name

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
    def is_of_age(self):
        return True

    @property
    def next_stage(self):
        return Senior()


class Senior(AbstractLifeStage):

    def __init__(self):
        self._name = "Senior"
        self._start = 60
        self._end = 79
        self._span = range(self._start, self._end)
        # Other senior specific attributes

    def __str__(self):
        return self._name

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
    def is_of_age(self):
        return True

    @property
    def next_stage(self):
        return False


class LifeStages:

    def __init__(self):
        self._life_stages = set()

    def life_stages(self):
        if self.life_stages is not None and len(self.life_stages) > 0:
            return [life_stage for life_stage in self._life_stages]

    def add(self, life_stage):
        self._life_stages.add(life_stage)
