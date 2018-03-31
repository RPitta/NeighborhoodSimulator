import career_lookup as cl

<<<<<<< HEAD
class Educations:

	#Personal data
	current_degree = 0
	acquired_major = None

	def __init__(self):
		self.acquired_major = cl.Majors()
		self.current_degree = cl.Degree.Uneducated

	def add_education(self, major, degree=0):
		if major in self.acquired_major.lists:
			self.acquired_major.lists[major].degree = degree
			if self.current_degree < degree :
				self.current_degree = degree
			return 1 
		else :
			return 0

	def get_traits(self,major):
		if major in self.acquired_major.lists:
			return self.major.lists[major].traits

	def create_major(self, name, traits=None, degree = Degree.Uneducated):
		created_major = cl.MajorCreator(name, traits = traits, degree = degree)
		return created_major

	def increase_degree_by(self, major, level = 1):
		if major in self.acquired_major.lists :
			return self.acquired_major.lists[major].increase_degree_by(major, level= level)
		return 0





=======
>>>>>>> 41940bd6ffde3a7d9bee75e2c2e2baa864cc60cf

class Educations:
    # Personal data
    current_degree = 0
    acquired_major = None

    def __init__(self):
        self.acquired_major = cl.Majors()
        self.current_degree = cl.Degree.Uneducated

    def add_education(self, major, degree=0):
        if major in self.acquired_major.lists:
            self.acquired_major.lists[major].degree = degree
            if self.current_degree < degree:
                self.current_degree = degree
            return 1
        else:
            return 0

    def get_traits(self, major):
        if major in self.acquired_major.lists:
            return self.major.lists[major].traits
