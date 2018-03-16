from person import Person

class PersonGenerator:

    def __init__(self, names, professions, traits, stages, statistics, developer):
        self.names = names
        self.professions = professions
        self.traits = traits
        self.stages = stages
        self.statistics = statistics
        self.developer = developer

    def generate_straight_yadult(self, gender, surnames):
        person = Person(gender, self.stages.YOUNGADULT, self.traits.CISGENDER,
                            self.traits.HETEROSEXUAL, self.traits.MONOAMOROUS)
        person.surname = self.statistics.get_surname(person, surnames)
        self.assign_random_traits(person)
        self.assign_romanceable_traits(person)
        person = self.developer.yadult_traits(person)
        return person

    def assign_romanceable_traits(self, baby):
        baby.wants_domestic_partnership = True
        baby.wants_marriage = True
        baby.can_have_bio_children = True
        baby.wants_children = True

    def generate_baby(self, couple):

        mother = couple.woman
        father = couple.man

        baby = Person(self.statistics.get_gender(), self.stages.BABY, self.statistics.get_gender_identity(),
                    self.statistics.get_sexual_orientation(), self.statistics.get_relationship_orientation())

        self.assign_family(baby, father, mother)

        self.assign_random_traits(baby)

        self.baby_validation(baby)

        return baby

    def assign_family(self, baby, father, mother):
        # Assign mother and father
        
        # PARENTS AND CHILDREN
        baby.parents = [father, mother]
        baby.father = father
        baby.father.children.append(baby)
        baby.mother = mother
        baby.mother.children.append(baby)

        # FATHER'S SURNAME
        baby.surname = baby.father.surname
        baby.original_surname = baby.surname

        # SIBLINGS
        baby.siblings = [
            child for child in baby.father.children if child.mother == baby.mother and child != baby]
        for sibling in baby.siblings:
            sibling.siblings.append(baby)

        # GRANDPARENTS
        if baby.father.parents is not None:
            baby.grandparents.extend(baby.father.parents)
        if baby.mother.parents is not None:
            baby.grandparents.extend(baby.mother.parents)
        for grandparent in baby.grandparents:
            grandparent.grandchildren.append(baby)

        # HALF-SIBLINGS
        baby.half_siblings = [child for child in baby.father.children if child.mother != baby.mother] + [child for child in baby.mother.children if child.father != baby.father]
        for sibling in baby.half_siblings:
            sibling.half_siblings.append(baby)

        # UNCLES/AUNTS AND COUSINS
        if baby.father.siblings is not None:
            baby.parents_siblings.extend(baby.father.siblings)
        if baby.mother.siblings is not None:
            baby.parents_siblings.extend(baby.mother.siblings)
        if baby.parents_siblings is not None:
            for uncle_aunt in baby.parents_siblings:
                uncle_aunt.siblings_children.append(baby)
                baby.cousins.extend(uncle_aunt.children)
            for cousin in baby.cousins:
                cousin.cousins.append(baby)

    def assign_random_traits(self, baby):
        # Assign unique name among their family
        baby.name = self.statistics.get_name(baby)
        baby.target_gender = [
            gender for gender in self.statistics.get_target_gender(baby)]
        baby.death_date = self.statistics.get_death_date(baby)
        baby.death_cause = self.statistics.get_death_cause(baby)
        baby.is_liberal = self.statistics.get_liberalism(baby)
        baby.wants_domestic_partnership = self.statistics.get_domestic_partnership_desire(baby)
        baby.wants_marriage = self.statistics.get_marriage_desire(baby)
        baby.can_have_bio_children = self.statistics.get_fertility(baby)
        baby.wants_children = self.statistics.get_children_desire(baby)

    def baby_validation(self, baby):

        if baby.name is None or baby.surname is None:
            raise Exception(
                "Unexpected error occurred. Baby has no name or surname.")

        # PARENTS AND SIBLINGS
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
        # OTHER FAMILY
        if baby.family is None:
            raise Exception(
                "Unexpected error occurred. Baby's family is null.")
        if baby in baby.family:
            raise Exception("Unexpected error occurred. Baby is inside his relatives list.")
        if len(set(baby.family)) != len(baby.family):
            raise Exception("Unexpected error occurred. Baby's family list contains duplicates.")
        for family_member in baby.family:
            if baby not in family_member.family:
                raise Exception(
                    "Unexpected error occurred. Baby not assigned to other family members.")
        for family_member in baby.mother.family:
            if family_member != baby and (baby not in family_member.family or family_member not in baby.family):
                raise Exception(
                    "Unexpected error occurred. Baby not assigned to other family members.")
        for family_member in baby.father.family:
            if family_member != baby and (baby not in family_member.family or family_member not in baby.family):
                raise Exception(
                    "Unexpected error occurred. Baby not assigned to other family members.")

        if baby.stage is None or baby.age is None or baby.age != self.stages.BABY.start:
            raise Exception("Unexpected error occurred. Baby's age is wrong.")

        if baby.gender is None or baby.gender_identity is None or \
            baby.sexual_orientation is None or baby.relationship_orientation is None:
            raise Exception("Unexpected error occurred. Baby's basic gender and/or orientation info are wrong.")

        if baby.death_cause is None or baby.death_date is None:
            raise Exception("Unexpected error occurred. Baby's death cause or date is wrong.")