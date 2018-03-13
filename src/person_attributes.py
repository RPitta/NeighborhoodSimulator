from utilities import Utilities

class PersonAttributes:

    MALE_NAMES = []
    FEMALE_NAMES = []
    SURNAMES = []
    PROFESSIONS = []

    MALE = "Male"
    FEMALE = "Female"
    GENDERS = (MALE, FEMALE)

    CISGENDER = "Cisgender"
    TRANSGENDER = "Transgender"
    GENDER_IDENTITIES = (CISGENDER, TRANSGENDER)

    SINGLE = "Single"
    COMMITTED = "Committed"
    MARRIED = "Married"
    DIVORCED = "Divorced"
    SEPARATED = "Separated"
    WIDOWED = "Widowed"
    CIVIL_STATUS = (SINGLE, COMMITTED, MARRIED, DIVORCED, SEPARATED, WIDOWED)

    EMPLOYED = "Employed"
    UNEMPLOYED = "Unemployed"
    RETIRED = "Retired"
    EMPLOYMENT = (EMPLOYED, UNEMPLOYED, RETIRED)

    BABY = "Baby"
    CHILD = "Child"
    TEEN = "Teen"
    YOUNG_ADULT = "Young adult"
    ADULT = "Adult"
    SENIOR = "Senior"
    LIFE_STAGES = (BABY, CHILD, TEEN, YOUNG_ADULT, ADULT, SENIOR)

    OLD_AGE = "Old age"
    SUICIDE = "Suicide"
    ILLNESS = "Illness"
    ACCIDENT = "Accident"
    DEATH_CAUSES = (OLD_AGE, SUICIDE, ILLNESS, ACCIDENT)

    AGES = {
        BABY: 1,
        CHILD: 2,
        TEEN: 3,
        YOUNG_ADULT: 4,
        ADULT: 5,
        SENIOR: 6
    }

    MONOAMOROUS = "Monoamorous"
    POLYAMOROUS = "Polyamorous"
    RELATIONSHIP_ORIENTATIONS = (MONOAMOROUS, POLYAMOROUS)

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

    def __init__(self):
        self.MALE_NAMES = self.get_male_names()
        self.FEMALE_NAMES = self.get_female_names()
        self.SURNAMES = self.get_surnames()
        self.PROFESSIONS = self.get_professions()

    def get_male_names(self):
        path_males = r"C:\Users\cugat\Documents\Programming\Python\NeighborhoodSimulator\src\files\male_names.txt"
        file_males = open(path_males, "r")
        names = set([x.split(' ')[0] for x in file_males.readlines()])
        names = [item.capitalize() for item in names]
        file_males.close()
        return names

    def get_female_names(self):
        path_females = r"C:\Users\cugat\Documents\Programming\Python\NeighborhoodSimulator\src\files\female_names.txt"
        file_females = open(path_females, "r")
        names = set([x.split(' ')[0] for x in file_females.readlines()])
        names = [item.capitalize() for item in names]
        return names

    def get_surnames(self):
        path_surnames = r"C:\Users\cugat\Documents\Programming\Python\NeighborhoodSimulator\src\files\surnames.txt"
        file_surnames = open(path_surnames, "r")    
        surnames = set([x.split(' ')[0] for x in file_surnames.readlines()])
        surnames = [item.capitalize() for item in surnames]    
        file_surnames.close()
        return surnames

    def get_professions(self):
        path_professions = r"C:\Users\cugat\Documents\Programming\Python\NeighborhoodSimulator\src\files\professions.txt"
        file_professions = open(path_professions, "r")
        professions = set([x.split('\n')[0] for x in file_professions.readlines()])
        professions = [item.capitalize() for item in professions]
        file_professions.close()
        return professions