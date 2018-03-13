
from person_attributes import PersonAttributes
from person_generator import PersonGenerator
from relationship_generator import RelationshipGenerator
from straight_relationship import StraightRelationship


class World(PersonAttributes):

    NEIGHBOORHOOD_APARTMENTS = 16
    NEIGHBOORHOOD_FAMILIES = NEIGHBOORHOOD_APARTMENTS
    FAMILY_IDS = NEIGHBOORHOOD_APARTMENTS

    def __init__(self):
        # Initialize generators once
        self.person_generator = PersonGenerator()
        self.relationship_generator = RelationshipGenerator()

        self.deceased_population = []
        self.population = []
        self.neighbors = []
        self.couples = []

        self.populate_romanceable_straights(self.TEEN)
        pass

    @property
    def population(self):
        return self._population

    @population.setter
    def population(self, persons):
        self._population = persons

        # Add dead senior to deceased population list
        for person in self._population:
            if not person.is_alive:
                self.deceased_population.append(person)

        # Remove dead seniors from population
        self._population[:] = [
            person for person in self._population if person.is_alive]

    @property
    def population_surnames(self):
        return set([person.surname for person in self.population])

    @property
    def romanceable_outsiders(self):
        return [person for person in self.population if person.is_free_and_willing_to_date]

    @property
    def unromanceable_outsiders(self):
        return [person for person in self.population if person.is_free_and_willing_to_date is False]

    @property
    def partnered_outsiders(self):
        return [person for person in self.population if person.partner is not None]

    def populate_romanceable_straights(self, age):

        for i in (number+1 for number in range(20)):
            self.population.append(self.person_generator.generate_romanceable_common_person(
                i, age, self.population_surnames))
        self.population = self.population

    def get_population(self):

        for person in self.population:
            yield "ID: {}\nName: {}\nSurname: {}\nGender: {}\nGender identity: {}\nSexual orientation: {}\nLife stage: {}\nFather: {}\nMother: {}\nSiblings: {}\nGrandparents: {}\nUncles: {}\nAunts: {}\nCousins: {}\nPartner: {}\nChildren: {}\nNephews: {}\nNieces: {}\nRelationship Status: {}\nPregnant: {}\nCan have children: {}\nWants children: {}\nProfession: {}\nEmployment: {}\n".format(
                person.family_id,
                person.name,
                person.surname,
                person.gender,
                person.gender_identity,
                person.sexual_orientation,
                person.life_stage,
                person.get_fathers_name(),
                person.get_mothers_name(),
                person.get_siblings_names(),
                person.get_grandparents_names(),
                person.get_uncles_names(),
                person.get_aunts_names(),
                person.get_cousins_names(),
                person.get_partners_name(),
                person.get_childrens_names(),
                person.get_nephews_names(),
                person.get_nieces_names(),
                person.relationship_status,
                person.is_pregnant,
                person.can_have_children,
                person.wants_children,
                person.occupation,
                person.employment
            )

    def age_up_population(self):

        self.population_copy = self.population


        for person in self.population_copy:
            person.age_up()
            if person.life_stage == self.SENIOR:
                print("\n{} {} has died of old age.\n".format(
                    person.name, person.surname))
                person.is_alive = False
            else:
                print("\n{} {} has aged up.\n".format(
                    person.name, person.surname))

        self.population = self.population

    def create_committed_relationship(self, person, persons_list):

        success = self.relationship_generator.assign_partner(
            person, persons_list)

        if not success:
            return

        # Create new couple and add it to couples list
        self.couples.append(StraightRelationship(person, person.partner))

        print("\n{} has started dating {}.\n".format(
            person.name, person.partner.name))

    def time_jump(self):

        for couple in self.couples:
            if not couple.is_married and couple.will_get_married:
                couple.get_married()
                print("\n{} and {} have married.\n".format(
                    couple.person1.name, couple.person2.name))
            elif couple.is_pregnant:
                self.give_birth(couple)
            elif couple.will_get_pregnant and couple.desired_num_of_children > 0 and not couple.is_pregnant:
                couple.get_pregnant()

        for person in self.romanceable_outsiders:
            self.create_committed_relationship(
                person, self.romanceable_outsiders)

        # Update population
        self.population = self.population

    def give_birth(self, couple):

        new_baby_names = []
        for _ in range(couple.expecting_children):
            new_baby = self.person_generator.generate_baby(couple)
            new_baby_names.append(new_baby.name)
            self.population.append(new_baby)

        print("{} and {} have given birth to {}.".format(
            couple.person1.name, couple.person2.name, new_baby_names))

        # Reset pregnancy variables
        couple.is_pregnant = False
        couple.get_female().is_pregnant = False
        couple.desired_num_of_children -= couple.expecting_children
        couple.expecting_children = 0

        # Update population
        self.population = self.population

    # NOT IMPLEMENTED YET

    def populate_neighborhood(self):
        pass

    def populate_world(self):
        pass
