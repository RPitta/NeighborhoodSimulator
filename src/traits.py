from life_stage import Baby, Child, Teen, YoungAdult, Adult, Senior


class Names:

    MALE_NAMES = []
    FEMALE_NAMES = []
    SURNAMES = []

    def __init__(self):
        # Initialize names from files
        self.MALE_NAMES = self.get_male_names()
        self.FEMALE_NAMES = self.get_female_names()
        self.SURNAMES = self.get_surnames()

    def get_male_names(self):
        path_males = r"C:\Users\cugat\Documents\Programming\Python\NeighborhoodSimulator\src\files\male_names.txt"
        file_males = open(path_males, "r")
        names = set([x.split('\n')[0] for x in file_males.readlines()])

        # Validation
        # Whatever number the developer wishes to set as minimum.
        if names is None or len(names) < 1000:
            raise Exception("List of names is empty or less than the minimum.")

        names = [item.capitalize() for item in names]

        file_males.close()
        return names

    def get_female_names(self):
        path_females = r"C:\Users\cugat\Documents\Programming\Python\NeighborhoodSimulator\src\files\female_names.txt"
        file_females = open(path_females, "r")
        names = set([x.split('\n')[0] for x in file_females.readlines()])

        # Validation
        # Whatever number the developer wishes to set as minimum.
        if names is None or len(names) < 800:
            raise Exception("List of names is empty or less than the minimum.")

        names = [item.capitalize() for item in names]

        file_females.close()
        return names

    def get_surnames(self):
        path_surnames = r"C:\Users\cugat\Documents\Programming\Python\NeighborhoodSimulator\src\files\surnames.txt"
        file_surnames = open(path_surnames, "r")
        surnames = set([x.split('\t')[0] for x in file_surnames.readlines()])

        # Validation
        # Whatever number the developer wishes to set as minimum.
        if surnames is None or len(surnames) < 1000:
            raise Exception(
                "List of surnames is empty or less than the minimum.")

        surnames = [item.capitalize() for item in surnames]

        file_surnames.close()
        return surnames


class Professions:

    PROFESSIONS = []

    def __init__(self):
        # Initialize professions from file
        self.PROFESSIONS = self.get_professions()

    def get_professions(self):
        path_professions = r"C:\Users\cugat\Documents\Programming\Python\NeighborhoodSimulator\src\files\professions.txt"
        file_professions = open(path_professions, "r")
        professions = set([x.split('\n')[0]
                           for x in file_professions.readlines()])

        # Validation
        # Whatever number the developer wishes to set as minimum.
        if professions is None or len(professions) < 1000:
            raise Exception(
                "List of professions is empty or less than the minimum.")

        professions = [item.capitalize() for item in professions]

        file_professions.close()
        return professions


class Traits:

    # Genders
    MALE = "Male"
    FEMALE = "Female"
    GENDERS = (MALE, FEMALE)

    # Gender identities
    CISGENDER = "Cisgender"
    TRANSGENDER = "Transgender"
    GENDER_IDENTITIES = (CISGENDER, TRANSGENDER)

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

    # Number of adopted children per couple
    ALLOWED_NUM_OF_ADOPTIONS = (ONE_CHILD, TWO_CHILDREN)

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
    DEATH_CAUSES = (OLD_AGE, SUICIDE, ILLNESS, ACCIDENT)


class LifeStages:

    BABY = Baby()
    CHILD = Child()
    TEEN = Teen()
    YOUNGADULT = YoungAdult()
    ADULT = Adult()
    SENIOR = Senior()
    LIFESTAGES = (BABY, CHILD, TEEN, YOUNGADULT, ADULT, SENIOR)
    LIFESPAN = range(BABY.start, SENIOR.end + 1)
