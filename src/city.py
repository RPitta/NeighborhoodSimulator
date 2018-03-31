from handler import CityPregnancyHandler, CityPersonalHandler, CityAddictionHandler, CityDeathHandler, \
    CityDivorceHandler, CityMarriageHandler, CityLgbtaHandler
from traits import Traits


class City:
    """City class."""

    def __init__(self, generator, developer, couple_creator, names, relationship_developer, statistics,
                 foster_care_system):
        self.generator = generator
        self.person_developer = developer
        self.couple_creator = couple_creator
        self.names = names
        self.couple_developer = relationship_developer
        self.statistics = statistics
        self.foster = foster_care_system

        # City handlers
        self.personal_handler = CityPersonalHandler(
            self.person_developer)
        self.lgbta_handler = CityLgbtaHandler(self.names)
        self.addiction_handler = CityAddictionHandler(self.person_developer)
        self.pregnancy_handler = CityPregnancyHandler(
            self.generator, self.statistics, self.foster)
        self.marriage_handler = CityMarriageHandler()
        self.divorce_handler = CityDivorceHandler()
        self.death_handler = CityDeathHandler(self.person_developer)

        # Lists for couples and global population
        self.city_couples = []
        self.population = []

        # Populate city
        self.populate_city()

    @property
    def living_population(self):
        """Returns list of living city and neighborhood people."""
        return [p for p in self.population if p.is_alive]

    @property
    def living_outsiders(self):
        """Returns list of living city people."""
        return [p for p in self.living_population if p.is_neighbor is False]

    @property
    def dead_population(self):
        """Returns list of dead people."""
        return [p for p in self.population if not p.is_alive]

    @property
    def romanceable_outsiders(self):
        """Returns all city inhabitants that are dating and do not live in the neighborhood."""
        return [p for p in self.living_outsiders if p.is_romanceable]

    @property
    def population_surnames(self):
        """Returns a list of all surnames from living people."""
        return set([p.surname for p in self.living_population])

    # ACTIONS

    def populate_city(self):
        """Populate the city with X number of random children."""
        #for _ in (number + 1 for number in range(200)):
        for i in (number + 1 for number in range(2)):
            person = self.generator.create_first_child(Traits.CHILD.end, self.population_surnames)
            print(person.name+" is born")
            person.degree.init_degree(person.age)
            self.population.append(person)

    def time_jump_city(self):
        """Age up city population."""
        # Add / Remove children in foster care
        self.foster.check_foster_care_system(self.living_outsiders)
        if len(self.foster.children_up_for_adoption) < 3:
            self.populate_foster_care_system()

        self.do_person_action()
        self.do_couple_action()

    def populate_foster_care_system(self):
        """Adds a number of different-age children to foster care centre."""
        new_children = [self.generator.create_first_child(Traits.BABY.start, self.population_surnames)]
        new_children += [self.generator.create_first_child(Traits.CHILD.start, self.population_surnames)]
        new_children += [self.generator.create_first_child(Traits.TEEN.start, self.population_surnames)]
        for children in new_children :
            children.degree.init_degree(children.age)
        self.foster.add_to_system(new_children)
        self.population.extend(new_children)

    def do_person_action(self):
        """Personal actions for each person."""
        for person in self.living_outsiders:
            # Age up neighborhood
            self.personal_handler.age_up(person)

            if person.is_death_date:
                self.death_handler.die(person)
                # Remove from city couples if applicable
                self.remove_dead_and_brokenup_couples()
                continue

            # Come out if applicable
            if person.is_come_out_date:
                self.lgbta_handler.come_out(person)

            # Become an addict if applicable
            if person.is_addiction_date:
                self.addiction_handler.become_an_addict(person)

            # Recover from addiction if applicable
            if person.is_rehabilitation_date:
                self.addiction_handler.get_sober(person)

            # Relapse if applicable
            if person.is_relapse_date:
                self.addiction_handler.relapse(person)

            # Get into a committed relationship if applicable
            if person.is_romanceable:
                # Create new couple if successful match
                couple = self.couple_creator.create_couple(person, self.romanceable_outsiders)
                if couple is not False:
                    # Set couple traits
                    self.couple_developer.set_new_couples_goals(couple)
                    # Set new love date for polys
                    self.person_developer.set_new_love_date_for_polys(couple)
                    # Add couple to city couples list
                    self.city_couples.append(couple)

    def do_couple_action(self):
        """Couple actions for each couple."""
        for couple in self.city_couples:
            # Birth
            if couple.is_birth_date and couple.is_pregnant:
                self.population.extend(self.pregnancy_handler.give_birth(couple))
                self.pregnancy_handler.reset_pregnancy(couple)
                # New pregnancy date
                if couple.will_have_children:
                    self.couple_developer.set_new_pregnancy_or_adoption_process_date(couple)

            # Adoption
            if couple.is_adoption_date:
                self.population.extend(self.pregnancy_handler.adopt(couple))
                self.pregnancy_handler.reset_adoption(couple)
                # New adoption date
                if couple.will_have_children:
                    self.couple_developer.set_new_pregnancy_or_adoption_process_date(couple)

            # Marriage
            if couple.is_marriage_date and couple.will_get_married:
                self.marriage_handler.get_married(couple)

            # Pregnancy
            if couple.is_pregnancy_date and couple.will_get_pregnant:
                self.pregnancy_handler.get_pregnant(couple)

            # Adoption process
            if couple.is_adoption_process_date and couple.will_adopt:
                self.pregnancy_handler.start_adoption_process(couple)

            # Breakup
            if couple.is_breakup_date and couple.will_breakup:
                self.divorce_handler.get_divorced(couple) if couple.is_married else self.divorce_handler.get_separated(couple)
                # New love dates
                for person in couple.persons:
                    self.person_developer.set_new_love_date(person)
                # Remove from city couples
                self.remove_dead_and_brokenup_couples()

    def remove_dead_and_brokenup_couples(self):
        """Remove city couples that are dead, have broken up, or live in the neighborhood."""
        if len(self.city_couples) > 0:
            self.city_couples = [couple for couple in self.city_couples if all(
                p.is_alive and p.is_partnered and not p.is_neighbor for p in couple.persons)]
