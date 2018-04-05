# -*- coding: utf-8 -*-

from household import Household
from utilities.randomizer import Randomizer
from handler import AddictionHandler, PersonalHandler, DeathHandler, DivorceHandler, MarriageHandler, PregnancyHandler, \
    LgbtaHandler, CareerHandler, ConditionsHandler


class Neighborhood:
    NEIGHBORHOOD_APARTMENTS = 10

    def __init__(self, names, baby_generator, person_developer, couple_creator, couple_developer, statistics,
                 foster_care_system):
        self.households = []
        self.neighbors = []
        self.neighbor_couples = []

        # Essential classes
        self.names = names
        self.person_developer = person_developer
        self.couple_creator = couple_creator
        self.couple_developer = couple_developer

        # Handler classes
        self.randomizer = Randomizer()
        self.death_handler = DeathHandler(self.person_developer)
        self.marriage_handler = MarriageHandler()
        self.divorce_handler = DivorceHandler()
        self.personal_handler = PersonalHandler(self.person_developer)
        self.lgbta_handler = LgbtaHandler(self.names, self.person_developer)
        self.addiction_handler = AddictionHandler(self.person_developer)
        self.pregnancy_handler = PregnancyHandler(baby_generator, statistics, foster_care_system)
        self.career_handler = CareerHandler(statistics)
        self.conditions_handler = ConditionsHandler()

        # Automatically create given number of apartments/households
        self.create_households()

    @property
    def all_households_members_lists(self):
        """Returns all members from all households."""
        return [members for h in self.households for members in h.members_list]

    def create_households(self):
        """Creates X number of households and adds them to list of households."""
        for i, _ in enumerate(range(self.NEIGHBORHOOD_APARTMENTS), 1):
            household = Household(i)
            self.households.append(household)

    def populate_neighborhood(self, city_population, city_couples):
        """Populate the neighborhood with X number of city inhabitants.
        Each person and their family are added to each household and to neighbors list."""
        self.choose_first_neighbors(city_population, city_couples)
        self.add_neighbors_families()
        self.neighborhood_validation()

    def choose_first_neighbors(self, city_population, city_couples):
        """Add first new random neighbors to each available apartment."""
        for i in range(len(self.households)):
            h = self.households[i]

            done = False
            while not done:
                invalid = False
                # Choose a random living person
                chosen_person = self.randomizer.get_random_item(
                    city_population)

                # Check that the person isn't already a neighbor, and that they are of age
                if chosen_person in self.neighbors or not chosen_person.is_of_age:
                    invalid = True

                # Check that the person isn't a relative from another neighbor
                for n in self.neighbors:
                    if chosen_person in n.partners or chosen_person in n.living_family or chosen_person in n.living_inlaws_family:
                        invalid = True

                if not invalid:
                    # If not, add it to neighbors list and to household's members list
                    self.add_to_neighbors_and_household(h, chosen_person)
                    # Add as couple if applicable
                    for couple in city_couples:
                        if chosen_person in couple.persons:
                            self.neighbor_couples.append(couple)
                    done = True

    # ADD EACH NEIGHBOR'S FAMILIES

    def add_neighbors_families(self):
        """Add each neighbor's families to the household if any."""
        for household in self.households:
            p = household.members[0]
            self.add_partners(p, household)
            self.add_children(p, household)
            if p.is_single_and_unemployed_adult:
                self.add_parents(p, household)
                self.add_siblings(p, household)

    def add_children(self, p, household):
        """Add underage or unemployed single children."""
        for child in p.children:
            self.add_child(p, child, household)
        for child in p.adoptive_children:
            self.add_child(p, child, household)
        for child in p.step_children:
            self.add_child(p, child, household)

    def add_child(self, p, child, household):
        """Helper method to add person's bio or adoptive children."""
        if child.is_alive and child not in household.members:
            if child.is_single_and_unemployed_adult or not child.is_of_age:
                self.add_to_neighbors_and_household(household, child)

    def add_partners(self, p, household):
        """Add spouse or 1 partner if unmarried"""
        for spouse in p.spouses:
            self.add_to_neighbors_and_household(household, spouse)
        if len(p.spouses) == 0 and len(p.partners) > 0:
            self.add_to_neighbors_and_household(household, p.partners[0])

    def add_parents(self, p, household):
        """Add parent 1 and their partner(s)."""
        if len(p.adoptive_parents) > 0 and p.adoptive_parents[0].is_alive:
            self.add_parent_to_household(p.adoptive_parents[0], household)
        elif len(p.parents) > 0 and p.parents[0].is_alive:
            self.add_parent_to_household(p.parents[0], household)

    def add_parent_to_household(self, parent1, household):
        """Helper method to add parents to household."""
        self.add_to_neighbors_and_household(household, parent1)
        for parent in parent1.partners:
            self.add_to_neighbors_and_household(household, parent)

    def add_siblings(self, p, household):
        """Add single and unemployed siblings or underage siblings (included adoptive, half and step-siblings)."""
        for sibling in p.siblings:
            if sibling not in household.members and (
                    sibling.is_single_and_unemployed_adult or not sibling.is_of_age):
                self.add_to_neighbors_and_household(household, sibling)

    def add_to_neighbors_and_household(self, household, person):
        """Helper method to add each neighbor to the household and neighbors list."""
        household.add_member(person)
        self.neighbors.append(person)


    # DISPLAY HOUSEHOLDS

    def display_households(self):
        """Display each household's basic info of its members."""
        for household in self.households:
            household.display()

    # TIME JUMP

    def time_jump_neighborhood(self, romanceable_outsiders):
        """Age up neighborhood."""
        self.do_person_action(romanceable_outsiders)
        self.do_couple_action()

    def do_person_action(self, romanceable_outsiders):
        """Personal actions for each person."""
        for person in self.neighbors:
            # Age up neighborhood
            self.personal_handler.age_up(person)

            # Die
            if person.is_death_date:
                self.death_handler.die(person)
                # Remove from household and neighborhood
                self.remove_from_household(person)
                self.remove_from_neighborhood(person)
                # Remove from neighborhood couples if applicable
                self.remove_dead_and_brokenup_couples()
                continue

            self.career_handler.check_employment_and_education_status(person)

            if person.is_autism_date:
                self.conditions_handler.get_autism_diagnostic(person)

            # Move in to new household if applicable
            if person.is_move_in_date:
                new_apartment_id = self.personal_handler.move_in(person)
                self.determine_new_household(person, new_apartment_id)

            # Start school if applicable
            if person.is_school_start_date:
                self.career_handler.start_school(person)

            # Come out if applicable
            if person.is_come_out_date:
                self.lgbta_handler.come_out(person)

            # Get thrown out of the household / neighborhood
            if person.is_thrown_out_date:
                new_apartment_id = self.lgbta_handler.get_thrown_out(person)
                self.determine_new_household(person, new_apartment_id)

            # Move out of the household / neighborhood
            if person.is_move_out_date:
                new_apartment_id = self.lgbta_handler.move_out(person)
                self.determine_new_household(person, new_apartment_id)

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
                couple = self.couple_creator.create_couple(person, romanceable_outsiders)
                if couple is not False:
                    self.couple_creator.display_new_relationship_message(person, couple)
                    # Set couple traits
                    self.couple_developer.set_new_couples_goals(couple)
                    # Set new love date for polys
                    self.person_developer.set_new_love_date_for_polys(couple)
                    # Add couple to couples list
                    self.neighbor_couples.append(couple)

    def do_couple_action(self):
        """Couple actions for each couple."""
        for couple in self.neighbor_couples:
            # Birth
            if couple.is_birth_date and couple.is_pregnant and couple.expecting_num_of_children >= 1:
                new_babies = self.pregnancy_handler.give_birth(couple)
                self.handle_new_babies(new_babies, couple)

            # Adoption
            if couple.is_adoption_date:
                children = self.pregnancy_handler.adopt(couple)
                self.handle_new_babies(children, couple)

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
                if couple.is_married:
                    self.divorce_handler.get_divorced(couple)
                else:
                    self.divorce_handler.get_separated(couple)
                # One person in couple will leave household / neighborhood
                d = self.divorce_handler.leave_household(couple)
                self.determine_new_household(d["person"], d["id"])
                # New love dates
                for person in couple.persons:
                    self.person_developer.set_new_love_date(person)
                # Remove from neighborhood couples
                self.remove_dead_and_brokenup_couples()

    def determine_new_household(self, person, new_apartment_id=None):
        """Remove person from household and may add them to new household or move out of neighborhood."""
        self.remove_from_household(person)
        if new_apartment_id is None:
            self.remove_from_neighborhood(person)
        else:
            new_household = next(h for h in self.households if h.apartment_id == new_apartment_id)
            new_household.add_member(person)
            # Add to neighbors list if not in it
            if person not in self.neighbors:
                self.neighbors.append(person)

    def remove_from_household(self, person):
        """Helper method to remove person from their household."""
        for h in self.households:
            if h.apartment_id == person.apartment_id:
                h.remove_member(person)

    def remove_from_neighborhood(self, person):
        """Helper method to remove person from the neighborhood."""
        self.neighbors = [n for n in self.neighbors if n != person]

    def handle_new_babies(self, new_babies, couple):
        # Add baby/babies to household and neighborhood
        household = [h for h in self.households if couple.person1.apartment_id == h.apartment_id]
        for baby in new_babies:
            self.add_to_neighbors_and_household(household[0], baby)
        # Reset vars
        if couple.is_pregnant:
            self.pregnancy_handler.reset_pregnancy(couple)
        elif couple.is_in_adoption_process:
            self.pregnancy_handler.reset_adoption(couple)
        # New pregnancy / adoption date
        if couple.will_have_children:
            self.couple_developer.set_new_pregnancy_or_adoption_process_date(couple)

    def remove_dead_and_brokenup_couples(self):
        if len(self.neighbor_couples) > 0:
            self.neighbor_couples = [c for c in self.neighbor_couples if
                                     all(p.is_alive and p.is_partnered for p in c.persons)]

    def neighborhood_validation(self):
        """Error handling."""
        # Individual household validation
        for household in self.households:
            household.household_validation()
        # Neighborhood validation
        if len(self.neighbors) == 0:
            raise Exception("There are no neighbors.")
        if len(set(self.neighbor_couples)) != len(self.neighbor_couples):
            raise Exception("Neighbor couples list contains duplicates.")
        if len(set(self.neighbors)) != len(self.neighbors):
            raise Exception("Neighbor list contains duplicates.")
        if sum(len(h.members_list) for h in self.households) != len(self.neighbors):
            raise Exception("Number of neighbors is not the same as the sum of members of all households.")
        if any(n.apartment_id not in range(1, self.NEIGHBORHOOD_APARTMENTS + 1) for n in self.neighbors):
            raise Exception("Not all neighbors are assigned to an apartment ID.")
        if any(n not in self.all_households_members_lists for n in self.neighbors):
            raise Exception("Not all neighbors are members of a household.")
        if any(n.apartment_id == h.apartment_id and n not in h.members_list for h in self.households for n in
               self.neighbors):
            raise Exception(
                "Neighbor has an apartment ID assigned to them but is not a member of its household.")
        if any(n.is_neighbor is False for n in self.neighbors):
            raise Exception("Not all neighbors have neighbor status.")
