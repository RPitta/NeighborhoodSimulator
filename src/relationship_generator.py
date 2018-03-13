
from person_attributes import PersonAttributes
from compatibility import Compatibility
from randomizer import Randomizer
import random

class RelationshipGenerator(Compatibility):

    def assign_partner(self, person, persons_list):
        """Returns a random compatible person """

        # Validation
        if len(persons_list) <= 1:
            return False

        candidates_list = self.get_compatible_candidates(person, persons_list)

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

    def get_compatible_candidates(self, person, persons_list):
        """Returns list of compatible persons that have the same age."""

        compatible_persons = []

        for candidate in persons_list:
            if person != candidate and self.are_compatible(person, candidate):
                compatible_persons.append(candidate)

        return compatible_persons

