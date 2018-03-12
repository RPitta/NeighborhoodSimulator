from collections import Counter
from person_attributes import PersonAttributes
from randomizer import Randomizer
from person import Person


class Relationship(PersonAttributes):

    ONE_CHILD = 1
    TWO_CHILDREN = 2
    THREE_CHILDREN = 3
    FOUR_CHILDREN = 4
    DESIRED_NUM_OF_CHILDREN = (ONE_CHILD, TWO_CHILDREN, THREE_CHILDREN, FOUR_CHILDREN)

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
        self.is_married = False
        self.is_pregnant = False
        self.expecting_children = 0

        # Break up
        self.will_breakup = self.get_breakup_chance()
        self.breakup_date = self.get_breakup_date()

        # Marriage and pregnancy/adoption
        self.will_get_married = self.all_want_marriage()
        self.will_get_pregnant = self.all_can_and_want_children()
        self.will_adopt = self.all_want_children_but_cant()
        self.desired_num_of_children = self.get_desired_number_of_children()

    def get_oldest(self):
        if self.person1.age > self.person2.age:
            return self.person1.life_stage
        else:
            return self.person2.life_stage

    def get_youngest(self):
        if self.person1.age < self.person2.age:
            return self.person1.life_stage
        else:
            return self.person2.life_stage
        
    def all_want_marriage(self):
        return all(person.wants_marriage for person in self.persons)

    def all_can_and_want_children(self):
        return all(person.can_and_wants_children() for person in self.persons)

    def all_want_children_but_cant(self):
        return all(person.cant_but_wants_children() for person in self.persons)

    def get_desired_number_of_children(self):

        if not self.will_get_pregnant and not self.will_adopt:
            return 0

        options = {
            self.ONE_CHILD : 40,
            self.TWO_CHILDREN : 30,
            self.THREE_CHILDREN : 20,
            self.FOUR_CHILDREN : 10
        }

        return Randomizer().get_random_dict_key(options)

    def get_children(self):

        common_children = []
        for child in self.person1.children:
            if child in self.person2.children and child not in common_children:
                common_children.append(child)
        return common_children

    def get_breakup_chance(self):

        # If a person is already a senior when they get into a committed relationship, they won't break up as death will come first
        if self.person1.life_stage == self.SENIOR or self.person2.life_stage == self.SENIOR:
            return False

        options = {
            True : 60,
            False : 40
        }

        return Randomizer().get_random_dict_key(options)

    def get_breakup_date(self):

        # Automatically return none if couple won't break up
        if not self.will_breakup:
            return None

        options_for_young_adults = {
            self.YOUNG_ADULT : 30,
            self.ADULT : 50,
            self.SENIOR : 20              
        }

        options_for_adults = {
            self.SENIOR : 50,
            self.ADULT : 50
        }

        options_for_intergenerational = {
            self.ADULT : 50,
            self.YOUNG_ADULT : 50               
        }

        # If couple are adults, they can break up soon as adults or as seniors
        # If couple are young adults, they can break up soon as young adults, adults or seniors
        # If couple is intergenerational, they can break up when soon when youngest is a young adult, or when youngest is an adult
        if not self.is_intergenerational:
            if self.person1.life_stage == self.ADULT:
                selected = Randomizer().get_random_dict_key(options_for_adults)        
            elif self.person1.life_stage == self.YOUNG_ADULT:
                selected = Randomizer().get_random_dict_key(options_for_young_adults)
            else:
                raise Exception("Unexpected error occurred. Couple's age is wrong, are seniors or underage.")     
        else:
            selected = Randomizer().get_random_dict_key(options_for_intergenerational)

        print("Breakup date:" + selected)
        if selected not in self.LIFE_STAGES:
            raise Exception("Unexpected error occurred. Break-up date is not correct.")

        return selected

    def get_married(self):
        
        for person in self.persons:
            person.relationship_status = self.MARRIED
        self.is_married = True