import itertools


class Compatibility:

    def are_compatible(self, person1, person2, person3=None):
        if person3 is None:
            persons = [person1, person2]
        else:
            persons = [person1, person2, person3]
        return self.are_different_persons(persons) and self.are_all_dating(persons) and self.are_sexually_compatible(persons) and \
            self.are_age_compatible(persons) and self.are_consanguinity_compatible(persons) and \
            self.are_compatible_if_minority(persons) and self.are_not_ex(
                persons) and self.are_throuple_compatible(persons)

    def are_different_persons(self, persons):
        if all(persons[0] == person for person in persons):
            return False
        if any(persons[0].partner == person for person in persons):
            return False
        if any(persons[0].spouse == person for person in persons):
            return False
        if any(persons[0] in person.partners for person in persons):
            return False
        return True

    def are_all_dating(self, persons):
        """Assumed all persons are romanceable, but check anyway."""
        return all(p.is_romanceable for p in persons)

    def are_sexually_compatible(self, persons):
        if len(persons) == 2:
            if persons[0].gender in persons[1].target_gender and \
                    persons[1].gender in persons[0].target_gender:
                return True
        else:
            if persons[0].gender in persons[1].target_gender and \
                    persons[0].gender in persons[2].target_gender and \
                    persons[1].gender in persons[0].target_gender and \
                    persons[1].gender in persons[2].target_gender and \
                    persons[2].gender in persons[0].target_gender and \
                    persons[2].gender in persons[1].target_gender:
                return True
        return False

    def are_age_compatible(self, persons):

        # If consang, skip age compatibility
        if all([persons[0].in_love_with_family for person in persons]):
            return True

        # Intergenerational+intergenerational = compatible
        if all([persons[0].in_love_with_intergenerational for person in persons]):
            if len(persons) == 2:
                return abs(persons[0].age - persons[1].age) >= 20
            else:
                return abs(persons[0].age - persons[1].age) >= 20 and abs(persons[0].age - persons[2].age) >= 20 and abs(persons[1].age - persons[2].age) >= 20

        # Intergenerational+NotIntergenerational = not compatible
        if any([persons[0].in_love_with_intergenerational for person in persons]):
            return False

        # NotIntergenerational+NotIntergenerational = compatible
        if len(persons) == 2:
            if persons[0].in_love_with_intergenerational or persons[1].in_love_with_intergenerational:
                return False
            else:
                return abs(persons[0].age - persons[1].age) < 20
        else:
            if persons[0].in_love_with_intergenerational or persons[1].in_love_with_intergenerational or persons[2].in_love_with_intergenerational:
                return False
            else:
                return abs(persons[0].age - persons[1].age) < 20 and abs(persons[0].age - persons[2].age) < 20 and abs(persons[1].age - persons[2].age) < 20

    def are_consanguinity_compatible(self, persons):

        # Consang+consang = compatible if family
        if all(persons[0].in_love_with_family for person in persons):
            if len(persons) == 2:
                if persons[0] in persons[1].living_bio_family:
                    return True
                else:
                    return False
            else:
                if persons[0] in persons[1].living_bio_family and persons[0] in persons[2].living_bio_family:
                    return True
                else:
                    return False
            return True

        # Consang+Noconsang = not compatible
        if any(persons[0].in_love_with_family for person in persons):
            return False

        # Noconsang+Noconsang = compatible if not family
        return all(persons[0] not in person.living_bio_family for person in persons)

    def are_throuple_compatible(self, persons):
        # If all want throuple = compatible
        if all(persons[0].in_love_as_throuple for person in persons):
            return True
        # If none want throuple = compatible
        if all(persons[0].in_love_as_throuple is False for person in persons):
            return True
        # If throuple-with+no throuple-wish = not compatible
        return False

    def are_not_ex(self, persons):
        # If expartners = not compatible
        if any(persons[0] in person.ex_partners for person in persons):
            return False
        # If exspouses = not compatible
        if any(persons[0] in person.ex_spouses for person in persons):
            return False
        return True

    def are_compatible_if_minority(self, persons):
        # If none is minority = compatible
        if all(persons[0].is_minority is False for person in persons):
            return True
        # If all are minority = compatible
        if all(persons[0].is_minority for person in persons):
            return True
        # If minority+liberal = compatible
        if any(persons[0].is_liberal for person in persons):
            return True
        # If minority+conservative = not compatible
        return False
