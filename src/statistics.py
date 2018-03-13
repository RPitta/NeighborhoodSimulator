import random
from person_attributes import PersonAttributes
from relationship_attributes import RelationshipAttributes
from randomizer import Randomizer


class Statistics(PersonAttributes, RelationshipAttributes):

    def get_name(self, person):

        unique = False
        while not unique:
            if person.is_male:
                name = Randomizer().get_random_list_item(self.MALE_NAMES)
            else:
                name = Randomizer().get_random_list_item(self.FEMALE_NAMES)
            unique = name not in person.get_siblings_names(
            ) and name not in person.get_cousins_names()
        return name

    def get_surname(self, unavailable_surnames):

        unique = False
        while not unique:
            surname = Randomizer().get_random_list_item(self.SURNAMES)
            unique = surname not in unavailable_surnames
        return surname

    def get_gender(self):

        options = {
            self.MALE: 50,
            self.FEMALE: 50
        }

        selected = Randomizer().get_random_dict_key(options)

        if selected not in self.GENDERS:
            raise Exception("Unexpected error occurred. Wrong gender.")

        return selected

    def get_gender_identity(self):

        options = {
            self.CISGENDER: 98,
            self.TRANSGENDER: 2
        }

        selected = Randomizer().get_random_dict_key(options)

        if selected not in self.GENDER_IDENTITIES:
            raise Exception("Unexpected error occurred. Wrong gender identity.")

        return selected

    def get_employment_chance(self, person):

        options = {
            self.EMPLOYED: 80,
            self.UNEMPLOYED: 20
        }

        selected = Randomizer().get_random_dict_key(options)

        if selected not in self.EMPLOYMENT:
            raise Exception("Unexpected error occurred. Wrong employment attribute.")

        return selected 

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
        if person.sexual_orientation == self.AROMANTIC_ASEXUAL:
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
            return self.SEXUAL_ORIENTATIONS_DICT[orientation]["allosexual"]

        # Returns either "homosexual" or "bisexual"
        if orientation == "homo/bi":
            orientation = Randomizer().get_random_dict_key(homo_bi)
            return self.SEXUAL_ORIENTATIONS_DICT[orientation]["allosexual"]

        if orientation == "ace":
            orientation = Randomizer().get_random_dict_key(romantic__aromantic)

            # Returns "aromantic asexual"
            if orientation == "aromantic":
                return self.SEXUAL_ORIENTATIONS_DICT[orientation]

            orientation = Randomizer().get_random_dict_key(romantic_orientations)

            # Returns "heteroromantic asexual"
            if orientation == "het":
                return self.SEXUAL_ORIENTATIONS_DICT[orientation]["asexual"]

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
        if not person.wants_domestic_partnership:
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
        if person.is_male:
            same_gender = self.MALE
            opposite_gender = self.FEMALE
        else:
            same_gender = self.FEMALE
            opposite_gender = self.MALE

        # Logic behind sexual orientation that returns appropiate gender(s)
        if person.sexual_orientation == self.HETEROSEXUAL or \
                person.sexual_orientation == self.HETEROROMANTIC_ASEXUAL:
            yield opposite_gender
        if person.sexual_orientation == self.HOMOSEXUAL or \
                person.sexual_orientation == self.HOMOROMANTIC_ASEXUAL:
            yield same_gender
        if person.sexual_orientation == self.BISEXUAL or \
                person.sexual_orientation == self.BIROMANTIC_ASEXUAL:
            yield same_gender
            yield opposite_gender
        if person.sexual_orientation == self.AROMANTIC_ASEXUAL:
            yield None

    def get_liberalism(self, person):

        # If person belongs to a minority group, a liberal ideology is automatically true
        if person.is_minority:
            return True

        rates = {
            True: 60,
            False: 40
        }

        return Randomizer().get_random_dict_key(rates)

    def get_desired_number_of_children(self, couple):

        if not couple.will_get_pregnant and not couple.will_adopt:
            return 0

        options = {
            self.ONE_CHILD : 40,
            self.TWO_CHILDREN : 30,
            self.THREE_CHILDREN : 20,
            self.FOUR_CHILDREN : 10
        }

        return Randomizer().get_random_dict_key(options)

    def get_breakup_chance(self, couple):

        # If a person is already a senior when they get into a committed relationship, they won't break up as death will come first
        if couple.person1.life_stage == self.SENIOR or couple.person2.life_stage == self.SENIOR:
            return False

        options = {
            True : 60,
            False : 40
        }

        return Randomizer().get_random_dict_key(options)

    def get_breakup_date(self, couple):

        # Automatically return none if couple won't break up
        if not couple.will_breakup:
            return None

        options_for_young_adults = {
            self.YOUNG_ADULT : 30,
            self.ADULT : 50,
            self.SENIOR : 20              
        }

        options_for_adults = {
            self.SENIOR : 50,
            self.ADULT : 50
        }

        options_for_intergenerational = {
            self.ADULT : 50,
            self.YOUNG_ADULT : 50               
        }

        # If couple are adults, they can break up soon as adults or as seniors
        # If couple are young adults, they can break up soon as young adults, adults or seniors
        # If couple is intergenerational, they can break up when soon when youngest is a young adult, or when youngest is an adult
        if not couple.is_intergenerational:
            if couple.person1.life_stage == self.ADULT:
                selected = Randomizer().get_random_dict_key(options_for_adults)        
            elif couple.person1.life_stage == self.YOUNG_ADULT:
                selected = Randomizer().get_random_dict_key(options_for_young_adults)
            else:
                raise Exception("Unexpected error occurred. Couple's age is wrong, are seniors or underage.")     
        else:
            selected = Randomizer().get_random_dict_key(options_for_intergenerational)

        if selected not in self.LIFE_STAGES:
            raise Exception("Unexpected error occurred. Break-up date is not correct.")

        return selected

    def get_intergenerational_chance(self, person):
        """Returns true if intergenerational relationship. False otherwise."""

        if not person.wants_domestic_partnership:
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