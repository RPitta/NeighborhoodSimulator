
from relationship import Relationship
from statistics import Statistics

class StraightRelationship(Relationship):

    def __init__(self, person1, person2):
        super().__init__(person1, person2)

    def get_male(self):
        return next(person for person in self.persons if person.is_male)

    def get_female(self):
        return next(person for person in self.persons if person.is_female)

    @property
    def is_pregnant(self):
        return self.get_female().is_pregnant

    @property
    def will_get_pregnant(self):
        return self.is_pregnant is False and self.desired_num_of_children > 0 and self.all_can_and_want_children


    # METHODS

    def get_pregnant(self):
        """Set pregnancy to True and assign number of expecting children"""
        self.expecting_children = self.get_pregnancy_num_of_children(self)
        self.print_expecting_num_of_children()

        self.get_female().is_pregnant = True

    # UI

    def print_expecting_num_of_children(self):
        if self.expecting_children not in self.ALLOWED_NUM_OF_CHILDREN:
            raise Exception(
                "Unexpected error occurred. Wrong number of expecting children.")

        if self.expecting_children == self.SINGLETON:
            print("{} and {} are pregnant with a child!".format(
                self.get_male().name, self.get_female().name))
        elif self.expecting_children == self.TWINS:
            print("{} and {} are pregnant with twins!".format(
                self.get_male().name, self.get_female().name))
        elif self.expecting_children == self.TRIPLETS:
            print("{} and {} are pregnant with triplets!".format(
                self.get_male().name, self.get_female().name))
        else:
            raise Exception(
                "Unexpected error occurred. Wrong number of expecting children.")
