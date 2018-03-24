from traits import Traits
from utilities.randomizer import Randomizer


class PersonDeveloper:

    def __init__(self, setup, life_stages, statistics):
        self.setup = setup
        self.stages = life_stages
        self.statistics = statistics
        self.randomizer = Randomizer()

    def set_new_stage_traits(self, person):
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

        # Set gender identity - must be set first
        teen.gender_identity = self.statistics.get_gender_identity()
        # Set sexual orientation
        teen.sexual_orientation = self.statistics.get_sexual_orientation()
        # Set target gender(s) based on sexual orientation, gender and gender identity
        teen.target_gender = [
            gender for gender in self.get_target_gender(teen)]
        # Set date to come out if LGBTA
        if teen.is_lgbta:
            teen.come_out_date = self.randomizer.get_random_item(
                (teen.span_left_till_next_stage))

        return teen

    def get_target_gender(self, teen):
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

        # Logic
        # If person is lgbt/asexual/poly -> Liberal
        # If person is gay/asexual/trans -> Cannot have bio children.

        # Set profession
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

        if person.is_lgbta and not person.is_bi:
            person.can_have_bio_children = False

        # Set relationship-oriented traits
        self.set_love_traits(person)

        # Set chance of drug/alcohol addiction
        self.set_addiction_traits(person)

        return person

    def set_adult_traits(self, person):

        # Set ability to have children to False
        person.can_have_bio_children = False

        return person

    def set_senior_traits(self, person):

        # Set employment to retired
        person.employment = Traits.RETIRED

        # Set ability to have children to False
        person.can_have_bio_children = False

        return person

    def set_love_traits(self, person):
        """Returns person with statistical / random traits for wish for romance / marriage / children.
        Chance for family or intergenerational love. Sets date to fall in love if applicable."""
        # Logic:
        # If person is poly and not straight -> Chance of triad vs V.
        # If triad -> Cannot get married, liberal.
        # If person is conservative -> Wants partnership, marriage and children.
        # If person has adult family -> Chance of family love.
        # If in love with family member -> Cannot have bio children, cannot get married, intergenerational not applicable, liberal.
        # If person does not want partnership -> Does not want marriage either, intergenerational not applicable, liberal.
        if len(person.span_left_till_old_age) <= 1:
            return

        if person.is_poly:
            person.in_love_as_throuple = self.statistics.get_triad_chance()

        if person.is_liberal:
            person.wants_domestic_partnership = self.statistics.get_domestic_partnership_desire()
            person.wants_children = self.statistics.get_children_desire()
        else:
            self.set_conservative_traits(person)

        if person.is_romanceable:
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

        return person

    def set_new_love_date_for_polys(self, couple):
        """After couple creation, set new future love date for each poly person from couple if any."""
        for person in couple.persons:
            if person.is_romanceable:
                self.set_new_love_date(person)
        return couple

    def set_conservative_traits(self, person):
        person.wants_domestic_partnership = True
        person.wants_marriage = True
        person.wants_children = True

    def set_aromantic_traits(self, person):
        person.is_liberal = True
        person.in_love_date = False
        person.in_love_with_family = False
        person.in_love_with_intergenerational = None  # Age not applicable
        person.wants_marriage = False

    def is_family_love_a_possibility(self, person):
        return len(person.living_bio_family) > 0 and any(f.is_of_age for f in person.living_bio_family) and any(
            f.gender in person.target_gender for f in person.living_bio_family)

    def set_family_love_traits(self, person):
        person.is_liberal = True
        person.in_love_date = person.age
        person.can_have_bio_children = False
        person.in_love_with_intergenerational = None  # Age not applicable

    def set_addiction_traits(self, person):
        """Chance for alcohol and/or drug addiction."""
        self.addiction_chance(person)
        if person.will_become_drug_addict or person.will_become_alcohol_addict:
            self.set_date_for_addiction(person)

    def addiction_chance(self, person):
        """Drug addiction or alcohol addiction."""
        person.will_become_drug_addict = self.statistics.get_drug_addiction_chance()
        if not person.will_become_drug_addict:
            person.will_become_alcohol_addict = self.statistics.get_alcohol_addiction_chance()

    def set_date_for_addiction(self, person):
        range_to_become_addict = person.span_left_till_old_age
        early = 70
        mid = 20
        late = 10
        person.addiction_date = self.statistics.get_chance_for_early_mid_late(range_to_become_addict, early, mid, late)

    def set_addiction_consequences(self, person):
        """Chance for rehabilitation / overdose / left untreated if addict."""
        self.rehabilitation_vs_overdose_chance(person)

        range_for_overdose = list(range(1, 20))
        range_for_rehabilitation = list(range(1, 20))
        range_for_relapse = list(range(1, 10))  # X years after rehabilitation

        # Set dates for rehabilitation / overdose.
        if person.will_overdose:
            person.death_date = person.age + self.randomizer.get_random_item(range_for_overdose)
            self.set_type_of_addiction_for_death_cause(person)
        elif person.will_recover:
            person.rehabilitation_date = person.age + self.randomizer.get_random_item(range_for_rehabilitation)

            # Relapse chance
            person.will_relapse = self.statistics.get_relapse_chance()
            if person.will_relapse:
                person.relapse_date = person.rehabilitation_date + self.randomizer.get_random_item(range_for_relapse)

    def rehabilitation_vs_overdose_chance(self, person):
        """Rehabilitation vs Overdose chances"""
        person.will_recover = self.statistics.get_alcohol_addiction_chance()
        if not person.will_recover:
            person.will_overdose = self.statistics.get_alcohol_addiction_chance()

    def set_type_of_addiction_for_death_cause(self, person):
        """Death by drug overdose or alcohol overdose."""
        if person.is_drug_addict:
            person.death_cause = Traits.DRUG_OVERDOSE
        else:
            person.death_cause = Traits.ALCOHOL_OVERDOSE
