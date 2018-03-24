import os

from life_stage import Baby, Child, Teen, YoungAdult, Adult, Senior


class Setup:
    """Initialize names and surnames from files."""
    MALE_NAMES = []
    FEMALE_NAMES = []
    SURNAMES = []
    PROFESSIONS = []
    MIN_WORDS = 800

    def __init__(self):
        self.MALE_NAMES = self.get_male_names()
        self.FEMALE_NAMES = self.get_female_names()
        self.SURNAMES = self.get_surnames()
        self.PROFESSIONS = self.get_professions()

    def get_male_names(self):
        with open(self.find_file_location("male_names.txt"), "r") as file_males:
            names = set([x.split('\n')[0] for x in file_males.readlines()])
            self.validate_list(names)
            names = self.capitalize_words(names)

            return names

    def get_female_names(self):
        with open(self.find_file_location("female_names.txt"), "r") as file_females:
            names = set([x.split('\n')[0] for x in file_females.readlines()])
            self.validate_list(names)
            names = self.capitalize_words(names)

            return names

    def get_surnames(self):
        with open(self.find_file_location("surnames.txt"), "r") as file_surnames:
            surnames = set([x.split('\t')[0] for x in file_surnames.readlines()])
            self.validate_list(surnames)
            surnames = self.capitalize_words(surnames)

            return surnames

    def get_professions(self):
        with open(self.find_file_location("professions.txt"), "r") as file_professions:
            professions = set([x.split('\n')[0] for x in file_professions.readlines()])
            self.validate_list(professions)
            professions = self.capitalize_words(professions)

            return professions

    @staticmethod
    def find_file_location(file_name):
        path_file = os.path.dirname(os.path.realpath(__file__))
        path_full = path_file + '\\files\\' + file_name
        return path_full

    @staticmethod
    def capitalize_words(lst):
        return [item.capitalize() for item in lst]

    def validate_list(self, lst):
        if lst is None or len(lst) < self.MIN_WORDS:
            raise Exception("Given list from file is empty or less than the minimum.")


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

    # Race
    WHITE = "White"
    BLACK = "Black"
    LATINO = "Latino"
    RACES = (WHITE, BLACK, LATINO)

    # Social class
    UPPERCLASS = "Upperclass"
    MIDDLECLASS = "Middleclass"
    LOWERCLASS = "Lowerclass"
    SOCIAL_CLASSES = (UPPERCLASS, MIDDLECLASS, LOWERCLASS)

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
    ALLOWED_NUM_OF_CHILDREN_PER_COUPLE = (
        ONE_CHILD, TWO_CHILDREN, THREE_CHILDREN, FOUR_CHILDREN)
    SIBLING_SET = (TWO_CHILDREN, THREE_CHILDREN, FOUR_CHILDREN)
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


class LifeStages:
    """Global variables for instantiated life stages."""
    BABY = Baby()
    CHILD = Child()
    TEEN = Teen()
    YOUNGADULT = YoungAdult()
    ADULT = Adult()
    SENIOR = Senior()
    LIFESTAGES = (BABY, CHILD, TEEN, YOUNGADULT, ADULT, SENIOR)
    LIFESPAN = list(range(BABY.start, SENIOR.end + 1))
