from traits import Traits
from person import Person


class BabyGenerator:

    def __init__(self, stages, statistics):
        self.stages = stages
        self.statistics = statistics

    def create_first_child(self, surnames):
        """Generates new child without family to populate city.
        Random surname that is unique among the population."""
        child = Person(self.statistics.get_gender(), self.stages.CHILD)

        self.set_first_child_traits(child, surnames)
        self.set_baby_essential_traits(child)

        return child

    def set_first_child_traits(self, child, surnames):
        child.surname = self.statistics.get_surname(child, surnames)
        child.original_surname = child.surname
        child.social_class = self.statistics.get_social_class()

    def set_baby_essential_traits(self, baby):
        """Gives baby a random name, target gender, death date/cause and fertility."""
        baby.name = self.statistics.get_name(baby)
        baby.death_date = self.statistics.get_death_date(baby)
        baby.death_cause = self.statistics.get_death_cause(baby)
        baby.can_have_bio_children = self.statistics.get_fertility(baby)

    def generate_baby(self, couple):
        """Generates baby from given couple."""
        baby = Person(self.statistics.get_gender(), self.stages.BABY)

        self.link_family(baby, couple)
        self.set_baby_essential_traits(baby)
        self.baby_validation(baby)

        return baby

    def link_family(self, baby, couple):
        """Assign's baby's family."""
        mother = couple.woman
        father = couple.man

        # PARENTS AND CHILDREN
        baby.parents = [father, mother]
        baby.father = father
        baby.father.children.append(baby)
        baby.mother = mother
        baby.mother.children.append(baby)

        # FATHER'S SURNAME
        baby.surname = baby.father.surname
        baby.original_surname = baby.surname
        # FATHER'S SOCIAL CLASS
        baby.social_class = baby.father.social_class
        # MOTHER'S APARTMENT ID
        baby.apartment_id = baby.mother.apartment_id

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
        baby.half_siblings = [child for child in baby.father.children if child.mother !=
                              baby.mother] + [child for child in baby.mother.children if child.father != baby.father]
        for sibling in baby.half_siblings:
            sibling.half_siblings.append(baby)

        # UNCLES/AUNTS
        for uncle_aunt in baby.father.siblings:
            uncle_aunt.siblings_children.append(baby)
            if uncle_aunt not in baby.parents_siblings:
                baby.parents_siblings.append(uncle_aunt)
        for uncle_aunt in baby.mother.siblings:
            uncle_aunt.siblings_children.append(baby)
            if uncle_aunt not in baby.parents_siblings:
                baby.parents_siblings.append(uncle_aunt)

        # COUSINS
        for uncle_aunt in baby.parents_siblings:
            for cousin in uncle_aunt.children:
                cousin.cousins.append(baby)
                if cousin not in baby.cousins:
                    baby.cousins.append(cousin)

    def baby_validation(self, baby):
        """Validates baby's correct traits and family."""
        # Baby attributes
        if baby.name is None:
            raise Exception("Person has no name.")
        if baby.surname is None or baby.original_surname is None:
            raise Exception("Person has no surname.")
        if baby.stage is None or baby.stage not in self.stages.LIFESTAGES:
            raise Exception("Person's life stage is wrong.")
        if baby.age is None or baby.age not in baby.stage.span or baby.age not in self.stages.LIFESPAN:
            raise Exception("Person's age is wrong.")
        if baby.gender is None or baby.gender not in Traits.GENDERS:
            raise Exception("Person's gender is wrong.")
        if baby.death_cause is None or baby.death_cause not in Traits.DEATH_CAUSES:
            raise Exception("Person's death cause is wrong.")
        if baby.death_date is not False and baby.death_date not in self.stages.LIFESPAN:
            raise Exception("Person's death date is wrong.")

        # Family
        if baby.bio_family is None:
            raise Exception("Baby's family is null.")
        if baby in baby.bio_family:
            raise Exception("Baby is inside his relatives list.")
        if len(set(baby.siblings)) != len(baby.siblings):
            raise Exception("Baby's siblings list contains duplicates.")
        if len(set(baby.cousins)) != len(baby.cousins):
            raise Exception("Baby's cousins list contains duplicates.")
        if len(set(baby.parents_siblings)) != len(baby.parents_siblings):
            raise Exception("Baby's uncles/aunts list contains duplicates.")

        # Parents
        if baby.mother is None or baby.father is None or baby not in baby.mother.children or baby not in baby.father.children:
            raise Exception("Baby and parents not correctly assigned.")
        # Full-siblings and siblings on mother's side
        for child in baby.mother.children:
            if child != baby:
                if child.name == baby.name:
                    raise Exception(
                        "Baby's name is the same as their sibling.")
                if child in baby.father.children and child not in baby.siblings:
                    raise Exception(
                        "Sibling not assigned to baby.")
                if child in baby.father.children and baby not in child.siblings:
                    raise Exception(
                        "Baby not assigned to sibling.")
                if child.father != baby.father and child in baby.siblings:
                    raise Exception("Half sibling assigned as full-sibling.")
                if child not in baby.father.children and child not in baby.half_siblings:
                    raise Exception(
                        "Half-Sibling not assigned to baby.")
        # Siblings on father's side
        for child in baby.father.children:
            if child != baby:
                if child.mother != baby.mother and child in baby.siblings:
                    raise Exception("Half sibling assigned as full-sibling.")
                if child not in baby.mother.children and child not in baby.half_siblings:
                    raise Exception(
                        "Half-Sibling not assigned to baby.")
        # Uncle/Aunt on father's side
        for sibling in baby.father.siblings:
            if sibling not in baby.parents_siblings:
                raise Exception(
                    "Uncle/Aunt not assigned to baby.")
            if baby not in sibling.siblings_children:
                raise Exception("Baby not assigned to Uncle/Aunt.")
        # Uncle/Aunt on mother's side
        for sibling in baby.mother.siblings:
            if sibling not in baby.parents_siblings:
                raise Exception(
                    "Uncle/Aunt not assigned to baby.")
            if baby not in sibling.siblings_children:
                raise Exception("Baby not assigned to Uncle/Aunt.")
        # Cousins on father's side
        for child in baby.father.siblings_children:
            if child not in baby.cousins:
                raise Exception("Cousin not assigned to baby.")
            if baby not in child.cousins:
                raise Exception("Baby not assigned to cousin.")
        # Cousins on mother's side
        for child in baby.mother.siblings_children:
            if child not in baby.cousins:
                raise Exception("Cousin not assigned to baby.")
            if baby not in child.cousins:
                raise Exception("Baby not assigned to cousin.")
        # Twin and triplets
        if baby.is_twin:
            if len(baby.siblings) == 0:
                raise Exception("Baby is twin but has no siblings.")
            if all([baby.is_twin is False for sibling in baby.siblings]):
                raise Exception("Baby is twin but has no twin sibling.")
        if baby.is_triplet:
            if len(baby.siblings) < 2:
                raise Exception(
                    "Baby is triplet but has an incorrect number of siblings.")
            if sum(1 for sibling in baby.siblings if sibling.is_triplet) < 2:
                raise Exception(
                    "Baby is triplet but has no triplet siblings.")
