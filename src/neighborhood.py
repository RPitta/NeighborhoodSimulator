# -*- coding: utf-8 -*-

from household import Household
from utilities.randomizer import Randomizer


class Neighborhood:

    NEIGHBORHOOD_APARTMENTS = 10

    def __init__(self):
        self.randomizer = Randomizer()
        self.households = []
        self.neighbors = []

        # Create given number of apartments the building has
        self.create_apartments()

    def create_apartments(self):
        for i, _ in enumerate(range(self.NEIGHBORHOOD_APARTMENTS), 1):
            household = Household(i)
            self.households.append(household)

    def populate_neighborhood(self, city_population):
        """Populate the neighborhood with X number of city inhabitants."""
        for i in range(len(self.households)):
            # Create household with unique ID
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
                        done = True

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
                if p.mother is not None and p.mother.is_alive:
                    household.add_member(p.mother)
                    if p.father is not None:
                        if p.father.is_alive and (p.mother.spouse == p.father or p.mother.partner == p.father):
                            household.add_member(p.father)
                            self.neighbors.append(p.father)
                # If father is alive and mother is not, add father.
                elif p.father is not None and p.father.is_alive:
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
            for nephew_niece in p.siblings_children:
                if all(parent.is_alive is False for parent in nephew_niece.parents):
                    household.add_member(nephew_niece)
                    self.neighbors.append(nephew_niece)

    def display_households(self):
        for household in self.households:
            household.display()
