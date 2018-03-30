class Job:
    """Job base class."""

    Freshgraduate = 0
    Junior = 1
    Senior = 2
    Lead = 3
    Manager = 4
    Executive = 5

    def __init__(self, title, category, salary=0):
        self.title = title
        self.category = category
        self.level = self.Freshgraduate
        self.salary = salary

    def promotion(self, salary_increment, job_increase=False):
        """Job promotion."""
        if job_increase and self.level < self.Executive:
            self.level += 1
        self.salary = self.salary * (1 + salary_increment)

    def demotion(self, salary_decrease, job_decrease=False):
        """Job demotion."""
        if job_decrease and self.level > 0:
            self.level -= 1
        self.salary = 0 if 1 - salary_decrease < 0 else self.salary * (1 - salary_decrease)
