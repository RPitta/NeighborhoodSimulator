import random
from utilities.randomizer import Randomizer


class Statistics:

    def __init__(self, names, professions, traits, stages, randomizer):
        self.names = names
        self.professions = professions
        self.traits = traits
        self.stages = stages
        self.randomizer = randomizer

    def get_name(self, person):

        unique = False
        while not unique:
            if person.is_male:
                name = self.randomizer.get_random_list_item(self.names.MALE_NAMES)
            else:
                name = self.randomizer.get_random_list_item(self.names.FEMALE_NAMES)
            unique = name not in person.get_siblings_names(
            ) and name not in person.get_cousins_names()
        return name

    def get_surname(self, person, unavailable_surnames=None):
        if unavailable_surnames is None:
            return self.randomizer.get_random_list_item(self.names.SURNAMES)
        unique = False
        while not unique:
            surname = self.randomizer.get_random_list_item(self.names.SURNAMES)
            unique = surname not in unavailable_surnames
        return surname

    def get_gender(self):

        options = {
            self.traits.MALE: 50,
            self.traits.FEMALE: 50
        }

        selected = self.randomizer.get_random_dict_key(options)

        if selected not in self.traits.GENDERS:
            raise Exception("Unexpected error occurred. Wrong gender.")

        return selected

    def get_gender_identity(self):

        options = {
            self.traits.CISGENDER: 98,
            self.traits.TRANSGENDER: 2
        }

        selected = self.randomizer.get_random_dict_key(options)

        if selected not in self.traits.GENDER_IDENTITIES:
            raise Exception(
                "Unexpected error occurred. Wrong gender identity.")

        return selected

    def get_employment_chance(self, person):

        options = {
            self.traits.EMPLOYED: 80,
            self.traits.UNEMPLOYED: 20
        }

        selected = self.randomizer.get_random_dict_key(options)

        if selected not in self.traits.EMPLOYMENT:
            raise Exception(
                "Unexpected error occurred. Wrong employment attribute.")

        return selected

    def get_death_cause(self, person):

        if person.death_date is None:
            raise Exception("Unexpected error occurred. Death date is null.")

        # If the deatraitste is false, automatically return old age as deatraitsuse
        if not person.death_date:
            return self.traits.OLD_AGE

        # If the deatraitste is baby or child, automatically return illness as deatraitsuse
        if person.death_date in self.stages.BABY.span or person.death_date in self.stages.CHILD.span:
            return self.traits.ILLNESS

        options_teen = {
            self.traits.ILLNESS: 30,
            self.traits.SUICIDE: 70
        }

        options_young_adult = {
            self.traits.ILLNESS: 30,
            self.traits.SUICIDE: 10,
            self.traits.ACCIDENT: 60
        }

        options_adult = {
            self.traits.ILLNESS: 45,
            self.traits.SUICIDE: 10,
            self.traits.ACCIDENT: 45
        }

        options_senior = {
            self.traits.ILLNESS: 80,
            self.traits.SUICIDE: 10,
            self.traits.ACCIDENT: 10
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
            raise Exception("Unexpected error occurred. Wrong deatraitste.")

        if selected not in self.traits.DEATH_CAUSES:
            raise Exception("Unexpected error occurred. Wrong deatraitsuse.")

        return selected

    def get_death_date(self, person):

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

        random_life_stage = self.randomizer.get_random_dict_key(options_before_old_age)

        death_date = self.randomizer.get_random_list_item(random_life_stage.span)

        return death_date

    def get_fertility(self, person):

        # If person is transgender, ability to have biological children is automatically off
        if person.gender_identity == self.traits.TRANSGENDER:
            return False

        options = {
            True: 90,
            False: 10
        }

        return self.randomizer.get_random_dict_key(options)

    def get_domestic_partnership_desire(self, person):

        # If person is aromantic asexual, a wish for romance is automatically false
        if person.sexual_orientation == self.traits.AROMANTIC_ASEXUAL:
            return False

        # If person is conservative, a wish (or obligation) for romance is automatically true
        if not person.is_liberal:
            return True

        options = {
            True: 80,
            False: 20
        }

        return self.randomizer.get_random_dict_key(options)

    def get_children_desire(self, person):

        # If person is conservative, a wish (or obligation) to have childre is automatically true
        if not person.is_liberal:
            return True

        options = {
            True: 60,
            False: 40
        }

        return self.randomizer.get_random_dict_key(options)

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

        orientation = self.randomizer.get_random_dict_key(main)

        # Returns "heterosexual"
        if orientation == "het":
            return self.traits.SEXUAL_ORIENTATIONS_DICT[orientation]["allosexual"]

        # Returns either "homosexual" or "bisexual"
        if orientation == "homo/bi":
            orientation = self.randomizer.get_random_dict_key(homo_bi)
            return self.traits.SEXUAL_ORIENTATIONS_DICT[orientation]["allosexual"]

        if orientation == "ace":
            orientation = self.randomizer.get_random_dict_key(romantic__aromantic)

            # Returns "aromantic asexual"
            if orientation == "aromantic":
                return self.traits.SEXUAL_ORIENTATIONS_DICT[orientation]

            orientation = self.randomizer.get_random_dict_key(romantic_orientations)

            # Returns "heteroromantic asexual"
            if orientation == "het":
                return self.traits.SEXUAL_ORIENTATIONS_DICT[orientation]["asexual"]

            # Returns either "homoromantic asexual" or "biromantic asexual"
            if orientation == "homo/bi":
                orientation = self.randomizer.get_random_dict_key(homo_bi)
                return self.traits.SEXUAL_ORIENTATIONS_DICT[orientation]["asexual"]

    def get_relationship_orientation(self):

        options = {
            self.traits.MONOAMOROUS: 80,
            self.traits.POLYAMOROUS: 20
        }

        return self.randomizer.get_random_dict_key(options)

    def get_marriage_desire(self, person):

        # If person doesn't want domestic partnership, marriage desire is automatically false
        if not person.wants_domestic_partnership:
            return False

        # If person is conservative, a wish (or obligation) to get married is automatically true
        if not person.is_liberal:
            return True

        options = {
            True: 60,
            False: 40
        }

        return self.randomizer.get_random_dict_key(options)

    def get_target_gender(self, person):

        # Assign same gender / opposite gender
        if person.is_male:
            same_gender = self.traits.MALE
            opposite_gender = self.traits.FEMALE
        else:
            same_gender = self.traits.FEMALE
            opposite_gender = self.traits.MALE

        # Logic behind sexual orientation that returns appropiate gender(s)
        if person.sexual_orientation == self.traits.HETEROSEXUAL or \
                person.sexual_orientation == self.traits.HETEROROMANTIC_ASEXUAL:
            yield opposite_gender
        if person.sexual_orientation == self.traits.HOMOSEXUAL or \
                person.sexual_orientation == self.traits.HOMOROMANTIC_ASEXUAL:
            yield same_gender
        if person.sexual_orientation == self.traits.BISEXUAL or \
                person.sexual_orientation == self.traits.BIROMANTIC_ASEXUAL:
            yield same_gender
            yield opposite_gender
        if person.sexual_orientation == self.traits.AROMANTIC_ASEXUAL:
            yield None

    def get_liberalism(self, person):

        # If person belongs to a minority group, a liberal ideology is automatically true
        if person.is_minority:
            return True

        rates = {
            True: 60,
            False: 40
        }

        return self.randomizer.get_random_dict_key(rates)

    def get_desired_num_of_children(self, couple):

        if not couple.all_can_and_want_children and not couple.all_want_children_but_cant:
            return 0

        options = {
            self.traits.ONE_CHILD: 40,
            self.traits.TWO_CHILDREN: 30,
            self.traits.THREE_CHILDREN: 20,
            self.traits.FOUR_CHILDREN: 10
        }

        return self.randomizer.get_random_dict_key(options)

    def get_pregnancy_num_of_children(self, couple):
        """Random number of children for pregnancy: singleton/twins/triplets"""

        options = {
            self.traits.SINGLETON: 96,
            self.traits.TWINS: 3,
            self.traits.TRIPLETS: 1
        }

        return self.randomizer.get_random_dict_key(options)

    def get_adoption_num_of_children(self, couple):

        options = {
            self.traits.ONE_CHILD: 70,
            self.traits.TWO_CHILDREN: 30
        }

        return self.randomizer.get_random_dict_key(options)

    def get_breakup_chance(self, couple):

        options = {
            True: 60,
            False: 40
        }

        return self.randomizer.get_random_dict_key(options)

    def get_intergenerational_chance(self, person):
        """Returns true if intergenerational relationship. False otherwise."""

        if not person.wants_domestic_partnership and not person.in_love_with_family:
            return False

        options = {
            True: 20,
            False: 80
        }

        return Randomizer().get_random_dict_key(options)

    def get_family_love_chance(self, person):
        """Returns true if person will fall in love with family member. False otherwise."""

        if person.family is None or len(person.family) == 0:
            return False
        if not person.wants_domestic_partnership:
            return False

        options = {
            True: 5,
            False: 95
        }

        return Randomizer().get_random_dict_key(options)
        

    # EARLY / MID / LATE WITHIN RANGE

    def get_oldest_breakup_date(self, couple):
        """Returns oldest person's breakup date"""

        breakable_range = range(
            couple.oldest.age + 1, self.stages.SENIOR.end)

        return self.get_chance_for_early_mid_late(breakable_range, 50, 30, 20)

    def get_oldest_pregnancy_date(self, couple):

        if couple.will_get_married:
            fertile_range = range(couple.oldest.marriage_date + 1, self.stages.YOUNGADULT.end - 1)     
        else:
            fertile_range = range(couple.oldest.age + 1, self.stages.YOUNGADULT.end)

        return self.get_chance_for_early_mid_late(fertile_range, 70, 20, 10)

    def get_chance_for_early_mid_late(self, lst, early_num, mid_num, late_num):

        if len(lst) < 3:
            return self.randomizer.get_random_list_item(lst)
        
        lst = self.split_list_in_three(lst)
        early = lst[0]
        mid = lst[1]
        late = lst[2]

        options = {
            early: early_num,
            mid: mid_num,
            late: late_num
        }

        selected = self.randomizer.get_random_dict_key(options)
        return self.randomizer.get_random_list_item(selected)

    def split_list_in_three(self, lst):
        breakpoint = int((len(lst) / 3) + 1)
        return [lst[: breakpoint], lst[breakpoint: 2 * breakpoint], lst[2 * breakpoint:]]  