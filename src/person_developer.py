
class PersonDeveloper:

    def __init__(self, names, professions, traits, life_stages, randomizer, statistics):
        self.statistics = statistics
        self.randomizer = randomizer
        self.professions = professions
        self.traits = traits
        self.stages = life_stages

    def yadult_traits(self, person):

        person.occupation = self.randomizer.get_random_list_item(self.professions.PROFESSIONS)
        person.employment = self.statistics.get_employment_chance(person)

        # First determine initial liberalism
        person.is_liberal = self.statistics.get_liberalism(person)

        # Check wish for romance
        person.wants_domestic_partnership = self.statistics.get_domestic_partnership_desire(person) # Depends on liberalism

        if person.wants_domestic_partnership:

            # Check if in love with family
            # If true, liberalism will automatically be set to true regardless of initial liberalism 
            person.in_love_with_family = self.statistics.get_family_love_chance(person) # Depends on wants_domestic_partnership.

            # Check if in love with intergenerational
            # If true, liberalism will automatically be set to true regardless of initial liberalism 
            person.in_love_with_intergenerational = self.statistics.get_intergenerational_chance(person) # Depends on wants_domestic_partnership and family love

            # If already in love with a family member, set love_date to their age. 
            # Otherwise, assign random age within reasonable _span.
            if person.in_love_with_family:
                person.in_love_date = person.age
            else:
                self.dateable_span = range(person.stage.start, 29)
                person.in_love_date = self.randomizer.get_random_list_item(self.dateable_span)

        return person

    def set_adult_traits(self, person):
        
        person.can_have_bio_children = False

    def set_senior_traits(self, person):

        person.employment = self.traits.UNEMPLOYED
        person.can_have_bio_children = False

        return person