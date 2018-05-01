from utilities.randomizer import Randomizer
from traits import Traits
import sql_connect


class Statistics:
    """Statistics base class."""

    def __init__(self, city_data):
        self.city_data = city_data
        self.randomizer = Randomizer()

    def get_gender(self):
        """Statistical chance for gender."""
        options = {
            Traits.MALE: 50,
            Traits.FEMALE: 50
        }
        selected = self.randomizer.get_random_dict_key(options)
        self.validate_selected(selected, Traits.GENDERS)
        return selected

    def get_gender_identity(self):
        """Statistical chance for gender identity."""
        # Link: https://en.wikipedia.org/wiki/Transgender
        options = {
            Traits.CISGENDER: 99.4,
            Traits.TRANSGENDER: 0.6
        }
        selected = self.randomizer.get_random_dict_key(options)
        self.validate_selected(selected, Traits.GENDER_IDENTITIES)
        return selected

    def get_race(self):
        """Statistical chance for race."""
        # Link: https://www.census.gov/quickfacts/fact/table/US/PST045216
        dbmgr = sql_connect.DatabaseManager("testdb.db")
        race_data = dbmgr.demo_data(self.city_data, "race")
        dbmgr.__del__()

        options = {
            Traits.WHITE: race_data[0]['white'],
            Traits.BLACK: race_data[0]['black'],
            Traits.LATINO: race_data[0]['latino'],
            Traits.ASIAN: race_data[0]['asian']
        }
        selected = self.randomizer.get_random_dict_key(options)
        self.validate_selected(selected, Traits.RACES)
        return selected

    def get_interracial_love_chance(self):
        """Statistical chance for interracial love."""
        # Link: https://en.wikipedia.org/wiki/Interracial_marriage_in_the_United_States
        options = {
            True: 15.1,
            False: 84.9
        }
        return self.randomizer.get_random_dict_key(options)

    def get_autistic_disorder_chance(self, baby):
        """Statistical chance of baby developing autism."""
        # Link: https://www.autismspeaks.org/what-autism/prevalence
        options_for_boy = {
            True: 2.3,
            False: 97.7
        }
        options_for_girl = {
            True: 0.5,
            False: 99.5
        }
        if baby.is_male:
            return self.randomizer.get_random_dict_key(options_for_boy)
        else:
            return self.randomizer.get_random_dict_key(options_for_girl)

    def get_social_class(self):
        """Statistical chance for social class."""
        dbmgr = sql_connect.DatabaseManager("testdb.db")
        social_class_data = dbmgr.demo_data(self.city_data, "social_class")
        dbmgr.__del__()

        options = {
            Traits.UPPER_CLASS: social_class_data[0]['lower_class'],
            Traits.MIDDLE_CLASS: social_class_data[0]['middle_class'],
            Traits.LOWER_CLASS: social_class_data[0]['upper_class']
        }
        selected = self.randomizer.get_random_dict_key(options)
        self.validate_selected(selected, Traits.SOCIAL_CLASSES)
        return selected

    def get_suicide_chance_as_coming_out_consequence(self):
        """Statistical chance of suicide after coming out in conservative family."""
        options = {
            True: 10,
            False: 90
        }
        return self.randomizer.get_random_dict_key(options)

    def get_suicide_chance_as_depression_consequence(self):
        """Statistical chance of suicide for a depressed person."""
        # Link: http://www.allaboutdepression.com/gen_04.html
        options = {
            True: 15,
            False: 85
        }
        return self.randomizer.get_random_dict_key(options)

    def get_thrown_out_chance(self):
        """Statistical chance of being thrown out after coming out in conservative family."""
        options = {
            True: 20,
            False: 80
        }
        return self.randomizer.get_random_dict_key(options)

    def get_employment_chance(self):
        """Statistical chance of employment."""
        # Link: https://tradingeconomics.com/united-states/unemployment-rate
        # To insert into DB: Employed: 95.9. Unemployed: 4.1.
        dbmgr = sql_connect.DatabaseManager("testdb.db")
        employment_data = dbmgr.demo_data(self.city_data, "employment")
        dbmgr.__del__()

        options = {
            Traits.EMPLOYED: employment_data[0]['employed'],
            Traits.UNEMPLOYED: employment_data[0]['unemployed']
        }
        selected = self.randomizer.get_random_dict_key(options)
        self.validate_selected(selected, Traits.EMPLOYMENT)
        return selected

    def get_chance_for_getting_bachelor_degree(self):
        """Statistical chance of getting a bachelor degree."""
        # Link: http://thehill.com/homenews/state-watch/326995-census-more-americans-have-college-degrees-than-ever-before
        options = {
            True: 33.4,
            False: 66.6
        }
        return self.randomizer.get_random_dict_key(options)

    def get_chance_for_getting_master_degree(self):
        """Statistical chance of getting a master's degree."""
        # Link: http://thehill.com/homenews/state-watch/326995-census-more-americans-have-college-degrees-than-ever-before
        options = {
            True: 9.3,
            False: 90.7
        }
        return self.randomizer.get_random_dict_key(options)

    def get_chance_for_getting_doctor_degree(self):
        """Statistical chance of getting a doctor's degree."""
        # Link: http://thehill.com/homenews/state-watch/326995-census-more-americans-have-college-degrees-than-ever-before
        options = {
            True: 2,
            False: 98
        }
        return self.randomizer.get_random_dict_key(options)

    def get_death_cause(self, person):
        """Statistical chance for death cause."""
        dbmgr = sql_connect.DatabaseManager("testdb.db")
        death_cause_data = dbmgr.demo_data(self.city_data, "death_cause")
        dbmgr.__del__()

        # If death date is False = Old Age
        if person.death_date is False:
            return Traits.OLD_AGE
        # If baby or child = Illness
        if person.death_date < Traits.TEEN.start:
            return Traits.ILLNESS

        options_teen = {
            Traits.ILLNESS: death_cause_data[0]['teen_illness'],
            Traits.SUICIDE: death_cause_data[0]['teen_suicide']
        }
        options_young_adult = {
            Traits.ILLNESS: death_cause_data[0]['young_adult_illness'],
            Traits.SUICIDE: death_cause_data[0]['young_adult_suicide'],
            Traits.ACCIDENT: death_cause_data[0]['young_adult_accident']
        }
        options_adult = {
            Traits.ILLNESS: death_cause_data[0]['adult_illness'],
            Traits.SUICIDE: death_cause_data[0]['adult_suicide'],
            Traits.ACCIDENT: death_cause_data[0]['adult_accident']
        }
        options_senior = {
            Traits.ILLNESS: death_cause_data[0]['senior_illness'],
            Traits.SUICIDE: death_cause_data[0]['senior_suicide'],
            Traits.ACCIDENT: death_cause_data[0]['senior_accident']
        }

        if person.death_date in Traits.TEEN.span:
            selected = self.randomizer.get_random_dict_key(options_teen)
        elif person.death_date in Traits.YOUNGADULT.span:
            selected = self.randomizer.get_random_dict_key(options_young_adult)
        elif person.death_date in Traits.ADULT.span:
            selected = self.randomizer.get_random_dict_key(options_adult)
        elif person.death_date in Traits.SENIOR.span:
            selected = self.randomizer.get_random_dict_key(options_senior)
        else:
            raise Exception("Wrong death date.")

        self.validate_selected(selected, Traits.DEATH_CAUSES)
        return selected

    def get_death_date(self):
        """Statistical chance for death date."""
        options_general = {
            "before_old_age": 50,
            "old_age": 50
        }

        options_before_old_age = {
            Traits.BABY: 1,
            Traits.CHILD: 2,
            Traits.TEEN: 3,
            Traits.YOUNGADULT: 4,
            Traits.ADULT: 10,
            Traits.SENIOR: 80
        }

        selected = self.randomizer.get_random_dict_key(options_general)
        if selected == "old_age":
            return False

        random_life_stage = self.randomizer.get_random_dict_key(options_before_old_age)
        death_date = self.randomizer.get_random_item(random_life_stage.span)
        self.validate_selected(death_date, Traits.LIFESPAN)
        return death_date

    def get_fertility(self):
        """Statistical chance of being infertile."""
        # Link: https://www.womenshealth.gov/a-z-topics/infertility
        options = {
            True: 90,
            False: 10
        }
        return self.randomizer.get_random_dict_key(options)

    def get_domestic_partnership_desire(self):
        """Statistical chance for domestic partnership wish."""
        options = {
            True: 90,
            False: 10
        }
        return self.randomizer.get_random_dict_key(options)

    def get_children_desire(self):
        """Statistical chance for children wish."""
        options = {
            True: 70,
            False: 30
        }
        return self.randomizer.get_random_dict_key(options)

    def get_sexual_orientation(self):
        """Statistical chance for sexual orientation."""
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

        # Returns [romantic orientation] + "asexual"
        if orientation == "ace":
            orientation = self.randomizer.get_random_dict_key(
                romantic__aromantic)

            # Returns "aromantic asexual"
            if orientation == "aromantic":
                return Traits.SEXUAL_ORIENTATIONS_DICT[orientation]

            orientation = self.randomizer.get_random_dict_key(romantic_orientations)

            # Returns "heteroromantic asexual"
            if orientation == "het":
                return Traits.SEXUAL_ORIENTATIONS_DICT[orientation]["asexual"]

            # Returns either "homoromantic asexual" or "biromantic asexual"
            if orientation == "homo/bi":
                orientation = self.randomizer.get_random_dict_key(homo_bi)
                return Traits.SEXUAL_ORIENTATIONS_DICT[orientation]["asexual"]

    def get_relationship_orientation(self):
        """Statistical chance for relationship orientation."""
        options = {
            Traits.MONOAMOROUS: 90,
            Traits.POLYAMOROUS: 10
        }
        return self.randomizer.get_random_dict_key(options)

    def get_marriage_desire(self):
        """Statistical chance for marriage wish."""
        # Link: http://www.abc.net.au/news/2017-04-26/more-people-than-ever-are-single-and-thats-a-good-thing/8473398
        options = {
            True: 75,
            False: 25
        }
        return self.randomizer.get_random_dict_key(options)

    def get_liberalism(self):
        """Statistical chance for liberal/conservative ideology."""
        # Link: https://www.theblaze.com/news/2018/01/12/poll-gap-between-liberal-and-conservative-steadily-narrowing-among-american-adults
        options = {
            True: 42.6,
            False: 57.3
        }
        return self.randomizer.get_random_dict_key(options)

    def willing_to_move_outside(self):
        """Statistical of family willing to move outside of neighborhood"""
        options = {
            True: 50,
            False: 50
        }
        return self.randomizer.get_random_dict_key(options)

    def willing_to_move_back(self):
        """Statistical of family willing to move back to inside of neighborhood"""
        options = {
            True: 50,
            False: 50
        }
        return self.randomizer.get_random_dict_key(options)


    def get_desired_num_of_children(self):
        """Statistical chance for desired number of children per couple."""
        dbmgr = sql_connect.DatabaseManager("testdb.db")
        children_data = dbmgr.demo_data(self.city_data, "desired_num_of_children")
        dbmgr.__del__()

        options = {
            Traits.ONE_CHILD: children_data[0]['one_child'],
            Traits.TWO_CHILDREN: children_data[0]['two_children'],
            Traits.THREE_CHILDREN: children_data[0]['three_children'],
            Traits.FOUR_CHILDREN: children_data[0]['four_children']
        }
        selected = self.randomizer.get_random_dict_key(options)
        self.validate_selected(selected, Traits.ALLOWED_NUM_OF_CHILDREN_PER_COUPLE)
        return selected

    def get_pregnancy_num_of_children(self):
        """Statistical chance of having singleton/twins/triplets."""
        # Link: https://en.wikipedia.org/wiki/Multiple_birth
        dbmgr = sql_connect.DatabaseManager("testdb.db")
        pregnancy_data = dbmgr.demo_data(self.city_data, "pregnancy")
        dbmgr.__del__()

        options = {
            Traits.SINGLETON: pregnancy_data[0]['singlton'],
            Traits.TWINS: pregnancy_data[0]['twins'],
            Traits.TRIPLETS: pregnancy_data[0]['triplets']
        }
        selected = self.randomizer.get_random_dict_key(options)
        self.validate_selected(selected, Traits.ALLOWED_NUM_OF_CHILDREN_PER_PREGNANCY)
        return selected

    def get_adoption_num_of_children(self):
        """Statistical chance of adopting one child or a sibling set."""
        options = {
            Traits.ONE_CHILD: 70,
            Traits.SIBLING_SET: 30
        }
        selected = self.randomizer.get_random_dict_key(options)
        self.validate_selected(selected, Traits.ALLOWED_NUM_OF_ADOPTIONS_PER_COUPLE)
        return self.randomizer.get_random_dict_key(options)

    def get_age_of_adoptive_children(self):
        """Statistical chance for age of child in adoption."""
        options = {
            5: 46.4,
            10: 27.4,
            Traits.MAX_AGE_FOR_ADOPTION: 26.1
        }
        selected = self.randomizer.get_random_dict_key(options)
        if selected == 5:
            return list(range(0, 6))
        elif selected == 10:
            return list(range(6, 11))
        elif selected == Traits.MAX_AGE_FOR_ADOPTION:
            return list(range(11, Traits.MAX_AGE_FOR_ADOPTION + 1))
        else:
            raise Exception("Wrong age.")

    def get_breakup_chance(self, couple):
        """Statistical chance of breaking up."""
        # Link: http://stories.avvo.com/relationships/divorce/numbers-breakdown-divorce-generation.html
        # Link: https://psychcentral.com/blog/is-my-marriage-doomed-if-my-parents-got-divorced-when-i-was-a-kid/
        # Insert to DB: True: 52.7. False: 48.3. If divorced parents: True: 79. False: 21.
        dbmgr = sql_connect.DatabaseManager("testdb.db")
        breakup_data = dbmgr.demo_data(self.city_data, "breakup")
        dbmgr.__del__()

        options_for_married_parents = {
            True: breakup_data[0]['breakup_true'],
            False: breakup_data[0]['breakup_false']
        }
        options_for_divorced_parents = {
            True: 79,
            False: 21
        }
        if all(p.has_divorced_parents for p in couple.persons):
            return self.randomizer.get_random_dict_key(options_for_divorced_parents)
        return self.randomizer.get_random_dict_key(options_for_married_parents)

    def get_couple_reconciliation_chance(self):
        """Statistical chance for a separated couple to get back together."""
        # Link: https://www.quora.com/How-common-is-it-for-divorced-couples-to-get-back-together
        options = {
            True: 6,
            False: 94
        }
        return self.randomizer.get_random_dict_key(options)

    def get_intergenerational_chance(self):
        """Statistical chance for intergenerational relationship."""
        options = {
            True: 10,
            False: 90
        }
        return self.randomizer.get_random_dict_key(options)

    def get_family_love_chance(self):
        """Statistical chance for consanguinamorous relationship."""
        options = {
            True: 10,
            False: 90
        }
        return self.randomizer.get_random_dict_key(options)

    def get_triad_chance(self):
        """Statistical chance for triads / throuples."""
        options = {
            True: 30,
            False: 70
        }
        return self.randomizer.get_random_dict_key(options)

    def get_drug_addiction_chance(self):
        """Statistical chance for drug addiction."""
        dbmgr = sql_connect.DatabaseManager("testdb.db")
        drug_addiction_data = dbmgr.demo_data(self.city_data, "drug_addiction")
        dbmgr.__del__()

        options = {
            True: drug_addiction_data[0]['addict_true'],
            False: drug_addiction_data[0]['addict_false']
        }
        return self.randomizer.get_random_dict_key(options)

    def get_alcohol_addiction_chance(self):
        """Statistical chance for alcohol addiction."""
        dbmgr = sql_connect.DatabaseManager("testdb.db")
        alcohol_addiction_data = dbmgr.demo_data(self.city_data, "alcohol_addiction")
        dbmgr.__del__()

        options = {
            True: alcohol_addiction_data[0]['addict_true'],
            False: alcohol_addiction_data[0]['addict_false']
        }
        return self.randomizer.get_random_dict_key(options)

    def get_rehabilitation_chance(self):
        """Statistical chance of going through rehabilitation for addiction."""
        dbmgr = sql_connect.DatabaseManager("testdb.db")
        rehabilitation_data = dbmgr.demo_data(self.city_data, "rehabilitation")
        dbmgr.__del__()

        options = {
            True: rehabilitation_data[0]['rehabilitation_true'],
            False: rehabilitation_data[0]['rehabilitation_false']
        }
        return self.randomizer.get_random_dict_key(options)

    def get_overdose_chance(self):
        """Statistical chance of overdosing."""
        dbmgr = sql_connect.DatabaseManager("testdb.db")
        overdose_data = dbmgr.demo_data(self.city_data, "overdose")
        dbmgr.__del__()

        options = {
            True: overdose_data[0]['overdose_true'],
            False: overdose_data[0]['overdose_false']
        }
        return self.randomizer.get_random_dict_key(options)

    def get_relapse_chance(self):
        """Statistical chance of relapsing"""
        dbmgr = sql_connect.DatabaseManager("testdb.db")
        relapse_data = dbmgr.demo_data(self.city_data, "relapse")
        dbmgr.__del__()

        options = {
            True: relapse_data[0]['relapse_true'],
            False: relapse_data[0]['relapse_false']
        }
        return self.randomizer.get_random_dict_key(options)

    def get_depression_chance(self):
        """Statistical chance of suffering from depression."""
        options = {
            True: 33.3,
            False: 66.7
        }
        return self.randomizer.get_random_dict_key(options)

    def get_therapy_chance(self):
        """Statistical chance of going to therapy."""
        options = {
            True: 33.3,
            False: 66.7
        }
        return self.randomizer.get_random_dict_key(options)

    def get_recovery_chance(self):
        """Statistical chance of recovering with therapy."""
        options = {
            True: 50,
            False: 50
        }
        return self.randomizer.get_random_dict_key(options)

    # EARLY / MID / LATE WITHIN RANGE

    def get_oldest_breakup_date(self, couple):
        """Returns statistical breakup date for oldest person in couple."""
        early = 50
        mid = 30
        late = 20
        return self.get_chance_for_early_mid_late(couple.oldest.span_left_till_old_age, early, mid, late)

    def get_oldest_pregnancy_date(self, couple):
        """Returns statistical pregnancy date for oldest person in couple."""
        early = 70
        mid = 20
        late = 10
        return self.get_chance_for_early_mid_late(couple.having_children_timespan, early, mid, late)

    def get_chance_for_early_mid_late(self, lst, early_num, mid_num, late_num):
        """Helper method for determining statistical chances within early-mid-late range."""
        if len(lst) == 0:
            raise Exception("List is empty.")
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

    @classmethod
    def validate_selected(cls, selected, lst):
        if selected not in lst:
            raise Exception("Statistically selected value is not valid.")
