from statistics import Statistics
from person_attributes import PersonAttributes

class Relationship(Statistics, PersonAttributes):

    def __init__(self, person1, person2, person3=None):

        self.person1 = person1
        self.person2 = person2
        self.person3 = person3

        if self.person3 is None:
            self.persons = [person1, person2]
        else:
            self.persons = [person1, person2, person3]

        # Random break up chance
        self.will_breakup = self.get_breakup_chance(self)
        self.breakup_date = self.get_breakup_date(self) # Depends on will_breakup

        # Pregnancy/Adoption
        self.desired_num_of_children = self.get_desired_number_of_children(self)
        self.expecting_children = 0 

    # PROPERTIES

    @property
    def oldest(self):
        return max(person.age for person in self.persons)

    @property
    def youngest(self):
        return min(person.age for person in self.persons)

    @property
    def is_intergenerational(self):
        return self.oldest == self.youngest

    @property
    def is_family_love(self):
        return all([self.persons[0] in p.family for p in self.persons])

    @property
    def all_can_and_want_children(self):
        return all([self.persons[0].can_and_wants_children for p in self.persons])

    @property
    def all_want_children_but_cant(self):
        return all([self.persons[0].cant_but_wants_children for p in self.persons])

    @property
    def is_married(self):
        return all([self.persons[0].relationship_status == self.MARRIED for p in self.persons])

    @property
    def common_children(self):
        if self.person3 is None:
            return [child for child in self.person1.children if child in self.person2.children]
        return [child for child in self.person1.children if child in self.person2.children and child in self.person3.children]

    # MODIFIABLE PROPERTIES

    @property
    def will_get_married(self):
        return self.is_married is False and all([self.persons[0].wants_marriage for p in self.persons])

    @property
    def will_adopt(self):
        return self.in_adoption_process is False and self.desired_num_of_children > 0 and self.all_want_children_but_cant

    @property
    def in_adoption_process(self):
        return all([self.persons[0].in_adoption_process for p in self.persons])

    # METHODS

    def get_married(self):

        for person in self.persons:
            person.relationship_status = self.MARRIED

        print("\n{} and {} have married.\n".format(
            self.person1.name, self.person2.name))

    def start_adoption_process(self):

        self.expecting_children = self.get_adoption_num_of_children(self)
        self.print_expecting_num_of_adoptions()

        for person in self.persons:
            person.in_adoption_process = True       

    def print_expecting_num_of_adoptions(self):
        if self.expecting_children not in self.ALLOWED_NUM_OF_ADOPTIONS:
            raise Exception(
                "Unexpected error occurred. Wrong number of expecting children.")

        if self.expecting_children == self.ONE_CHILD:
            print("{} and {} are going to adopt a child!".format(
                self.person1.name, self.person2.name))
        elif self.expecting_children == self.TWO_CHILDREN:
            print("{} and {} are going to adopt two children!".format(
                self.person1.name, self.person2.name))
        else:
            raise Exception(
                "Unexpected error occurred. Wrong number of expecting children.") 