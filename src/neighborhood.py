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
                    if chosen_person in [neighbor.living_bio_family, neighbor.living_inlaws_family]:
                        continue

                # If not, add it to neighbors list and to household's members list
                self.add_to_neighbors_and_household(h, chosen_person)
                # Add as couple if applicable
                for couple in city_couples:
                    if chosen_person in couple.persons:
                        self.neighbor_couples.append(couple)
                done = True

    def add_neighbors_families(self):
        # Pick each chosen neighbor from each household and add their families to the household if it applies
        for household in self.households:
            p = household.members[0]
            # Partner or spouse, if mono / married-poly
            if p.partner is not None and p.partner not in household.members:
                self.add_to_neighbors_and_household(household, p.partner)
            elif p.spouse is not None and p.spouse not in household.members:
                self.add_to_neighbors_and_household(household, p.spouse)
            # 1 partner if unmarried poly
            elif len(p.partners) == 1 and p.spouse is None and p.partners[0] not in household.members:
                self.add_to_neighbors_and_household(household, p.partners[0])
            else:
                # If person has no partners/spouses, add other family members;
                # Add mother if alive. Add father only if alive and married/committed to mother.
                if p.mother and p.mother.is_alive and p.mother not in household.members:
                    self.add_to_neighbors_and_household(household, p.mother)
                    if p.father is not None and p.father not in household.members and p.father.is_alive and (
                            p.mother.spouse == p.father or p.mother.partner == p.father):
                        self.add_to_neighbors_and_household(household, p.father)
                # If father is alive and mother is not, add father.
                elif p.father and p.father.is_alive and p.father not in household.members:
                    self.add_to_neighbors_and_household(household, p.father)
                # Add single or underage siblings / half-siblings.
                for sibling in p.full_siblings:
                    if sibling not in household.members and (
                            sibling.is_single_and_unemployed_adult or not sibling.is_of_age):
                        self.add_to_neighbors_and_household(household, sibling)
                for half_sib in p.half_siblings:
                    if half_sib not in household.members and (
                            half_sib.is_single_and_unemployed_adult or not half_sib.is_of_age):
                        self.add_to_neighbors_and_household(household, half_sib)

            # Children
            for child in p.children:
                if not child.is_alive or child in household.members:
                    continue
                # Automatically add mother's underage and/or single and unemployed children
                if p.is_female and (child.is_single_and_unemployed_adult or not child.is_of_age):
                    self.add_to_neighbors_and_household(household, child)
                # Add father's children if mother is dead or he is still married/committed to their mother
                elif p.is_male and (
                        child.is_single_and_unemployed_adult or not child.is_of_age) and child not in household.members:
                    if not child.mother.is_alive or child.mother == p.spouse or child.mother == p.partner:
                        self.add_to_neighbors_and_household(household, child)
                    elif len(p.partners) == 1 and child.mother == p.partners[0]:
                        self.add_to_neighbors_and_household(household, child)
            # Add grandchildren and/or nephews/nieces if their parents are dead
            for grandchild in p.grandchildren:
                if grandchild not in household.members and all(
                        parent.is_alive is False for parent in grandchild.parents):
                    self.add_to_neighbors_and_household(household, grandchild)
            for nephew_niece in p.uncles:
                if nephew_niece not in household.members and all(
                        parent.is_alive is False for parent in nephew_niece.parents):
                    self.add_to_neighbors_and_household(household, nephew_niece)
            for nephew_niece in p.aunts:
                if nephew_niece not in household.members and all(
                        parent.is_alive is False for parent in nephew_niece.parents):
                    self.add_to_neighbors_and_household(household, nephew_niece)

    def add_to_neighbors_and_household(self, household, person):
        person.apartment_id = household.apartment_id
        self.neighbors.append(person)
        household.add_member(person)

    def set_neighbor_status(self):
        """Set neighbor status to True for each neighbor."""
        for neighbor in self.neighbors:
            neighbor.is_neighbor = True

    def display_households(self):
        """Display each household's basic info of its members."""
        for household in self.households:
            household.display()

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
            self.neighbors.extend(self.pregnancy_handler.give_birth(couple))
            couple = self.pregnancy_handler.reset_pregnancy(couple)

            if couple.will_have_children:
                couple = self.couple_developer.set_new_pregnancy_or_adoption_process_date(
                    couple)

        if couple.is_adoption_date:
            self.neighbors.extend(self.pregnancy_handler.adopt(couple))
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

    def neighborhood_validation(self):
        # Individual household validation
        for household in self.households:
            household.household_validation()
        # Neighborhood validation
        if len(self.neighbors) == 0:
            raise Exception("There are no neighbors.")
        if len(set(self.neighbors)) != len(self.neighbors):
            for n in self.neighbors:
                attrs = vars(n)
                print(', '.join("%s: %s" % item for item in attrs.items()))
                print()
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
