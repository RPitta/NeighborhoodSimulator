from utilities.statistics import Statistics
from utilities.randomizer import Randomizer
from person import Person


class Relationship(Person):

    def __init__(self, person1, person2, person3=None):

        self.person1 = person1
        self.person2 = person2
        self.person3 = person3

        if self.person3 is None:
            self.persons = [person1, person2]
        else:
            self.persons = [person1, person2, person3]

        self.desired_num_of_children = 0
        self.expecting_children = 0
        self.will_breakup = None

    # OVERRIDEN PROPERTIES

    @property
    def is_straight(self):
        return False

    @property
    def will_get_pregnant(self):
        return False

    # SHARED READ-ONLY PROPERTIES

    @property
    def oldest(self):
        return next(person for person in self.persons if person.age == self.get_oldest_age)

    @property
    def youngest(self):
        return next(person for person in self.persons if person.age == self.get_youngest_age)

    @property
    def is_intergenerational(self):
        return self.oldest.stage != self.youngest.stage

    @property
    def is_family_love(self):
        return all([self.persons[0] in p.family for p in self.persons])

    # TIME-CHANGING PROPERTIES

    @property
    def all_can_and_want_children(self):
        return all([self.persons[0].can_and_wants_children for p in self.persons])

    @property
    def all_want_children_but_cant(self):
        return all([self.persons[0].cant_but_wants_children for p in self.persons])

    @property
    def common_children(self):
        if self.person3 is None:
            return [child for child in self.person1.children if child in self.person2.children]
        return [child for child in self.person1.children if child in self.person2.children and child in self.person3.children]

    # RELATIONSHIP GOALS NOT YET ACHIEVED

    @property
    def will_get_married(self):
        return self.is_married is False and all([self.persons[0].wants_marriage for p in self.persons])

    @property
    def will_have_children(self):
        """Returns true if all persons want children and their expected pregnancy/adoption date is within young adult stage."""
        if self.will_get_married:
            return (self.all_can_and_want_children or self.all_want_children_but_cant) and \
            self.oldest.age < self.YOUNGADULT.end and self.oldest.marriage_date < (self.YOUNGADULT.end - 1)
        return (self.all_can_and_want_children or self.all_want_children_but_cant) and self.oldest.age < self.YOUNGADULT.end

    @property
    def will_adopt(self):
        return self.in_adoption_process is False and self.desired_num_of_children > 0 and self.all_want_children_but_cant

    # RELATIONSHIP GOALS IN PROCESS PRESENTLY

    @property
    def in_adoption_process(self):
        return all([self.persons[0].in_adoption_process for p in self.persons])

    # ACHIEVED RELATIONSHIP GOALS

    @property
    def is_married(self):
        return all([self.persons[0].is_married for p in self.persons])

    # HELPER METHODS

    @property
    def get_oldest_age(self):
        return max(person.age for person in self.persons)

    @property
    def get_youngest_age(self):
        return min(person.age for person in self.persons)