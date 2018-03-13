from person_attributes import PersonAttributes
from statistics import Statistics
from randomizer import Randomizer


class Relationship(Statistics, PersonAttributes):

    def __init__(self, person1, person2, person3 = None):

        self.person1 = person1
        self.person2 = person2
        self.person3 = person3

        if self.person3 is None:
            self.persons = [person1, person2]
        else:
            self.persons = [person1, person2, person3]

        # Type of relationship
        self.is_intergenerational = all([self.persons[0].life_stage == p.life_stage for p in self.persons])
        self.is_incest = None

        # Status
        self.is_pregnant = False
        self.expecting_children = 0

        # Marriage and pregnancy/adoption
        self.will_get_married = self.all_want_marriage
        self.will_get_pregnant = self.all_can_and_want_children
        self.will_adopt = self.all_want_children_but_cant

        # Random break up chance
        self.will_breakup = self.get_breakup_chance(self)
        self.breakup_date = self.get_breakup_date(self)

        # Random desired number of children
        self.desired_num_of_children = self.get_desired_number_of_children(self)

    @property
    def oldest(self):
        return max(person.age for person in self.persons)

    @property
    def youngest(self):
        return min(person.age for person in self.persons)
    
    @property
    def all_want_marriage(self):
        return all(person.wants_marriage for person in self.persons)

    @property
    def all_can_and_want_children(self):
        return all(person.can_and_wants_children for person in self.persons)

    @property
    def all_want_children_but_cant(self):
        return all(person.cant_but_wants_children for person in self.persons)

    @property
    def common_children(self):
        if self.person3 is None:
            return [child for child in self.person1.children if child in self.person2.children]
        return [child for child in self.person1.children if child in self.person2.children and child in self.person3.children]

    @property
    def is_married(self):
        return all([self.persons[0].relationship_status == self.MARRIED for p in self.persons])

    def get_married(self):
        
        # Set each person to married status
        for person in self.persons:
            person.relationship_status = self.MARRIED