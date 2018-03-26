class Degree :
	Uneducated = 0
	Elementary = 1
	JuniorHigh = 2
	SeniorHigh = 3
	Bachelor = 4
	Master = 5
	PHd = 6

class JobLevel :
	Freshgraduate = 0
	Junior = 1
	Senior = 2
	Lead = 3
	Manager = 4
	Executive = 5


class MajorCreator :
	name = None 
	traits = None
	degree = Degree.Uneducated

	def __init__(self, name, traits=None, degree = Degree.Uneducated):
		self.name = name 
		self.traits = traits
		self.degree = Degree.Uneducated

class ProfessionCreator : 
	title = None
	requirement = None

	def __init__(self, title, requirements):
		self.title = title 
		self.requirement = []
		for requirement in requirements:
			self.requirement.append(requirement)

class Majors:
	lists = {}

	def __init__(self):
		self.lists['medical'] = MajorCreator('medical',traits = professional_trait.medical_trait)
		self.lists['engineering'] = MajorCreator('engineering')
		#add more major

	def increase_degree_by(self, major, level = 1):
		if major in self.lists :
			if self.lists[major].degree == 6 :
				return 0
			self.lists[major].degree += level
			return 1
		else :
			return 0

class Professions :
	lists = {}

	def __init__(self):
		doctor_requirement = []
		doctor_requirement.append(MajorCreator('medical', degree = Degree.Bachelor))
		doctor_requirement.append(MajorCreator('science', degree = Degree.SeniorHigh))
		self.lists['doctor'] = ProfessionCreator('doctor', doctor_requirement)

		programmer_requirement = []
		programmer_requirement.append(MajorCreator('engineer', degree = Degree.Bachelor))
		programmer_requirement.append(MajorCreator('science', degree = Degree.SeniorHigh))
		self.lists['programmer'] = ProfessionCreator('programmer', programmer_requirement)

		#add more profession category
	


class professional_trait :

	def medical_trait(self):
		#do nothing yet
		return 0


