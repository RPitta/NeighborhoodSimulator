from traits import Traits
from utilities.randomizer import Randomizer
from utilities.compatibility import Compatibility


class PersonDeveloper:

    def __init__(self, names, professions, life_stages, statistics):
        self.names = names
        self.professions = professions
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
            self.professions.PROFESSIONS)
        person.employment = self.statistics.get_employment_chance(person)

        # Set relationship orientation (mono/poly)
        person.relationship_orientation = self.statistics.get_relationship_orientation()

        # Set (initial) liberalism
        if person.is_lgbta or person.is_poly:
            person.is_liberal = True
        else:
            person.is_liberal = self.statistics.get_liberalism(person)

        if person.is_lgbta and not person.is_bi:
            person.can_have_bio_children = False

        # Set relationship-oriented traits
        person = self.set_love_traits(person)

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
            return person

        if person.is_poly:
            person.in_love_as_throuple = self.statistics.get_triad_chance(
                person)

        if person.is_liberal:
            person.wants_domestic_partnership = self.statistics.get_domestic_partnership_desire(
                person)
            person.wants_children = self.statistics.get_children_desire(person)
        else:
            self.set_conservative_traits(person)

        if person.is_romanceable:
            person.wants_marriage = self.statistics.get_marriage_desire(person)
            self.set_new_love_date(person)
        else:
            self.set_aromantic_traits(person)

        return person

    def set_new_love_date(self, person):
        """Sets in_love_date within person's age and X.
        Chance of intergenerational / family love."""

        if self.is_family_love_a_possibility(person):
            person.in_love_with_family = self.statistics.get_family_love_chance(
                person)

        if person.in_love_with_family:
            self.set_family_love_traits(person)
        else:
            person.in_love_with_intergenerational = self.statistics.get_intergenerational_chance(
                person)
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
                person = self.set_new_love_date(person)

        return couple

    def reset_love_date_for_next_year(self, person):
        """If no match, increase love date by 1 if old age not reached yet."""
        if len(person.span_left_till_old_age) <= 1:
            return person

        person.in_love_date = person.age + 1
        return person

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
        # Has family
        if person.living_bio_family is None or len(person.living_bio_family) == 0:
            return False
        # Adult age only
        if all([person.living_bio_family[0].is_of_age is False for p in person.living_bio_family]):
            return False
        # Is target gender
        if all([person.living_bio_family[0].gender not in person.target_gender for family_member in person.living_bio_family]):
            return False
        return True

    def set_family_love_traits(self, person):
        person.is_liberal = True
        person.in_love_date = person.age
        person.can_have_bio_children = False
        person.in_love_with_intergenerational = None  # Age not applicable
