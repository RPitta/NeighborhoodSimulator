from utilities.randomizer import Randomizer
from traits import Traits


class CoupleDeveloper:
    """Couple developer base class."""

    NEXT_YEAR = 1
    MAX_YEAR_FOR_MOVE_IN = 6
    MAX_YEAR_FOR_MARRIAGE = 8
    YEARS_TILL_ADOPTION = 2

    def __init__(self, statistics):
        self.statistics = statistics
        self.randomizer = Randomizer()

    def set_new_couples_goals(self, couple):
        """Set new couple's goals."""
        if len(couple.oldest.span_left_till_old_age) <= self.NEXT_YEAR:  # No time left for marriage/breakup if old age.
            return couple

        # Set random move in date if applicable
        self.set_move_in(couple)

        # If couple wants to get married, set random marriage date.
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
            couple.desired_num_of_children = self.statistics.get_desired_num_of_children()
            couple.desired_children_left = couple.desired_num_of_children
            couple = self.set_new_pregnancy_or_adoption_process_date(couple)

        self.unique_dates_validation(couple)
        return couple

    def set_move_in(self, couple):
        """Set move in date and household ID if applicable."""
        if all(p.is_neighbor for p in couple.persons) and all(
                couple.persons[0].apartment_id == p.apartment_id for p in couple.persons):
            for p in couple.persons:
                p.move_in_date = p.age  # If all live in the same household already, assign move in date to present time

        # If neighbors from different households, assign move in date for random person
        if all(p.is_neighbor for p in couple.persons) and any(
                couple.persons[0].apartment_id != p.apartment_id for p in couple.persons[0]):
            chosen_person = self.randomizer.get_random_item(couple.persons)
            self.set_move_in_date_and_id(chosen_person, couple)

        # Assign move in date for the outsider if not all are neighbors
        if any(p.is_neighbor for p in couple.persons):
            neighbor = next(p for p in couple.persons if p.is_neighbor)
            outsider = next(p for p in couple.persons if p.is_neighbor is False)
            # If neighbor does not have another partner, and outsider is not married, move in
            if len(neighbor.partners) < 2 and outsider.is_married_or_remarried is False:
                self.set_move_in_date_and_id(outsider, couple)

    def set_move_in_date_and_id(self, person, couple):
        """Set move in date and household."""
        moving_range = range(self.NEXT_YEAR, self.MAX_YEAR_FOR_MOVE_IN)
        person.move_in_date = person.age + self.randomizer.get_random_item(moving_range)
        person.house_to_move_in = next(p.apartment_id for p in couple.persons if p != person)

    def set_marriage_date(self, couple):
        """Sets couple's marriage date based on move in date."""
        marriable_range = range(self.NEXT_YEAR, self.MAX_YEAR_FOR_MARRIAGE)
        if couple.move_in_date == -1:
            date = couple.oldest.age + self.randomizer.get_random_item(marriable_range)
        else:
            date = couple.move_in_date + self.randomizer.get_random_item(marriable_range)
        if date not in couple.oldest.span_left_till_old_age:
            date = self.randomizer.get_random_item(couple.oldest.span_left_till_old_age)
        couple.marriage_date = date

    def set_breakup_date(self, couple):
        """Sets couple's break up date."""
        if abs(Traits.SENIOR.end - couple.marriage_date) <= self.NEXT_YEAR or abs(
                Traits.SENIOR.end - couple.move_in_date) <= self.NEXT_YEAR:
            # Couple will not break up if no time left after move in date or marriage date.
            couple.will_breakup = False
            return
        date = couple.marriage_date
        while date <= couple.move_in_date or date <= couple.marriage_date or date in range(couple.pregnancy_date,
                                                                                           couple.birth_date + 2) or date in range(
            couple.adoption_process_date, couple.adoption_date + 2):
            date = self.statistics.get_oldest_breakup_date(couple)

        # If selected breakup date is before move in date,
        # add age difference to breakup date (which is based on oldest person's age)
        if couple.move_in_date + couple.age_difference >= date:
            couple.breakup_date = date + (couple.age_difference + self.NEXT_YEAR)
            # If oldest person will be dead by breakup date, set will break up to False
            if couple.breakup_date not in couple.oldest.span_left_till_old_age:
                couple.will_breakup = False
                couple.breakup_date = -1
        else:
            couple.breakup_date = date

    def set_new_pregnancy_or_adoption_process_date(self, couple):
        """Sets pregnancy or adoption date and birth date."""
        if abs(Traits.ADULT.start - couple.marriage_date) <= 2 or abs(Traits.ADULT.start - couple.move_in_date) <= 2:
            return couple
        if abs(couple.oldest.age - couple.breakup_date) <= 4 or abs(
                couple.marriage_date - couple.breakup_date) <= 4 or abs(
            couple.move_in_date - couple.breakup_date) <= 4:
            return couple

        date = couple.breakup_date
        while date <= couple.move_in_date or date <= couple.marriage_date or date in range(
                couple.breakup_date - 3, couple.breakup_date + 3):
            date = self.statistics.get_oldest_pregnancy_date(couple)

        if couple.will_get_pregnant:
            couple.pregnancy_date = date
            couple.birth_date = date + self.NEXT_YEAR
        elif couple.will_adopt:
            couple.adoption_process_date = date
            couple.adoption_date = date + self.YEARS_TILL_ADOPTION
        else:
            raise Exception(
                "Couple is set on having a child but won't get pregnant nor adopt.")

        if (couple.will_adopt and couple.adoption_process_date > 0) or (couple.pregnancy_date > 0):
           check_date = couple.pregnancy_date if couple.pregnancy_date > 0 else couple.adoption_process_date
           if (check_date not in couple.oldest.span_left_till_old_age):
               couple.pregnancy_date = 0
               couple.adoption_process_date = 0
               couple.will_adopt = 0

        self.unique_dates_validation(couple)
        return couple

    @classmethod
    def unique_dates_validation(cls, couple):
        if couple.will_get_married and couple.marriage_date >= couple.oldest.age:
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
        if couple.will_adopt and couple.adoption_process_date > 0:
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
