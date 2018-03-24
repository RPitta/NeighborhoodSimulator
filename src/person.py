from traits import Traits, LifeStages


class Person(Traits, LifeStages):
    def __init__(self, gender, age):
        self.gender = gender
        self.age = age
        self.stage = next(stage for stage in self.LIFESTAGES if age in stage.span)

        # Names
        self.name = None  # May depend on family
        self.surname = None
        self.original_surname = self.surname  # Depends on surname

        # Basics
        self.gender_identity = None  # Linked to gender
        self.sexual_orientation = None
        self.target_gender = []  # Linked to sexual_orientation
        self.race = None
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
        self.children = []
        self.adoptive_parents = []
        self.adoptive_children = []
        self.partner = None
        self.spouse = None
        self.partners = []
        self.ex_partners = []
        self.ex_spouses = []

        # Death (Default: Old age)
        self.death_date = False
        self.death_cause = self.OLD_AGE  # Depends on death_date

        # Will be initialized once Teen if applicable
        self.come_out_date = -1

        # Relationship traits -> Will be initialized once Young Adult
        self.is_liberal = None
        self.wants_domestic_partnership = False
        self.wants_marriage = False
        self.wants_children = False
        self.in_love_with_family = False
        self.in_love_with_intergenerational = False
        self.in_love_as_throuple = False
        self.in_love_date = -1

        # Professions -> Will be initialized once Young Adult
        self.occupation = None
        self.employment = None

        # Addiction attributes -> Will be initialized once Young Adult
        self.will_become_drug_addict = False
        self.will_become_alcohol_addict = False
        self.addiction_date = -1
        self.is_drug_addict = False
        self.is_alcohol_addict = False
        self.will_recover = False
        self.will_overdose = False
        self.was_drug_addict = False
        self.was_alcohol_addict = False
        self.rehabilitation_date = -1
        self.relapse_date = -1

        # Will be initialized if within Neighborhood
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
        return self.relationship_status in (self.MARRIED or self.REMARRIED)

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
            return any(so is not None for so in [self.partner, self.spouse])
        return len(self.partners) >= self.ALLOWED_NUM_OF_PARTNERS_FOR_POLYS or self.spouse is not None and (
                1 + (len(self.partners))) == self.ALLOWED_NUM_OF_PARTNERS_FOR_POLYS

    @property
    def is_not_partnered(self):
        return self.is_single or self.is_separated or self.is_divorced or self.is_widowed

    @property
    def is_single_and_unemployed_adult(self):
        return self.is_of_age and self.is_not_partnered and self.employment is False

    @property
    def is_romanceable(self):
        """Returns true if: person is alive, of age, wants partnership, has reached their dateable date, and is not fully partnered."""
        return self.wants_domestic_partnership and self.is_alive and self.is_of_age and self.in_love_date in [0,
                                                                                                              self.age + 1] and not self.is_fully_partnered

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
        """Wants children. Has not reached maximum number of children.
        Is young adult. Can have biological children."""
        return self.wants_children and not self.has_max_num_of_children and self.is_young_adult and self.can_have_bio_children

    @property
    def cant_but_wants_children(self):
        """Wants children. Has not reached maximum number of children.
        Is young adult. Cannot have biological children."""
        return self.wants_children and not self.has_max_num_of_children and self.is_young_adult and not self.can_have_bio_children

    @property
    def must_place_children_up_for_adoption(self):
        """Person will give up their children up for adoption if they are within the system's adoption age,
        he/she is an addict and either has no partners or partner(s) is also an addict."""
        return self.has_children_within_adoption_age and self.is_addict and (
                self.is_not_partnered or self.has_addict_partner)

    @property
    def has_addict_partner(self):
        if self.partner is not None and self.partner.is_addict:
            return True
        if self.spouse is not None and self.spouse.is_addict:
            return True
        if len(self.partners) is not None and all(partner.is_addict for partner in self.partners):
            return True
        return False

    @property
    def has_children_within_adoption_age(self):
        return len(self.children) > 0 and all(child.age <= self.MAX_AGE_FOR_ADOPTION for child in self.children)

    @property
    def has_max_num_of_children(self):
        return len(self.children) >= len(self.ALLOWED_NUM_OF_CHILDREN_PER_COUPLE)

    # ADDICTION

    @property
    def is_addict(self):
        return self.is_drug_addict or self.is_alcohol_addict

    @property
    def is_addiction_date(self):
        return self.age == self.addiction_date

    @property
    def is_rehabilitation_date(self):
        return self.age == self.rehabilitation_date

    @property
    def is_relapse_date(self):
        return self.age == self.relapse_date

    # FAMILY

    @property
    def bio_family(self):
        """Returns biological family members; Parents, Grandparents, Siblings, Half-Siblings,
        Children, Grandchildren, Cousins, Aunts/Uncles and Nephews/Nieces."""
        family_2d_list = [self.parents, self.children, self.grandparents, self.grandchildren, self.full_siblings,
                          self.half_siblings, self.cousins, self.uncles, self.aunts, self.nephews, self.nieces]
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
        return [family_member for inlaws_family_1d_list in inlaws_family_2d_filtered_list for family_member in
                inlaws_family_1d_list if family_member.is_alive]

    @property
    def parents_ids(self):
        return [id(parent) for parent in self.parents]

    @property
    def adoptive_parents_ids(self):
        return [id(parent) for parent in self.adoptive_parents]

    @property
    def mother(self):
        """Returns mother, or returns False if no straight parents."""
        if len(self.parents) > 0:
            if all(p.is_male for p in self.parents) or all(p.is_female for p in self.parents):
                return False
            return next(p for p in self.parents if p.is_female)
        else:
            if all(p.is_male for p in self.adoptive_parents) or all(p.is_female for p in self.adoptive_parents):
                return False
            return next(p for p in self.adoptive_parents if p.is_female)

    @property
    def father(self):
        """Returns father, or returns False if no straight parents."""
        if len(self.parents) > 0:
            if all(p.is_male for p in self.parents) or all(p.is_female for p in self.parents):
                return False
            return next(p for p in self.parents if p.is_male)
        else:
            if all(p.is_male for p in self.adoptive_parents) or all(p.is_female for p in self.adoptive_parents):
                return False
            return next(p for p in self.adoptive_parents if p.is_male)

    @property
    def grandparents(self):
        return [grandparent for parent in self.parents for grandparent in parent.parents]

    @property
    def grandchildren(self):
        return [grandchild for child in self.children for grandchild in child.children]

    @property
    def step_parents(self):
        return [step_parent for parent in self.parents for step_parent in parent.partner if
                parent.partner not in self.parents]

    @property
    def step_children(self):
        if self.partner is not None:
            return [step_child for step_child in self.partner.children if step_child not in self.children]
        return []

    @property
    def siblings(self):
        return self.full_siblings | self.half_siblings | self.step_siblings | self.adoptive_siblings

    @property
    def full_siblings(self):
        return set([sibling for parent in self.parents for sibling in parent.children if sibling != self and sibling.parents_ids == self.parents_ids])


    @property
    def half_siblings(self):
        return set([half_sib for parent in self.parents for half_sib in parent.children if
                half_sib != self and half_sib not in self.full_siblings])

    @property
    def step_siblings(self):
        if any(parent.step_children is not None for parent in self.parents):
            return set([step_sib for parent in self.parents for step_sib in parent.step_children])
        return set()

    @property
    def adoptive_siblings(self):
        return set([sibling for parent in self.adoptive_parents for sibling in parent.children if
                sibling != self and set(sibling.adoptive_parents_ids) == set(self.adoptive_parents_ids)])

    @property
    def uncles(self):
        return set([uncle for grandparent in self.grandparents for uncle in grandparent.children if
                uncle not in self.parents and uncle.is_male])

    @property
    def aunts(self):
        return set([aunt for grandparent in self.grandparents for aunt in grandparent.children if
                aunt not in self.parents and aunt.is_female])

    @property
    def nephews(self):
        return set([nephew for sibling in self.siblings for nephew in sibling.children if nephew.is_male])

    @property
    def nieces(self):
        return set([niece for sibling in self.siblings for niece in sibling.children if niece.is_female])

    @property
    def cousins(self):
        c = set([cousin for uncle in self.uncles for cousin in uncle.children])
        c | set([cousin for uncle in self.aunts for cousin in uncle.children])
        return c

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
