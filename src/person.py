from randomizer import Randomizer
from statistics import Statistics
from person_attributes import PersonAttributes


class Person(Statistics, PersonAttributes):

    def __init__(self, gender, life_stage, gender_identity, sexual_orientation, relationship_orientation):
        super(Person, self).__init__()
        
        self.family_id = None
        self.gender = gender
        self.age = self.AGES[life_stage]
        self.gender_identity = gender_identity
        self.sexual_orientation = sexual_orientation
        self.relationship_orientation = relationship_orientation

        # Attributes that (may) depend on other attributes
        self.name = None
        self.surname = None
        self.original_surname = None
        self.target_gender = []
        self.can_have_children = None
        self.is_liberal = None
        self.death_date = None
        self.death_cause = None
        self.occupation = None
        self.employment = None

        self.relationship_status = self.SINGLE
        self.wants_domestic_partnership = None
        self.wants_marriage = None

   
        self.in_love_with_family = None
        self.in_love_with_intergenerational = None

        self.is_alive = True
        self.is_pregnant = False

        # Family
        self.father = None
        self.mother = None
        self.parents = []
        self.siblings = []
        self.half_siblings = []
        self.parents_siblings = []
        self.siblings_children = []
        self.cousins = []
        self.partner = None
        self.partners = []
        self.ex_partners = []
        self.children = []
        self.grandparents = []
        self.grandchildren = []

        self.wants_children = None


    @property
    def family(self):
        family = [self.parents, self.children, self.grandparents, self.grandchildren, self.siblings, self.half_siblings, self.cousins, self.parents_siblings, self.siblings_children, [self.partner]]
        family = list(filter(any, family))
        return [j for i in family for j in i]

    @property
    def surname(self):
        return self._surname

    @surname.setter
    def surname(self, surname):
        self._surname = surname

    @property
    def life_stage(self):
        for key, value in self.AGES.items():
            if self._age == value:
                return key

    @property
    def age(self):
        return self._age

    @age.setter
    def age(self, age):
        self._age = age
        
        if self.life_stage == self.YOUNG_ADULT:
            self.occupation = Randomizer().get_random_list_item(self.PROFESSIONS)
            self.employment = self.get_employment_chance(self)
            self.check_if_in_love()

        if self.life_stage == self.SENIOR:
            self.can_have_children = False
            self.employment = self.RETIRED

    @property
    def can_have_children(self):
        return self._can_have_children

    @can_have_children.setter
    def can_have_children(self, bool):
        self._can_have_children = bool

    @property
    def partner(self):
        return self._partner

    @partner.setter
    def partner(self, partner):
        self._partner = partner

        # If single person finds a new partner, automatically update relationship status to Committed
        if self._partner is not None and self._relationship_status == self.SINGLE:
            self._relationship_status = self.COMMITTED

    @property
    def relationship_status(self):
        return self._relationship_status

    @relationship_status.setter
    def relationship_status(self, status):
        self._relationship_status = status

        # If person is female and is married to a male, take male's surname
        if self.is_female and self._relationship_status == self.MARRIED and self.partner.gender == self.MALE:
            self._surname = self.partner.surname

        # If person is married to a same-gender person, 50/50 chance of who changes their name
        elif self._relationship_status == self.MARRIED:
            chosen = Randomizer().get_random_list_item(
                [self.surname, self.partner.surname])
            if self._surname == chosen:
                self.partner.surname = self._surname
            else:
                self._surname = self.partner.surname

    
    # READ ONLY

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
    def parents(self):
        return self._parents

    @parents.setter
    def parents(self, parents):
        self._parents = parents

        if self._parents is None or len(self._parents) == 0:
            return

        # MOTHER AND FATHER
        self.father = next(
            parent for parent in self._parents if parent.is_male)
        self.mother = next(
            parent for parent in self._parents if parent.is_female)
        self.father.children.append(self)
        self.mother.children.append(self)

        # FATHER'S SURNAME
        self._surname = self.father.surname
        self.original_surname = self._surname

        # SIBLINGS
        self.siblings = [
            child for child in self.father.children if child.mother == self.mother and child != self]
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
        self.half_siblings = [child for child in self.father.children if child.mother !=
                              self.mother] + [child for child in self.mother.children if child.father != self.father]
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
                self.cousins.extend(uncle_aunt.children)
            for cousin in self.cousins:
                cousin.cousins.append(self)

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
        return self.age >= self.AGES[self.YOUNG_ADULT]

    @property
    def is_free_and_willing_to_date(self):

        # If person is underage, automatically returns false
        # If mono, return true if they are single/divorced/widowed and want a committed relationship
        # If poly, return true if they want (a / another) committed relationship
        if self.is_mono:
            return self.is_of_age and self.wants_domestic_partnership and self.is_free
        else:
            return self.is_of_age and self.wants_domestic_partnership

    @property
    def is_free(self):
        return self.relationship_status != self.MARRIED and self.relationship_status != self.COMMITTED

    @property
    def can_and_wants_children(self):
        return self.can_have_children and self.wants_children

    @property
    def cant_but_wants_children(self):
        return self.can_have_children is False and self.wants_children

    @property
    def wants_children(self):
        return self._wants_children
    
    @wants_children.setter
    def wants_children(self, bool):
        self._wants_children = bool

        if self.children is not None and len(self.children) >= 4:
            self._wants_children = False

    # FAMILY
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

    # HELPER METHODS
    def get_names_list(self, lst):
        if lst is None or len(lst) == 0:
            return "None"
        return [person.name for person in lst]

    def get_single_name(self, person):
        if person is None:
            return "None"
        return person.name

    def age_up(self):

        if self.life_stage == self.SENIOR:
            return False
        
        self.age = self.age + 1

        return True

    # READ/WRITE ATTRIBUTES

    def check_if_in_love(self):

        if self.get_family_love_chance(self):
            self.in_love_with_family = True
            return
        if self.get_intergenerational_chance(self):
            self.in_love_with_intergenerational = True
            return
        return