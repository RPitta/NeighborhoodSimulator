from abstract_couple import AbstractCouple, AbstractMarriableCouple, AbstractFertileCouple
from traits import Traits


class StraightCouple(AbstractMarriableCouple, AbstractFertileCouple, AbstractCouple):

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
        """Returns true if all persons want marriage, haven't married yet and are able to."""
        if self.is_married:
            return False
        if any([p.is_married_or_remarried or p.spouse is not None for p in self.persons]):
            return False
        if len(self.oldest.span_left_till_old_age) <= 0:
            return False
        return self.can_get_married and all([p.wants_marriage for p in self.persons])

    @property
    def will_have_children(self):
        """Returns true if all persons want children and their expected pregnancy/adoption date is within young adult stage."""
        if any([person.has_max_num_of_children for person in self.persons]) or self.has_desired_children:
            return False
        if self.is_pregnant or self.birth_date > self.oldest.age or self.pregnancy_date > self.oldest.age:
            return False
        return self.can_and_wants_bio_or_adopted_children and self.is_within_pregnancy_span

    @property
    def will_get_pregnant(self):
        """Returns true if not already pregnant and can/wants biological children."""
        return self.is_pregnant is False and self.has_desired_children is False and self.all_can_and_want_children

    @property
    def will_adopt(self):
        """Returns true if not already in adoption process and can/wants adopted children."""
        return self.is_in_adoption_process is False and self.has_desired_children is False and self.all_want_children_but_cant

    @property
    def is_marriage_date(self):
        return self.oldest.age == self.marriage_date

    @property
    def is_pregnancy_date(self):
        """Overriden in Straight Couple"""
        return self.oldest.age == self.pregnancy_date

    @property
    def is_adoption_date(self):
        return self.oldest.age == self.adoption_date

    @property
    def is_adoption_process_date(self):
        return self.oldest.age == self.adoption_process_date

    @property
    def is_birth_date(self):
        return self.oldest.age == self.birth_date

    # Achieved goals

    @property
    def is_married(self):
        """Returns true if all persons are married to each other."""
        return all([p.is_married_or_remarried for p in self.persons]) and self.person1.spouse == self.person2

    @property
    def is_pregnant(self):
        return self.woman.is_pregnant and self.birth_date >= self.woman.age

    @property
    def is_in_adoption_process(self):
        """Returns true if all persons are in adoption process."""
        return all([self.persons[0].is_in_adoption_process for p in self.persons])

    # Helper methods

    @property
    def can_and_wants_bio_or_adopted_children(self):
        return self.is_within_pregnancy_span and self.all_can_and_want_children

    @property
    def is_within_pregnancy_span(self):
        timespan = self.pregnancy_timespan
        return timespan is not None and len(timespan) > 0

    @property
    def pregnancy_timespan(self):
        """Returns the range of years between person's age and young adult's stage end."""
        """If they are set to marry, children will come afterwards."""
        if self.oldest.is_young_adult is False:
            return None
        if self.will_get_married:
            return range(self.marriage_date + 1, self.oldest.stage.end)
        else:
            return self.oldest.span_left_till_next_stage


class GayCouple(AbstractMarriableCouple, AbstractCouple):

    def __init__(self, person1, person2):
        super().__init__(person1, person2)

    @property
    def is_straight(self):
        return False

    @property
    def will_get_married(self):
        """Returns true if all persons want marriage, haven't married yet and are able to."""
        if self.is_married:
            return False
        if any([p.is_married_or_remarried or p.spouse is not None for p in self.persons]):
            return False
        if len(self.oldest.span_left_till_old_age) <= 0:
            return False
        return self.can_get_married and all([p.wants_marriage for p in self.persons])

    @property
    def is_marriage_date(self):
        return self.oldest.age == self.marriage_date

    @property
    def is_married(self):
        """Returns true if all persons are married to each other."""
        return all([p.is_married_or_remarried for p in self.persons]) and self.person1.spouse == self.person2


class ConsangCouple(AbstractCouple):

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

    def __init__(self, person1, person2, person3):
        super().__init__(person1, person2, person3)
        pass

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
