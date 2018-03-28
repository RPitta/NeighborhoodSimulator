from itertools import combinations
from couple import *
from traits import Traits
from utilities.randomizer import Randomizer
from utilities.compatibility import Compatibility


class CityCoupleCreator:
    """Creates new relationships."""

    def __init__(self):
        self.randomizer = Randomizer()
        self.compatibility = Compatibility()

    def create_couple(self, person, romanceable_outsiders):
        """Creates couple if found a match."""
        romanceables = [r for r in romanceable_outsiders if r != person]
        candidates = self.get_candidates_list(person, romanceables)
        if not self.there_are_candidates(candidates):
            return False
        if person.in_love_as_throuple:
            return self.get_throuple(person, candidates)
        return self.get_couple(person, candidates)

    def get_throuple(self, person, candidates):
        """Returns new throuple."""
        found_persons = self.get_random_candidate(candidates)
        found_person1 = found_persons[0]
        found_person2 = found_persons[1]
        self.set_as_partner(person, found_person1, found_person2)
        self.update_relationship_status_to_committed(
            person, found_person1, found_person2)
        return self.create_new_relationship(person, found_person1, found_person2)

    def get_couple(self, person, candidates):
        """Returns new couple."""
        found_person = self.get_random_candidate(candidates)
        self.set_as_partner(person, found_person)
        self.update_relationship_status_to_committed(person, found_person)
        return self.create_new_relationship(person, found_person)

    def get_candidates_list(self, person, romanceables):
        """Returns list of compatible individuals or pairs."""
        if person.in_love_as_throuple is False:
            return [candidate for candidate in romanceables if self.compatibility.are_compatible(person, candidate)]
        else:
            pairs = list(combinations(romanceables, 2))
            pair_candidates = []
            for romanceable in pairs:
                if self.compatibility.are_compatible(person, romanceable[0], romanceable[1]):
                    pair_candidates.extend([[romanceable[0], romanceable[1]]])
            return pair_candidates

    @classmethod
    def there_are_candidates(cls, candidates):
        return candidates is not None and len(candidates) >= 1

    def get_random_candidate(self, candidates):
        return self.randomizer.get_random_item(candidates)

    @classmethod
    def set_as_partner(cls, person, found_person, found_person2=None):
        if found_person2 is None:
            person.partners.append(found_person)
            found_person.partners.append(person)
        else:
            person.partners.append(found_person)
            person.partners.append(found_person2)
            found_person.partners.append(person)
            found_person.partners.append(found_person2)
            found_person2.partners.append(person)
            found_person2.partners.append(found_person)

    @classmethod
    def update_relationship_status_to_committed(cls, person1, person2, person3=None):
        if not person1.is_married_or_remarried:
            person1.relationship_status = Traits.COMMITTED
        if not person2.is_married_or_remarried:
            person2.relationship_status = Traits.COMMITTED
        if person3 is not None and not person3.is_married_or_remarried:
            person3.relationship_status = Traits.COMMITTED

    @classmethod
    def create_new_relationship(cls, person1, person2, person3=None):
        """Create new relationship."""
        if person3 is None:
            if person1 in person2.living_bio_family:
                couple = ConsangCouple(person1, person2)
            elif person1.gender != person2.gender:
                couple = StraightCouple(person1, person2)
            else:
                couple = GayCouple(person1, person2)
            return couple
        return Throuple(person1, person2, person3)


class CoupleCreator(CityCoupleCreator):
    """Adds print messages to city couple creator class."""

    @classmethod
    def display_new_relationship_message(cls, person, couple):
        second = next(p for p in couple.persons if p != person)
        if len(couple.persons) == 2:
            print("\n{} has started dating {}.\n".format(person, second))
        else:
            third = next(p for p in couple.persons if p != person and p != second)
            print("\n{} has started dating {} and {}.\n".format(
                person, second, third))
