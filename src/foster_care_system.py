from utilities.randomizer import Randomizer


class FosterCareSystem:

    def __init__(self, statistics):
        self.statistics = statistics
        self.randomizer = Randomizer()
        self.children = []

    @property
    def only_childs(self):
        return [child for child in self.children if len(child.siblings) == 0]

    @property
    def sibling_sets(self):
        return [child for child in self.children if len(child.siblings) > 0]

    def check_foster_care_system(self, living_outsiders):
        """Removes newly adult children from the system and adds new children to it if requirements are met."""
        adults = [child for child in self.children if child.is_of_age]
        siblings_of_adults = [sibling for adult in adults for sibling in self.children if
                              sibling in adult.siblings]
        # Remove adults and their siblings
        self.remove_from_system(adults)
        self.remove_from_system(siblings_of_adults)

        # Add new kids
        new_children = [child for person in living_outsiders for child in person.children if
                        person.must_place_children_up_for_adoption and child not in self.children]
        self.add_to_system(new_children)

    def add_to_system(self, children):
        """Adds given children to the list of child up for adoption."""
        self.children.extend(children)

    def remove_from_system(self, children):
        """Removes adopted children or newly-adult children from the system."""
        self.children = [child for child in self.children if child not in children]

    def adopt_child(self, couple):
        """Returns only child with statistically random age."""
        self.check_children_in_foster_care()

        children_within_range = []
        while len(children_within_range) == 0:
            age_range = self.statistics.get_age_of_adoptive_children()
            children_within_range = [child for child in self.only_childs if child.age in age_range]

        child = self.randomizer.get_random_item(children_within_range)

        self.link_adoptive_family(couple, [child])
        self.remove_from_system([child])
        return [child]

    def adopt_sibling_set(self, couple):
        """Returns a set of siblings with statistically random age."""
        self.check_children_in_foster_care()
        if len(self.sibling_sets) == 0:
            couple.expecting_num_of_children = 1
            return self.adopt_child(couple)

        age_range = self.statistics.get_age_of_adoptive_children()
        children_within_range = [child for child in self.sibling_sets if child.age in age_range]

        child = self.randomizer.get_random_item(children_within_range)
        children = [child] + child.siblings

        couple.expecting_num_of_children = len(children)
        self.link_adoptive_family(couple, children)
        self.remove_from_system(children)
        return children

    @classmethod
    def link_adoptive_family(cls, couple, children):
        """Link adopted children to their adoptive family."""
        for child in children:
            child.adoptive_parents.extend(couple.persons)
            child.social_class = child.adoptive_parents[0].social_class

        for parent in children[0].adoptive_parents:
            parent.adoptive_children.extend(children)

        if couple.is_straight:
            for child in children:
                child.surname = couple.man.surname
                child.apartment_id = couple.woman.apartment_id
        else:
            for child in children:
                child.surname = child.adoptive_parents[0].surname
                child.apartment_id = child.adoptive_parents[0].apartment_id

        for child in children:
            child.original_surname = child.surname

    def check_children_in_foster_care(self):
        if len(self.children) == 0:
            raise Exception("No children in foster care.")
