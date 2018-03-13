from person import Person
from relationship import Relationship
from randomizer import Randomizer


class StraightRelationship(Relationship):

    SINGLETON = 1
    TWINS = 2
    TRIPLET = 3
    ALLOWED_NUM_OF_CHILDREN = (SINGLETON, TWINS, TRIPLET)

    def __init__(self, person1, person2):
        super().__init__(person1, person2)

    def get_male(self):
        return next(person for person in self.persons if person.is_male)

    def get_female(self):
        return next(person for person in self.persons if person.is_female)

    def get_pregnant(self):
        """Set pregnancy to True and assign number of expecting children"""
        if not self.will_get_pregnant or self.desired_num_of_children <= 0:
            raise Exception(
                "Unexpected error occurred. You're trying to get pregnant a couple that won't or can't.")

        self.expecting_children = self.get_pregnancy_num_of_children()
        self.print_expecting_num_of_children()

        self.is_pregnant = True
        self.get_female().is_pregnant = True

    def get_pregnancy_num_of_children(self):
        """Random number of children for pregnancy: singleton/twins/triplets"""

        if not self.will_get_pregnant or self.desired_num_of_children <= 0:
            raise Exception(
                "Unexpected error occurred. Couple does not want to get pregnant or already had all desired children.")

        options = {
            self.SINGLETON: 96,
            self.TWINS: 3,
            self.TRIPLET: 1
        }

        return Randomizer().get_random_dict_key(options)

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
        elif self.expecting_children == self.TRIPLET:
            print("{} and {} are pregnant with a triplet!".format(
                self.get_male().name, self.get_female().name))
        else:
            raise Exception(
                "Unexpected error occurred. Wrong number of expecting children.")
