from person_attributes import PersonAttributes
from randomizer import Randomizer
from statistics import Statistics
from life_stage import *

class Person(Statistics, PersonAttributes):

    def __init__(self, gender, life_stage, gender_identity, sexual_orientation, relationship_orientation):
        super(Person, self).__init__()

        # Names
        self.name = None # May depend on family
        self.surname = None
        self.original_surname = self.surname # Depends on surname

        # Basics
        self.family_id = None
        self.gender = gender
        self.gender_identity = gender_identity # Linked to gender
        self.sexual_orientation = sexual_orientation
        self.target_gender = [] # Linked to sexual_orientation
        self.relationship_orientation = relationship_orientation

        # Default: Alive, Single, Not Pregnant, Not in adoption process
        self.is_alive = True
        self.relationship_status = self.SINGLE
        self.is_pregnant = False
        self.in_adoption_process = False

        # Family
        self.parents = None
        self.father = None
        self.mother = None
        self.siblings = []
        self.half_siblings = []
        self.parents_siblings = []
        self.siblings_children = []
        self.cousins = []
        self.partner = None
        self.spouse = None
        self.ex_spouses = []
        self.partners = []
        self.ex_partners = []
        self.children = []
        self.grandparents = []
        self.grandchildren = []
        
        # Personality
        self.can_have_children = None # Depends on gender identity and sexual orientation
        self.wants_children = None
        self.is_liberal = None
        self.wants_domestic_partnership = None
        self.wants_marriage = None # Depends on wants_domestic_partnership
        
        self.occupation = None
        self.employment = None
        self.in_love_with_family = None
        self.in_love_with_intergenerational = None

        self.death_date = None
        self.death_cause = None # Depends on death_date
        self.will_die = None # Depends on death date and age

        # Age > Initialized last as it depends on above attributes
        self.life_stage = life_stage
        self.age = self.life_stage.start


    # READ ONLY PROPERTIES

    @property
    def fullname(self):
        return "{} {}".format(self.name, self.surname)

    @property
    def is_male(self):
        return self.gender == self.MALE

    @property
    def is_female(self):
        return self.gender == self.FEMALE

    @property
    def is_mono(self):
        return self.relationship_orientation == self.MONOAMOROUS

    @property
    def is_poly(self):
        return self.relationship_orientation == self.POLYAMOROUS

    @property
    def is_minority(self):
        """Returns true if person is not cis-straight, mono or is/was in love with a family member."""
        return self.sexual_orientation != self.HETEROSEXUAL or \
            self.gender_identity == self.TRANSGENDER or \
            self.relationship_orientation == self.POLYAMOROUS or \
            self.in_love_with_family

    @property
    def is_of_age(self):
        return self.life_stage.is_of_age

    @property
    def is_free(self):
        return self.relationship_status != self.MARRIED and self.relationship_status != self.COMMITTED

    @property
    def is_romanceable(self):
        if self.is_mono:
            return self.is_of_age and self.wants_domestic_partnership and self.is_free
        else:
            return self.is_of_age and self.wants_domestic_partnership

    @property
    def can_and_wants_children(self):
        return self.can_have_children and self.wants_children

    @property
    def cant_but_wants_children(self):
        return self.can_have_children is False and self.wants_children

    @property
    def family(self):
        family_2d_list = [self._parents, self.children, self.grandparents, self.grandchildren, self.siblings, self.half_siblings, self.cousins, self.parents_siblings, self.siblings_children, [self._partner], [self._partners], [self.spouse]]
        family_2d_list = list(filter(any, family_2d_list))
        return [family_member for family_1d_list in family_2d_list for family_member in family_1d_list]

    @property
    def uncles(self):
        return [uncle for uncle in self.parents_siblings if uncle.is_male]

    @property
    def aunts(self):
        return [aunt for aunt in self.parents_siblings if aunt.is_female]

    @property
    def nephews(self):
        return [nephew for nephew in self.siblings_children if nephew.is_male]

    @property
    def nieces(self):
        return [niece for niece in self.siblings_children if niece.is_female]

    @property
    def is_death_date(self):
        return self.death_date == self._age


    # READ/WRITE ATTRIBUTES

    @property
    def is_alive(self):
        return self._is_alive

    @is_alive.setter
    def is_alive(self, is_alive):
        self._is_alive = is_alive

        if not self._is_alive:

            # Remove self from their partner(s) / spouse
            if self._partner is not None:
                self._partner._partner = None
            if self._partners is not None and len(self._partners) > 0:
                for partner in self._partners:
                    partner._partners.remove(self)
            if self.spouse is not None:
                self.spouse.spouse = None 
                self.spouse._relationship_status = self.WIDOWED

    @property
    def age(self):
        return self._age

    @age.setter
    def age(self, age):
        self._age = age
        
        if self.life_stage == YoungAdult():
            self.occupation = Randomizer().get_random_list_item(self.PROFESSIONS)
            self.employment = self.get_employment_chance(self)
            self.check_if_in_love()

        if self.life_stage == Senior():
            self.can_have_children = False
            self.employment = self.RETIRED

    @property
    def parents(self):
        return self._parents

    @parents.setter
    def parents(self, parents):
        
        if parents is None:
            self._parents = []
        else:
            self._parents = parents
        
            # MOTHER AND FATHER
            self.father = next(
                parent for parent in self._parents if parent.is_male)
            self.mother = next(
                parent for parent in self._parents if parent.is_female)

            # Update parents' children. It may also update the property wants_children from children method.
            self.father._children.append(self)
            self.mother._children.append(self)
            self.father._children = self.father._children
            self.mother._children = self.mother._children

            # FATHER'S SURNAME
            self.surname = self.father.surname
            self.original_surname = self.surname

            # SIBLINGS
            self.siblings = [
                child for child in self.father._children if child.mother == self.mother and child != self]
            for sibling in self.siblings:
                sibling.siblings.append(self)

            # GRANDPARENTS

            if self.father._parents is not None:
                self.grandparents.extend(self.father._parents)
            if self.mother._parents is not None:
                self.grandparents.extend(self.mother._parents)
            for grandparent in self.grandparents:
                grandparent.grandchildren.append(self)

            # HALF-SIBLINGS
            self.half_siblings = [child for child in self.father._children if child.mother !=
                                self.mother] + [child for child in self.mother._children if child.father != self.father]
            for sibling in self.half_siblings:
                sibling.half_siblings.append(self)

            # UNCLES/AUNTS AND COUSINS
            if self.father.siblings is not None:
                self.parents_siblings.extend(self.father.siblings)
            if self.mother.siblings is not None:
                self.parents_siblings.extend(self.mother.siblings)
            if self.parents_siblings is not None:
                for uncle_aunt in self.parents_siblings:
                    uncle_aunt.siblings_children.append(self)
                    self.cousins.extend(uncle_aunt._children)
                for cousin in self.cousins:
                    cousin.cousins.append(self)

    @property
    def children(self):
        return self._children
    
    @children.setter
    def children(self, children):
        self._children = children

        if self._children is not None and len(self._children) >= 4:
            self.wants_children = False

    @property
    def partner(self):
        return self._partner

    @partner.setter
    def partner(self, partner):
        self._partner = partner

        # If mono person finds a new partner, automatically update relationship status to Committed
        if self._partner is not None and self._relationship_status == self.SINGLE:
            self._relationship_status = self.COMMITTED

    @property
    def relationship_status(self):
        return self._relationship_status

    @relationship_status.setter
    def relationship_status(self, status):
        self._relationship_status = status

        if self._relationship_status == self.MARRIED:
            
            # Assign spouse and remove partner
            self.spouse = self._partner
            self._partner = None

            # If person is female and is married to a male, take male's surname. Else, 50/50 chance.
            if self.is_female and self.spouse.gender == self.MALE:
                self.surname = self.spouse.surname
            else:
                chosen = Randomizer().get_random_list_item([self.surname, self.spouse.surname])
                if self.surname == chosen:
                    self.spouse.surname = self.surname
                else:
                    self.surname = self.spouse.surname

    @property
    def partners(self):
        return self._partners

    @partners.setter
    def partners(self, partners):
        self._partners = partners

        # If poly person is single and finds a new partner, automatically update relationship status to Committed
        if self._partners is not None and len(self._partners) > 0 and self._relationship_status == self.SINGLE:
            self._relationship_status = self.COMMITTED

    # METHODS

    # FAMILY NAMES
    def get_fathers_name(self):
        return self.get_single_name(self.father)

    def get_mothers_name(self):
        return self.get_single_name(self.mother)

    def get_partners_name(self):
        return self.get_single_name(self.partner)

    def get_nephews_names(self):
        return self.get_names_list(self.nephews)

    def get_nieces_names(self):
        return self.get_names_list(self.nieces)

    def get_aunts_names(self):
        return self.get_names_list(self.aunts)

    def get_uncles_names(self):
        return self.get_names_list(self.uncles)

    def get_siblings_names(self):
        return self.get_names_list(self.siblings)

    def get_childrens_names(self):
        return self.get_names_list(self.children)

    def get_cousins_names(self):
        return self.get_names_list(self.cousins)

    def get_grandparents_names(self):
        return self.get_names_list(self.grandparents)

    def get_names_list(self, lst):
        if lst is None or len(lst) == 0:
            return "None"
        return ', '.join(map(str, [person.name for person in lst])) 

    def get_single_name(self, person):
        if person is None:
            return "None"
        return person.name

    # ACTIONS

    def age_up(self):
        
        if self._age != self.life_stage.end:
            self._age = self._age + 1
        else:
            if self.life_stage.next_stage is False or self.is_death_date:
                self.die()
            else:
                self._age = self._age + 1
                self.life_stage = self.life_stage.next_stage
                print("{} is now a {}.".format(self.fullname, self.life_stage))

    def die(self):

        self.is_alive = False
        
        if self.death_cause == self.ILLNESS:
            print("\n{} {} has died of an illness.\n".format(self.name, self.surname))
        if self.death_cause == self.SUICIDE:
            print("\n{} {} has committed suicide.\n".format(self.name, self.surname))
        if self.death_cause == self.ACCIDENT:
            print("\n{} {} has died in a road accident.\n".format(self.name, self.surname))
        if self.death_cause is False:
            print("\n{} {} has died of old age".format(self.name, self.surname))

        return

    def check_if_in_love(self):

        if self.get_family_love_chance(self):
            self.in_love_with_family = True
            return
        if self.get_intergenerational_chance(self):
            self.in_love_with_intergenerational = True
            return
        return

    