
from person_attributes import PersonAttributes
from randomizer import Randomizer
import random

class RelationshipGenerator(PersonAttributes):

    def get_intergenerational(self):
        """Returns true if intergenerational relationship. False otherwise."""
        options = {
            True: 20,
            False: 80
        }

        return Randomizer().get_random_dict_key(options)

    def get_incest(self):
        """Returns true if incestuous relationship. False otherwise."""
        options = {
            True: 20,
            False: 80
        }

        return Randomizer().get_random_dict_key(options)

    def find_partner(self, person, romanceable_outsiders):
        """Returns a random compatible person"""
        lst = self.get_list_of_compatible_common_persons(person, romanceable_outsiders)
        return random.choice(lst)

    def get_list_of_compatible_persons(self, person, romanceable_outsiders):

        # If incest
        if self.get_incest():
            pass

        # If intergenerational
        age_gap = self.get_intergenerational()

        compatible_outsiders = []

        for i in range(len(romanceable_outsiders)-1):
            person2 = romanceable_outsiders[i]

            if person != person2 and person.is_compatible(person2):
                if age_gap:
                    if not person.is_of_same_age(person2):
                        compatible_outsiders.append(person2)
                else:
                    if person.is_of_same_age(person2):
                        compatible_outsiders.append(person2)

        return compatible_outsiders

    def assign_common_partner(self, person, persons_list):
        """Returns a random compatible common person (not intergenerational / incest) """

        # Validation
        if len(persons_list) <= 1:
            raise Exception("Unexpected error occurred. List of persons is less than 2.")

        candidates_list = self.get_list_of_compatible_common_persons(person, persons_list)

        # Validation
        if candidates_list is None or len(candidates_list) <= 0:
            return False
        if person in candidates_list:
            raise Exception("Unexpected error occurred. Person is in list of candidates.")
            
        # Get random partner from candidates list
        person2 = random.choice(candidates_list)

        # Validation
        if person2 is None or person2 == person or person2 not in persons_list:
            raise Exception("Unexpected error occurred. Assigned partner is empty or wrong.")
        
        # Assign partners
        person.partner = person2
        person2.partner = person

        return True

    def get_list_of_compatible_common_persons(self, person, persons_list):
        """Returns list of compatible persons that have the same age."""

        compatible_persons = []

        for candidate in persons_list:
            if person != candidate and person.is_compatible(candidate):
                compatible_persons.append(candidate)

        return compatible_persons

