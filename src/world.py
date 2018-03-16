from utilities.randomizer import Randomizer
from utilities.compatibility import Compatibility
from utilities.statistics import Statistics

from life_stage import Baby, Child, Teen, YoungAdult, Adult, Senior
from relationship import Relationship
from straight_relationship import StraightRelationship


class World:

    NEIGHBOORHOOD_APARTMENTS = 16
    NEIGHBOORHOOD_FAMILIES = NEIGHBOORHOOD_APARTMENTS
    FAMILY_IDS = NEIGHBOORHOOD_APARTMENTS

    def __init__(self, generator, developer, relationship_generator, traits, stages, statistics, randomizer, relationship_developer):
        self.generator = generator
        self.developer = developer
        self.relationship_generator = relationship_generator
        self.traits = traits
        self.stages = stages
        self.statistics = statistics
        self.randomizer = randomizer
        self.relationship_developer = relationship_developer

        self.couples = []
        self.thruples = []
        self.population = []
        self.populate_world()

    @property
    def population(self):
        return self._population

    @population.setter
    def population(self, persons):

        if persons is None:
            self._population = []

        else:
            self._population = persons
            if self.couples is not None:
                # Remove dead couples from couples list
                deceased = [
                    couple for couple in self.couples for person in couple.persons if not person.is_alive]

                if deceased is not None and len(deceased) > 0:
                    self.couples = [
                        couple for couple in self.couples if couple not in deceased]

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
        return [person for person in self.living_population if person.partner is not None]

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
        for _ in (number+1 for number in range(4)):
            self.population.append(self.generator.generate_straight_yadult(
                self.traits.MALE, self.population_surnames))
            self.population.append(self.generator.generate_straight_yadult(
                self.traits.FEMALE, self.population_surnames))

    def do_couple_action(self, couple):

        if couple.will_get_married and all([couple.persons[0].marriage_date == couple.persons[0].age for c in couple.persons]):
            self.get_married(couple)
            return
        if couple.will_get_pregnant and all([couple.persons[0].pregnancy_date == couple.persons[0].age for c in couple.persons]):
            self.get_pregnant(couple)
            return
        if couple.will_adopt and all([couple.persons[0].adoption_date == couple.persons[0].age for c in couple.persons]):
            self.start_adoption_process(couple)
            return
        if couple.is_pregnant:
            self.give_birth(couple)
            return
        if couple.in_adoption_process:
            self.adopt(couple)
        return

    def time_jump(self):

        for person in self.living_population:
            self.age_up(person)

        for person in self.living_population:
            if person.is_romanceable:
                new_relationship = self.relationship_generator.get_new_couple(
                    person, self.romanceable_outsiders)

                if new_relationship:
                    self.couples.append(new_relationship)

        for couple in self.couples:
            self.do_couple_action(couple)

        self.person_validation()
        self.couples_validation()

    def age_up(self, person):

        if self.is_stage_end(person):
            return
        else:
            person.age += 1

        self.die_if_reached_death_date(person)

    def is_stage_end(self, person):
        if person.age == person.stage.end:
            if self.reached_old_age(person):
                return True
            else:
                self.set_new_stage(person)
                return True
        return False

    def reached_old_age(self, person):
        if person.stage.next_stage is False:
            self.die(person)
            return True
        return False

    def set_new_stage(self, person):
        person.stage = person.stage.next_stage
        person.age = person.stage.start
        self.set_new_stage_traits(person)

    def set_new_stage_traits(self, person):
        if person.stage == self.stages.YOUNGADULT:
            person = self.developer.yadult_traits(person)
        if person.stage == self.stages.SENIOR:
            person = self.developer.senior_traits(person)

    def display_new_stage_message(self, person):
        print("\n{} is now a {}.\n".format(person.fullname, person.stage))

    def die_if_reached_death_date(self, person):
        # If reached death date, die
        if person.is_death_date:
            self.die(person)

    # DEATH
    def die(self, person):

        person.is_alive = False

        # Remove person from their partner(s) / spouse
        if person.partner is not None:
            person.partner.partner = None
        if person.partners is not None and len(person.partners) > 0:
            for partner in person.partners:
                partner.partners.remove(person)
        if person.spouse is not None:
            person.spouse.spouse = None
            person.spouse.relationship_status = self.traits.WIDOWED

        self.display_death_message(person)

    def display_death_message(self, person):
        if person.death_cause == self.traits.ILLNESS:
            print("\n{} has died of an illness.\n".format(person.fullname))
        if person.death_cause == self.traits.SUICIDE:
            print("\n{} has committed suicide.\n".format(person.fullname))
        if person.death_cause == self.traits.ACCIDENT:
            print("\n{} has died in a road accident.\n".format(person.fullname))
        if person.death_cause is False:
            print("\n{} has died of old age".format(person.fullname))


    # NOT IMPLEMENTED YET

    def populate_neighborhood(self):
        pass

    def give_birth(self, couple):

        new_babies = []
        for _ in range(couple.expecting_children):
            new_baby = self.generator.generate_baby(couple)
            new_babies.append(new_baby)

        # Print
        baby_names = [baby.name for baby in new_babies]
        print("{} and {} have given birth to {}.".format(
            couple.person1.name, couple.person2.name, baby_names))

        # Reset pregnancy variables
        couple.woman.is_pregnant = False
        couple.expecting_children = 0

        couple.desired_num_of_children -= couple.expecting_children
        
        if couple.desired_num_of_children > 0:
            self.relationship_developer.set_new_pregnancy_or_adoption_date(couple)

        # Update population
        self.population = self.population + new_babies

    def adopt(self, couple):

        new_babies = []
        for _ in range(couple.expecting_children):
            new_baby = self.generator.generate_baby(couple)
            new_babies.append(new_baby)

        # Print
        baby_names = [baby.name for baby in new_babies]
        print("{} and {} have adopted {}.".format(
            couple.person1.name, couple.person2.name, baby_names))

        # Reset adoption variables
        for person in couple.persons:
            person.in_adoption_process = False
        couple.desired_num_of_children -= couple.expecting_children
        couple.expecting_children = 0

        # Update population
        self.population = self.population + new_babies

    # Relationship generator

    def person_validation(self):

        for person in self.living_population:
            if person.is_romanceable and person not in self.romanceable_outsiders:
                raise Exception(
                    "Unexpected error occurred. Person is romanceable but they are not in romanceable persons list.")
            if person.children is not None and len(person.children) > (self.traits.NUM_OF_CHILDREN_PER_COUPLE + (self.traits.TRIPLETS - 1)):
                raise Exception(
                    "Unexpected error occurred. Person has a greater number of children than permitted (possibility of twins/triplets included)")
            if person.is_single and person.partner is not None:
                raise Exception(
                    "Unexpected error occurred. Person is single but has a partner.")
            if person.is_mono and (person.is_committed or person.is_married) and person.partner is None:
                raise Exception(
                    "Unexpected error occurred. Person is committed/married but has no partner.")
            if person.is_poly and (person.is_committed or person.is_married) and (person.partners is None or len(person.partners) <= 0):
                raise Exception(
                    "Unexpected error occurred. Person is committed/married but has no partners.")
            if person.age >= self.stages.YOUNGADULT.start and person.occupation is None:
                raise Exception(
                    "Unexpected error occurred. Adult person has no occupation.")            
        for person in self.romanceable_outsiders:
            if person.is_mono:
                if person.partner is not None or person.is_committed:
                    raise Exception(
                        "Unexpected error occurred. Person is not romanceable but is in romanceable persons list.")

    def couples_validation(self):

        for couple in self.couples:

            # Committed relationship
            if not all([couple.persons[0].wants_domestic_partnership for p in couple.persons]):
                raise Exception(
                    "Unexpected error occurred. Couple is together but not all want to.")
            if not all([couple.persons[0].in_love_date <= couple.persons[0].age for p in couple.persons]):
                raise Exception(
                    "Unexpected error occurred. Couple is together before each person has fallen in love.")
            if not couple.is_married:
                if not all([couple.persons[0].is_committed for p in couple.persons]):
                    raise Exception(
                        "Unexpected error occurred. Unmarried couple is not set as COMMITTED.")
                if not all([couple.persons[0].partner is not None for p in couple.persons]):
                    raise Exception(
                        "Unexpected error occurred. Unmarried couple has not assigned partner.")

            # Marriage
            if couple.will_get_married and couple.is_married:
                raise Exception(
                    "Unexpected error occurred. Couple cannot wish to get married if they already are.")

            if couple.will_get_married:
                if couple.will_get_married and (couple.person1.marriage_date is None or couple.person2.marriage_date is None):
                    raise Exception(
                        "Unexpected error occurred. Marriage dates are null.")
                if couple.will_get_married and not couple.is_married:
                    if couple.person1.marriage_date < couple.person1.age or couple.person2.marriage_date < couple.person2.age:
                        raise Exception(
                            "Unexpected error occurred. Couple's marriage date is set in the past.")
                if couple.person1.marriage_date is not None:
                    if couple.person1.marriage_date > self.stages.SENIOR.end or \
                            couple.person2.marriage_date > self.stages.SENIOR.end:
                        raise Exception(
                            "Unexpected error occurred. Marriage dates are greater than old age.")
                    if abs(couple.person1.age-couple.person2.age) != abs(couple.person1.marriage_date-couple.person2.marriage_date):
                        raise Exception(
                            "Unexpected error occurred. Marriage dates do not match.")

            if couple.is_married:
                if couple.person1.surname != couple.person2.surname:
                    raise Exception(
                        "Unexpected error occurred. Married couple does not have the same surname.")
                if not all([couple.persons[0].is_married for p in couple.persons]):
                    raise Exception(
                        "Unexpected error occurred. Unmarried couple is not set as COMMITTED.")
                if not all([couple.persons[0].spouse is not None for p in couple.persons]):
                    raise Exception(
                        "Unexpected error occurred. Unmarried couple has not assigned spouse.")

            # Breakup
            if couple.will_breakup and (couple.person1.breakup_date is None or couple.person2.breakup_date is None):
                raise Exception(
                    "Unexpected error occurred. Breakup dates are null.")
            if couple.person1.breakup_date is not None:
                if couple.person1.breakup_date > self.stages.SENIOR.end or \
                        couple.person2.breakup_date > self.stages.SENIOR.end:
                    raise Exception(
                        "Unexpected error occurred. Breakup dates are greater than old age.")

            # Children
            if couple.desired_num_of_children > self.traits.NUM_OF_CHILDREN_PER_COUPLE:
                raise Exception(
                    "Unexpected error occurred. Couple's desired number of children is greater than permitted.")
            if couple.expecting_children < 0 or couple.expecting_children > self.traits.ALLOWED_NUM_OF_CHILDREN:
                raise Exception(
                    "Unexpected error occurred. Couple's expecting number of children is greater than permitted or a negative number.")
            if (couple.is_pregnant or couple.in_adoption_process) and (couple.desired_num_of_children <= 0 or couple.common_children > self.traits.NUM_OF_CHILDREN_PER_COUPLE):
                raise Exception(
                    "Unexpected error occurred. Couple is pregnant or in adoption process when it shouldn't be.")
            if couple.will_get_married and (couple.is_pregnant or couple.in_adoption_process):
                raise Exception(
                    "Unexpected error occurred. Couple is pregnant or in adoption process when they haven't married yet.")

    def get_pregnant(self, couple):
        """Set pregnancy to True and assign number of expecting children"""
        couple.expecting_children = self.statistics.get_pregnancy_num_of_children(couple)
        couple.woman.is_pregnant = True

        self.print_expecting_num_of_children(couple)

    # UI

    def print_expecting_num_of_children(self, couple):
        if couple.expecting_children not in self.traits.ALLOWED_NUM_OF_CHILDREN:
            raise Exception(
                "Unexpected error occurred. Wrong number of expecting children.")

        if couple.expecting_children == self.traits.SINGLETON:
            print("{} and {} are pregnant with a child!".format(
                couple.man.name, couple.woman.name))
        elif couple.expecting_children == self.traits.TWINS:
            print("{} and {} are pregnant with twins!".format(
                couple.man.name, couple.woman.name))
        elif couple.expecting_children == self.traits.TRIPLETS:
            print("{} and {} are pregnant with triplets!".format(
                couple.man.name, couple.woman.name))
        else:
            raise Exception(
                "Unexpected error occurred. Wrong number of expecting children.")

    def get_married(self, couple):

        # Replace "committed" with "married".
        # This will automatically set true "is married" and false "will get married"
        for person in couple.persons:
            person.relationship_status = self.traits.MARRIED
            self.replace_partner_with_spouse(person)

        # Set the same surname
        self.assign_surname(couple)

        print("\n{} and {} have married. Their surname is now {}.\n".format(
            couple.person1.name, couple.person2.name, couple.person1.surname))

    def replace_partner_with_spouse(self, person):
        person.spouse = person.partner
        person.partner = None

    def assign_surname(self, couple):

        # If person is female and is married to a male, take male's surname. Else, 50/50 chance.
        if couple.is_straight:
            couple.woman.surname = couple.man.surname
        else:
            chosen = Randomizer().get_random_list_item(
                [couple.person1.surname, couple.person2.surname])
            couple.person1.surname = chosen
            couple.person2.surname = chosen

    def start_adoption_process(self, couple):

        couple.expecting_children = self.statistics.get_adoption_num_of_children(
            couple)
        couple.print_expecting_num_of_adoptions()

        for person in couple.persons:
            person.in_adoption_process = True

    def print_expecting_num_of_adoptions(self, couple):
        if couple.expecting_children not in self.traits.ALLOWED_NUM_OF_ADOPTIONS:
            raise Exception(
                "Unexpected error occurred. Wrong number of expecting children.")

        if couple.expecting_children == self.traits.ONE_CHILD:
            print("{} and {} are going to adopt a child!".format(
                couple.person1.name, couple.person2.name))
        elif couple.expecting_children == self.traits.TWO_CHILDREN:
            print("{} and {} are going to adopt two children!".format(
                couple.person1.name, couple.person2.name))
        else:
            raise Exception(
                "Unexpected error occurred. Wrong number of expecting children.")
