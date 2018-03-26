import career_lookup as cl


class JobHistory :

	lists = []
	current_job = None

	def add_job(job):
		if (self.current_job is None):
			self.current_job = job
			return 1
		else :
			lists.append(self.current_job)
			self.current_job = job
			return 1

class Job :
	# title will be received from organized professions.txt
	title = None
	profession_category = None
	job_level = None
	salary = 0

	def __init__(self, title, profession_category, job_level = cl.Freshgraduate, salary = 0):
		self.title = title 
		self.profession_category = profession_category 
		self.job_level = job_level 
		self.salary = 0

	def promotions(self, salary_increment, job_increase = False):

		if (job_increase and self.job_level < 5) :
			self.job_level += 1
		self.salary = self.salary * (1+salary_increment)

		return 1

	def demotions(self, salary_decrease, job_decrease = False):

		if (job_decrease and self.job_level > 0) :
			self.job_level -= 1
		if(1-salary_increment < 0):
			self.salary = 0
		else :
			self.salary = self.salary * (1-salary_increment)

		return 1

