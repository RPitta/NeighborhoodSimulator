from utilities.randomizer import Randomizer


class Education:
    """Education base class."""

    SCHOOL_START_DATE = 6
    BACHELOR_START_DATE = 18
    MASTER_START_DATE = 24
    DOCTOR_START_DATE = 26

    SCHOOL_NUM_OF_YEARS = (12, 12)
    BACHELOR_NUM_OF_YEARS = (4, 4)
    MASTER_NUM_OF_YEARS = (2, 2)
    DOCTOR_NUM_OF_YEARS = (6, 10)
    YEARS_TO_COMPLETE = [0, SCHOOL_NUM_OF_YEARS, BACHELOR_NUM_OF_YEARS, MASTER_NUM_OF_YEARS, DOCTOR_NUM_OF_YEARS]

    FAILING_CLASS_MAX = 3

    # Degrees
    UNEDUCATED = 0
    SCHOOL = 1
    BACHELOR = 2
    MASTER = 3
    DOCTOR = 4
    LITERAL_DEGREES = ['Uneducated', 'High School Diploma', 'Bachelor Degree', 'Master Degree', 'Doctoral Degree']

    # External Factor
    # Value range from 0 to 1
    DRUG_ADDICTION_EFFECT = 0.25
    ALCOHOL_ADDICTION_EFFECT = 0.25
    CHANCE_OF_BAD_DECISION = 0.02

    def __init__(self):
        self.available_degree = self.SCHOOL
        self.acquired_degree = [self.UNEDUCATED]
        self.in_study = False
        self.current_year = 0
        self.years_to_complete_degree = 0
        self.total_fail = 0
        self.randomizer = Randomizer()

    def __str__(self):
        return self.LITERAL_DEGREES[self.acquired_degree[-1]]

    @property
    def current_degree(self):
        """Returns person's current degree level."""
        return self.acquired_degree[-1]

    def init_degree(self, person):
        """Initialize education for non-natural born persons."""
        if person.age < self.SCHOOL_START_DATE:
            return False
        elif person.age < self.BACHELOR_START_DATE:
            self.start_degree(self.SCHOOL)
            self.years_to_complete_degree = self.SCHOOL_NUM_OF_YEARS[0] - (person.age - 6)
        elif person.age >= self.DOCTOR_START_DATE and person.will_do_doctor:
            self.acquired_degree.append(self.MASTER)
            self.start_degree(self.DOCTOR)
            self.years_to_complete_degree -= self.randomizer.get_random_number(1, person.age - 25)
        elif person.age >= self.MASTER_START_DATE and person.will_do_master:
            self.acquired_degree.append(self.BACHELOR)
            self.start_degree(self.MASTER)
            self.years_to_complete_degree -= self.randomizer.get_random_number(0, 1)
        elif person.will_do_bachelor:
            self.acquired_degree.append(self.SCHOOL)
            self.start_degree(self.SCHOOL)
            self.years_to_complete_degree -= self.randomizer.get_random_number(0, 3)
        else:
            self.acquired_degree.append(self.SCHOOL)
            self.in_study = False
            self.years_to_complete_degree = 0

    def start_degree(self, degree):
        """Starts new degree."""
        start = self.YEARS_TO_COMPLETE[degree][0]
        end = self.YEARS_TO_COMPLETE[degree][1]
        self.years_to_complete_degree = self.randomizer.get_random_number(start, end)
        self.in_study = True
        self.total_fail = 0
        self.current_year = 0

    def advance_degree(self, is_drug_addict=False, is_alcohol_addict=False):
        """Advance degree."""
        chance_to_fail = self.DRUG_ADDICTION_EFFECT * is_drug_addict + self.ALCOHOL_ADDICTION_EFFECT * is_alcohol_addict + self.CHANCE_OF_BAD_DECISION
        chance_to_success = 100 - (chance_to_fail * 100)
        if self.randomizer.get_random_number(0, 100) <= chance_to_success:
            if self.current_degree == self.years_to_complete_degree:
                self.current_year += 1
            else:
                self.acquire_degree()
                if self.current_degree + 1 != self.DOCTOR:
                    self.available_degree = self.current_degree + 1
        else:
            # Doctor candidate will never drop out
            if self.current_degree + 1 == self.DOCTOR:
                return
            self.total_fail += 1
            # Fail out
            if self.total_fail > self.FAILING_CLASS_MAX:
                self.fail_out()

    def acquire_degree(self):
        """Append new obtained degree and finish studies."""
        self.current_year = 0
        self.in_study = False
        self.total_fail = 0
        self.acquired_degree.append(self.current_degree + 1)

    def fail_out(self):
        """Fail out of current degree."""
        self.in_study = False
        self.total_fail = 0
        self.current_year = 0
