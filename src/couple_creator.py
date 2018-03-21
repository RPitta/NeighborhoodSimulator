from itertools import combinations
from couple import *
from traits import Traits
from utilities.randomizer import Randomizer
from utilities.compatibility import Compatibility


class CoupleCreator:

    def __init__(self):
        self.randomizer = Randomizer()
        self.compatibility = Compatibility()

    def create_couple(self, person, romanceable_outsiders):

        romanceables = [
            romanceable for romanceable in romanceable_outsiders if romanceable != person]

        candidates = self.get_candidates_list(person, romanceables)

        if not self.there_are_candidates(person, candidates):
            return False

        if person.in_love_as_throuple:
            throuple = self.get_throuple(person, candidates)
            return throuple
        else:
            couple = self.get_couple(person, candidates)
            return couple

    def get_throuple(self, person, candidates):
        found_persons = self.get_random_candidate(candidates)
        found_person1 = found_persons[0]
        found_person2 = found_persons[1]
        self.set_as_partner(person, found_person1, found_person2)
        self.update_relationship_status_to_committed(
            person, found_person1, found_person2)
        self.display_new_relationship_message(
            person, found_person1, found_person2)
        throuple = self.create_new_relationship(
            person, found_person1, found_person2)

        return throuple

    def get_couple(self, person, candidates):
        found_person = self.get_random_candidate(candidates)
        self.set_as_partner(person, found_person)
        self.update_relationship_status_to_committed(person, found_person)
        self.display_new_relationship_message(person, found_person)
        couple = self.create_new_relationship(person, found_person)

        return couple

    def get_candidates_list(self, person, romanceables):
        """Returns list of compatible persons."""
        if person.in_love_as_throuple is False:
            # Return list of compatible individuals
            return [candidate for candidate in romanceables if self.compatibility.are_compatible(person, candidate)]
        else:
            pairs = list(combinations(romanceables, 2))

            pair_candidates = []
            for romanceable in pairs:
                if self.compatibility.are_compatible(person, romanceable[0], romanceable[1]):
                    pair_candidates.extend([[romanceable[0], romanceable[1]]])

            # Return 2d list of compatible pairs
            return pair_candidates

    def there_are_candidates(self, person, candidates):
        return candidates is not None and len(candidates) >= 1

    def get_random_candidate(self, candidates):
        return self.randomizer.get_random_item(candidates)

    def set_as_partner(self, person, found_person, found_person2=None):
        if found_person2 is None:
            if person.is_mono:
                person.partner = found_person
            else:
                person.partners.append(found_person)

            if found_person.is_mono:
                found_person.partner = person
            else:
                found_person.partners.append(person)
        else:
            person.partners.append(found_person)
            person.partners.append(found_person2)
            found_person.partners.append(person)
            found_person.partners.append(found_person2)
            found_person2.partners.append(person)
            found_person2.partners.append(found_person)

    def update_relationship_status_to_committed(self, person1, person2, person3=None):
        if not person1.is_married_or_remarried:
            person1.relationship_status = Traits.COMMITTED
        if not person2.is_married_or_remarried:
            person2.relationship_status = Traits.COMMITTED
        if person3 is not None:
            if not person3.is_married_or_remarried:
                person3.relationship_status = Traits.COMMITTED

    def create_new_relationship(self, person1, person2, person3=None):

        if person3 is None:
            if person1 in person2.living_bio_family:
                couple = ConsangCouple(person1, person2)
            elif person1.gender != person2.gender:
                couple = StraightCouple(person1, person2)
            else:
                couple = GayCouple(person1, person2)
            return couple
        else:
            new_throuple = Throuple(person1, person2, person3)
            return new_throuple

    def display_new_relationship_message(self, person, found_person, found_person2=None):
        if found_person2 is None:
            print("\n{} has started dating {}.\n".format(person, found_person))
        else:
            print("\n{} has started dating {} and {}.\n".format(
                person, found_person, found_person2))