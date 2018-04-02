from traits import Traits, Setup
from utilities.randomizer import Randomizer
from education import Education


class Job:
    """Job base class."""

    PART_TIMER = -0.5  # half salary
    INTERN = 0
    FRESHGRADUATE = 1
    JUNIOR = 2
    SENIOR = 3
    LEAD = 4
    MANAGER = 5
    EXECUTIVE = 6

    GOOD_PERFORMANCE = 1
    BAD_PERFORMANCE = -1
    FLAT_PERFORMANCE = 0

    SALARY_MIN_STANDARD = 20000 # per year
    SALARY_MAX_STANDARD = 30000 # per year

    def __init__(self, level=0, salary=0, employment=Traits.UNEMPLOYED):
        self.level = level
        self.salary = salary  # per year
        self.employment = employment
        self.title = None
        self.current_performance = 0
        self.randomizer = Randomizer()
        self.setup = Setup()

    def __str__(self):
        ret_val = {
            'occupation': self.title,
            'level': self.level,
            'salary': self.salary,
            'employment': self.employment
        }
        return str(ret_val)

    def get_job(self, degree):
        """Set occupation and job level."""
        self.title = self.randomizer.get_random_item(self.setup.PROFESSIONS)
        if degree == Education.UNEDUCATED:
            self.level = self.PART_TIMER
        if degree == Education.SCHOOL:
            self.level = self.INTERN
        elif degree == Education.BACHELOR:
            self.level = self.FRESHGRADUATE
        elif degree == Education.MASTER:
            self.level = self.SENIOR
        elif degree == Education.DOCTOR:
            self.level = self.EXECUTIVE
        # Set salary based on job level
        self.salary = self.randomizer.get_random_number(
                                        self.SALARY_MIN_STANDARD,
                                        self.SALARY_MAX_STANDARD)\
                        * (self.level + 1)
        # Switch to Employed
        self.employment = Traits.EMPLOYED

    def promotion(self, salary_increment, job_increase=False):
        """Job promotion."""
        if job_increase and self.level < self.EXECUTIVE:
            self.level += 1
        self.salary = self.salary * (1 + salary_increment)
        self.current_performance = self.GOOD_PERFORMANCE

    def demotion(self, salary_decrease, job_decrease=False):
        """Job demotion."""
        if job_decrease and self.level > 0:
            self.level -= 1
        self.salary = 0 if 1 - salary_decrease < 0 else self.salary * (1 - salary_decrease)
        self.current_performance = self.BAD_PERFORMANCE
