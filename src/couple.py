from abstract_couple import AbstractCouple, AbstractMarriableCouple, AbstractFertileCouple


class StraightCouple(AbstractMarriableCouple, AbstractFertileCouple, AbstractCouple):
    """Straight couple base class."""

    def __init__(self, person1, person2):
        super().__init__(person1, person2)

    @property
    def is_straight(self):
        return True

    @property
    def man(self):
        return next((person for person in self.persons if person.is_male), None)

    @property
    def woman(self):
        return next((person for person in self.persons if person.is_female), None)

    # Relationship future goals

    @property
    def will_get_married(self):
        return super().will_get_married

    @property
    def is_marriage_date(self):
        return super().is_marriage_date

    @property
    def will_get_pregnant(self):
        return self.is_pregnant is False and self.has_desired_children is False and self.all_can_and_want_children

    @property
    def is_pregnancy_date(self):
        return self.oldest.age == self.pregnancy_date

    @property
    def is_birth_date(self):
        return self.oldest.age == self.birth_date

    # Achieved goals

    @property
    def is_married(self):
        return super().is_married

    @property
    def is_pregnant(self):
        return self.woman.is_pregnant and self.birth_date >= self.woman.age


class GayCouple(AbstractMarriableCouple, AbstractCouple):
    """Gay couple base class."""

    def __init__(self, person1, person2):
        super().__init__(person1, person2)

    @property
    def is_straight(self):
        return False

    @property
    def will_get_married(self):
        return super().will_get_married

    @property
    def is_marriage_date(self):
        return super().is_marriage_date

    @property
    def is_married(self):
        return super().is_married


class ConsangCouple(AbstractCouple):
    """Consanguinamorous couple base class."""

    def __init__(self, person1, person2):
        super().__init__(person1, person2)

    @property
    def is_straight(self):
        if self.person1.is_female and self.person2.is_male:
            return True
        return self.person1.is_male and self.person2.is_female

    @property
    def can_get_married(self):
        """First-degree related persons cannot get legally married in developed countries AFAIK.
        Cousins might, but it's not implemented yet."""
        return False

    @property
    def can_and_wants_bio_or_adopted_children(self):
        """Not implemented yet for consang. May not be legal."""
        return False

    @property
    def will_get_pregnant(self):
        """Not implemented yet for consang. May not be legal."""
        return False

    @property
    def will_adopt(self):
        """Not implemented yet for consang. May not be legal."""
        return False


class Throuple(AbstractCouple):
    """Throuple/triad base class."""

    def __init__(self, person1, person2, person3):
        super().__init__(person1, person2, person3)

    @property
    def is_throuple(self):
        return True

    @property
    def is_mixed_throuple(self):
        """Returns true if throuple is f/f/m or m/m/f."""
        return len(self.females) < 3 or len(self.males) < 3

    @property
    def is_straight(self):
        """Bisexual throuples contain at least one bisexual person."""
        return False

    @property
    def females(self):
        return [person for person in self.persons if person.is_female]

    @property
    def males(self):
        return [person for person in self.persons if person.is_male]

    @property
    def can_get_married(self):
        """Three persons cannot get legally married in developed countries AFAIK."""
        return False

    @property
    def can_and_wants_bio_or_adopted_children(self):
        """Not implemented yet for throuples."""
        return False
