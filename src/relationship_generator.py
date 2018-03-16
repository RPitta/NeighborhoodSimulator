from relationship import Relationship
from straight_relationship import StraightRelationship
from throuple import Throuple


class RelationshipGenerator:

    def __init__(self, traits, compatibility, randomizer, statistics, relationship_developer):
        self.traits = traits
        self.compatibility = compatibility
        self.randomizer = randomizer
        self.statistics = statistics
        self.relationship_developer = relationship_developer

    def get_new_couple(self, person, romanceable_outsiders):

        candidates = self.get_candidates_list(person, romanceable_outsiders)

        if not self.there_are_candidates(candidates):
            return False

        found_person = self.get_random_candidate(candidates)

        self.set_as_partner(person, found_person)
        self.update_relationship_status(
            self.traits.COMMITTED, person, found_person)
        self.display_new_relationship_message(person)

        return self.create_new_relationship(person, found_person)

    def get_candidates_list(self, person, romanceable_outsiders):
        return [candidate for candidate in self.get_compatible_candidates(person, romanceable_outsiders)]

    def get_compatible_candidates(self, person, romanceable_outsiders):
        """Returns list of compatible persons."""
        return [candidate for candidate in romanceable_outsiders if self.compatibility.are_compatible(person, candidate)]

    def there_are_candidates(self, candidates):
        return candidates is not None and len(candidates) > 0

    def get_random_candidate(self, candidates):
        """Returns a random compatible person."""
        return self.randomizer.get_random_list_item(candidates)

    def set_as_partner(self, person, found_person):
        if person.is_mono:
            person.partner = found_person
        else:
            person.partners.append(found_person)

        if found_person.is_mono:
            found_person.partner = person
        else:
            found_person.partners.append(person)

    def update_relationship_status(self, status, person, person2=None, person3=None):

        person.relationship_status = status

        if person2 is not None:
            person2.relationship_status = status
        if person3 is not None:
            person3.relationship_status = status

    def create_new_relationship(self, person1, person2, person3=None):

        if person3 is None:

            if person1.gender != person2.gender:
                new_couple = StraightRelationship(person1, person2)
            else:
                new_couple = Relationship(person1, person2)

            new_couple = self.relationship_developer.set_new_couple_traits(new_couple)

        else:
            new_thruple = Throuple(person1, person2, person3)
            return new_thruple

        return new_couple         


    def display_new_relationship_message(self, person):
        print("\n{} has started dating {}.\n".format(
            person.name, person.partner.name))
