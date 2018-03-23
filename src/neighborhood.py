# -*- coding: utf-8 -*-

from household import Household
from utilities.randomizer import Randomizer
from handler import *


class Neighborhood:

    NEIGHBORHOOD_APARTMENTS = 10

    def __init__(self, baby_generator, person_developer, couple_creator, stages, couple_developer, statistics):
        self.households = []
        self.neighbors = []
        self.neighbor_couples = []

        # Handler classes
        self.randomizer = Randomizer()
        self.death_handler = DeathHandler()
        self.marriage_handler = MarriageHandler()
        self.divorce_handler = DivorceHandler()
        self.personal_handler = PersonalHandler(statistics, person_developer)
        self.pregnancy_handler = PregnancyHandler(baby_generator, statistics)

        # Essential classes
        self.person_developer = person_developer
        self.couple_creator = couple_creator
        self.couple_developer = couple_developer

        # Automatically create given number of apartments/households
        self.create_households()

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

    def choose_first_neighbors(self, city_population, city_couples):
        for i in range(len(self.households)):
            h = self.households[i]

            done = False
            while not done:
                # Choose a random living person
                chosen_person = self.randomizer.get_random_item(
                    city_population)

                # Check that the person isn't already a neighbor, and that they are of age
                if chosen_person not in self.neighbors and chosen_person.is_of_age:

                    # Check that the person isn't a relative from another neighbor
                    is_related = False
                    for neighbor in self.neighbors:
                        if chosen_person in neighbor.living_bio_family or chosen_person in neighbor.living_inlaws_family:
                            is_related = True

                    # If not, add it to neighbors list and to household's members list
                    if is_related is False:
                        self.neighbors.append(chosen_person)
                        h.add_member(chosen_person)
                        for couple in city_couples:
                            if chosen_person in couple.persons:
                                self.neighbor_couples.append(couple)
                        done = True

    def add_neighbors_families(self):
        # Pick each chosen neighbor from each household and add their families to the household if it applies
        for household in self.households:
            p = household.members_list[0]
            # Partner or spouse, if mono / married-poly
            if p.partner is not None:
                household.add_member(p.partner)
                self.neighbors.append(p.partner)
            elif p.spouse is not None:
                household.add_member(p.spouse)
                self.neighbors.append(p.spouse)
            # 1 partner if unmarried poly
            elif len(p.partners) == 1:
                if p.spouse is None:
                    household.add_member(p.partners[0])
                    self.neighbors.append(p.partners[0])
            else:
                # If person has no partners/spouses, add other family members;
                # Add mother if alive. Add father only if alive and married/committed to mother.
                if p.mother and p.mother.is_alive:
                    household.add_member(p.mother)
                    if p.father is not None:
                        if p.father.is_alive and (p.mother.spouse == p.father or p.mother.partner == p.father):
                            household.add_member(p.father)
                            self.neighbors.append(p.father)
                # If father is alive and mother is not, add father.
                elif p.father and p.father.is_alive:
                    household.add_member(p.father)
                    self.neighbors.append(p.father)
                # Add single or underage siblings / half-siblings.
                for sibling in p.siblings:
                    if sibling.is_single or sibling.is_of_age is False:
                        household.add_member(sibling)
                        self.neighbors.append(sibling)
                for half_sib in p.half_siblings:
                    if half_sib.is_single or half_sib.is_of_age is False:
                        household.add_member(half_sib)
                        self.neighbors.append(half_sib)

            # Children
            for child in p.children:
                if child.is_alive is False:
                    continue
                # Automatically add underage / single children if person is their mother
                if p.is_female and (child.is_of_age is False or child.is_single):
                    household.add_member(child)
                    self.neighbors.append(child)
                # If person is their father, add his children if mother is dead or he is still married/committed to their mother
                elif p.is_male and (child.is_of_age is False or child.is_single):
                    if child.mother.is_alive is False or child.mother == p.spouse or child.mother == p.partner:
                        household.add_member(child)
                        self.neighbors.append(child)
                    if len(p.partners) == 1:
                        if child.mother == p.partners[0]:
                            household.add_member(child)
                            self.neighbors.append(child)
            # Add grandchildren and/or nephews/nieces if their parents are dead
            for grandchild in p.grandchildren:
                if all(parent.is_alive is False for parent in grandchild.parents):
                    household.add_member(grandchild)
                    self.neighbors.append(grandchild)
            for nephew_niece in p.uncles:
                if all(parent.is_alive is False for parent in nephew_niece.parents):
                    household.add_member(nephew_niece)
                    self.neighbors.append(nephew_niece)
            for nephew_niece in p.aunts:
                if all(parent.is_alive is False for parent in nephew_niece.parents):
                    household.add_member(nephew_niece)
                    self.neighbors.append(nephew_niece)

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
        for person in self.neighbors:
            self.do_person_action(person, romanceable_outsiders)

        # Remove dead couples
        self.remove_dead_and_brokenup_couples()

        for couple in self.neighbor_couples:
            self.do_couple_action(couple)

        # Set neighbor status for newborns
        self.set_neighbor_status()

        # Remove broken-up couples
        self.remove_dead_and_brokenup_couples()

    def do_person_action(self, person, romanceable_outsiders):
        # Age up neighborhood
        person = self.personal_handler.age_up(person)

        # Come out if applicable
        if person.is_come_out_date:
            self.personal_handler.come_out(person)

        if person.is_romanceable:
            # Create new couple if successful match
            couple = self.couple_creator.create_couple(
                person, romanceable_outsiders)

            if couple is False:
                pass
            else:
                # Else, set couple traits
                couple = self.couple_developer.set_new_couple_traits(
                    couple)
                # Set new love date for polys
                couple = self.person_developer.set_new_love_date_for_polys(
                    couple)
                # Add couple to couples list
                self.neighbor_couples.append(couple)

    def do_couple_action(self, couple):

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
