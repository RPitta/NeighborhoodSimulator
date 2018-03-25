from handler import CityPregnancyHandler, CityPersonalHandler, CityAddictionHandler, CityDeathHandler, \
    CityDivorceHandler, CityMarriageHandler


class City:

    def __init__(self, generator, developer, couple_creator, stages, names, relationship_developer, statistics,
                 foster_care_system):
        self.generator = generator
        self.person_developer = developer
        self.couple_creator = couple_creator
        self.stages = stages
        self.names = names
        self.relationship_developer = relationship_developer
        self.statistics = statistics
        self.foster_care_system = foster_care_system

        self.personal_handler = CityPersonalHandler(
            self.names, self.person_developer)
        self.addiction_handler = CityAddictionHandler(self.person_developer)
        self.pregnancy_handler = CityPregnancyHandler(
            self.generator, self.statistics, self.foster_care_system)
        self.marriage_handler = CityMarriageHandler()
        self.divorce_handler = CityDivorceHandler()
        self.death_handler = CityDeathHandler()

        self.city_couples = []
        self.population = []

        # Populate city
        self.populate_city()

    @property
    def living_population(self):
        return [person for person in self.population if person.is_alive]

    @property
    def living_outsiders(self):
        return [person for person in self.living_population if person.is_neighbor is False]

    @property
    def dead_population(self):
        return [person for person in self.population if not person.is_alive]

    @property
    def population_surnames(self):
        return set([person.surname for person in self.living_population])

    @property
    def romanceable_outsiders(self):
        """Returns all city inhabitants that are dating and do not live in the neighborhood."""
        return [person for person in self.living_population if person.is_romanceable and person.is_neighbor is False]

    # ACTIONS

    def populate_city(self):
        """Populate the city with X number of random people.
        Starting at the Child stage so that they can be set with essential traits once they reach the teen stage."""
        for _ in (number + 1 for number in range(50)):
            person = self.generator.create_first_child(
                self.population_surnames)
            self.population.append(person)

    def time_jump_city(self):
        """Ages up city inhabitants."""

        self.do_person_action()

            # Remove dead couples
        self.remove_dead_and_brokenup_couples()

        for couple in self.city_couples:
            self.do_couple_action(couple)

        # Remove broken-up couples
        self.remove_dead_and_brokenup_couples()

    def remove_dead_and_brokenup_couples(self):
        """Remove city couples that are dead, have broken up, or live in the neighborhood."""
        if self.city_couples is not None and len(self.city_couples) > 0:
            self.city_couples = [couple for couple in self.city_couples if all(
                p.is_alive and (p.is_committed or p.is_married_or_remarried) and p.is_neighbor is False for p in
                couple.persons)]

    def do_person_action(self):
        """Personal actions for each person."""
        for person in self.living_outsiders:
            # Age up neighborhood
            person = self.personal_handler.age_up(person)
            if person.is_alive is False:
                continue

            # Add / Remove children in foster care
            self.foster_care_system.check_foster_care_system(self.living_outsiders)

            # Come out if applicable
            if person.is_come_out_date:
                person = self.personal_handler.come_out(person)

            # Become an addict if applicable
            if person.is_addiction_date:
                person = self.addiction_handler.become_an_addict(person)

            # Recover from addiction if applicable
            if person.is_rehabilitation_date:
                person = self.addiction_handler.get_sober(person)

            # Relapse if applicable
            if person.is_relapse_date:
                person = self.addiction_handler.relapse(person)

            # Get into a committed relationship if applicable
            if person.is_romanceable:
                # Create new couple if successful match
                couple = self.couple_creator.create_couple(
                    person, self.romanceable_outsiders)

                if couple is not False:
                    # Set couple traits
                    couple = self.relationship_developer.set_new_couple_traits(
                        couple)
                    # Set new love date for polys
                    couple = self.person_developer.set_new_love_date_for_polys(
                        couple)
                    # Add couple to couples list
                    self.city_couples.append(couple)

    def do_couple_action(self, couple):

        # Pregnancy handler first so that baby can be correctly linked to family.
        if couple.is_birth_date and couple.is_pregnant and couple.expecting_num_of_children >= 1:
            self.population.extend(self.pregnancy_handler.give_birth(couple))
            couple = self.pregnancy_handler.reset_pregnancy(couple)
            # New pregnancy date
            if couple.will_have_children:
                couple = self.relationship_developer.set_new_pregnancy_or_adoption_process_date(
                    couple)

        if couple.is_adoption_date:
            self.population.extend(self.pregnancy_handler.adopt(couple))
            couple = self.pregnancy_handler.reset_adoption(couple)
            # New adoption date
            if couple.will_have_children:
                couple = self.relationship_developer.set_new_pregnancy_or_adoption_process_date(
                    couple)

        if couple.is_marriage_date and couple.will_get_married:
            couple = self.marriage_handler.get_married(couple)

        if couple.is_pregnancy_date and couple.will_get_pregnant:
            couple = self.pregnancy_handler.get_pregnant(couple)

        if couple.is_adoption_process_date and couple.will_adopt:
            couple = self.pregnancy_handler.start_adoption_process(couple)

        if couple.is_breakup_date and couple.will_breakup:
            if couple.is_married:
                couple = self.divorce_handler.get_divorced(couple)
            else:
                couple = self.divorce_handler.get_separated(couple)
            for person in couple.persons:
                self.person_developer.set_love_traits(person)
