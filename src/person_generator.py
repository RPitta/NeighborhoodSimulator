from person import Person
from person_attributes import PersonAttributes
from statistics import Statistics

class PersonGenerator(Statistics):

    def generate_romanceable_common_person(self, family_id, life_stage, unavailable_surnames):
        """Returns a cis-straight, monoamorous romanceable person."""

        person = Person(self.get_gender(), life_stage, self.CISGENDER,
                        self.HETEROSEXUAL, self.MONOAMOROUS)

        person.family_id = family_id
        person.name = self.get_name(person)
        person.surname = self.get_surname(unavailable_surnames)
        person.original_surname = person.surname
        person.target_gender = [
            gender for gender in self.get_target_gender(person)]
        person.is_liberal = self.get_liberalism(person)
        person.wants_domestic_partnership = True
        person.wants_marriage = True
        person.can_have_children = True
        person.wants_children = True

        return person

    def generate_baby(self, couple):

        if couple is None or len(couple.persons) <= 1 or couple.is_pregnant is None:
            raise Exception(
                "Unexpected error occurred. Given couple is wrong.")

        mother = couple.get_female()
        father = couple.get_male()

        baby = Person(self.get_gender(), self.BABY, self.get_gender_identity(),
                      self.get_sexual_orientation(), self.get_relationship_orientation())
        self.assign_child_attributes(baby, father, mother)

        self.baby_validation(baby)

        return baby

    def assign_child_attributes(self, baby, father, mother):

        # Assign mother and father
        baby.parents = [father, mother]

        baby.family_id = baby.father.family_id

        # Assign unique name among their family
        baby.name = self.get_name(baby)
        baby.target_gender = [
            gender for gender in self.get_target_gender(baby)]

        # Random
        baby.death_date = self.get_death_date(baby)
        baby.death_cause = self.get_death_cause(baby)
        baby.can_have_children = self.get_fertility(baby)
        baby.is_liberal = self.get_liberalism(baby)
        baby.wants_domestic_partnership = self.get_domestic_partnership_desire(
            baby)
        baby.wants_marriage = self.get_marriage_desire(baby)
        baby.wants_children = self.get_children_desire(baby)

    def baby_validation(self, baby):

        if baby.mother is None or baby.father is None or baby not in baby.mother.children or baby not in baby.father.children:
            raise Exception(
                "Unexpected error occurred. Baby and parents not correctly assigned.")
        for child in baby.mother.children:
            if child != baby and (child not in baby.siblings or baby not in child.siblings):
                raise Exception(
                    "Unexpected error occurred. Baby and siblings not correctly assigned.")
            if child != baby and child.name == baby.name:
                raise Exception(
                    "Unexpected error occurred. Baby's name is the same as their sibling.")
        if baby.family is None:
            raise Exception("Unexpected error occurred. Baby's family is null.")