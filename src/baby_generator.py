from traits import Traits
from person import Person


class BabyGenerator:
    """Baby generator base class."""

    def __init__(self, statistics, names):
        self.statistics = statistics
        self.names = names

    def create_first_child(self, age, surnames):
        """Generates new child without family to populate city."""
        child = Person(self.statistics.get_gender(), age)
        self.set_first_child_traits(child, surnames)
        self.set_baby_essential_traits(child)
        return child

    def set_first_child_traits(self, child, surnames):
        """Set statistical/random basic traits for new child."""
        child.surname = self.names.get_surname(surnames)
        child.original_surname = child.surname
        child.race = self.get_race()

    def get_race(self):
        """Return race dictionary with statistical race set."""
        race = self.statistics.get_race()
        race_dict_copy = dict(Traits.race_dict)

        if race == Traits.WHITE:
            race_dict_copy[Traits.WHITE] = 100
            return race_dict_copy
        elif race == Traits.BLACK:
            race_dict_copy[Traits.BLACK] = 100
            return race_dict_copy
        elif race == Traits.LATINO:
            race_dict_copy[Traits.LATINO] = 100
            return race_dict_copy
        elif race == Traits.ASIAN:
            race_dict_copy[Traits.ASIAN] = 100
            return race_dict_copy
        else:
            raise Exception("Wrong race.")

    def set_baby_essential_traits(self, baby):
        """Gives baby a random name, target gender, death date/cause and fertility."""
        baby.name = self.names.get_name(baby)
        baby.death_date = self.statistics.get_death_date()
        baby.death_cause = self.statistics.get_death_cause(baby)
        baby.can_have_bio_children = self.statistics.get_fertility()
        if self.statistics.get_autistic_disorder_chance(baby):
            baby.conditions.append(Traits.AUTISTIC_DISORDER)

    def generate_baby(self, couple):
        """Generates baby from given couple."""
        baby = Person(self.statistics.get_gender(), Traits.BABY.start)
        self.link_family(baby, couple)
        self.set_baby_essential_traits(baby)
        self.baby_validation(baby)
        return baby

    def link_family(self, baby, couple):
        """Assign's baby's family."""
        baby.parents.extend(couple.persons)
        for parent in baby.parents:
            parent.children.append(baby)

        # Race
        self.set_race(baby)
        # Surname and apartment ID
        if couple.is_straight:
            baby.surname = couple.man.surname
        else:
            baby.surname = baby.parents[0].surname
        baby.original_surname = baby.surname

    @classmethod
    def set_race(cls, baby):
        if all(baby.parents[0].race == p.race for p in baby.parents):
            baby.race = baby.parents[0].race
        else:
            baby.race = dict(Traits.race_dict)
            for parent in baby.parents:
                for r, n in parent.race.items():
                    if n > 0:
                        baby.race[r] = int(n / 2)
                        if baby.race[r] < 0:
                            baby.race[r] = 0

    @classmethod
    def baby_validation(cls, baby):
        """Validates baby's correct traits and family."""
        if baby.name is None:
            raise Exception("Person has no name.")
        if baby.surname is None or baby.original_surname is None:
            raise Exception("Person has no surname.")
        if baby.stage is None or baby.stage not in Traits.LIFE_STAGES:
            raise Exception("Person's life stage is wrong.")
        if baby.age is None or baby.age not in baby.stage.span or baby.age not in Traits.LIFESPAN:
            raise Exception("Person's age is wrong.")
        if baby.gender is None or baby.gender not in Traits.GENDERS:
            raise Exception("Person's gender is wrong.")
        if baby.death_cause is None or baby.death_cause not in Traits.DEATH_CAUSES:
            raise Exception("Person's death cause is wrong.")
        if baby.death_date is not False and baby.death_date not in Traits.LIFESPAN:
            raise Exception("Person's death date is wrong.")
        if sum(baby.race.values()) != 100:
            raise Exception("Race does not add up to 100.")

        # Family
        if len(baby.bio_family) == 0:
            raise Exception("Baby's family is null.")
        if baby in baby.bio_family:
            raise Exception("Baby is inside his relatives list.")
        if len(baby.parents) <= 0 and len(baby.adoptive_parents) <= 0:
            raise Exception("Baby has no parents.")
        if len(set(baby.parents)) != len(baby.parents):
            raise Exception("List of parents contains duplicates.")
        for parent in baby.parents:
            if len(set(parent.children)) != len(parent.children):
                raise Exception("List of children contains duplicates.")
        # Siblings
        if len(set(baby.full_siblings)) != len(baby.full_siblings):
            raise Exception("List of siblings contains duplicates.")
        for sibling in baby.full_siblings:
            if sibling in [baby.half_siblings, baby.step_siblings, baby.adoptive_full_siblings]:
                raise Exception("Full-sibling inside list of half/step/adoptive siblings.")
        for half_sib in baby.half_siblings:
            if half_sib in [baby.full_siblings, baby.step_siblings, baby.adoptive_full_siblings]:
                raise Exception("Half-sibling inside list of full/step/adoptive siblings.")
        for step_sib in baby.half_siblings:
            if step_sib in [baby.full_siblings, baby.half_siblings, baby.adoptive_full_siblings]:
                raise Exception("Step-sibling inside list of full/half/adoptive siblings.")
        for adoptive_sib in baby.half_siblings:
            if adoptive_sib in [baby.full_siblings, baby.half_siblings, baby.step_siblings]:
                raise Exception("Adoptive sibling inside list of full/half/step siblings.")
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
