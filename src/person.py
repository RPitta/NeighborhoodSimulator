
from person_attributes import PersonAttributes
from randomizer import Randomizer


class Person(PersonAttributes):

    def __init__(self, gender, life_stage, gender_identity, sexual_orientation, relationship_orientation):
        self.family_id = None
        self.gender = gender
        self.life_stage = life_stage
        self.age = None
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

        self.wants_domestic_partnership = None
        self.wants_marriage = None
        self.wants_children = None

        self.relationship_status = self.SINGLE
        self.loves_family_member = None

        self.is_alive = True
        self.is_pregnant = False

        # Family
        self.father = None
        self.mother = None

        self.uncles = []
        self.aunts = []
        self.nephews = []
        self.nieces = []
        self.cousins = []

        self.partner = None
        self.partners = []
        self.children = []

        self.grandparents = []
        self.grandchildren = []

        self.siblings = []
        self.half_siblings = []

    @property
    def surname(self):
        return self._surname

    @surname.setter
    def surname(self, surname):
        self._surname = surname

    @property
    def can_have_children(self):
        return self._can_have_children

    @can_have_children.setter
    def can_have_children(self, bool):
        self._can_have_children = bool


    # AGE
    
    @property
    def age(self):
        return self._age

    @age.setter
    def age(self, age):
        self._age = age

    @property
    def life_stage(self):
        return self._life_stage

    @life_stage.setter
    def life_stage(self, life_stage):
        """Automatically update age and children ability when life stage changes."""
        self._life_stage = life_stage
        self._age = self.AGES[self._life_stage]

        if self._life_stage == self.SENIOR:
            self.can_have_children = False

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
        if self.is_female() and self._relationship_status == self.MARRIED and self.partner.gender == self.MALE:
            self._surname = self.partner.surname

        # If person is married to a same-gender person, 50/50 chance of who changes their name
        elif self._relationship_status == self.MARRIED:
            chosen = Randomizer().get_random_list_item(
                [self.surname, self.partner.surname])
            if self._surname == chosen:
                self.partner.surname = self._surname
            else:
                self._surname = self.partner.surname

    @property
    def father(self):
        return self._father

    @property
    def mother(self):
        return self._mother

    @property
    def grandparents(self):
        return self._grandparents

    @property
    def siblings(self):
        return self._siblings

    @property
    def cousins(self):
        return self._cousins

    @property
    def uncles(self):
        return self._uncles

    @property
    def aunts(self):
        return self._aunts

    @property
    def nephews(self):
        return self._nephews

    @property
    def nieces(self):
        return self._nieces

    @property
    def children(self):
        return self._children

    @father.setter
    def father(self, father):
        self._father = father

        # If has father
        if self._father is not None:

            # Same surname as father
            self._surname = self._father.surname
            self.original_surname = self._surname

            # Grandparents and grandchildren on father's side
            if self._father._mother is not None:
                self._grandparents.append(self._father._mother)
                self._father._mother._grandchildren.append(self)
            if self._father._father is not None:
                self._grandparents.append(self._father._father)
                self._father._father._grandchildren.append(self)

            # Siblings
            for sibling in self._father.children:
                if sibling not in self._siblings:
                    self._siblings.append(sibling)
                if self not in sibling._siblings:
                    sibling._siblings.append(self)

            # Uncles and aunts, nephews and nieces on father's side
            if self._father._siblings is not None:
                for fathers_sibling in self._father.siblings:
                    if fathers_sibling.is_male() and fathers_sibling not in self._uncles:
                        self._uncles.append(fathers_sibling)
                    if self.is_male() and self not in fathers_sibling._nephews:
                        fathers_sibling._nephews.append(self)
                    if fathers_sibling.is_female() and fathers_sibling not in self._aunts:
                        self._aunts.append(fathers_sibling)
                    if self.is_female() and self not in fathers_sibling._nieces:
                        self._aunts._nieces.append(fathers_sibling)

            # Cousins on father's side
            for cousin in self._father.nephews:
                if cousin not in self._cousins:
                    self._cousins.append(cousin)
                if self not in cousin.self._cousins:
                    cousin._cousins.append(self)
            for cousin in self._father.nieces:
                if cousin not in self._cousins:
                    self._cousins.append(cousin)
                if self not in cousin.self._cousins:
                    cousin._cousins.append(self)

            # Child of Father
            self._father._children.append(self)

    @mother.setter
    def mother(self, mother):
        self._mother = mother

        # If has mother
        if self._mother is not None:

            # Grandparents on mother's side
            if self._mother.mother is not None:
                self._grandparents.append(self._mother.mother)
            if self._mother.father is not None:
                self._grandparents.append(self._mother.father)

            # Siblings
            for sibling in self._mother.children:
                if sibling not in self._siblings:
                    self._siblings.append(sibling)
                if self not in sibling._siblings:
                    sibling._siblings.append(self)

            # Uncles and aunts on mother's side
            if self._mother.siblings is not None:
                for mothers_sibling in self._mother.siblings:
                    if mothers_sibling.is_male() and mothers_sibling not in self.uncles:
                        self.uncles.append(mothers_sibling)
                    if mothers_sibling.is_female() and mothers_sibling not in self.aunts:
                        self.aunts.append(mothers_sibling)

            # Cousins on mother's side
            for cousin in self._mother.nephews:
                if cousin not in self._cousins:
                    self._cousins.append(cousin)
            for cousin in self._mother.nieces:
                if cousin not in self._cousins:
                    self._cousins.append(cousin)

            # Child of Mother
            self._mother._children.append(self)

    @grandparents.setter
    def grandparents(self, grandparents):
        self._grandparents = grandparents

    @nephews.setter
    def nephews(self, nephews):
        self._nephews = nephews

    @nieces.setter
    def nieces(self, nieces):
        self._nieces = nieces

    @siblings.setter
    def siblings(self, siblings):
        self._siblings = siblings

    @cousins.setter
    def cousins(self, cousins):
        self._cousins = cousins

    @uncles.setter
    def uncles(self, uncles):
        self._uncles = uncles

    @aunts.setter
    def aunts(self, aunts):
        self._aunts = aunts

    @children.setter
    def children(self, children):
        self._children = children

        

    def is_male(self):
        return self.gender == self.MALE

    def is_female(self):
        return self.gender == self.FEMALE

    def is_mono(self):
        return self.relationship_orientation == self.MONOAMOROUS

    def is_poly(self):
        return self.relationship_orientation == self.POLYAMOROUS

    def is_minority(self):
        """Returns true if person is not cis-straight, mono or is/was in love with a family member."""
        return self.sexual_orientation != self.HETEROSEXUAL or \
            self.gender_identity == self.TRANSGENDER or \
            self.relationship_orientation == self.POLYAMOROUS or \
            self.loves_family_member

    def is_of_age(self):
        return self.age >= self.AGES[self.YOUNG_ADULT]

    def is_free_and_willing_to_date(self):

        # If person is underage, automatically returns false
        if not self.is_of_age():
            return False

        # If mono, return true if they are single/divorced/widowed and want a committed relationship
        # If poly, return true if they want (a / another) committed relationship
        if self.is_mono():
            return self.wants_domestic_partnership and self.is_not_in_relationship()
        if self.is_poly():
            return self.wants_domestic_partnership

    def is_not_in_relationship(self):
        return self.relationship_status != self.MARRIED and self.relationship_status != self.COMMITTED

    def can_and_wants_children(self):
        return self.can_have_children and self.wants_children

    def cant_but_wants_children(self):
        return self.can_have_children == False and self.wants_children

    # DETERMINING COMPATIBILITY WITH ANOTHER PERSON

    def is_target_gender(self, person):
        return person.gender in self.target_gender

    def is_of_same_age(self, person):
        return self.age == person.age

    def is_compatible_if_minority(self, candidate):

        # If the other person is not trans or poly, compatibility is automatically true.
        # If the other person is trans and/or poly, and self is liberal, return true.
        # If the other person is trans and/or poly, and self is conservative, return false.

        if candidate.is_minority():
            if self.is_liberal:
                return True
            else:
                return False
        else:
            return True

    def is_compatible(self, candidate):

        if self.is_free_and_willing_to_date() and candidate.is_free_and_willing_to_date() and candidate.family_id != self.family_id:
            # Returns true if self is compatible with another person when it comes to age, sexual orientation and ideology if minority
            return self.is_target_gender(candidate) and self.is_compatible_if_minority(candidate) and candidate.is_target_gender(self) and candidate.is_compatible_if_minority(self)
        else:
            return False

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

        self.age += 1
        self.life_stage = self.get_lifestage_from_age(self.age)

        return True
