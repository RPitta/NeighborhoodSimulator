from traits import Traits, LifeStages


class Person(Traits, LifeStages):
    def __init__(self, gender, stage):
        self.gender = gender
        self.stage = stage
        self.age = self.stage.start

        # Names
        self.name = None  # May depend on family
        self.surname = None
        self.original_surname = self.surname  # Depends on surname

        # Basics
        self.gender_identity = None  # Linked to gender
        self.sexual_orientation = None
        self.target_gender = []  # Linked to sexual_orientation
        self.relationship_orientation = None
        self.social_class = None
        self.can_have_bio_children = False

        # Default: Alive, not adopted, not a twin or triplet
        # Single, not pregnant or in adoption process
        self.is_alive = True
        self.is_adopted = False
        self.is_twin = False
        self.is_triplet = False
        self.relationship_status = self.SINGLE
        self.is_pregnant = False
        self.is_in_adoption_process = False

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

        # Death (Default: Old age)
        self.death_date = False
        self.death_cause = self.OLD_AGE  # Depends on death_date

        # Will be intitialized once Teen if applicable
        self.come_out_date = -1

        # Relationship traits -> Will be intitialized once Young Adult
        self.is_liberal = None
        self.wants_domestic_partnership = False
        self.wants_marriage = False
        self.wants_children = False
        self.in_love_with_family = False
        self.in_love_with_intergenerational = False
        self.in_love_as_throuple = False
        self.in_love_date = -1

        # Professions -> Will be intitialized once Young Adult
        self.occupation = None
        self.employment = None

        # Will be intitialized if within Neighborhood
        self.apartment_id = -1
        self.is_neighbor = False

    def __str__(self):
        return self.fullname

    @property
    def fullname(self):
        """Name + Surname"""
        return "{} {}".format(self.name, self.surname)

    @property
    def is_male(self):
        return self.gender == self.MALE

    @property
    def is_female(self):
        return self.gender == self.FEMALE

    @property
    def baby_gender(self):
        if self.is_male:
            return "boy"
        return "girl"

    @property
    def is_straight(self):
        return self.sexual_orientation == self.HETEROSEXUAL

    @property
    def is_heteroromantic(self):
        return self.is_straight or self.sexual_orientation == self.HETEROROMANTIC_ASEXUAL

    @property
    def is_bi(self):
        return self.sexual_orientation == self.BISEXUAL

    @property
    def is_gay(self):
        return self.sexual_orientation == self.HOMOSEXUAL

    @property
    def is_asexual(self):
        return self.sexual_orientation in self.ASEXUAL_ORIENTATIONS

    @property
    def is_trans(self):
        return self.gender_identity == self.TRANSGENDER

    @property
    def is_lgbta(self):
        """True if gay, bisexual, asexual or transgender."""
        return self.is_gay or self.is_bi or self.is_trans or self.is_asexual

    @property
    def is_mono(self):
        return self.relationship_orientation == self.MONOAMOROUS

    @property
    def is_poly(self):
        return self.relationship_orientation == self.POLYAMOROUS

    @property
    def is_minority(self):
        """Returns true if person is LGBTA, poly or is/was in love with a family member."""
        return self.is_lgbta or self.is_poly or self.in_love_with_family

    # AGE

    @property
    def is_of_age(self):
        return self.age >= self.YOUNGADULT.start

    @property
    def is_young_adult(self):
        return self.age in self.YOUNGADULT.span

    @property
    def adult_timespan_till_present_age(self):
        return list(range(self.YOUNGADULT.start, self.age + 1))

    @property
    def span_left_till_next_stage(self):
        return list(range(self.age + 1, self.stage.end + 1))

    @property
    def span_left_till_old_age(self):
        return list(range(self.age + 1, self.SENIOR.end + 1))

    # RELATIONSHIP STATUS

    @property
    def is_single(self):
        return self.relationship_status == self.SINGLE

    @property
    def is_committed(self):
        return self.relationship_status == self.COMMITTED

    @property
    def is_married_or_remarried(self):
        return self.relationship_status == self.MARRIED or self.relationship_status == self.REMARRIED

    @property
    def is_divorced(self):
        return self.relationship_status == self.DIVORCED

    @property
    def is_separated(self):
        return self.relationship_status == self.SEPARATED

    @property
    def is_widowed(self):
        return self.relationship_status == self.WIDOWED

    @property
    def is_fully_partnered(self):
        """Returns true if: Mono person has a partner or a spouse.
        Poly person has max number of partners, or a spouse + remaining possible number of partners until max."""
        if self.is_mono:
            return self.partner is not None or self.spouse is not None
        return len(self.partners) >= self.ALLOWED_NUM_OF_PARTNERS_FOR_POLYS or self.spouse is not None and (1 + (len(self.partners))) == self.ALLOWED_NUM_OF_PARTNERS_FOR_POLYS

    @property
    def is_romanceable(self):
        """Returns true if: person is alive, of age, wants partnership, has reached their dateable date, and is not fully partnered."""
        return self.wants_domestic_partnership and self.is_alive and self.is_of_age and not self.is_fully_partnered and self.in_love_date <= self.age

    # FUTURE DATES

    @property
    def is_death_date(self):
        return self.age == self.death_date

    @property
    def is_love_date(self):
        return self.age == self.in_love_date

    @property
    def is_come_out_date(self):
        return self.age == self.come_out_date

    # CHILDREN

    @property
    def can_and_wants_bio_or_adopted_children(self):
        """Wants children and can get pregnant or adopt."""
        return self.can_and_wants_bio_children or self.cant_but_wants_children

    @property
    def can_and_wants_bio_children(self):
        """Wants children. Has not reached maximum number of children. Is young adult. Can have biological children."""
        return self.wants_children and self.has_max_num_of_children is False and self.is_young_adult and self.can_have_bio_children

    @property
    def cant_but_wants_children(self):
        """Wants children. Has not reached maximum number of children. Is young adult. Cannot have biological children."""
        return self.wants_children and self.has_max_num_of_children is False and self.is_young_adult and self.can_have_bio_children is False

    @property
    def has_max_num_of_children(self):
        return len(self.children) >= len(self.ALLOWED_NUM_OF_CHILDREN_PER_COUPLE)

    # FAMILY

    @property
    def bio_family(self):
        """Returns biological family members; Parents, Grandparents, Siblings, Half-Siblings,
        Children, Grandchildren, Cousins, Aunts/Uncles and Nephews/Nieces."""
        family_2d_list = [self.parents, self.children, self.grandparents, self.grandchildren, self.siblings, self.half_siblings,
                          self.cousins, self.parents_siblings, self.siblings_children]
        family_2d_filtered_list = list(filter(any, family_2d_list))
        return [family_member for family_1d_list in family_2d_filtered_list for family_member in family_1d_list]

    @property
    def living_bio_family(self):
        """Returns all living biological family members."""
        return [family_member for family_member in self.bio_family if family_member.is_alive]

    @property
    def living_inlaws_family(self):
        inlaws_family_2d_list = [[self.partner], [self.spouse], self.partners]
        if self.partner is not None:
            inlaws_family_2d_list.extend([self.partner.living_bio_family])
        elif self.spouse is not None:
            inlaws_family_2d_list.extend([self.spouse.living_bio_family])
        elif len(self.partners) == 1:
            inlaws_family_2d_list.extend([self.partners[0].living_bio_family])

        inlaws_family_2d_filtered_list = list(
            filter(any, inlaws_family_2d_list))
        return [family_member for inlaws_family_1d_list in inlaws_family_2d_filtered_list for family_member in inlaws_family_1d_list if family_member.is_alive]

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
        return ', '.join(map(str, [p.name for p in lst]))
