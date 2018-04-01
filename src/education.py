from utilities.randomizer import Randomizer


class Education:
    """Education base class."""

    SCHOOL_START_DATE = 6
    BACHELOR_START_DATE = 18
    MASTER_START_DATE = 24
    DOCTOR_START_DATE = 26

    SCHOOL_NUM_OF_YEARS = 12
    BACHELOR_NUM_OR_YEARS = 4
    MASTER_NUM_OF_YEARS = 2
    DOCTOR_NUM_OF_YEARS = (6, 10)

    # Degrees
    UNEDUCATED = 0
    SCHOOL = 1
    BACHELOR = 2
    MASTER = 3
    DOCTOR = 4
    LITERAL_DEGREES = ['Uneducated', 'High School Diploma', 'Bachelor Degree',
                       'Master Degree', 'Doctoral Degree']

    def __init__(self):
        self.available_degree = self.SCHOOL
        self.acquired_degree = [self.UNEDUCATED]
        self.in_study = False
        self.graduated = False
        self.dropped_out = False
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
        """Initialize education."""
        if person.age < self.SCHOOL_START_DATE:
            return False
        elif person.age < self.BACHELOR_START_DATE:
            self.start_school()
            self.years_to_complete_degree = 12 - (person.age - 6)
        elif person.age >= self.DOCTOR_START_DATE and person.will_do_doctor:
            self.acquired_degree.append(self.MASTER)
            self.start_doctor()
            self.years_to_complete_degree -= self.randomizer.get_random_number(1, person.age - 25)
        elif person.age >= self.MASTER_START_DATE and person.will_do_master:
            self.acquired_degree.append(self.BACHELOR)
            self.start_master()
            self.years_to_complete_degree -= self.randomizer.get_random_number(0, 1)
        elif person.will_do_bachelor:
            self.acquired_degree.append(self.SCHOOL)
            self.start_bachelor()
            self.years_to_complete_degree -= self.randomizer.get_random_number(0, 3)
        else:
            self.acquired_degree.append(self.SCHOOL)
            self.in_study = False
            self.years_to_complete_degree = 0

    def advance_degree_process(self, is_drug_addict=False, is_alcohol_addict=False):
        """Advance degree."""
        chance_to_fail = 0.25 * (is_drug_addict + is_alcohol_addict)
        chance_to_success = 98 - (chance_to_fail * 100)
        if self.randomizer.get_random_number(0, 100) <= chance_to_success:
            if self.current_year == self.years_to_complete_degree:
                self.current_year = 0
                self.in_study = False
                self.total_fail = 0
                self.acquired_degree.append(self.current_degree + 1)
                if self.current_degree + 1 != self.DOCTOR:
                    self.available_degree = self.current_degree + 1
            else:
                self.current_year += 1
        else:
            # Doctor candidate will never drop out
            if self.current_degree + 1 == self.DOCTOR:
                return
            self.total_fail += 1
            if self.total_fail > 3:
                self.in_study = False
                self.total_fail = 0
                self.current_year = 0

    def start_school(self):
        self.years_to_complete_degree = self.SCHOOL_NUM_OF_YEARS
        self.in_study = True
        self.total_fail = 0
        self.current_year = 0

    def start_bachelor(self):
        self.years_to_complete_degree = self.BACHELOR_NUM_OR_YEARS
        self.in_study = True
        self.total_fail = 0
        self.current_year = 0

    def start_master(self):
        self.years_to_complete_degree = self.MASTER_NUM_OF_YEARS
        self.in_study = True
        self.total_fail = 0
        self.current_year = 0

    def start_doctor(self):
        self.years_to_complete_degree = self.randomizer.get_random_number(self.DOCTOR_NUM_OF_YEARS[0], self.DOCTOR_NUM_OF_YEARS[1])
        self.in_study = True
        self.total_fail = 0
        self.current_year = 0
