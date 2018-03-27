from traits import Traits
from utilities.randomizer import Randomizer


class PersonDeveloper:

    def __init__(self, setup, life_stages, statistics):
        self.setup = setup
        self.stages = life_stages
        self.statistics = statistics
        self.randomizer = Randomizer()

    def set_new_stage_traits(self, person):
        """Link each new stage to their methods for setting new traits."""
        if person.stage == self.stages.BABY or person.stage == self.stages.CHILD:
            pass
        elif person.stage == self.stages.TEEN:
            person = self.set_teen_traits(person)
        elif person.stage == self.stages.ADULT:
            person = self.set_adult_traits(person)
        elif person.stage == self.stages.YOUNGADULT:
            person = self.set_youngadult_traits(person)
        elif person.stage == self.stages.SENIOR:
            person = self.set_senior_traits(person)
        else:
            raise Exception("Person's stage is wrong.")
        return person

    def set_teen_traits(self, teen):
        "Teen traits."
        teen.gender_identity = self.statistics.get_gender_identity()  # Gender identity must be set first
        teen.sexual_orientation = self.statistics.get_sexual_orientation()
        teen.target_gender = [gender for gender in self.get_target_gender(teen)]
        # Set date to come out if LGBTA
        if teen.is_lgbta:
            teen.come_out_date = self.randomizer.get_random_item(teen.span_left_till_next_stage)
        return teen

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

    def set_youngadult_traits(self, person):
        """Young adult traits."""
        person.occupation = self.randomizer.get_random_item(
            self.setup.PROFESSIONS)
        person.employment = self.statistics.get_employment_chance()

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
        return person

    @classmethod
    def set_adult_traits(cls, person):
        """Adult traits."""
        person.can_have_bio_children = False
        return person

    @classmethod
    def set_senior_traits(cls, person):
        """Senior traits."""
        person.employment = Traits.RETIRED
        return person

    # LOVE

    def set_love_traits(self, person):
        """Returns person with statistical / random traits for wish for romance / marriage / children.
        Chance for family or intergenerational love. Sets date to fall in love if applicable."""
        if len(person.span_left_till_old_age) <= 1:
            return person

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

            # Assign date to fall in love. Ex: within 10 years.
            # If person will be dead before then, just loop through their remaining years.
            if len(person.span_left_till_old_age) < 10:
                person.in_love_date = self.randomizer.get_random_item(
                    person.span_left_till_old_age)
            else:
                person.in_love_date = self.randomizer.get_random_item(
                    range(person.age, person.age + 11))

    def set_new_love_date_for_polys(self, couple):
        """After couple creation, set new future love date for each poly person from couple if any."""
        for person in couple.persons:
            if person.is_romanceable:
                self.set_new_love_date(person)
        return couple

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
        self.rehabilitation_vs_overdose_chance(person)
        # Set dates for rehabilitation / overdose.
        if person.will_overdose:
            range_for_overdose = list(range(1, 20))
            person.death_date = person.age + self.randomizer.get_random_item(range_for_overdose)
            self.set_type_of_addiction_for_death_cause(person)
        elif person.will_recover:
            range_for_rehabilitation = list(range(1, 20))
            person.rehabilitation_date = person.age + self.randomizer.get_random_item(range_for_rehabilitation)
        return person

    def rehabilitation_vs_overdose_chance(self, person):
        """Rehabilitation vs overdose chance."""
        person.will_recover = self.statistics.get_alcohol_addiction_chance()
        if not person.will_recover:
            person.will_overdose = self.statistics.get_alcohol_addiction_chance()

    @classmethod
    def set_type_of_addiction_for_death_cause(cls, person):
        """Death by drug overdose or alcohol overdose."""
        if person.is_drug_addict:
            person.death_cause = Traits.DRUG_OVERDOSE
        else:
            person.death_cause = Traits.ALCOHOL_OVERDOSE

    def relapse_chance(self, person):
        """Chance of relapsing and relapse date if so."""
        person.will_relapse = self.statistics.get_relapse_chance()
        # Set relapse date if applicable
        if person.will_relapse:
            range_for_relapse = list(range(1, 10))
            person.relapse_date = person.age + self.randomizer.get_random_item(range_for_relapse)
        return person
