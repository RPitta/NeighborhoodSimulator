import os
from utilities.randomizer import Randomizer
from life_stage import *
from social_class import *


class Setup:
    """Initialize names, surnames and professions from files."""
    MIN_WORDS = 800

    def __init__(self):
        self.MALE_NAMES = self.get_male_names()
        self.FEMALE_NAMES = self.get_female_names()
        self.SURNAMES = self.get_surnames()
        self.PROFESSIONS = self.get_professions()

    def get_male_names(self):
        """Add all male names from file to list."""
        with open(self.find_file_location("male_names.txt"), "r") as file_males:
            names = set([x.split('\n')[0] for x in file_males.readlines()])
            self.validate_list(names)
            return self.capitalize_words(names)

    def get_female_names(self):
        """Add all female names from file to list."""
        with open(self.find_file_location("female_names.txt"), "r") as file_females:
            names = set([x.split('\n')[0] for x in file_females.readlines()])
            self.validate_list(names)
            return self.capitalize_words(names)

    def get_surnames(self):
        """Add all surnames from file to list."""
        with open(self.find_file_location("surnames.txt"), "r") as file_surnames:
            surnames = set([x.split('\t')[0] for x in file_surnames.readlines()])
            self.validate_list(surnames)
            return self.capitalize_words(surnames)

    def get_professions(self):
        """Add all professions from file to list."""
        with open(self.find_file_location("professions.txt"), "r") as file_professions:
            professions = set([x.split('\n')[0] for x in file_professions.readlines()])
            self.validate_list(professions)
            return self.capitalize_words(professions)

    @staticmethod
    def find_file_location(file_name):
        path_file = os.path.dirname(os.path.realpath(__file__))
        path_full = os.path.join(path_file,'files', file_name)
        return path_full

    @staticmethod
    def capitalize_words(lst):
        return [item.capitalize() for item in lst]

    def validate_list(self, lst):
        if lst is None or len(lst) < self.MIN_WORDS:
            raise Exception("Given list from file is empty or less than the minimum.")


class Names:
    """Helper class to get names from lists initialized in Setup."""

    def __init__(self, setup):
        self.setup = setup
        self.randomizer = Randomizer()

    def get_name(self, person):
        """Returns a name from provided list that is unique among person's siblings and cousins."""
        name = unique = False
        while not unique:
            name = self.randomizer.get_random_item(
                self.setup.MALE_NAMES) if person.is_male else self.randomizer.get_random_item(self.setup.FEMALE_NAMES)
            unique = name not in (person.get_siblings_names, person.get_cousins_names)

        self.validate_name(name)
        return name

    def get_surname(self, unavailable_surnames=None):
        """Returns a surname from provided list that is unique among the population."""
        if unavailable_surnames is None:
            surname = self.randomizer.get_random_item(self.setup.SURNAMES)
            self.validate_surname(surname)
            return surname

        surname = unique = False
        while not unique:
            surname = self.randomizer.get_random_item(self.setup.SURNAMES)
            unique = surname not in unavailable_surnames

        self.validate_surname(surname, unavailable_surnames)
        return surname

    def validate_name(self, name):
        if name is None or name is False:
            raise Exception("Name is null.")
        if name not in self.setup.MALE_NAMES and name not in self.setup.FEMALE_NAMES:
            raise Exception("Name is wrong.")

    def validate_surname(self, surname, unavailable_surnames=None):
        if surname is None:
            raise Exception("Surname is null.")
        if unavailable_surnames is not None and surname in unavailable_surnames:
            raise Exception("Surname is not unique.")
        if surname not in self.setup.SURNAMES:
            raise Exception("Surname is wrong.")


class Traits:
    """Global variables for person traits."""
    # Genders
    MALE = "Male"
    FEMALE = "Female"
    GENDERS = (MALE, FEMALE)

    # Gender identities
    CISGENDER = "Cisgender"
    TRANSGENDER = "Transgender"
    GENDER_IDENTITIES = (CISGENDER, TRANSGENDER)

    # Life stages
    BABY = Baby()
    CHILD = Child()
    TEEN = Teen()
    YOUNGADULT = YoungAdult()
    ADULT = Adult()
    SENIOR = Senior()
    LIFE_STAGES = (BABY, CHILD, TEEN, YOUNGADULT, ADULT, SENIOR)
    LIFESPAN = list(range(BABY.start, SENIOR.end + 1))

    # Races
    WHITE = "White"
    BLACK = "Black"
    LATINO = "Latino"
    ASIAN = "Asian"
    RACES = (WHITE, BLACK, LATINO, ASIAN)

    # Race dict
    race_dict = {
        WHITE: 0,
        BLACK: 0,
        LATINO: 0,
        ASIAN: 0
    }

    # Conditions
    AUTISTIC_DISORDER = "Autistic Disorder"
    ASPERGERS = "Asperger's Syndrome"
    CONDITIONS = (AUTISTIC_DISORDER, ASPERGERS)
    AUTISM_AGE = 2
    DEPRESSION = "Depression"

    # Social classes
    UPPER_CLASS = UpperClass()
    MIDDLE_CLASS = MiddleClass()
    LOWER_CLASS = LowerClass()
    SOCIAL_CLASSES = (UPPER_CLASS, MIDDLE_CLASS, LOWER_CLASS)

    # Sexual orientations
    HETEROSEXUAL = "Heterosexual"
    HOMOSEXUAL = "Homosexual"
    BISEXUAL = "Bisexual"
    AROMANTIC_ASEXUAL = "Aromantic asexual"
    HETEROROMANTIC_ASEXUAL = "Heteroromantic asexual"
    HOMOROMANTIC_ASEXUAL = "Homoromantic asexual"
    BIROMANTIC_ASEXUAL = "Biromantic asexual"
    SEXUAL_ORIENTATIONS = (HETEROSEXUAL, HOMOSEXUAL, BISEXUAL, AROMANTIC_ASEXUAL,
                           HETEROROMANTIC_ASEXUAL, HOMOROMANTIC_ASEXUAL, BIROMANTIC_ASEXUAL)
    ASEXUAL_ORIENTATIONS = (AROMANTIC_ASEXUAL, HETEROROMANTIC_ASEXUAL,
                            HOMOROMANTIC_ASEXUAL, BIROMANTIC_ASEXUAL)

    SEXUAL_ORIENTATIONS_DICT = {
        "het": {
            "allosexual": HETEROSEXUAL,
            "asexual": HETEROROMANTIC_ASEXUAL
        },
        "bi": {
            "allosexual": BISEXUAL,
            "asexual": BIROMANTIC_ASEXUAL
        },
        "homo": {
            "allosexual": HOMOSEXUAL,
            "asexual": HOMOROMANTIC_ASEXUAL
        },
        "aromantic": AROMANTIC_ASEXUAL
    }

    # Employment
    EMPLOYED = "Employed"
    UNEMPLOYED = "Unemployed"
    RETIRED = "Retired"
    EMPLOYMENT = (EMPLOYED, UNEMPLOYED, RETIRED)

    # Civil status
    SINGLE = "Single"
    COMMITTED = "Committed"
    MARRIED = "Married"
    REMARRIED = "Remarried"
    DIVORCED = "Divorced"
    SEPARATED = "Separated"
    WIDOWED = "Widowed"
    CIVIL_STATUS = (SINGLE, COMMITTED, MARRIED, DIVORCED, SEPARATED, WIDOWED)

    # Relationship orientations
    MONOAMOROUS = "Monoamorous"
    POLYAMOROUS = "Polyamorous"
    RELATIONSHIP_ORIENTATIONS = (MONOAMOROUS, POLYAMOROUS)

    # Allowed number of partners for polys
    ALLOWED_NUM_OF_PARTNERS_FOR_POLYS = 2

    # Number of children per couple
    ONE_CHILD = 1
    TWO_CHILDREN = 2
    THREE_CHILDREN = 3
    FOUR_CHILDREN = 4
    ALLOWED_NUM_OF_CHILDREN_PER_COUPLE = (ONE_CHILD, TWO_CHILDREN, THREE_CHILDREN, FOUR_CHILDREN)

    # Adoption-related
    SIBLING_SET = (TWO_CHILDREN, THREE_CHILDREN, FOUR_CHILDREN)
    ALLOWED_NUM_OF_ADOPTIONS_PER_COUPLE = (ONE_CHILD, SIBLING_SET)
    MAX_AGE_FOR_ADOPTION = 15

    # Number of children per pregnancy
    SINGLETON = 1
    TWINS = 2
    TRIPLETS = 3
    ALLOWED_NUM_OF_CHILDREN_PER_PREGNANCY = (SINGLETON, TWINS, TRIPLETS)

    # Death causes
    OLD_AGE = "Old age"
    SUICIDE = "Suicide"
    ILLNESS = "Illness"
    ACCIDENT = "Accident"
    DRUG_OVERDOSE = "Drug overdose"
    ALCOHOL_OVERDOSE = "Alcohol overdose"
    DEATH_CAUSES = (OLD_AGE, SUICIDE, ILLNESS, ACCIDENT)
