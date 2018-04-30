from traits import Traits, Setup
from utilities.randomizer import Randomizer
from education import Education


class Job:
    """Job base class."""

    BACHELOR_JOB_LIST = 'BACHELOR'
    FAMOUS_JOB_LIST = 'FAMOUS'
    LOW_JOB_LIST = 'LOW'

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
    PERFORMANCE_LIST = [GOOD_PERFORMANCE, BAD_PERFORMANCE, FLAT_PERFORMANCE, FLAT_PERFORMANCE]

    SALARY_MIN_STANDARD = 20000  # per year
    SALARY_MAX_STANDARD = 30000  # per year

    MAXIMUM_SALARY_CHANGE = 30 # in percentages

    def __init__(self, level=0, salary=0, employment=Traits.UNEMPLOYED):
        self.level = level
        self.salary = salary  # per year
        self.employment = employment
        self.unemployed_year = 0
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

    def progress_job(self):
        self.current_performance += self.randomizer.get_random_item(self.PERFORMANCE_LIST)
        self.change_salary_rate = self.randomizer.get_random_number(0, 30) / 100
        if (self.current_performance > 2) :
            self.promotion(self.change_salary_rate)
        elif (self.current_performance > 1):
            self.promotion(self.change_salary_rate,job_increase=True)
        elif (self.current_performance < -3 ):
            self.termination()
        elif (self.current_performance < -2):
            self.demotion(self.change_salary_rate, job_decrease=True)
        elif (self.current_performance < -1):
            self.demotion(self.change_salary_rate)

    def get_job(self, degree):
        """Set occupation and job level."""
        job_chance = [self.LOW_JOB_LIST, self.FAMOUS_JOB_LIST]

        if degree == Education.UNEDUCATED:
            self.level = self.PART_TIMER
        if degree == Education.SCHOOL:
            self.level = self.INTERN
        elif degree == Education.BACHELOR:
            job_chance.append(self.BACHELOR_JOB_LIST)
            self.level = self.FRESHGRADUATE
        elif degree == Education.MASTER:
            job_chance.append(self.BACHELOR_JOB_LIST)
            self.level = self.SENIOR
        elif degree == Education.DOCTOR:
            job_chance.append(self.BACHELOR_JOB_LIST)
            self.level = self.EXECUTIVE

        self.title = self.randomizer.get_random_item(
                        self.setup.PROFESSIONS[self.randomizer.get_random_item(job_chance)])
        # Set salary based on job level
        self.salary = self.randomizer.get_random_number(
            self.SALARY_MIN_STANDARD, self.SALARY_MAX_STANDARD) * (self.level + 1)
        # Switch to Employed
        self.employment = Traits.EMPLOYED

    def promotion(self, salary_increment, job_increase=False):
        """Job promotion."""
        if job_increase and self.level < self.EXECUTIVE:
            self.level += 1
            self.current_performance = self.FLAT_PERFORMANCE
        self.salary = self.salary * (1 + salary_increment)


    def demotion(self, salary_decrease, job_decrease=False):
        """Job demotion."""
        if job_decrease and self.level > 0:
            self.level -= 1
            self.current_performance = self.FLAT_PERFORMANCE
        self.salary = 0 if 1 - salary_decrease < 0 else self.salary * (1 - salary_decrease)

    def termination(self):
        """Job termination"""
        self.salary = 0
        self.level = 0
        self.employment = Traits.UNEMPLOYED
        self.title="ex-"+self.title
        self.current_performance = self.FLAT_PERFORMANCE
