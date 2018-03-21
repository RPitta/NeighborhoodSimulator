from abc import ABCMeta, abstractmethod


class AbstractCouple(metaclass=ABCMeta):

    def __init__(self, person1, person2, person3=None):
        self.person1 = person1
        self.person2 = person2
        self.person3 = person3

        if self.person3 is None:
            self.persons = [person1, person2]
        else:
            self.persons = [person1, person2, person3]

        # Default
        self.will_breakup = False
        # Will only be initialized if couple wants children
        self.desired_num_of_children = -1
        self.desired_children_left = 10  # Must be a positive number, any.
        self.expecting_num_of_children = -1
        # Dates for possible future relationship goals
        self.breakup_date = -1
        self.marriage_date = -1
        self.pregnancy_date = -1
        self.birth_date = -1
        self.adoption_date = -1
        self.adoption_process_date = -1

    # OVERRIDEN PROPERTIES

    @property
    def is_straight(self):
        """Overriden in Straight Couple"""
        return False

    @property
    def is_throuple(self):
        """Overriden in Throuple"""
        return False

    @property
    def is_consang(self):
        """Overriden in Consang Couple"""
        return False

    @property
    def can_get_married(self):
        """Overriden in Throuple and Consang Couple"""
        return False

    @property
    def is_adoption_process_date(self):
        return False

    @property
    def will_have_children(self):
        return False

    @property
    def will_adopt(self):
        return False

    @property
    def is_in_adoption_process(self):
        return False

    @property
    def can_and_wants_bio_or_adopted_children(self):
        return False

    @property
    def will_get_pregnant(self):
        return False

    @property
    def is_pregnancy_date(self):
        return False

    @property
    def is_pregnant(self):
        return False

    @property
    def is_within_pregnancy_span(self):
        return False

    @property
    def pregnancy_timespan(self):
        return False

    @property
    def will_get_married(self):
        return False

    @property
    def is_marriage_date(self):
        return False

    @property
    def is_married(self):
        return False

    @property
    def is_birth_date(self):
        return False

    @property
    def is_adoption_date(self):
        return False

    # SHARED READ-ONLY NON-ABSTRACT PROPERTIES

    @property
    def is_intergenerational(self):
        return abs(self.oldest.age - self.youngest.age) >= 20

    @property
    def oldest(self):
        return next(person for person in self.persons if person.age == self.get_oldest_age)

    @property
    def youngest(self):
        return next(person for person in self.persons if person.age == self.get_youngest_age)

    @property
    def is_breakup_date(self):
        return self.oldest.age == self.breakup_date

    @property
    def has_desired_children(self):
        if any([p.wants_children is False for p in self.persons]):
            return True
        return self.desired_children_left <= 0

    # HELPER METHODS

    @property
    def get_oldest_age(self):
        return max(person.age for person in self.persons)

    @property
    def get_youngest_age(self):
        return min(person.age for person in self.persons)

    @property
    def all_can_and_want_children(self):
        """Returs true if all persons can have biological children and want to."""
        return all([self.persons[0].can_and_wants_bio_children for p in self.persons])

    @property
    def all_want_children_but_cant(self):
        """Returns true if all persons want children but at least one of them can't."""
        if all([self.persons[0].wants_children for p in self.persons]):
            return any([self.persons[0].cant_but_wants_children for p in self.persons])
        return False


class AbstractMarriableCouple(AbstractCouple, metaclass=ABCMeta):

    @property
    def can_get_married(self):
        """Overriden in Throuple and Consang Couple"""
        return True

    @property
    @abstractmethod
    def will_get_married(self):
        raise NotImplementedError

    @property
    @abstractmethod
    def is_marriage_date(self):
        raise NotImplementedError

    @property
    @abstractmethod
    def is_married(self):
        raise NotImplementedError


class AbstractFertileCouple(AbstractCouple, metaclass=ABCMeta):

    @property
    @abstractmethod
    def pregnancy_timespan(self):
        raise NotImplementedError

    @property
    @abstractmethod
    def is_within_pregnancy_span(self):
        raise NotImplementedError

    @property
    @abstractmethod
    def will_get_pregnant(self):
        raise NotImplementedError

    @property
    @abstractmethod
    def is_pregnancy_date(self):
        raise NotImplementedError

    @property
    @abstractmethod
    def is_pregnant(self):
        raise NotImplementedError

    @property
    @abstractmethod
    def is_birth_date(self):
        raise NotImplementedError
