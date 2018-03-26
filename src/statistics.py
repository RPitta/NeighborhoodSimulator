from utilities.randomizer import Randomizer
from traits import Traits
import sql_connect

class Statistics:

    def __init__(self, stages):
        self.stages = stages
        self.randomizer = Randomizer()

    def get_gender(self):

        options = {
            Traits.MALE: 50,
            Traits.FEMALE: 50
        }

        selected = self.randomizer.get_random_dict_key(options)

        if selected not in Traits.GENDERS:
            raise Exception("Wrong gender.")

        return selected

    def get_gender_identity(self):

        options = {
            Traits.CISGENDER: 98,
            Traits.TRANSGENDER: 2
        }

        selected = self.randomizer.get_random_dict_key(options)

        if selected not in Traits.GENDER_IDENTITIES:
            raise Exception("Wrong gender identity.")

        return selected

    def get_race(self):
        dbmgr = sql_connect.DatabaseManager("testdb.db")
        race_data = dbmgr.demo_data("default", "race")
        options = {
            Traits.WHITE: race_data[0]['white'],
            Traits.BLACK: race_data[0]['black'],
            Traits.LATINO: race_data[0]['latino']
        }

        selected = self.randomizer.get_random_dict_key(options)

        if selected not in Traits.RACES:
            raise Exception("Wrong race.")

        return selected

    def get_social_class(self):
        # The database connection, and the city variable probably need doing somewhere once rather than for
        # every function, every time
        # Start the db connection
        dbmgr = sql_connect.DatabaseManager("testdb.db")

        # Get the data, passing the city
        social_class_data = dbmgr.demo_data("default", "social_class")

        # Close the connection
        dbmgr.__del__()

        options = {
            Traits.LOWERCLASS: social_class_data[0]['lower_class'],
            Traits.MIDDLECLASS: social_class_data[0]['middle_class'],
            Traits.UPPERCLASS: social_class_data[0]['upper_class']
        }

        selected = self.randomizer.get_random_dict_key(options)

        if selected not in Traits.SOCIAL_CLASSES:
            raise Exception("Wrong social class.")

        return selected

    def get_employment_chance(self):

        options = {
            Traits.EMPLOYED: 80,
            Traits.UNEMPLOYED: 20
        }

        selected = self.randomizer.get_random_dict_key(options)

        if selected not in Traits.EMPLOYMENT:
            raise Exception("Wrong employment attribute.")

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
            True: 10,
            False: 90
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
            Traits.SIBLING_SET: 30
        }

        return self.randomizer.get_random_dict_key(options)

    def get_age_of_adoptive_children(self):

        options = {
            "five_or_younger": 46.4,
            "between_six_and_ten": 27.4,
            "between_eleven_and_fifteen": 26.1
        }

        selected = self.randomizer.get_random_dict_key(options)

        if selected == "five_or_younger":
            return [0, 5]
        elif selected == "between_six_and_ten":
            return [6, 10]
        elif selected == "between_eleven_and_fifteen":
            return [11, 15]
        else:
            raise Exception("Wrong age.")

        return selected

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

    def get_drug_addiction_chance(self):

        options = {
            True: 5.3,
            False: 94.7
        }

        return self.randomizer.get_random_dict_key(options)

    def get_alcohol_addiction_chance(self):

        options = {
            True: 12.7,
            False: 87.3
        }

        return self.randomizer.get_random_dict_key(options)

    def get_rehabilitation_chance(self):

        options = {
            True: 10.0,
            False: 90.0
        }

        return self.randomizer.get_random_dict_key(options)

    def get_overdose_chance(self):

        options = {
            True: 10.0,
            False: 90.0
        }

        return self.randomizer.get_random_dict_key(options)

    def get_relapse_chance(self):

        options = {
            True: 10.0,
            False: 90.0
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
