
class RelationshipDeveloper:

    def __init__(self, randomizer, statistics):
        self.randomizer = randomizer
        self.statistics = statistics

    def set_new_couple_traits(self, couple):

        # If couple wants to get married, set random (within the next X-Y years) marriage date to each person
        if couple.will_get_married:
            self.set_marriage_date(couple)

        # Statistical break up chance
        couple.will_breakup = self.statistics.get_breakup_chance(couple)

        # If couple will break up, set break-up date to each person
        if couple.will_breakup:
            self.set_breakup_date(couple)

        # If couple will have children, set number of desired children and first child pregnancy/adoption date
        if couple.will_have_children:
            
            # Statistical chance of desired number of children
            couple.desired_num_of_children = self.statistics.get_desired_num_of_children(couple)
        
            self.set_new_pregnancy_or_adoption_date(couple)
            
        return couple

    def set_marriage_date(self, couple):
        self.years_left_before_marriage = self.randomizer.get_random_list_item(range(1, 5))

        couple.person1.marriage_date = couple.person1.age + self.years_left_before_marriage
        couple.person2.marriage_date = couple.person2.age + self.years_left_before_marriage

    def set_breakup_date(self, couple):
        date = self.statistics.get_oldest_breakup_date(couple)

        couple.oldest.breakup_date = date
        for person in couple.persons:
            if person != couple.oldest:
                person.breakup_date = date - abs(couple.oldest.age - couple.youngest.age)

    def set_new_pregnancy_or_adoption_date(self, couple):
        date = self.statistics.get_oldest_pregnancy_date(couple)

        if couple.will_get_pregnant:
            couple.oldest.pregnancy_date = date
            for person in couple.persons:
                if person != couple.oldest:
                    person.pregnancy_date = date - abs(couple.oldest.age - couple.youngest.age)
        elif couple.will_adopt:
            couple.oldest.adoption_date = date
            for person in couple.persons:
                if person != couple.oldest:
                    person.adoption_date = date - abs(couple.oldest.age - couple.youngest.age)   

