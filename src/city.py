from handler import PregnancyHandler, PersonalHandler, AddictionHandler, DeathHandler, DivorceHandler, MarriageHandler, \
    LgbtaHandler, CareerHandler
from traits import Traits


class City:
    """City base class."""

    def __init__(self, generator, developer, couple_creator, names, couple_developer, statistics,
                 foster_care_system):
        self.baby_generator = generator
        self.person_developer = developer
        self.couple_creator = couple_creator
        self.names = names
        self.couple_developer = couple_developer
        self.statistics = statistics
        self.foster = foster_care_system

        # City handlers
        self.personal_handler = PersonalHandler(self.person_developer)
        self.lgbta_handler = LgbtaHandler(self.names, self.person_developer)
        self.addiction_handler = AddictionHandler(self.person_developer)
        self.pregnancy_handler = PregnancyHandler(self.baby_generator, self.statistics, self.foster)
        self.marriage_handler = MarriageHandler()
        self.divorce_handler = DivorceHandler()
        self.death_handler = DeathHandler(self.person_developer)
        self.career_handler = CareerHandler(statistics)

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
        for _ in (number + 1 for number in range(400)):
            person = self.baby_generator.create_first_child(Traits.BABY.end, self.population_surnames)
            self.population.append(person)

    def time_jump_city(self, neighborhood=None):
        """Age up city population."""
        # Add / Remove children in foster care
        self.foster.check_foster_care_system(self.living_outsiders)
        if len(self.foster.children_up_for_adoption) < 7:
            self.populate_foster_care_system()

        self.do_household_action(neighborhood)
        self.do_person_action(neighborhood)
        self.do_couple_action()

    def populate_foster_care_system(self):
        """Adds a number of different-age children to foster care centre."""
        new_children = [self.baby_generator.create_first_child(Traits.BABY.start, self.population_surnames)]
        new_children += [self.baby_generator.create_first_child(Traits.CHILD.start, self.population_surnames)]
        new_children += [self.baby_generator.create_first_child(Traits.TEEN.start, self.population_surnames)]
        new_children += [self.baby_generator.create_first_child(Traits.BABY.start, self.population_surnames)]
        new_children += [self.baby_generator.create_first_child(Traits.BABY.end, self.population_surnames)]
        new_children += [self.baby_generator.create_first_child(Traits.CHILD.end, self.population_surnames)]
        # Assign education
        for child in new_children:
            child.education.init_degree(child)
        # Add to foster care centre and city population
        self.foster.add_to_system(new_children)
        self.population.extend(new_children)

    def do_household_action(self, neighborhood):
        """Action for each household"""
        if neighborhood is None:
            return
        for household in neighborhood.households:
            if household.household_income == 0:
                if household.finance_status == household.SAFE:
                    household.finance_status = household.BROKE
                elif household.finance_status == household.BROKE:
                    household.finance_status = household.HOMELESS
                    if self.statistics.willing_to_move_outside():
                        household.set_living_outside()
            else:
                household.finance_status = household.SAFE
                if (not household.is_neighbor and self.statistics.willing_to_move_back()):
                    household.set_living_inside()

    def do_person_action(self, neighborhood):
        """Personal actions for each person."""
        for person in self.living_outsiders:
            # Age up neighborhood
            self.personal_handler.age_up(person)

            if person.is_death_date:
                self.death_handler.die(person)
                # Remove from city couples if applicable
                self.remove_dead_and_brokenup_couples()
                continue

            # Advance career / job
            self.career_handler.check_employment_and_education_status(person)

            # Move in to neighborhood if applicable
            if person.is_move_in_date:
                new_apartment_id = self.personal_handler.move_in(person)
                neighborhood.determine_new_household(person, new_apartment_id)
                for child in person.underage_children:
                    neighborhood.determine_new_household(child, new_apartment_id)

            # Start school if applicable
            if person.is_school_start_date:
                self.career_handler.start_school(person)

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

            # Single adoption
            if person.is_single_adoption_process_date:
                self.pregnancy_handler.start_single_adoption_process(person)
            if person.is_single_adoption_date:
                self.population.extend(self.pregnancy_handler.adopt_as_single(person))

    def do_couple_action(self):
        """Couple actions for each couple."""
        for couple in self.city_couples:

            # Breakup
            if couple.is_breakup_date and couple.will_breakup:
                self.divorce_handler.get_divorced(couple) if couple.is_married else self.divorce_handler.get_separated(
                    couple)
                # New love dates
                for person in couple.persons:
                    self.person_developer.set_new_love_date(person)
                # Remove from city couples
                self.remove_dead_and_brokenup_couples()
                continue

            # Birth
            if couple.is_birth_date and couple.is_pregnant:
                self.population.extend(self.pregnancy_handler.give_birth(couple))
                self.pregnancy_handler.reset_pregnancy(couple)
                # New pregnancy date
                if couple.will_have_children:
                    self.couple_developer.set_new_pregnancy_or_adoption_process_date(couple)

            # Adoption
            if couple.is_adoption_date and couple.is_in_adoption_process:
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

    def remove_dead_and_brokenup_couples(self):
        """Remove city couples that are dead, have broken up, or live in the neighborhood."""
        if len(self.city_couples) > 0:
            self.city_couples = [couple for couple in self.city_couples if all(
                p.is_alive and p.is_partnered and not p.is_neighbor for p in couple.persons)]
