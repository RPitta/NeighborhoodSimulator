from utilities.randomizer import Randomizer
from traits import Traits


class CoupleDeveloper:
    """Couple developer base class."""

    def __init__(self, statistics):
        self.statistics = statistics
        self.randomizer = Randomizer()

    def set_new_couples_goals(self, couple):
        """Set new couple's goals."""
        if len(couple.oldest.span_left_till_old_age) <= 1:  # No time left for marriage/breakup if old age.
            return couple

        # If couple wants to get married, set random (within the next X-Y years) marriage date.
        if couple.will_get_married:
            self.set_marriage_date(couple)

        # Statistical break up chance.
        couple.will_breakup = self.statistics.get_breakup_chance()

        # If couple will break up, set break-up date to each person
        if couple.will_breakup:
            self.set_breakup_date(couple)

        # If couple will have children, set number of desired children and first child pregnancy/adoption date
        if couple.will_have_children:
            # Statistical chance of desired number of children
            couple.desired_num_of_children = self.statistics.get_desired_num_of_children()
            couple.desired_children_left = couple.desired_num_of_children
            couple = self.set_new_pregnancy_or_adoption_process_date(couple)

        self.unique_dates_validation(couple)
        return couple

    def set_marriage_date(self, couple):
        marriable_range = range(1, 8)
        date = couple.oldest.age + \
               self.randomizer.get_random_item(marriable_range)
        if date not in couple.oldest.span_left_till_old_age:
            date = self.randomizer.get_random_item(
                couple.oldest.span_left_till_old_age)
        couple.marriage_date = date

    def set_breakup_date(self, couple):
        """Sets couple's break up date."""
        date = couple.marriage_date
        while date <= couple.marriage_date or \
                date in range(couple.pregnancy_date, couple.birth_date + 2) or \
                date in range(couple.adoption_process_date, couple.adoption_date + 2):
            date = self.statistics.get_oldest_breakup_date(couple)
        couple.breakup_date = date

    def set_new_pregnancy_or_adoption_process_date(self, couple):
        """Sets pregnancy or adoption date and birth date."""
        if abs(couple.oldest.age - couple.breakup_date) <= 4 or abs(couple.marriage_date - couple.breakup_date) <= 4:
            return couple
        date = couple.breakup_date
        while date in range(couple.breakup_date - 3, couple.breakup_date + 3):
            date = self.statistics.get_oldest_pregnancy_date(couple)

        if couple.will_get_pregnant:
            couple.pregnancy_date = date
            couple.birth_date = date + 1 # baby is born next year (although realistically it'd be about 8 months later)
        elif couple.will_adopt:
            couple.adoption_process_date = date
            couple.adoption_date = date + 2 # adoption will take place about 2 years later
        else:
            raise Exception(
                "Couple is set on having a child but won't get pregnant nor adopt.")

        self.unique_dates_validation(couple)
        return couple

    @classmethod
    def unique_dates_validation(cls, couple):
        if couple.will_get_married and couple.marriage_date > 0:
            if couple.marriage_date not in couple.oldest.span_left_till_old_age:
                raise Exception(
                    "Marriage date cannot be set outside oldest person's lifetime.")
        if couple.will_breakup:
            if couple.breakup_date not in couple.oldest.span_left_till_old_age:
                raise Exception(
                    "Breakup date cannot be set outside oldest person's lifetime.")
        if couple.pregnancy_date > 0:
            if couple.pregnancy_date not in couple.oldest.span_left_till_old_age or \
                    couple.birth_date not in couple.oldest.span_left_till_old_age:
                raise Exception(
                    "Pregnancy/birth date cannot be set outside oldest person's lifetime.")
            if couple.oldest.is_young_adult is False:
                raise Exception(
                    "Pregnancy/birth date cannot be set if couple is older than young adult.")
        if couple.adoption_process_date > 0:
            if couple.adoption_process_date not in couple.oldest.span_left_till_old_age or \
                    couple.adoption_date not in couple.oldest.span_left_till_old_age:
                raise Exception(
                    "Adoption process/adoption date cannot be set outside oldest person's lifetime.")
        if couple.will_breakup and couple.will_get_married:
            if couple.breakup_date == couple.marriage_date:
                raise Exception(
                    "Breakup date and marriage date cannot be set at the same time.")
        if couple.breakup_date > 0 and couple.pregnancy_date > 0:
            if couple.breakup_date == couple.pregnancy_date or couple.breakup_date == couple.birth_date:
                raise Exception(
                    "Breakup date and pregnancy/birth date cannot be set at the same time.")
        if couple.breakup_date > 0 and couple.adoption_process_date > 0:
            if couple.breakup_date == couple.adoption_process_date or couple.breakup_date == couple.adoption_date:
                raise Exception(
                    "Breakup date and adoption process/adoption date cannot be set at the same time.")
