# -*- coding: utf-8 -*-

from household import Household
from utilities.randomizer import Randomizer
from handler import AddictionHandler, PersonalHandler, DeathHandler, DivorceHandler, MarriageHandler, PregnancyHandler


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
        self.death_handler = DeathHandler()
        self.marriage_handler = MarriageHandler()
        self.divorce_handler = DivorceHandler()
        self.personal_handler = PersonalHandler(names, person_developer)
        self.addiction_handler = AddictionHandler(person_developer)
        self.pregnancy_handler = PregnancyHandler(baby_generator, statistics, foster_care_system)

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
        self.set_neighbor_status()
        self.neighborhood_validation()

    def choose_first_neighbors(self, city_population, city_couples):
        """Add first new random neighbors to each available apartment."""
        for i in range(len(self.households)):
            h = self.households[i]

            done = False
            while not done:
                # Choose a random living person
                chosen_person = self.randomizer.get_random_item(
                    city_population)

                # Check that the person isn't already a neighbor, and that they are of age
                if chosen_person in self.neighbors or not chosen_person.is_of_age:
                    continue

                # Check that the person isn't a relative from another neighbor
                for neighbor in self.neighbors:
                    if chosen_person in neighbor.partners or chosen_person in neighbor.living_bio_family or chosen_person in neighbor.living_inlaws_family:
                        continue

                # If not, add it to neighbors list and to household's members list
                self.add_to_neighbors_and_household(h, chosen_person)
                done = True

                # Add as couple if applicable
                for couple in city_couples:
                    if chosen_person in couple.persons:
                        self.neighbor_couples.append(couple)

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
            if p.is_female and (child.is_single_and_unemployed_adult or not child.is_of_age):
                self.add_to_neighbors_and_household(household, child)
            elif p.is_male and (child.is_single_and_unemployed_adult or not child.is_of_age):
                if not child.mother.is_alive or child.mother in p.partners:
                    self.add_to_neighbors_and_household(household, child)

    def add_partners(self, p, household):
        """Add spouse or 1 partner if unmarried"""
        for spouse in p.spouses:
            self.add_to_neighbors_and_household(household, spouse)
        if len(p.partners) > 0 and p.partners[0] not in p.spouses and p.partners[0] not in household.members:
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
        person.apartment_id = household.apartment_id
        self.neighbors.append(person)
        household.add_member(person)

    # NEIGHBOR STATUS

    def set_neighbor_status(self):
        """Set neighbor status to True for each neighbor."""
        for neighbor in self.neighbors:
            neighbor.is_neighbor = True

    # DISPLAY HOUSEHOLDS

    def display_households(self):
        """Display each household's basic info of its members."""
        for household in self.households:
            household.display()

    # TIME JUMP

    def time_jump_neighborhood(self, romanceable_outsiders):
        """Main function: age up neighborhood."""
        self.do_person_action(romanceable_outsiders)

        # Remove dead couples
        self.remove_dead_and_brokenup_couples()

        for couple in self.neighbor_couples:
            self.do_couple_action(couple)

        # Set neighbor status for newborns
        self.set_neighbor_status()

        # Remove broken-up couples
        self.remove_dead_and_brokenup_couples()

    def do_person_action(self, romanceable_outsiders):
        """Personal actions for each person."""
        for person in self.neighbors:
            # Age up neighborhood
            person = self.personal_handler.age_up(person)
            if not person.is_alive:
                continue

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
                    person, romanceable_outsiders)

                if couple is not False:
                    # Set couple traits
                    couple = self.couple_developer.set_new_couple_traits(
                        couple)
                    # Set new love date for polys
                    couple = self.person_developer.set_new_love_date_for_polys(
                        couple)
                    # Add couple to couples list
                    self.neighbor_couples.append(couple)

    def do_couple_action(self, couple):
        """Couple actions for each couple."""
        # Pregnancy handler first so that baby can be correctly linked to family.
        if couple.is_birth_date and couple.is_pregnant and couple.expecting_num_of_children >= 1:
            new_babies = self.pregnancy_handler.give_birth(couple)
            household = next(h for h in self.households if new_babies[0].apartment_id == h.apartment_id)
            for baby in new_babies:
                self.add_to_neighbors_and_household(household, baby)
            couple = self.pregnancy_handler.reset_pregnancy(couple)

            if couple.will_have_children:
                couple = self.couple_developer.set_new_pregnancy_or_adoption_process_date(
                    couple)

        if couple.is_adoption_date:
            children = self.pregnancy_handler.adopt(couple)
            household = next([h for h in self.households if children[0].apartment_id == h.apartment_id])
            for child in children:
                self.add_to_neighbors_and_household(household, child)
            couple = self.pregnancy_handler.reset_adoption(couple)

            if couple.will_have_children:
                couple = self.couple_developer.set_new_pregnancy_or_adoption_process_date(
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
                person = self.person_developer.set_love_traits(person)

    def remove_dead_and_brokenup_couples(self):
        if self.neighbor_couples is not None and len(self.neighbor_couples) > 0:
            self.neighbor_couples = [couple for couple in self.neighbor_couples if all(
                p.is_alive and (p.is_committed or p.is_married_or_remarried) for p in couple.persons)]

    # VALIDATION

    def neighborhood_validation(self):
        # Individual household validation
        for household in self.households:
            household.household_validation()
        # Neighborhood validation
        if len(self.neighbors) == 0:
            raise Exception("There are no neighbors.")
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
