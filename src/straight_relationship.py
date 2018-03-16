from relationship import Relationship
from utilities.statistics import Statistics


class StraightRelationship(Relationship):

    def __init__(self, person1, person2):
        super().__init__(person1, person2)
        
    @property
    def is_straight(self):
        return True

    @property
    def man(self):
        return next(person for person in self.persons if person.is_male)

    @property
    def woman(self):
        return next(person for person in self.persons if person.is_female)

    @property
    def is_pregnant(self):
        return self.woman.is_pregnant

    @property
    def will_get_pregnant(self):
        return self.is_pregnant is False and self.desired_num_of_children > 0 and self.all_can_and_want_children

    # METHODS