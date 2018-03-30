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
        return self.get_new_relationship(person, candidates)

    def get_candidates_list(self, person, romanceables):
        """Returns list of compatible individuals or pairs."""
        if person.in_love_as_throuple is False:
            return [candidate for candidate in romanceables if self.compatibility.are_compatible(person, candidate)]
        pairs = list(combinations(romanceables, 2))
        pair_candidates = []
        for romanceable in pairs:
            if self.compatibility.are_compatible(person, romanceable[0], romanceable[1]):
                pair_candidates.extend([[romanceable[0], romanceable[1]]])
        return pair_candidates

    def get_new_relationship(self, person, candidates):
        """Returns new relationship."""
        found_person2 = None
        if person.in_love_as_throuple:
            found_persons = self.get_random_candidate(candidates)
            found_person1 = found_persons[0]
            found_person2 = found_persons[1]
        else:
            found_person1 = self.get_random_candidate(candidates)
        self.configure_relationship(person, found_person1, found_person2)
        return self.create_new_relationship(person, found_person1, found_person2)

    def configure_relationship(self, person, found_person1, found_person2):
        """Assign partners, update relationship status and social class."""
        lst = [person, found_person1] if found_person2 is None else [person, found_person1, found_person2]
        self.set_as_partner(lst)
        self.update_relationship_status_to_committed(lst)
        self.set_shared_social_class(lst)

    @classmethod
    def there_are_candidates(cls, candidates):
        """Checks if there is at least one candidate."""
        return candidates is not None and len(candidates) >= 1

    def get_random_candidate(self, candidates):
        """Returns one random item from list of candidates."""
        return self.randomizer.get_random_item(candidates)

    @classmethod
    def set_as_partner(cls, lst):
        """Add each person to their partners list."""
        for person in lst:
            person.partners += [partner for partner in lst if partner != person]

    @classmethod
    def set_shared_social_class(cls, lst):
        """Set the same social class for all persons."""
        highest_social_class = next(p.social_class for p in lst if p.social_class.rank == max([p.social_class.rank for p in lst]))
        for person in lst:
            person.social_class = highest_social_class

    @classmethod
    def update_relationship_status_to_committed(cls, lst):
        """Change status from single to committed."""
        for person in lst:
            if person is not None and not person.is_married_or_remarried:
                person.relationship_status = Traits.COMMITTED

    @classmethod
    def create_new_relationship(cls, person1, person2, person3=None):
        """Create new relationship."""
        if person3 is not None:
            return Throuple(person1, person2, person3)
        if person1 in person2.living_bio_family:
            return ConsangCouple(person1, person2)
        if person1.gender != person2.gender:
            return StraightCouple(person1, person2)
        return GayCouple(person1, person2)


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
