
from randomizer import Randomizer
from person_attributes import PersonAttributes
from person import Person
from straight_relationship import StraightRelationship


class PersonGenerator(PersonAttributes):

    def __init__(self):
        self.add_names()

    def add_names(self):
        """Adds file names to lists."""

        # Open files
        path_males = r"C:\Users\cugat\Documents\Programming\Python\NeighborhoodSimulator\src\files\male_names.txt"
        file_males = open(path_males, "r")
        path_females = r"C:\Users\cugat\Documents\Programming\Python\NeighborhoodSimulator\src\files\female_names.txt"
        file_females = open(path_females, "r")
        path_surnames = r"C:\Users\cugat\Documents\Programming\Python\NeighborhoodSimulator\src\files\surnames.txt"
        file_surnames = open(path_surnames, "r")

        # Add all names to list
        self.MALE_NAMES = [x.split(' ')[0] for x in file_males.readlines()]
        self.FEMALE_NAMES = [x.split(' ')[0] for x in file_females.readlines()]
        self.SURNAMES = [x.split(' ')[0] for x in file_surnames.readlines()]

        # Capitalize uppercase names
        self.MALE_NAMES = [item.capitalize() for item in self.MALE_NAMES]
        self.FEMALE_NAMES = [item.capitalize() for item in self.FEMALE_NAMES]
        self.SURNAMES = [item.capitalize() for item in self.SURNAMES]

        # Close files
        file_males.close()
        file_females.close()
        file_surnames.close()

    # RANDOMS

    def get_death_cause(self, person):

        if person.death_date is None:
            raise Exception("Unexpected error occurred. Death date is null.")

        # If the death date is false, automatically return old age as death cause
        if not person.death_date:
            return self.OLD_AGE

        # If the death date is baby or child, automatically return illness as death cause
        if person.death_date == self.BABY or person.death_date == self.CHILD:
            return self.ILLNESS

        options_teen = {
            self.ILLNESS: 30,
            self.SUICIDE: 70
        }

        options_young_adult = {
            self.ILLNESS: 30,
            self.SUICIDE: 10,
            self.ACCIDENT: 60
        }

        options_adult = {
            self.ILLNESS: 45,
            self.SUICIDE: 10,
            self.ACCIDENT: 45
        }

        options_senior = {
            self.ILLNESS: 80,
            self.SUICIDE: 10,
            self.ACCIDENT: 10
        }

        if person.death_date == self.TEEN:
            selected = Randomizer().get_random_dict_key(options_teen)
        elif person.death_date == self.YOUNG_ADULT:
            selected = Randomizer().get_random_dict_key(options_young_adult)
        elif person.death_date == self.ADULT:
            selected = Randomizer().get_random_dict_key(options_adult)
        elif person.death_date == self.SENIOR:
            selected = Randomizer().get_random_dict_key(options_senior)
        else:
            raise Exception("Unexpected error occurred. Wrong death date.")

        if selected not in self.DEATH_CAUSES:
            raise Exception("Unexpected error occurred. Wrong death cause.")

        return selected

    def get_death_date(self, person):

        options_general = {
            "before_old_age": 50,
            "old_age": 50
        }

        options_before_old_age = {
            self.BABY: 1,
            self.CHILD: 2,
            self.TEEN: 3,
            self.YOUNG_ADULT: 4,
            self.ADULT: 10,
            self.SENIOR: 80
        }

        selected = Randomizer().get_random_dict_key(options_general)

        if selected == "old_age":
            return False

        random_life_stage = Randomizer().get_random_dict_key(options_before_old_age)

        if random_life_stage not in self.LIFE_STAGES:
            raise Exception("Unexpected error occurred. Wrong life stage.")

        return random_life_stage

    def get_gender(self):

        options = {
            self.MALE: 50,
            self.FEMALE: 50
        }

        return Randomizer().get_random_dict_key(options)

    def get_gender_identity(self):

        options = {
            self.CISGENDER: 98,
            self.TRANSGENDER: 2
        }

        return Randomizer().get_random_dict_key(options)

    def get_fertility(self, person):

        # If person is transgender, ability to have biological children is automatically off
        if person.gender_identity == self.TRANSGENDER:
            return False

        options = {
            True: 90,
            False: 10
        }

        return Randomizer().get_random_dict_key(options)

    def get_domestic_partnership_desire(self, person):

        # If person is aromantic asexual, a wish for romance is automatically false
        if person.sexual_orientation == self.SEXUAL_ORIENTATIONS_DICT["aromantic"]:
            return False

        # If person is conservative, a wish (or obligation) for romance is automatically true
        if not person.is_liberal:
            return True

        options = {
            True: 80,
            False: 20
        }

        return Randomizer().get_random_dict_key(options)

    def get_children_desire(self, person):

        # If person is conservative, a wish (or obligation) to have childre is automatically true
        if not person.is_liberal:
            return True

        options = {
            True: 60,
            False: 40
        }

        return Randomizer().get_random_dict_key(options)

    def get_sexual_orientation(self):

        main = {
            "het": 93,
            "homo/bi": 5,
            "ace": 2
        }

        homo_bi = {
            "homo": 50,
            "bi": 50
        }

        romantic__aromantic = {
            "aromantic": 50,
            "romantic": 50
        }

        romantic_orientations = {
            "het": 95,
            "homo/bi": 5
        }

        orientation = Randomizer().get_random_dict_key(main)

        # Returns "heterosexual"
        if orientation == "het":
            return self.SEXUAL_ORIENTATIONS_DICT["het"]["allosexual"]

        # Returns either "homosexual" or "bisexual"
        if orientation == "homo/bi":
            orientation = Randomizer().get_random_dict_key(homo_bi)
            return self.SEXUAL_ORIENTATIONS_DICT[orientation]["allosexual"]

        if orientation == "ace":
            orientation = Randomizer().get_random_dict_key(romantic__aromantic)

            # Returns "aromantic asexual"
            if orientation == "aromantic":
                return self.SEXUAL_ORIENTATIONS_DICT["aromantic"]

            orientation = Randomizer().get_random_dict_key(romantic_orientations)

            # Returns "heteroromantic asexual"
            if orientation == "het":
                return self.SEXUAL_ORIENTATIONS_DICT["het"]["asexual"]

            # Returns either "homoromantic asexual" or "biromantic asexual"
            if orientation == "homo/bi":
                orientation = Randomizer().get_random_dict_key(homo_bi)
                return self.SEXUAL_ORIENTATIONS_DICT[orientation]["asexual"]

    def get_relationship_orientation(self):

        options = {
            self.MONOAMOROUS: 80,
            self.POLYAMOROUS: 20
        }

        return Randomizer().get_random_dict_key(options)

    def get_marriage_desire(self, person):

        # If person doesn't want domestic partnership, marriage desire is automatically false
        if person.wants_domestic_partnership == False:
            return False

        # If person is conservative, a wish (or obligation) to get married is automatically true
        if not person.is_liberal:
            return True

        options = {
            True: 60,
            False: 40
        }

        return Randomizer().get_random_dict_key(options)

    def get_target_gender(self, person):

        # Assign same gender / opposite gender
        if person.is_male():
            same_gender = self.MALE
            opposite_gender = self.FEMALE
        else:
            same_gender = self.FEMALE
            opposite_gender = self.MALE

        # Logic behind sexual orientation that returns appropiate gender(s)
        if person.sexual_orientation == self.SEXUAL_ORIENTATIONS_DICT["het"]["allosexual"] or \
                person.sexual_orientation == self.SEXUAL_ORIENTATIONS_DICT["het"]["asexual"]:
            yield opposite_gender
        if person.sexual_orientation == self.SEXUAL_ORIENTATIONS_DICT["homo"]["allosexual"] or \
                person.sexual_orientation == self.SEXUAL_ORIENTATIONS_DICT["homo"]["asexual"]:
            yield same_gender
        if person.sexual_orientation == self.SEXUAL_ORIENTATIONS_DICT["bi"]["allosexual"] or \
                person.sexual_orientation == self.SEXUAL_ORIENTATIONS_DICT["bi"]["asexual"]:
            yield same_gender
            yield opposite_gender
        if person.sexual_orientation == self.SEXUAL_ORIENTATIONS_DICT["aromantic"]:
            yield None

    def get_liberalism(self, person):

        # If person belongs to a minority group, a liberal ideology is automatically true
        if person.sexual_orientation != self.SEXUAL_ORIENTATIONS_DICT["het"] or \
                person.gender_identity != self.CISGENDER or \
                person.relationship_orientation != self.MONOAMOROUS:
            return True

        rates = {
            True: 60,
            False: 40
        }

        return Randomizer().get_random_dict_key(rates)

    def get_name(self, person):

        # If male
        if person.is_male():

            # Validate that the randomly chosen name is not the same as their siblings or cousins
            unique = False
            while not unique:
                name = Randomizer().get_random_list_item(self.MALE_NAMES)
                unique = name not in person.get_siblings_names() and name not in person.get_cousins_names()
            return name

        # If female
        elif person.is_female():

            # Validate that the randomly chosen name is not the same as their siblings or cousins
            unique = False
            while not unique:
                name = Randomizer().get_random_list_item(self.FEMALE_NAMES)
                unique = name not in person.siblings and name not in person.cousins
            return name

        else:
            raise Exception("Unexpected error occurred. Gender is wrong.")

    def get_surname(self, unavailable_surnames):

        unique = False
        while not unique:
            surname = Randomizer().get_random_list_item(self.SURNAMES)
            unique = surname not in unavailable_surnames

        return surname

    # GENERATOR

    def generate_new_person(self, age, unavailable_surnames):
        person = Person(self.get_gender(), age, self.get_gender_identity(),
                        self.get_sexual_orientation(), self.get_relationship_orientation())

        self.assign_all_random_attributes(person, unavailable_surnames)

        self.validate_new_person(person)

        return person

    def assign_all_random_attributes(self, person, unavailable_surnames):
        person.name = self.get_name(person)
        person.surname = self.get_surname(unavailable_surnames)
        person.original_surname = person.surname
        person.target_gender = [
            gender for gender in self.get_target_gender(person)]
        person.can_have_children = self.get_fertility(person)
        person.is_liberal = self.get_liberalism(person)
        person.wants_domestic_partnership = self.get_domestic_partnership_desire(
            person)
        person.wants_marriage = self.get_marriage_desire(person)
        person.wants_children = self.get_children_desire(person)



    def assign_child_attributes(self, baby, father, mother):

        # Assign mother and father
        baby.father = father
        baby.mother = mother
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

    def generate_romanceable_common_person(self, family_id, age, unavailable_surnames):
        """Returns a cis-straight, monoamorous romanceable person. Only gender, name and ideology are random."""

        person = Person(self.get_gender(), age, self.CISGENDER,
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

        self.validate_new_person(person)

        return person

    def generate_baby(self, couple):

        if couple is None or len(couple.persons) <= 1:
            raise Exception(
                "Unexpected error occurred. Given couple is wrong.")

        mother = couple.get_female()
        father = couple.get_male()

        baby = self.new_baby(father, mother)

        if baby.mother is None or baby.father is None or baby not in baby.mother.children or baby not in baby.father.children:
            raise Exception(
                "Unexpected error occurred. Baby and parents not correctly assigned.")
        for child in mother.children:
            if child != baby and (child not in baby.siblings or baby not in child.siblings):
                raise Exception(
                    "Unexpected error occurred. Baby and siblings not correctly assigned.")
            if child != baby and child.name == baby.name:
                raise Exception(
                    "Unexpected error occurred. Baby's name is the same as their sibling.")

        return baby

    def new_baby(self, father, mother):
        baby = Person(self.get_gender(), self.BABY, self.get_gender_identity(),
                      self.get_sexual_orientation(), self.get_relationship_orientation())

        self.assign_child_attributes(baby, father, mother)

        self.validate_new_person(baby)

        return baby

    def validate_new_person(self, person):
        lst = [person.gender, person.sexual_orientation, person.gender_identity,
               person.life_stage, person.age, person.is_liberal, person.relationship_orientation,
               person.wants_domestic_partnership, person.wants_marriage,
               person.wants_children, person.can_have_children]

        if any(attr is None for attr in lst):
            raise Exception(
                "Unexpected error occurred. Null values found when creating new person.")