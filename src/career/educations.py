import career_lookup as cl


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
