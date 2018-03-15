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

    # ABOUT RELATIONSHIPS

    ONE_CHILD = 1
    TWO_CHILDREN = 2
    THREE_CHILDREN = 3
    FOUR_CHILDREN = 4
    NUM_OF_CHILDREN_PER_COUPLE = (ONE_CHILD, TWO_CHILDREN, THREE_CHILDREN, FOUR_CHILDREN)
    
    ALLOWED_NUM_OF_ADOPTIONS = (ONE_CHILD, TWO_CHILDREN)


    SINGLETON = 1
    TWINS = 2
    TRIPLETS = 3
    ALLOWED_NUM_OF_CHILDREN = (SINGLETON, TWINS, TRIPLETS)

    def __init__(self):
        pass