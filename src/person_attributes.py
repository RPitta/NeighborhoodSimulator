
class PersonAttributes:

    MALE_NAMES = []
    FEMALE_NAMES = []
    SURNAMES = []

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

    def get_lifestage_from_age(self, age):
        for key, value in self.AGES.items():
            if value == age:
                return key

        raise Exception(
            "Unexpected error occurred. Given age not found in dict.")