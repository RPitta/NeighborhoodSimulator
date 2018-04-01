from utilities.randomizer import Randomizer
from statistics import Statistics

class Education:
    Uneducated = 0
    School = 1
    Bachelor = 2
    Master = 3
    Doctor = 4

    literal_Degree = ['Uneducated','High School Diploma','Bachelor Degree',
                      'Master Degree','Doctoral Degree']

    #Personal data
    available_degree = 0
    current_year = 0
    current_year_to_take = 0
    in_study = False
    dropped_out = False
    total_fail = 0
    acquired_degree = None

    random = Randomizer()

    def __init__(self,age):
        self.available_degree = self.School
        self.acquired_degree = []
        self.acquired_degree.append(self.Uneducated)
        self.current_year = 0
        self.in_study = False
        self.graduated = False
        self.dropped_out = False
        self.total_fail = 0
        self.current_year_to_take = 0
        self.init_degree(age)

    def __str__(self):
        return self.strDegree

    @property
    def currentDegree(self):
        return self.acquired_degree[-1]

    @property
    def strDegree(self):
            return self.literal_Degree[self.acquired_degree[-1]]

    def init_degree(self, age):
        if age < 7 :
            return False
        elif age < 18 :
            self.startSchool()
            self.current_year_to_take = 12 - (age - 6)
        elif age > 26 and self.get_chance_for_getting_doctor_degree() :
            self.acquired_degree.append(self.Master)
            self.startDoctor()
            self.current_year_to_take -= self.random.get_random_number(1,age-25)
        elif age > 24 and self.get_chance_for_getting_master_degree() :
            self.acquired_degree.append(self.Bachelor)
            self.startMaster()
            self.current_year_to_take -= self.random.get_random_number(0,1)
        elif self.get_chance_for_getting_bachelor_degree():
            self.acquired_degree.append(self.School)
            self.startBachelor()
            self.current_year_to_take -= self.random.get_random_number(0,3)
        else :
            self.acquired_degree.append(self.School)
            self.in_study = False
            self.current_year_to_take = 0

    def advance_degree_process(self,
                               is_drug_addict=False,
                               is_alcohol_addict=False):
        if (not self.in_study):
            return False
        chance_to_fail = 0.25 * ( is_drug_addict + is_alcohol_addict)
        chance_to_success = 98 - ((chance_to_fail*100))
        if (self.random.get_random_number(0,100) <= chance_to_success):
            if (self.current_year == self.current_year_to_take) :
                self.current_year = 0
                self.in_study = False
                self.total_fail = 0
                self.acquired_degree.append(self.currentDegree+1)
                if (self.currentDegree+1 != self.Doctor):
                    self.available_degree = self.currentDegree+1
            else :
                self.current_year +=1
        else :
            #Doctor candidate will never dropped out
            if (self.currentDegree+1 == self.Doctor):
                return
            self.total_fail +=1
            if (self.total_fail > 3):
                self.in_study = False
                self.total_fail = 0
                self.current_year = 0

    def startNextDegree(self):
        if self.available_degree == self.Bachelor\
           and self.get_chance_for_getting_bachelor_degree():
            self.startBachelor()
        elif self.available_degree == self.Master\
             and self.get_chance_for_getting_master_degree():
            self.startMaster()
        elif self.available_degree == self.Doctor\
             and self.get_chance_for_getting_doctor_degree():
            self.startDoctor()
        else :
            return False
        return True

    def startSchool(self):
        self.current_year_to_take = 12
        self.in_study = True
        self.total_fail = 0
        self.current_year = 0


    def startBachelor(self):
        self.current_year_to_take = 4
        self.in_study = True
        self.total_fail = 0
        self.current_year = 0

    def startMaster(self):
        self.current_year_to_take = 2
        self.in_study = True
        self.total_fail = 0
        self.current_year = 0

    def startDoctor(self):
        self.current_year_to_take = self.random.get_random_number(6,10)
        self.in_study = True
        self.total_fail = 0
        self.current_year = 0

    def get_chance_for_getting_bachelor_degree(self):
        options = {
            True: 46,
            False: 54
        }
        return self.random.get_random_dict_key(options)

    def get_chance_for_getting_master_degree(self):
        options = {
            True: 20,
            False: 80
        }
        return self.random.get_random_dict_key(options)

    def get_chance_for_getting_doctor_degree(self):
        options = {
            True: 9,
            False: 91
        }
        return self.random.get_random_dict_key(options)
