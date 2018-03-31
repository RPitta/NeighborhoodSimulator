from traits import Traits, Setup
from utilities.randomizer import Randomizer
from education import Education

class Job:
    """Job base class."""

    Parttimer = -0.5 #half salary
    Intern = 0
    Freshgraduate = 1
    Junior = 2
    Senior = 3
    Lead = 4
    Manager = 5
    Executive = 6

    good_performance = 1
    bad_performance = -1
    flat_performance = 0
    current_performance = 0

    employment = None
    level = None
    salary = 0 #per year

    randomizer = Randomizer()
    setup = Setup()

    def __init__(self, title ='Unemployed', level=0, salary=0, employment=Traits.UNEMPLOYED):
        self.occupation = 'Unemployed'
        self.level = level
        self.salary = salary
        self.employment = employment

    def getAJob(self,degree):
        self.occupation = self.randomizer.get_random_item(self.setup.PROFESSIONS)
        if degree is Education.Uneducated :
            self.level = self.Parttimer
        if degree is Education.School:
            self.level = self.Intern
        elif degree is Education.Bachelor :
            self.level = self.Freshgraduate
        elif degree is Education.Master :
            self.level = self.Senior
        elif degree is Education.Doctor :
            self.level = self.Executive
        self.salary = self.randomizer.get_random_number(20000, 30000) * (self.level + 1)

        self.employment=Traits.EMPLOYED


    def promotion(self, salary_increment, job_increase=False):
        """Job promotion."""
        if job_increase and self.level < self.Executive:
            self.level += 1
        self.salary = self.salary * (1 + salary_increment)
        self.current_performance = self.good_performance

    def demotion(self, salary_decrease, job_decrease=False):
        """Job demotion."""
        if job_decrease and self.level > 0:
            self.level -= 1
        self.salary = 0 if 1 - salary_decrease < 0 else self.salary * (1 - salary_decrease)
        self.current_performance = self.bad_performance
