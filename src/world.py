from person_attributes import PersonAttributes
from person import Person
from life_stage import *

from statistics import Statistics
from compatibility import Compatibility
from relationship import Relationship
from straight_relationship import StraightRelationship
from randomizer import Randomizer

class World(Statistics, PersonAttributes):

    NEIGHBOORHOOD_APARTMENTS = 16
    NEIGHBOORHOOD_FAMILIES = NEIGHBOORHOOD_APARTMENTS
    FAMILY_IDS = NEIGHBOORHOOD_APARTMENTS

    def __init__(self):

        self.MALE_NAMES = self.get_male_names()
        self.FEMALE_NAMES = self.get_female_names()
        self.SURNAMES = self.get_surnames()
        self.PROFESSIONS = self.get_professions()

        self.baby = Baby()
        self.child = Child()
        self.teen = Teen()
        self.young_adult = YoungAdult()
        self.adult = Adult()
        self.senior = Senior()
        self.life_stages = LifeStages()
        
        self.life_stages.add(self.baby)
        self.life_stages.add(self.child)
        self.life_stages.add(self.teen)
        self.life_stages.add(self.young_adult)
        self.life_stages.add(self.adult)
        self.life_stages.add(self.senior)

        self.couples = []
        self.population = []
        self.neighbors = []
        self.populate_world()

    def get_male_names(self):
        path_males = r"C:\Users\cugat\Documents\Programming\Python\NeighborhoodSimulator\src\files\male_names.txt"
        file_males = open(path_males, "r")
        names = set([x.split(' ')[0] for x in file_males.readlines()])
        names = [item.capitalize() for item in names]
        file_males.close()
        return names

    def get_female_names(self):
        path_females = r"C:\Users\cugat\Documents\Programming\Python\NeighborhoodSimulator\src\files\female_names.txt"
        file_females = open(path_females, "r")
        names = set([x.split(' ')[0] for x in file_females.readlines()])
        names = [item.capitalize() for item in names]
        return names

    def get_surnames(self):
        path_surnames = r"C:\Users\cugat\Documents\Programming\Python\NeighborhoodSimulator\src\files\surnames.txt"
        file_surnames = open(path_surnames, "r")    
        surnames = set([x.split(' ')[0] for x in file_surnames.readlines()])
        surnames = [item.capitalize() for item in surnames]    
        file_surnames.close()
        return surnames

    def get_professions(self):
        path_professions = r"C:\Users\cugat\Documents\Programming\Python\NeighborhoodSimulator\src\files\professions.txt"
        file_professions = open(path_professions, "r")
        professions = set([x.split('\n')[0] for x in file_professions.readlines()])
        professions = [item.capitalize() for item in professions]
        file_professions.close()
        return professions

    @property
    def population(self):
        return self._population

    @population.setter
    def population(self, persons):
        
        if persons is None:
            self._population = []

        else:
            self._population = persons
            if self.couples is not None:
                # Remove dead couples from couples list
                deceased = [couple for couple in self.couples for person in couple.persons if not person.is_alive]

                if deceased is not None and len(deceased) > 0:
                    self.couples = [couple for couple in self.couples if couple not in deceased]
            
    @property
    def living_population(self):
        return [person for person in self.population if person.is_alive]

    @property
    def dead_population(self):
        return [person for person in self.population if not person.is_alive]

    @property
    def population_surnames(self):
        return set([person.surname for person in self.living_population])

    @property
    def romanceable_outsiders(self):
        return [person for person in self.living_population if person.is_romanceable] 

    @property
    def unromanceable_outsiders(self):
        return [person for person in self.living_population if person.is_romanceable is False]

    @property
    def partnered_outsiders(self):
        return [person for person in self.living_population if person.partner is not None]

    def get_population(self):

        for person in self.population:
            yield "ID: {}\nName: {}\nSurname: {}\nGender: {}\nGender identity: {}\nSexual orientation: {}\nLife stage: {}\nFather: {}\nMother: {}\nSiblings: {}\nGrandparents: {}\nUncles: {}\nAunts: {}\nCousins: {}\nPartner: {}\nChildren: {}\nNephews: {}\nNieces: {}\nRelationship Status: {}\nPregnant: {}\nCan have children: {}\nWants children: {}\nProfession: {}\nEmployment: {}\n".format(
                person.family_id,
                person.name,
                person.surname,
                person.gender,
                person.gender_identity,
                person.sexual_orientation,
                person.life_stage,
                person.get_fathers_name(),
                person.get_mothers_name(),
                person.get_siblings_names(),
                person.get_grandparents_names(),
                person.get_uncles_names(),
                person.get_aunts_names(),
                person.get_cousins_names(),
                person.get_partners_name(),
                person.get_childrens_names(),
                person.get_nephews_names(),
                person.get_nieces_names(),
                person.relationship_status,
                person.is_pregnant,
                person.can_have_children,
                person.wants_children,
                person.occupation,
                person.age
            )


    # ACTIONS

    def populate_world(self):
        for _ in (number+1 for number in range(1)):
            self.population.append(self.generate_straight_yadult(self.MALE))
            self.population.append(self.generate_straight_yadult(self.FEMALE))

    def do_couple_action(self, couple):
        
        if couple.will_get_married:
            couple.get_married()
            return
        if couple.will_get_pregnant:
            couple.get_pregnant()
            return
        if couple.will_adopt:
            couple.start_adoption_process()
            return
        if couple.is_pregnant:
            self.give_birth(couple)
            return
        if couple.in_adoption_process:
            self.adopt(couple)
        return

    def time_jump(self):

        for person in self.living_population:
            person.age_up()
            if person.is_romanceable:
                self.find_partner(person)
                pass
            else:
                pass
        
        if self.couples is not None:
            for couple in self.couples:
                self.do_couple_action(couple)

    # NOT IMPLEMENTED YET

    def populate_neighborhood(self):
        pass


    # PERSON GENERATOR

    def generate_straight_yadult(self, gender):
        person = Person(gender, YoungAdult(), self.CISGENDER,
                        self.HETEROSEXUAL, self.MONOAMOROUS)
        person.surname = self.get_surname(person, self.population_surnames)
        self.assign_random_traits(person)
        self.assign_romanceable_traits(person)
        return person

    def assign_romanceable_traits(self, baby):
        baby.wants_domestic_partnership = True
        baby.wants_marriage = True
        baby.can_have_children = True
        baby.wants_children = True

    def generate_baby(self, couple):

        mother = couple.get_female()
        father = couple.get_male()

        baby = Person(self.get_gender(), self.baby, self.get_gender_identity(),
                      self.get_sexual_orientation(), self.get_relationship_orientation())
        
        self.assign_family(baby, father, mother)
        
        self.assign_random_traits(baby)
        
        self.baby_validation(baby)

        return baby

    def assign_family(self, baby, father, mother):
        # Assign mother and father
        baby.parents = [father, mother]
        baby.family_id = baby.father.family_id

    def assign_random_traits(self, baby):
        # Assign unique name among their family
        baby.name = self.get_name(baby)
        baby.target_gender = [
            gender for gender in self.get_target_gender(baby)]
        baby.death_date = self.get_death_date(baby)
        baby.death_cause = self.get_death_cause(baby)
        baby.is_liberal = self.get_liberalism(baby)
        baby.wants_domestic_partnership = self.get_domestic_partnership_desire(
            baby)
        baby.wants_marriage = self.get_marriage_desire(baby)
        baby.can_have_children = self.get_fertility(baby)
        baby.wants_children = self.get_children_desire(baby)

    def baby_validation(self, baby):
        
        if baby.name is None or baby.surname is None:
            raise Exception("Unexpected error occurred. Baby has no name or surname.")

        # PARENTS AND SIBLINGS
        if baby.mother is None or baby.father is None or baby not in baby.mother.children or baby not in baby.father.children:
            raise Exception(
                "Unexpected error occurred. Baby and parents not correctly assigned.")
        for child in baby.mother.children:
            if child != baby and (child not in baby.siblings or baby not in child.siblings):
                raise Exception(
                    "Unexpected error occurred. Baby and siblings not correctly assigned.")
            if child != baby and child.name == baby.name:
                raise Exception(
                    "Unexpected error occurred. Baby's name is the same as their sibling.")
        # OTHER FAMILY
        if baby.family is None:
            raise Exception("Unexpected error occurred. Baby's family is null.")
        if baby in baby.family or len(set(baby.family)) != len(baby.family):
            raise Exception("Unexpected error occurred. Baby is inside his relatives list or it contains duplicates.")
        for family_member in baby.family:
            if baby not in family_member.family:
                raise Exception("Unexpected error occurred. Baby not assigned to other family members.")
        for family_member in baby.mother.family:
            if family_member != baby and (baby not in family_member.family or family_member not in baby.family):
                raise Exception("Unexpected error occurred. Baby not assigned to other family members.")
        for family_member in baby.father.family:
            if family_member != baby and (baby not in family_member.family or family_member not in baby.family):
                raise Exception("Unexpected error occurred. Baby not assigned to other family members.")

    def give_birth(self, couple):

        new_babies = []
        for _ in range(couple.expecting_children):
            new_baby = self.generate_baby(couple)
            new_babies.append(new_baby)

        # Print
        baby_names = [baby.name for baby in new_babies]
        print("{} and {} have given birth to {}.".format(
            couple.person1.name, couple.person2.name, baby_names))

        # Reset pregnancy variables
        couple.get_female().is_pregnant = False
        couple.desired_num_of_children -= couple.expecting_children
        couple.expecting_children = 0

        # Update population
        self.population = self.population + new_babies
    
    def adopt(self, couple):

        new_babies = []
        for _ in range(couple.expecting_children):
            new_baby = self.generate_baby(couple)
            new_babies.append(new_baby)

        # Print
        baby_names = [baby.name for baby in new_babies]
        print("{} and {} have adopted {}.".format(
            couple.person1.name, couple.person2.name, baby_names))

        # Reset adoption variables
        for person in couple.persons:
            person.in_adoption_process = False        
        couple.desired_num_of_children -= couple.expecting_children
        couple.expecting_children = 0

        # Update population
        self.population = self.population + new_babies

    # Relationship generator

    def find_partner(self, person):
        
        # Find a random person
        found_person = self.assign_partner(person)

        # Return couples list as is if no compatible partner found
        if not found_person:
            return

        print("\n{} has started dating {}.\n".format(
            person.name, found_person.name))
        
        # Assign partners
        if person.is_mono:
            person.partner = found_person
        else:
            person.partners.append(found_person)
            
        if found_person.is_mono:
            found_person.partner = person
        else:
            found_person.partners.append(person)

        # Create relationship
        self.create_new_relationship(person, found_person)

    def assign_partner(self, person):
        """Returns a random compatible person """

        candidates_list = [candidate for candidate in self.get_compatible_candidates(person)]
        
        # Validation
        if candidates_list is None or len(candidates_list) <= 0:
            return False
            
        # Get random partner from candidates list
        person2 = Randomizer().get_random_list_item(candidates_list)

        return person2

    def get_compatible_candidates(self, person):
        """Returns list of compatible persons that have the same age."""

        for candidate in self.romanceable_outsiders:
            if Compatibility().are_compatible(person, candidate):
                yield candidate

    def create_new_relationship(self, person1, person2):

        if person1.gender != person2.gender:
            self.couples.append(StraightRelationship(person1, person2))
        else:
            self.couples.append(Relationship(person1, person2))