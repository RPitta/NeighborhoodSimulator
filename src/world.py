from handler import *
from utilities.randomizer import Randomizer
from household import Household


class World:

    NEIGHBOORHOOD_APARTMENTS = 10
    NEIGHBOORHOOD_FAMILIES = NEIGHBOORHOOD_APARTMENTS
    FAMILY_IDS = NEIGHBOORHOOD_APARTMENTS

    def __init__(self, generator, developer, couple_creator, stages, relationship_developer, statistics):
        self.generator = generator
        self.person_developer = developer
        self.couple_creator = couple_creator
        self.stages = stages
        self.relationship_developer = relationship_developer
        self.statistics = statistics
        self.randomizer = Randomizer()

        self.personal_handler = PersonalHandler(
            self.statistics, self.person_developer)
        self.pregnancy_handler = PregnancyHandler(
            self.generator, self.statistics)

        self.marriage_handler = MarriageHandler()
        self.divorce_handler = DivorceHandler()
        self.death_handler = DeathHandler()

        self.couples = []
        self.population = []
        self.neighbors = []
        self.households = []
        self.populate_world()

    @property
    def living_population(self):
        return [person for person in self.population if person.is_alive]

    @property
    def dead_population(self):
        return [person for person in self.population if not person.is_alive]

    @property
    def population_surnames(self):
        return set([person.surname for person in self.living_population])

    @property
    def romanceable_outsiders(self):
        return [person for person in self.living_population if person.is_romanceable]

    @property
    def unromanceable_outsiders(self):
        return [person for person in self.living_population if person.is_romanceable is False]

    @property
    def partnered_outsiders(self):
        return [person for person in self.living_population if person.partner is not None or person.spouse is not None or len(person.partners) > 0]

    def get_population(self):

        for person in self.population:
            yield "ID: {}\nName: {}\nSurname: {}\nGender: {}\nGender identity: {}\nSexual orientation: {}\nLife stage: {}\nAge: {}\nFather: {}\nMother: {}\nSiblings: {}\nGrandparents: {}\nUncles: {}\nAunts: {}\nCousins: {}\nPartner: {}\nChildren: {}\nNephews: {}\nNieces: {}\nRelationship Status: {}\nPregnant: {}\nCan have children: {}\nWants children: {}\nProfession: {}\nEmployment: {}\n".format(
                person.family_id,
                person.name,
                person.surname,
                person.gender,
                person.gender_identity,
                person.sexual_orientation,
                person.stage,
                person.age,
                person.father,
                person.mother,
                person.get_siblings_names(),
                person.get_grandparents_names(),
                person.get_uncles_names(),
                person.get_aunts_names(),
                person.get_cousins_names(),
                person.partner,
                person.get_childrens_names(),
                person.get_nephews_names(),
                person.get_nieces_names(),
                person.relationship_status,
                person.is_pregnant,
                person.can_have_bio_children,
                person.wants_children,
                person.occupation,
                person.employment
            )

    # ACTIONS

    def populate_world(self):

        for _ in (number+1 for number in range(200)):
            person = self.generator.create_first_child(
                self.population_surnames)
            self.population.append(person)

    def time_jump(self):

        for person in self.living_population:
            person = self.personal_handler.age_up(person)

            if person.is_come_out_date:
                person = self.personal_handler.come_out(person)

            if person.is_romanceable:
                # Create new couple if successful match
                couple = self.couple_creator.create_couple(
                    person, self.romanceable_outsiders)

                if couple is False:
                    pass
                else:
                    # Else, set couple traits
                    couple = self.relationship_developer.set_new_couple_traits(
                        couple)
                    # Set new love date for polys
                    couple = self.person_developer.set_new_love_date_for_polys(
                        couple)
                    # Add couple to couples list
                    self.couples.append(couple)

        # Remove dead couples
        self.remove_dead_and_brokenup_couples()

        for couple in self.couples:
            self.do_couple_action(couple)

        # Remove broken-up couples
        self.remove_dead_and_brokenup_couples()

    def remove_dead_and_brokenup_couples(self):
        if self.couples is not None and len(self.couples) > 0:
            self.couples = [couple for couple in self.couples if all(
                p.is_alive and (p.is_committed or p.is_married_or_remarried) for p in couple.persons)]

    def do_couple_action(self, couple):

        # Pregnancy handler first so that baby can be correctly linked to family.
        if couple.is_birth_date and couple.is_pregnant and couple.expecting_num_of_children >= 1:
            self.population.extend(self.pregnancy_handler.give_birth(couple))
            couple = self.pregnancy_handler.reset_pregnancy(couple)

            if couple.will_have_children:
                couple = self.relationship_developer.set_new_pregnancy_or_adoption_process_date(
                    couple)

        if couple.is_adoption_date:
            self.population.extend(self.pregnancy_handler.adopt(couple))
            couple = self.pregnancy_handler.reset_adoption(couple)
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
                person = self.person_developer.set_love_traits(person)

    # NOT IMPLEMENTED YET

    def populate_neighborhood(self):
        for i, apartment in enumerate(range(self.NEIGHBOORHOOD_APARTMENTS), 1):
            # Create household with unique ID
            h = Household(i)
            self.households.append(h)

            done = False
            while not done:
                # Choose a random living person
                chosen_person = self.randomizer.get_random_item(
                    self.living_population)

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
                if p.mother.is_alive:
                    household.add_member(p.mother)
                    if p.father.is_alive and (p.mother.spouse == p.father or p.mother.partner == p.father):
                        household.add_member(p.father)
                        self.neighbors.append(p.father)
                # If father is alive and mother is not, add father.
                elif p.father.is_alive:
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
            print("\n***** " + str(household.apartment_id) + " ********\n")
            for person in household.members:
                desc = "\nApartmment ID: {}\nName: {}\nSurname: {}\nGender: {}\nAge: {}\nSocial Class: {}\nCivil Status: {}\nProfession: {}\nEmployment: {}".format(
                    household.apartment_id,
                    person.name,
                    person.surname,
                    person.gender,
                    person.age,
                    person.social_class,
                    person.relationship_status,
                    person.occupation,
                    person.employment
                )
                if person.partner in household.members:
                    desc += "\nPartner: {}".format(person.partner)
                if person.spouse in household.members:
                    desc += "\nSpouse: {}".format(person.spouse)
                if len(person.partners) == 1 and person.spouse is None:
                    desc += "\nPartner: {}".format(person.partners[0])
                for child in person.children:
                    if child in household.members:
                        desc += "\nChild: {}".format(child)
                if person.father in household.members:
                    desc += "\nFather: {}".format(person.father)
                if person.mother in household.members:
                    desc += "\nMother: {}".format(person.mother)
                for sibling in person.siblings:
                    if sibling in household.members:
                        desc += "\nSibling: {}".format(sibling)
                for half_sibling in person.half_siblings:
                    if half_sibling in household.members:
                        desc += "\nHalf-Sibling: {}".format(half_sibling)
                for grandchild in person.grandchildren:
                    if grandchild in household.members:
                        desc += "\nGrandchild: {}".format(grandchild)
                for nephew in person.nephews:
                    if nephew in household.members:
                        desc += "\nUncle: {}".format(nephew)
                for niece in person.nieces:
                    if niece in household.members:
                        desc += "\nUncle: {}".format(niece)
                yield desc
