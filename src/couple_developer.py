from utilities.randomizer import Randomizer
from traits import Traits


class CoupleDeveloper:

    def __init__(self, statistics):
        self.statistics = statistics
        self.randomizer = Randomizer()

    def set_new_couple_traits(self, couple):

        # If oldest person is at the end of senior stage, no time left for marriage/breakup.
        if len(couple.oldest.span_left_till_old_age) <= 1:
            return couple

        # If couple wants to get married, set random (within the next X-Y years) marriage date.
        if couple.will_get_married:
            self.set_marriage_date(couple)

        # Statistical break up chance.
        couple.will_breakup = self.statistics.get_breakup_chance(couple)

        # If couple will break up, set break-up date to each person
        if couple.will_breakup:
            self.set_breakup_date(couple)

        # If couple will have children, set number of desired children and first child pregnancy/adoption date
        if couple.will_have_children:
            # Statistical chance of desired number of children
            couple.desired_num_of_children = self.statistics.get_desired_num_of_children(
                couple)
            couple.desired_children_left = couple.desired_num_of_children

            # Validation
            if couple.desired_num_of_children not in Traits.ALLOWED_NUM_OF_CHILDREN_PER_COUPLE:
                raise Exception(
                    "Couple's desired number of children is not permitted.")

            couple = self.set_new_pregnancy_or_adoption_process_date(couple)

        # Validation
        self.unique_dates_validation(couple)
        return couple

    def set_marriage_date(self, couple):
        marriable_range = range(1, 5)
        date = couple.oldest.age + \
            self.randomizer.get_random_item(marriable_range)
        if date not in couple.oldest.span_left_till_old_age:
            date = self.randomizer.get_random_item(
                    couple.oldest.span_left_till_old_age)
        couple.marriage_date = date

    def set_breakup_date(self, couple):
        """Sets couple's break up date. Cannot be the same as marriage's date."""
        date = couple.marriage_date
        while date == couple.marriage_date or date in [couple.pregnancy_date, couple.birth_date] or date in [couple.adoption_process_date, couple.adoption_date]:
            date = self.statistics.get_oldest_breakup_date(couple)

        couple.breakup_date = date

    def set_new_pregnancy_or_adoption_process_date(self, couple):
        """Sets pregnancy or adoption date and birth date. Cannot be the same as breakup date or marriage date."""
        date = couple.breakup_date
        while date == couple.breakup_date - 1 or date == couple.breakup_date or date == couple.breakup_date + 1:
            date = self.statistics.get_oldest_pregnancy_date(couple)
        if couple.will_get_pregnant:
            couple.pregnancy_date = date
            couple.birth_date = date + 1
        elif couple.will_adopt:
            couple.adoption_process_date = date
            couple.adoption_date = date + 1
        else:
            raise Exception(
                "Couple is set on having a child but won't get pregnant nor adopt.")

        # Validation
        self.unique_dates_validation(couple)

        return couple

    def unique_dates_validation(self, couple):
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
