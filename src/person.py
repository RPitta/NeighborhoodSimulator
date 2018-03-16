
from utilities.randomizer import Randomizer
from traits import Traits, LifeStages

class Person(Traits, LifeStages):
    def __init__(self, gender, stage, gender_identity, sexual_orientation, relationship_orientation):

            # Age-related -> Will be overriden
            self.stage = stage
            self.age = self.stage.start

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
            self.relationship_status = None
            self.is_pregnant = False
            self.in_adoption_process = False

            # Family
            self.parents = []
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
            self.can_have_bio_children = None # Depends on gender identity, sexual orientation, age and love target
            self.is_liberal = None
            self.wants_children = None # Depends on liberalism
            self.wants_domestic_partnership = None # Depends on liberalism
            self.in_love_with_family = None # Depends on wants_domestic_partnership and if person has family. Initialized false because of is_minority()
            self.in_love_with_intergenerational = None # Depends on wants_domestic_partnership
            self.in_love_date = False # Depends on wants_domestic_partnership
            self.wants_marriage = None # Depends on wants_domestic_partnership
            self.marriage_date = None # Depends on wants_marriage and is set in Relationship.py
            self.pregnancy_date = None # Depends on wants_children and is set in Relationship.py
            self.adoption_date = None
            self.breakup_date = None # Depends on wants_domestic_partnership and is set in Relationship.py
            
            self.occupation = None
            self.employment = None

            self.death_date = None
            self.death_cause = None # Depends on death_date

    # READ ONLY PROPERTIES

    # Will be overriden

    # READ ONLY GLOBAL PERSON PROPERTIES

    def __str__(self):
        return self.fullname

    @property
    def span_left(self):
        return range(self.age + 1, self.stage.end)

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
    def is_of_age(self):
        return self.age >= self.YOUNGADULT.start

    @property
    def is_minority(self):
        """Returns true if person is not cis-straight, mono or is/was in love with a family member."""
        return self.sexual_orientation != self.HETEROSEXUAL or \
            self.gender_identity == self.TRANSGENDER or \
            self.relationship_orientation == self.POLYAMOROUS or \
            self.in_love_with_family

    @property
    def is_single(self):
        return self.relationship_status == self.SINGLE

    @property
    def is_committed(self):
        return self.relationship_status == self.COMMITTED
    
    @property
    def is_married(self):
        return self.relationship_status == self.MARRIED

    @property
    def is_free(self):
        return self.is_committed is False and self.is_married is False

    @property
    def is_romanceable(self):
        if self.is_mono:
            return self.is_of_age and self.age >= self.in_love_date and self.wants_domestic_partnership and self.is_free
        else:
            return self.is_of_age and self.age >= self.in_love_date and self.wants_domestic_partnership

    @property
    def is_death_date(self):
        return self.death_date == self.age

    @property
    def can_and_wants_children(self):
        return self.can_have_bio_children and self.wants_children

    @property
    def cant_but_wants_children(self):
        return self.can_have_bio_children is False and self.wants_children

    @property
    def family(self):
        family_2d_list = [self.parents, self.children, self.grandparents, self.grandchildren, self.siblings, self.half_siblings, self.cousins, self.parents_siblings, self.siblings_children, [self.partner], self.partners, [self.spouse]]
        family_2d_filtered_list = list(filter(any, family_2d_list))
        return [family_member for family_1d_list in family_2d_filtered_list for family_member in family_1d_list]

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

    # READ/WRITE ATTRIBUTES

    # Set liberalism to true if in love with family/intergenerational
    @property
    def in_love_with_family(self):
        return self._in_love_with_family

    @in_love_with_family.setter
    def in_love_with_family(self, is_in_love):
        self._in_love_with_family = is_in_love

        # If in love with family, automatically become liberal
        if self._in_love_with_family:
            self.is_liberal = True

    @property
    def in_love_with_intergenerational(self):
        return self._in_love_with_intergenerational

    @in_love_with_intergenerational.setter
    def in_love_with_intergenerational(self, is_in_love):
        self._in_love_with_intergenerational = is_in_love

        # If in love with intergenerational, automatically become liberal
        if self._in_love_with_intergenerational:
            self.is_liberal = True

    # METHODS

    # FAMILY NAMES

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