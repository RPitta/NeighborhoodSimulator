class Compatibility:

    def are_different_persons(self, person1, person2):
        if person1 == person2:
            return False
        if person1.partner == person2 or person2.partner == person1:
            return False
        return person1 not in person2.partners and person2 not in person1.partners
        
    def are_both_dating(self, person1, person2):
        return person1.is_romanceable and person2.is_romanceable

    def are_sexually_compatible(self, person1, person2):
        return person1.gender in person2.target_gender and person2.gender in person1.target_gender

    def are_age_compatible(self, person1, person2):
        if person1.in_love_with_intergenerational and person2.in_love_with_intergenerational:
            return person1.age not in person2.stage.span and person2.age not in person1.stage.span
        return person1.age in person2.stage.span and person2.age in person1.stage.span
        
    def are_consanguinity_compatible(self, person1, person2):
        if person1.in_love_with_family and person2.in_love_with_family:
            return person1 in person2.family and person2 in person1.family
        return person1 not in person2.family and person2 not in person1.family

    def are_compatible_if_minority(self, person1, person2):
        if not person1.is_minority and not person2.is_minority:
            return True
        if (person1.is_minority and person2.is_minority) or (person1.is_minority and person2.is_liberal) or (person2.is_minority and person1.is_liberal):
            return True
        return False

    def are_compatible(self, person1, person2):
        return self.are_different_persons(person1, person2) and self.are_both_dating(person1, person2) and self.are_sexually_compatible(person1, person2) and self.are_age_compatible(person1, person2) \
            and self.are_consanguinity_compatible(person1, person2) and self.are_compatible_if_minority(person1, person2)