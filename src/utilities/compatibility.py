import itertools


class Compatibility:
    """Determines compatibility for romantic relationships."""

    def are_compatible(self, person1, person2, person3=None):
        """Returns true if all persons are compatible to be in a relationship."""
        persons = [person1, person2] if person3 is None else [person1, person2, person3]

        return self.are_different_persons(persons) and \
               self.are_all_dating(persons) and \
               self.are_sexually_compatible(persons) and \
               self.are_age_compatible(persons) and \
               self.are_consanguinity_compatible(persons) and \
               self.are_compatible_if_minority(persons) and \
               self.are_not_ex(persons) and \
               self.are_throuple_compatible(persons) and \
               self.are_race_compatible(persons)

    @classmethod
    def are_different_persons(cls, persons):
        """Returns true if all persons are unique and not already set as each other's partners."""
        return all(p not in persons[0].partners for p in persons)

    @classmethod
    def are_all_dating(cls, persons):
        """Assumed all persons are romanceable, but check anyway."""
        return all(p.is_romanceable for p in persons)

    @classmethod
    def are_throuple_compatible(cls, persons):
        """Compatible if all or neither want throuple."""
        return all(p.in_love_as_throuple for p in persons) or all(p.in_love_as_throuple is False for p in persons)

    @classmethod
    def are_not_ex(cls, persons):
        """Compatible if not ex-partners / ex-spouses."""
        return all(persons[0] not in p.ex_partners and persons[0] not in p.ex_spouses for p in persons)

    @classmethod
    def are_compatible_if_minority(cls, persons):
        """Compatible if all are minorities or neither is minority, or minority+non-minority if liberal."""
        if all(p.is_minority is False for p in persons) or all(p.is_minority for p in persons):
            return True
        return any(p.is_liberal for p in persons)

    @classmethod
    def are_sexually_compatible(cls, persons):
        """Compatible if all persons are in each other's target genders."""
        pairs = list(itertools.permutations(persons, r=2))
        compatible_rate = 0
        for p in pairs:
            compatible_rate += int(p[0].gender in p[1].target_gender)
        return compatible_rate == len(pairs)

    @classmethod
    def are_consanguinity_compatible(cls, persons):
        """Compatible if all or neither want a consanguinamorous relationship and are/are not related."""
        if all(p.in_love_with_family for p in persons):
            pairs = list(itertools.permutations(persons, r=2))
            compatible_rate = 0
            for p in pairs:
                compatible_rate += int(p[0] in p[1].living_bio_family)
            return compatible_rate == len(pairs)

        return all(p.in_love_with_family is False for p in persons) and all(
            persons[0] not in p.living_bio_family for p in persons)

    @classmethod
    def are_age_compatible(cls, persons):
        """Compatible if all persons are within desired age range."""
        if all([p.in_love_with_intergenerational is None for p in persons]):
            return True

        pairs = list(itertools.permutations(persons, r=2))

        if all(p.in_love_with_intergenerational for p in persons):
            compatible_rate = 0
            for p in pairs:
                compatible_rate += int(abs(p[0].age - p[1].age) >= 20)
            return compatible_rate == len(pairs)

        compatible_rate = 0
        for p in pairs:
            compatible_rate += int(abs(p[0].age - p[1].age) < 20)
        return compatible_rate == len(pairs) and all(p.in_love_with_intergenerational is not True for p in persons)

    @classmethod
    def are_race_compatible(cls, persons):
        """Compatible if all persons are desired race."""
        if all([p.in_love_with_another_race is None for p in persons]):
            return True
        if all(p.in_love_with_another_race is False for p in persons):
            return all(persons[0].race == p.race for p in persons)
        if all(p.in_love_with_another_race in [True, None] for p in persons):
            pairs = list(itertools.permutations(persons, r=2))
            compatible_rate = 0
            for p in pairs:
                compatible_rate += int(p[0].race != p[1].race)
            return compatible_rate == len(pairs)
        return False
