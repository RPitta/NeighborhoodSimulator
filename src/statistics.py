from utilities.randomizer import Randomizer
from traits import Traits


class Statistics:

    def __init__(self, setup, stages):
        self.setup = setup
        self.stages = stages
        self.randomizer = Randomizer()

    def get_name(self, person):
        """Returns a name from provided list that is unique among person's siblings and cousins."""
        unique = False
        while not unique:
            name = self.randomizer.get_random_item(
                self.setup.MALE_NAMES) if person.is_male else self.randomizer.get_random_item(
                self.setup.FEMALE_NAMES)
            unique = name not in (person.get_siblings_names(), person.get_cousins_names())
        return name

    def get_surname(self, unavailable_surnames=None):
        """Returns a surname from provided list that is unique among the population."""
        if unavailable_surnames is None:
            return self.randomizer.get_random_item(self.setup.SURNAMES)
        unique = False
        while not unique:
            surname = self.randomizer.get_random_item(self.setup.SURNAMES)
            unique = surname not in unavailable_surnames
        return surname

    def get_gender(self):

        options = {
            Traits.MALE: 50,
            Traits.FEMALE: 50
        }

        selected = self.randomizer.get_random_dict_key(options)

        if selected not in Traits.GENDERS:
            raise Exception("Unexpected error occurred. Wrong gender.")

        return selected

    def get_gender_identity(self):

        options = {
            Traits.CISGENDER: 98,
            Traits.TRANSGENDER: 2
        }

        selected = self.randomizer.get_random_dict_key(options)

        if selected not in Traits.GENDER_IDENTITIES:
            raise Exception(
                "Wrong gender identity.")

        return selected

    def get_race(self):

        options = {
            Traits.WHITE: 69.5,
            Traits.BLACK: 12.7,
            Traits.LATINO: 17.8
        }

        selected = self.randomizer.get_random_dict_key(options)

        if selected not in Traits.RACES:
            raise Exception(
                "Wrong race.")

        return selected


    def get_social_class(self):

        options = {
            Traits.LOWERCLASS: 10,
            Traits.MIDDLECLASS: 80,
            Traits.UPPERCLASS: 10
        }

        selected = self.randomizer.get_random_dict_key(options)

        if selected not in Traits.SOCIAL_CLASSES:
            raise Exception(
                "Wrong social class.")

        return selected

    def get_employment_chance(self):

        options = {
            Traits.EMPLOYED: 80,
            Traits.UNEMPLOYED: 20
        }

        selected = self.randomizer.get_random_dict_key(options)

        if selected not in Traits.EMPLOYMENT:
            raise Exception(
                "Wrong employment attribute.")

        return selected

    def get_death_cause(self, person):

        if person.death_date is False:
            return Traits.OLD_AGE

        if person.death_date < self.stages.TEEN.start:
            return Traits.ILLNESS

        options_teen = {
            Traits.ILLNESS: 30,
            Traits.SUICIDE: 70
        }

        options_young_adult = {
            Traits.ILLNESS: 30,
            Traits.SUICIDE: 10,
            Traits.ACCIDENT: 60
        }

        options_adult = {
            Traits.ILLNESS: 45,
            Traits.SUICIDE: 10,
            Traits.ACCIDENT: 45
        }

        options_senior = {
            Traits.ILLNESS: 80,
            Traits.SUICIDE: 10,
            Traits.ACCIDENT: 10
        }

        if person.death_date in self.stages.TEEN.span:
            selected = self.randomizer.get_random_dict_key(options_teen)
        elif person.death_date in self.stages.YOUNGADULT.span:
            selected = self.randomizer.get_random_dict_key(options_young_adult)
        elif person.death_date in self.stages.ADULT.span:
            selected = self.randomizer.get_random_dict_key(options_adult)
        elif person.death_date in self.stages.SENIOR.span:
            selected = self.randomizer.get_random_dict_key(options_senior)
        else:
            raise Exception("Wrong death date.")

        if selected not in Traits.DEATH_CAUSES:
            raise Exception("Wrong death cause.")

        return selected

    def get_death_date(self):

        options_general = {
            "before_old_age": 50,
            "old_age": 50
        }

        options_before_old_age = {
            self.stages.BABY: 1,
            self.stages.CHILD: 2,
            self.stages.TEEN: 3,
            self.stages.YOUNGADULT: 4,
            self.stages.ADULT: 10,
            self.stages.SENIOR: 80
        }

        selected = self.randomizer.get_random_dict_key(options_general)

        if selected == "old_age":
            return False

        random_life_stage = self.randomizer.get_random_dict_key(
            options_before_old_age)

        death_date = self.randomizer.get_random_item(random_life_stage.span)

        if death_date not in self.stages.LIFESPAN:
            raise Exception("Wrong death date.")

        return death_date

    def get_fertility(self):

        options = {
            True: 90,
            False: 10
        }

        return self.randomizer.get_random_dict_key(options)

    def get_domestic_partnership_desire(self):

        options = {
            True: 80,
            False: 20
        }

        return self.randomizer.get_random_dict_key(options)

    def get_children_desire(self):

        options = {
            True: 60,
            False: 40
        }

        return self.randomizer.get_random_dict_key(options)

    def get_sexual_orientation(self):

        main = {
            "het": 90,
            "homo/bi": 8,
            "ace": 2
        }

        homo_bi = {
            "homo": 40,
            "bi": 60
        }

        romantic__aromantic = {
            "aromantic": 50,
            "romantic": 50
        }

        romantic_orientations = {
            "het": 90,
            "homo/bi": 10
        }

        orientation = self.randomizer.get_random_dict_key(main)

        # Returns "heterosexual"
        if orientation == "het":
            return Traits.SEXUAL_ORIENTATIONS_DICT[orientation]["allosexual"]

        # Returns either "homosexual" or "bisexual"
        if orientation == "homo/bi":
            orientation = self.randomizer.get_random_dict_key(homo_bi)
            return Traits.SEXUAL_ORIENTATIONS_DICT[orientation]["allosexual"]

        if orientation == "ace":
            orientation = self.randomizer.get_random_dict_key(
                romantic__aromantic)

            # Returns "aromantic asexual"
            if orientation == "aromantic":
                return Traits.SEXUAL_ORIENTATIONS_DICT[orientation]

            orientation = self.randomizer.get_random_dict_key(
                romantic_orientations)

            # Returns "heteroromantic asexual"
            if orientation == "het":
                return Traits.SEXUAL_ORIENTATIONS_DICT[orientation]["asexual"]

            # Returns either "homoromantic asexual" or "biromantic asexual"
            if orientation == "homo/bi":
                orientation = self.randomizer.get_random_dict_key(homo_bi)
                return Traits.SEXUAL_ORIENTATIONS_DICT[orientation]["asexual"]

    def get_relationship_orientation(self):

        options = {
            Traits.MONOAMOROUS: 90,
            Traits.POLYAMOROUS: 10
        }

        return self.randomizer.get_random_dict_key(options)

    def get_marriage_desire(self):

        options = {
            True: 60,
            False: 40
        }

        return self.randomizer.get_random_dict_key(options)

    def get_liberalism(self):

        rates = {
            True: 60,
            False: 40
        }

        return self.randomizer.get_random_dict_key(rates)

    def get_desired_num_of_children(self):

        options = {
            Traits.ONE_CHILD: 40,
            Traits.TWO_CHILDREN: 30,
            Traits.THREE_CHILDREN: 20,
            Traits.FOUR_CHILDREN: 10
        }

        return self.randomizer.get_random_dict_key(options)

    def get_pregnancy_num_of_children(self):
        """Random number of children for pregnancy: singleton/twins/triplets"""

        options = {
            Traits.SINGLETON: 96,
            Traits.TWINS: 3,
            Traits.TRIPLETS: 1
        }

        return self.randomizer.get_random_dict_key(options)

    def get_adoption_num_of_children(self):

        options = {
            Traits.ONE_CHILD: 70,
            Traits.TWO_CHILDREN: 30
        }

        return self.randomizer.get_random_dict_key(options)

    def get_breakup_chance(self):

        options = {
            True: 60,
            False: 40
        }

        return self.randomizer.get_random_dict_key(options)

    def get_intergenerational_chance(self):
        """Returns true if intergenerational relationship. False otherwise."""

        options = {
            True: 10,
            False: 90
        }

        return self.randomizer.get_random_dict_key(options)

    def get_family_love_chance(self):
        """Returns true if person will fall in love with family member. False otherwise."""

        options = {
            True: 10,
            False: 90
        }

        return self.randomizer.get_random_dict_key(options)

    def get_triad_chance(self):

        options = {
            True: 30,
            False: 70
        }

        return self.randomizer.get_random_dict_key(options)

    # EARLY / MID / LATE WITHIN RANGE

    def get_oldest_breakup_date(self, couple):
        """Returns breakup date for oldest person."""
        return self.get_chance_for_early_mid_late(couple.oldest.span_left_till_old_age, 50, 30, 20)

    def get_oldest_pregnancy_date(self, couple):
        """Returns pregnancy date for oldest person."""
        return self.get_chance_for_early_mid_late(couple.pregnancy_timespan, 70, 20, 10)

    def get_chance_for_early_mid_late(self, lst, early_num, mid_num, late_num):

        if len(lst) in range(1, 4):
            return self.randomizer.get_random_item(lst)

        lst = list(self.split_list_in_three(lst, 3))
        early = lst[0]
        mid = lst[1]
        late = lst[2]

        options = {
            1: early_num,
            2: mid_num,
            3: late_num
        }

        selected = self.randomizer.get_random_dict_key(options)
        if selected == 1:
            return self.randomizer.get_random_item(early)
        if selected == 2:
            return self.randomizer.get_random_item(mid)
        return self.randomizer.get_random_item(late)

    @staticmethod
    def split_list_in_three(lst, n):
        k, m = divmod(len(lst), n)
        return (lst[i * k + min(i, m):(i + 1) * k + min(i + 1, m)] for i in range(n))
