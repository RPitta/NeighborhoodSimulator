from traits import Traits
from utilities.randomizer import Randomizer
from job import Job


class PersonDeveloper:
    """Base class for person developer."""

    def __init__(self, setup, statistics):
        self.setup = setup
        self.statistics = statistics
        self.randomizer = Randomizer()

    def set_new_stage_traits(self, person):
        """Link each new stage to their methods for setting new traits."""
        if person.stage == Traits.BABY:
            pass
        elif person.stage == Traits.CHILD:
            self.set_child_traits(person)
        elif person.stage == Traits.TEEN:
            self.set_teen_traits(person)
        elif person.stage == Traits.ADULT:
            self.set_adult_traits(person)
        elif person.stage == Traits.YOUNGADULT:
            self.set_youngadult_traits(person)
        elif person.stage == Traits.SENIOR:
            self.set_senior_traits(person)
        else:
            raise Exception("Person's stage is wrong.")

    @classmethod
    def set_child_traits(cls, child):
        child.school_start_date = child.education.SCHOOL_START_DATE

    def set_teen_traits(self, teen):
        """Teen traits."""
        teen.gender_identity = self.statistics.get_gender_identity()  # Gender identity must be set first
        teen.sexual_orientation = self.statistics.get_sexual_orientation()
        teen.target_gender = [gender for gender in self.get_target_gender(teen)]
        # Set date to come out if LGBTA
        if teen.is_lgbta:
            teen.come_out_date = self.randomizer.get_random_item(teen.span_left_till_next_stage)

    @classmethod
    def get_target_gender(cls, teen):
        """Returns target gender(s) based on sexual orientation logic."""
        if teen.is_male or (teen.is_female and teen.is_trans):
            same = Traits.MALE
            opposite = Traits.FEMALE
        elif teen.is_female or (teen.is_male and teen.is_trans):
            same = Traits.FEMALE
            opposite = Traits.MALE

        if teen.sexual_orientation in [Traits.HETEROSEXUAL, Traits.HETEROROMANTIC_ASEXUAL]:
            yield opposite
        if teen.sexual_orientation in [Traits.HOMOSEXUAL, Traits.HOMOROMANTIC_ASEXUAL]:
            yield same
        if teen.sexual_orientation in [Traits.BISEXUAL, Traits.BIROMANTIC_ASEXUAL]:
            yield same
            yield opposite
        if teen.sexual_orientation == Traits.AROMANTIC_ASEXUAL:
            yield None

    def set_coming_out_consequences(self, teen):
        """Chance of teen moving out / being thrown out / committing suicide if conservative family."""
        if not teen.has_conservative_parents:
            return
        # Suicide chance
        if not self.suicide_consequence(teen):
            # Thrown out chance
            if not self.thrown_out_consequence(teen):
                # Otherwise, will move out
                teen.will_move_out = True
                teen.move_out_date = Traits.YOUNGADULT.start

    def suicide_consequence(self, teen):
        """Determine chance of suicide as coming out in conservative family consequence."""
        if not self.statistics.get_suicide_chance_as_coming_out_consequence():
            return False
        teen.death_date = teen.age + 1 if len(teen.span_left_till_next_stage) < 1 else self.randomizer.get_random_item(
            teen.span_left_till_next_stage)
        teen.death_cause = Traits.SUICIDE
        return True

    def thrown_out_consequence(self, teen):
        """Determine chance of being thrown out of home as coming out consequence."""
        if not self.statistics.get_thrown_out_chance():
            return False
        teen.will_be_thrown_out = True
        teen.thrown_out_date = Traits.YOUNGADULT.start
        return True

    def set_youngadult_traits(self, person):
        """Young adult traits."""

        # Education
        person.will_do_bachelor = self.statistics.get_chance_for_getting_bachelor_degree()
        person.will_do_master = self.statistics.get_chance_for_getting_master_degree()
        person.will_do_doctor = self.statistics.get_chance_for_getting_master_degree()

        # Set relationship orientation (mono/poly)
        person.relationship_orientation = self.statistics.get_relationship_orientation()

        # Set (initial) liberalism
        if person.is_lgbta or person.is_poly:
            person.is_liberal = True
        else:
            person.is_liberal = self.statistics.get_liberalism()

        # Cannot have biological children if LGTA
        if person.is_lgbta and not person.is_bi:
            person.can_have_bio_children = False

        # Set relationship-oriented traits
        self.set_love_traits(person)
        # Set chance of drug/alcohol addiction
        self.set_addiction_traits(person)

    @classmethod
    def set_adult_traits(cls, person):
        """Adult traits."""
        person.can_have_bio_children = False

    def set_senior_traits(self, person):
        """Senior traits."""
        person.job.employment = Traits.RETIRED
        if person.is_neighbor:
            self.display_retired_message(person)

    @classmethod
    def display_retired_message(cls, person):
        print("\n{} has retired.".format(person))

    # LOVE

    def set_love_traits(self, person):
        """Returns person with statistical / random traits for wish for romance / marriage / children.
        Chance for family or intergenerational love. Sets date to fall in love if applicable."""
        if len(person.span_left_till_old_age) <= 1:
            return

        if person.is_poly:
            person.in_love_as_throuple = self.statistics.get_triad_chance()

        if person.is_liberal:
            person.wants_domestic_partnership = self.statistics.get_domestic_partnership_desire()
            person.wants_children = self.statistics.get_children_desire()
        else:
            self.set_conservative_traits(person)

        if person.wants_domestic_partnership:
            person.wants_marriage = self.statistics.get_marriage_desire()
            self.set_new_love_date(person)
        else:
            self.set_aromantic_traits(person)

    def set_new_love_date(self, person):
        """Sets in_love_date within person's age and X.
        Chance of intergenerational / family love."""
        if self.is_family_love_a_possibility(person):
            person.in_love_with_family = self.statistics.get_family_love_chance()

        if person.in_love_with_family:
            self.set_family_love_traits(person)
        else:
            person.in_love_with_intergenerational = self.statistics.get_intergenerational_chance()
            if person.in_love_with_intergenerational:
                person.is_liberal = True
            # If mixed race, race compatibility not applicable
            if person.is_mixed_race:
                person.in_love_with_another_race = None
            else:
                person.in_love_with_another_race = self.statistics.get_interracial_love_chance()
                if person.in_love_with_another_race:
                    person.is_liberal = True

            # Assign date to fall in love. Ex: within 10 years.
            # If person will be dead before then, just loop through their remaining years.
            if len(person.span_left_till_old_age) <= 1:
                return
            if len(person.span_left_till_old_age) < 10:
                person.in_love_date = self.randomizer.get_random_item(person.span_left_till_old_age)
            else:
                person.in_love_date = self.randomizer.get_random_item(
                    range(person.age, person.age + 11))

    def set_new_love_date_for_polys(self, couple):
        """After couple creation, set new future love date for each poly person from couple if any."""
        for person in couple.persons:
            if person.is_romanceable:
                self.set_new_love_date(person)

    @classmethod
    def set_conservative_traits(cls, person):
        """Wants marriage and children if conservative."""
        person.wants_domestic_partnership = True
        person.wants_marriage = True
        person.wants_children = True

    @classmethod
    def set_aromantic_traits(cls, person):
        """Is liberal and does not want committed relationships if aromantic."""
        person.is_liberal = True
        person.in_love_date = False
        person.in_love_with_family = False
        person.in_love_with_intergenerational = None  # Age not applicable
        person.wants_marriage = False

    @classmethod
    def is_family_love_a_possibility(cls, person):
        """Determine if person could fall in love with a family member."""
        return len(person.living_bio_family) > 0 and any(
            f.is_of_age and f.gender in person.target_gender for f in person.living_bio_family)

    @classmethod
    def set_family_love_traits(cls, person):
        """Traits for person in love with a family member."""
        person.is_liberal = True
        person.in_love_date = person.age
        person.can_have_bio_children = False
        person.in_love_with_intergenerational = None  # Age not applicable
        person.in_love_with_another_race = None  # Race not applicable

    # ADDICTION

    def set_addiction_traits(self, person):
        """Chance for alcohol and/or drug addiction. Addiction date."""
        self.addiction_chance(person)
        if person.will_become_drug_addict or person.will_become_alcohol_addict:
            self.set_date_for_addiction(person)

    def addiction_chance(self, person):
        """Drug addiction or alcohol addiction."""
        person.will_become_drug_addict = self.statistics.get_drug_addiction_chance()
        if not person.will_become_drug_addict:
            person.will_become_alcohol_addict = self.statistics.get_alcohol_addiction_chance()

    def set_date_for_addiction(self, person):
        """Set date when person becomes addicted."""
        range_to_become_addict = person.span_left_till_old_age
        early = 70
        mid = 20
        late = 10
        person.addiction_date = self.statistics.get_chance_for_early_mid_late(range_to_become_addict, early, mid, late)

    def set_addiction_consequences(self, person):
        """Chance for rehabilitation / overdose / left untreated if addict."""
        will_recover = self.statistics.get_rehabilitation_chance()
        if will_recover:
            range_for_rehabilitation = list(range(1, 20))
            person.rehabilitation_date = person.age + self.randomizer.get_random_item(range_for_rehabilitation)
        else:
            will_overdose = self.statistics.get_alcohol_addiction_chance()
            # Set dates for rehabilitation / overdose.
            if will_overdose:
                range_for_overdose = list(range(1, 20))
                person.death_date = person.age + self.randomizer.get_random_item(range_for_overdose)
                self.set_type_of_addiction_for_death_cause(person)

    @classmethod
    def set_type_of_addiction_for_death_cause(cls, person):
        """Death by drug overdose or alcohol overdose."""
        if person.is_drug_addict:
            person.death_cause = Traits.DRUG_OVERDOSE
        else:
            person.death_cause = Traits.ALCOHOL_OVERDOSE

    def relapse_chance(self, person):
        """Chance of relapsing and relapse date if so."""
        will_relapse = self.statistics.get_relapse_chance()
        # Set relapse date if applicable
        if will_relapse:
            range_for_relapse = range(1, 10)
            person.relapse_date = person.age + self.randomizer.get_random_item(range_for_relapse)

    def set_depression_for_housemates(self, person, household):
        """Adds statistical chance of depression to each housemate of dead person."""
        housemates = [p for p in household.members if p != person]
        for p in housemates:
            if p.age >= Traits.TEEN.start:
                depressed = self.statistics.get_depression_chance()
                if depressed:
                    p.conditions.append(Traits.DEPRESSION)
                    p.depression_date = p.age + 1  # Depression will be diagnosed next year
                    self.set_depression_consequences(p)

    def set_depression_consequences(self, person):
        """Depressed person will go to therapy, commit suicide, or depression will be left untreated."""
        will_go_to_therapy = self.statistics.get_therapy_chance()
        if will_go_to_therapy:
            person.therapy_date = person.depression_date + 1  # Therapy will start one year after depression diagnosis
            will_recover = self.statistics.get_recovery_chance()
            if will_recover:
                recovery_range = range(1, 5)
                person.depression_recovery_date = person.therapy_date + self.randomizer.get_random_item(recovery_range)
        else:
            suicide = self.statistics.get_suicide_chance_as_depression_consequence()
            if suicide:
                suicidal_range = range(1, 5)
                person.death_date = person.depression_date + self.randomizer.get_random_item(suicidal_range)
                person.death_cause = Traits.SUICIDE
