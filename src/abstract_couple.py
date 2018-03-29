from abc import ABCMeta, abstractmethod


class AbstractCouple(metaclass=ABCMeta):
    """Abstract couple base class."""

    def __init__(self, person1, person2, person3=None):
        self.person1 = person1
        self.person2 = person2
        self.person3 = person3
        self.persons = [person1, person2] if self.person3 is None else [person1, person2, person3]

        # Default
        self.will_breakup = False

        # Will only be initialized if couple wants children
        self.desired_num_of_children = -1
        self.desired_children_left = 10  # Must be any positive number
        self.expecting_num_of_children = -1

        # Dates for possible future relationship goals
        self.breakup_date = -1
        self.marriage_date = -1
        self.pregnancy_date = -1
        self.adoption_process_date = -1
        self.birth_date = -1
        self.adoption_date = -1

    # OVERRIDDEN PROPERTIES

    @property
    def is_straight(self):
        return False

    @property
    def is_throuple(self):
        return False

    @property
    def is_consang(self):
        return False

    @property
    def can_get_married(self):
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

    # SHARED READ-ONLY NON-ABSTRACT PROPERTIES

    @property
    def is_intergenerational(self):
        """Returns true if couple's age difference is at least X years."""
        return abs(self.oldest.age - self.youngest.age) >= 20

    @property
    def oldest(self):
        """Returns oldest person in couple."""
        return next(person for person in self.persons if person.age == self.get_oldest_age)

    @property
    def youngest(self):
        """Returns youngest person in couple."""
        return next(person for person in self.persons if person.age == self.get_youngest_age)

    @property
    def is_breakup_date(self):
        """Returns true if oldest person in couple has reached breakup date."""
        return self.oldest.age == self.breakup_date

    # HELPER METHODS

    @property
    def get_oldest_age(self):
        """Returns oldest person's age in couple."""
        return max(person.age for person in self.persons)

    @property
    def get_youngest_age(self):
        """Returns youngest person's age in couple."""
        return min(person.age for person in self.persons)

    # CHILDREN HELPER METHODS

    @property
    def will_have_children(self):
        if any([p.has_max_num_of_children for p in self.persons]) or self.has_desired_children or self.is_pregnant or self.birth_date > self.oldest.age:
            return False
        return self.can_and_wants_bio_or_adopted_children

    @property
    def has_desired_children(self):
        """Returns true if couple's had all desired children."""
        return any([p.wants_children is False for p in self.persons]) or self.desired_children_left <= 0

    @property
    def can_and_wants_bio_or_adopted_children(self):
        """Returns true if couple can and want to have biological or adopted children."""
        return self.is_within_having_children_span and \
               (self.will_get_pregnant or self.will_adopt)

    @property
    def is_within_having_children_span(self):
        """Returns true if valid timespan for having children."""
        timespan = self.having_children_timespan
        return timespan is not None and len(timespan) > 0

    @property
    def having_children_timespan(self):
        """Returns the range of years between person's age and young adult's stage end."""
        if self.oldest.is_young_adult is False:
            return None
        if self.will_get_married:
            return range(self.marriage_date + 1, self.oldest.stage.end)
        return self.oldest.span_left_till_next_stage

    @property
    def all_can_and_want_children(self):
        """Returns true if all persons can have biological children and want to."""
        return all([p.can_and_wants_bio_children for p in self.persons])

    @property
    def all_want_children_but_cant(self):
        """Returns true if all persons want children but at least one of them can't."""
        if all([p.wants_children for p in self.persons]):
            return any([p.cant_but_wants_children for p in self.persons])
        return False

    # ADOPTION HELPER METHODS

    @property
    def will_adopt(self):
        return self.is_in_adoption_process is False and self.has_desired_children is False and self.all_want_children_but_cant

    @property
    def is_adoption_process_date(self):
        return self.oldest.age == self.adoption_process_date

    @property
    def is_in_adoption_process(self):
        return all([p.is_in_adoption_process for p in self.persons])

    @property
    def is_adoption_date(self):
        return self.oldest.age == self.adoption_date


class AbstractMarriableCouple(AbstractCouple, metaclass=ABCMeta):
    """Abstract marriable couple base class."""

    @property
    def can_get_married(self):
        return True

    @property
    @abstractmethod
    def will_get_married(self):
        if self.is_married or any([p.is_married_or_remarried for p in self.persons]) or \
                len(self.oldest.span_left_till_old_age) <= 1:
            return False
        return self.can_get_married and all([p.wants_marriage for p in self.persons])

    @property
    @abstractmethod
    def is_marriage_date(self):
        return self.oldest.age == self.marriage_date

    @property
    @abstractmethod
    def is_married(self):
        return all([p.is_married_or_remarried for p in self.persons]) and self.person2 in self.person1.spouses


class AbstractFertileCouple(AbstractCouple, metaclass=ABCMeta):
    """Abstract fertile couple base class."""

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
