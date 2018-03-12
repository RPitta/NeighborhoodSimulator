
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

        self.population = []
        self.deceased_population = []
        self.population_surnames = []
        self.neighbors = []
        self.outsiders = []
        self.adult_outsiders = []
        self.romanceable_neighbors = []
        self.romanceable_outsiders = []
        self.partnered_outsiders = []
        self.couples = []

        self.populate_romanceable_straights(self.YOUNG_ADULT)

        # self.populate_world()
        # self.add_adult_outsiders()
        # self.add_romanceable_outsiders()
        # self.populate_neighborhood()
        # self.assign_partners()
        pass

    @property
    def population(self):
        return self._population

    @property
    def population_surnames(self):
        return self._population_surnames

    @population.setter
    def population(self, persons):

        if persons is None or len(persons) == 0:
            self._population = persons
        else:
            self._population = persons

            if any([person.is_alive is False for person in self._population]):
                raise Exception(
                    "Unexpected error occurred. One or more persons are dead.")

            # Update population surnames
            for person in self.population:
                if person.surname not in self._population_surnames:
                    self._population_surnames.append(person.surname)
            self._population_surnames = self._population_surnames

            # Update romanceable outsiders
            for person in persons:
                if person.is_free_and_willing_to_date():
                    self._romanceable_outsiders.append(person)
                    self._romanceable_outsiders = self._romanceable_outsiders

    @population_surnames.setter
    def population_surnames(self, surnames):
        self._population_surnames = surnames

    @property
    def romanceable_outsiders(self):
        return self._romanceable_outsiders

    @romanceable_outsiders.setter
    def romanceable_outsiders(self, persons):
        self._romanceable_outsiders = persons

    def get_population(self):

        for person in self.population:
            str = "ID: {}\nName: {}\nSurname: {}\nGender: {}\nGender identity: {}\nSexual orientation: {}\nLife stage: {}\nFather: {}\nMother: {}\nSiblings: {}\nGrandparents: {}\nUncles: {}\nAunts: {}\nCousins: {}\nPartner: {}\nChildren: {}\nNephews: {}\nNieces: {}\nRelationship Status: {}\nPregnant: {}\nCan have children: {}\nWants children: {}\n".format(
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
                person.wants_children
            )
            yield str

    def get_population_surnames(self):
        return self.population_surnames

    def age_up_population(self):

        self.population_copy = self.population

        for person in self.population_copy:
            if person.life_stage == self.SENIOR:
                print("{} {} has died of old age.".format(
                    person.name, person.surname))

                person.is_alive = False

                # Add dead senior to deceased population list
                self.deceased_population.append(person)
            else:
                print("{} {} has aged up and is now a {}".format(
                    person.name, person.surname, person.life_stage))

        # Remove dead seniors from population
        self.population[:] = [
            person for person in self.population if person.age_up() is True]

    def populate_romanceable_straights(self, age):

        for i in (number+1 for number in range(8)):
            self.population.append(self.person_generator.generate_romanceable_common_person(
                i, age, self.get_population_surnames()))
        self.population = self.population

    def create_committed_relationship(self, person, persons_list):

        success = self.relationship_generator.assign_common_partner(
            person, persons_list)

        if success:

            # Add person and their partner to partnered list
            self.partnered_outsiders.append(person)
            self.partnered_outsiders.append(person.partner)

            # Create new couple and add it to couples list
            self.couples.append(StraightRelationship(person, person.partner))

            # Remove person and their partner from romanceable persons
            self.romanceable_outsiders.remove(person.partner)
            self.romanceable_outsiders.remove(person)

    def time_jump(self):

        for couple in self.couples:
            if not couple.is_married and couple.will_get_married:
                couple.get_married()
                print("{} and {} have married.".format(
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
        # for i in range(self.NEIGHBOORHOOD_APARTMENTS):
        # self.neighbors.append(random.choice(self.adult_outsiders))

    def populate_world(self):
        for _ in range(10):
            self.outsiders.append(
                self.person_generator.generate_new_person("baby", self.get_population_surnames()))
        for _ in range(10):
            self.outsiders.append(
                self.person_generator.generate_new_person("child", self.get_population_surnames()))
        for _ in range(20):
            self.outsiders.append(
                self.person_generator.generate_new_person("teen", self.get_population_surnames()))
        for _ in range(20):
            self.outsiders.append(
                self.person_generator.generate_new_person("young adult", self.get_population_surnames()))
        for _ in range(20):
            self.outsiders.append(
                self.person_generator.generate_new_person("adult", self.get_population_surnames()))
        for _ in range(20):
            self.outsiders.append(
                self.person_generator.generate_new_person("senior", self.get_population_surnames()))

    def add_adult_outsiders(self):

        for person in self.outsiders:
            if person.is_of_age():
                self.adult_outsiders.append(person)

    def assign_partners(self):

        for person in self.romanceable_neighbors:
            self.relationship_generator.find_partner(
                person, self.romanceable_neighbors)


"""         attrs = vars(person1)
        print(', '.join("%s: %s" % item for item in attrs.items()))

        attrs2 = vars(person2)
        print(', '.join("%s: %s" % item for item in attrs2.items())) """
