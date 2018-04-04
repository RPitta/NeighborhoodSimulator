from traits import Traits
from education import Education
from job import Job


class Person(Traits):

    def __init__(self, gender, age):
        self.gender = gender
        self.age = age
        self.stage = next(stage for stage in self.LIFE_STAGES if age in stage.span)

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
        self.can_have_bio_children = False
        self.conditions = []

        # Default vars
        self.is_alive = True
        self.is_adopted = False
        self.was_in_foster_care = False
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
        self.partners = []
        self.spouses = []
        self.ex_partners = []
        self.ex_spouses = []

        # Death (Default: Old age)
        self.death_date = False
        self.death_cause = self.OLD_AGE  # Depends on death_date

        # Will be initialized once Teen if applicable
        self.come_out_date = -1
        self.move_out_date = -1
        self.thrown_out_date = -1

        # Relationship traits -> Will be initialized once Young Adult
        self.is_liberal = None
        self.wants_domestic_partnership = False
        self.wants_marriage = False
        self.wants_children = False
        self.in_love_with_family = False
        self.in_love_with_intergenerational = False
        self.in_love_with_another_race = False
        self.in_love_as_throuple = False
        self.in_love_date = -1

        # Degree
        self.education = Education()
        self.school_start_date = -1
        self.will_do_bachelor = False
        self.will_do_master = False
        self.will_do_doctor = False

        # Professions -> Will be initialized once Young Adult
        # self.occupation = None
        # self.employment = None
        # self.current_job = None
        # self.job_history = []
        self.job = Job()

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
        self.neighbor_friends = []
        self.move_in_date = -1
        self.house_to_move_in = -1

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
    def social_class(self):
        """Returns social class based on job salary."""
        for social_class in self.SOCIAL_CLASSES:
            if social_class.belongs_to(self.job.salary):
                return social_class
        raise Exception("No social class within valid salary range.")

    @property
    def is_white(self):
        return self.race[self.WHITE] == 100

    @property
    def is_mixed_race(self):
        for r, n in self.race.items():
            if n in range(1, 100):
                return True
        return False

    @property
    def is_challenged(self):
        return len(self.conditions) > 0

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
        """Returns true if person has mental/physical conditions,
        is LGBTA, poly or is/was in love with a family member,
        or is non-white."""
        return self.is_lgbta or self.is_poly or self.in_love_with_family or self.is_challenged or self.is_white is False

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
    def is_partnered(self):
        return self.is_married_or_remarried or self.is_committed

    @property
    def is_not_partnered(self):
        return self.is_single or self.is_separated or self.is_divorced or self.is_widowed

    @property
    def is_fully_partnered(self):
        """Returns true if: Mono person has 1 partner, or poly partner has max number of partners."""
        return len(self.partners) == 1 if self.is_mono else len(self.partners) == self.ALLOWED_NUM_OF_PARTNERS_FOR_POLYS

    @property
    def is_single_and_unemployed_adult(self):
        """Returns true if person has no partner and is unemployed."""
        return self.is_of_age and self.is_not_partnered and self.job.employment is False

    @property
    def is_romanceable(self):
        return self.wants_domestic_partnership and self.is_love_date and not self.is_fully_partnered

    # FUTURE DATES

    @property
    def is_autism_date(self):
        return self.age == self.AUTISM_AGE

    @property
    def is_school_start_date(self):
        return self.age == self.school_start_date

    @property
    def is_death_date(self):
        return self.age == self.death_date

    @property
    def is_love_date(self):
        return self.in_love_date in [self.YOUNGADULT.start, self.age]

    @property
    def is_come_out_date(self):
        return self.age == self.come_out_date

    @property
    def is_move_in_date(self):
        return self.age == self.move_in_date

    @property
    def is_move_out_date(self):
        return self.age == self.move_out_date

    @property
    def is_thrown_out_date(self):
        return self.age == self.thrown_out_date

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
        return len(self.partners) > 0 and all(partner.is_addict for partner in self.partners)

    @property
    def has_children_within_adoption_age(self):
        return len(self.children) > 0 and all(
            child.is_alive and child.age <= self.MAX_AGE_FOR_ADOPTION for child in self.children)

    @property
    def has_max_num_of_children(self):
        return len(self.children) >= len(self.ALLOWED_NUM_OF_CHILDREN_PER_COUPLE) or len(self.adoptive_children) >= len(
            self.ALLOWED_NUM_OF_CHILDREN_PER_COUPLE)

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
    def underage_children(self):
        return [child for child in self.children if child.is_of_age is False and child.is_alive]

    @property
    def has_conservative_parents(self):
        """Returns true if parents are conservative."""
        if len(self.adoptive_parents) > 0:
            return all(parent.is_liberal is False for parent in self.adoptive_parents)
        elif len(self.parents) > 0:
            return all(parent.is_liberal is False for parent in self.parents)
        elif len(self.step_parents) > 0:
            return all(parent.is_liberal is False for parent in self.step_parents)

    @property
    def bio_family(self):
        """Returns biological family members."""
        family_2d_list = [self.parents, self.children, self.full_grandparents, self.full_grandchildren,
                          self.full_siblings, self.half_siblings, self.full_cousins, self.half_cousins,
                          self.full_uncles,
                          self.half_uncles, self.full_aunts, self.half_aunts, self.full_nephews, self.half_nephews,
                          self.full_nieces, self.half_nieces]
        family_2d_filtered_list = list(filter(any, family_2d_list))
        return [family_member for family_1d_list in family_2d_filtered_list for family_member in family_1d_list]

    @property
    def living_bio_family(self):
        """Returns all living biological family members."""
        return [family_member for family_member in self.bio_family if family_member.is_alive]

    @property
    def all_family(self):
        """Returns all family members; adoptive and step family included."""
        family_2d_list = [self.parents, self.children, self.grandparents, self.grandchildren, self.siblings,
                          self.cousins, self.uncles, self.aunts, self.nephews, self.nieces, self.adoptive_parents,
                          self.adoptive_children]
        family_2d_filtered_list = list(filter(any, family_2d_list))
        return [family_member for family_1d_list in family_2d_filtered_list for family_member in family_1d_list]

    @property
    def living_family(self):
        """Returns all living family members."""
        return [family_member for family_member in self.all_family if family_member.is_alive]

    @property
    def living_inlaws_family(self):
        """Returns list of partners' family; in-laws."""
        inlaws_family = []
        for partner in self.partners:
            inlaws_family.extend([partner.living_family])
        filtered_inlaws_family = list(filter(any, inlaws_family))
        return [family_member for inlaws_family_lst in filtered_inlaws_family for family_member in inlaws_family_lst if
                family_member.is_alive]

    @property
    def parents_ids(self):
        return [id(parent) for parent in self.parents]

    @property
    def adoptive_parents_ids(self):
        return [id(parent) for parent in self.adoptive_parents]

    # MOTHER AND FATHER IF APPLICABLE

    @property
    def mother(self):
        """Returns bio/adoptive mother, or returns False if no straight parents."""
        if len(self.adoptive_parents) > 0:
            if all(p.is_male for p in self.adoptive_parents) or all(p.is_female for p in self.adoptive_parents):
                return False
            return next(p for p in self.adoptive_parents if p.is_female)
        elif len(self.parents) > 0:
            if all(p.is_male for p in self.parents) or all(p.is_female for p in self.parents):
                return False
            return next(p for p in self.parents if p.is_female)

    @property
    def father(self):
        """Returns bio/adoptive father, or returns False if no straight parents."""
        if len(self.adoptive_parents) > 0:
            if all(p.is_male for p in self.adoptive_parents) or all(p.is_female for p in self.adoptive_parents):
                return False
            return next(p for p in self.adoptive_parents if p.is_male)
        elif len(self.parents) > 0:
            if all(p.is_male for p in self.parents) or all(p.is_female for p in self.parents):
                return False
            return next(p for p in self.parents if p.is_male)

    # GRANDPARENTS

    @property
    def grandparents(self):
        return self.full_grandparents | self.adoptive_grandparents | self.step_grandparents

    @property
    def full_grandparents(self):
        return set([grandparent for parent in self.parents for grandparent in parent.parents])

    @property
    def adoptive_grandparents(self):
        return set([grandparent for parent in self.adoptive_parents for grandparent in parent.parents])

    @property
    def step_grandparents(self):
        return set([step_grandparent for step_parent in self.step_parents for step_grandparent in step_parent.parents])

    # GRANDCHILDREN

    @property
    def grandchildren(self):
        return self.full_grandparents | self.adoptive_grandparents | self.step_grandparents

    @property
    def full_grandchildren(self):
        return set([grandchild for child in self.children for grandchild in child.children])

    @property
    def adoptive_grandchildren(self):
        return set([grandchild for child in self.adoptive_children for grandchild in child.children])

    @property
    def step_grandchildren(self):
        return set([step_grandchild for step_child in self.step_children for step_grandchild in step_child.children])

    # STEP PARENTS

    @property
    def step_parents(self):
        if len(self.adoptive_step_parents) > 0:
            return self.adoptive_step_parents
        return self.bio_step_parents

    @property
    def bio_step_parents(self):
        return set([step_parent for parent in self.parents for step_parent in parent.partners if
                    step_parent not in self.parents])

    @property
    def adoptive_step_parents(self):
        return set([step_parent for parent in self.adoptive_parents for step_parent in parent.partners if
                    step_parent not in self.adoptive_parents])

    # STEP CHILDREN

    @property
    def step_children(self):
        if len(self.adoptive_step_children) > 0:
            return self.adoptive_step_children
        return self.bio_step_children

    @property
    def bio_step_children(self):
        return set([step_child for partner in self.partners for step_child in partner.children if
                    step_child not in self.children])

    @property
    def adoptive_step_children(self):
        return set([step_child for partner in self.partners for step_child in partner.adoptive_children if
                    step_child not in self.adoptive_children])

    # SIBLINGS

    @property
    def siblings(self):
        return self.full_siblings | self.half_siblings | self.step_siblings | self.adoptive_full_siblings | self.adoptive_half_siblings | self.adoptive_step_siblings

    @property
    def full_siblings(self):
        return set([sibling for parent in self.parents for sibling in parent.children if
                    sibling != self and sibling.parents_ids == self.parents_ids])

    @property
    def adoptive_full_siblings(self):
        return set([sibling for parent in self.adoptive_parents for sibling in parent.children if
                    sibling != self and set(sibling.adoptive_parents_ids) == set(self.adoptive_parents_ids)])

    @property
    def half_siblings(self):
        return set([half_sib for parent in self.parents for half_sib in parent.children if
                    half_sib != self and half_sib not in self.full_siblings])

    @property
    def adoptive_half_siblings(self):
        return set([half_sib for parent in self.adoptive_parents for half_sib in parent.children if
                    half_sib != self and half_sib not in self.adoptive_full_siblings])

    @property
    def step_siblings(self):
        if any(parent.step_children is not None for parent in self.parents):
            return set([step_sib for parent in self.parents for step_sib in parent.step_children])
        return set()

    @property
    def adoptive_step_siblings(self):
        if any(parent.step_children is not None for parent in self.adoptive_parents):
            return set([step_sib for parent in self.adoptive_parents for step_sib in parent.step_children])
        return set()

    # UNCLES

    @property
    def uncles(self):
        return self.full_uncles | self.adoptive_full_uncles | self.half_uncles | self.adoptive_half_uncles | self.step_uncles | self.adoptive_step_uncles

    @property
    def full_uncles(self):
        return set([uncle for parent in self.parents for uncle in parent.full_siblings if uncle.is_male])

    @property
    def adoptive_full_uncles(self):
        return set([uncle for parent in self.adoptive_parents for uncle in parent.full_siblings if uncle.is_male])

    @property
    def half_uncles(self):
        return set([uncle for parent in self.parents for uncle in parent.half_siblings if uncle.is_male])

    @property
    def adoptive_half_uncles(self):
        return set([uncle for parent in self.adoptive_parents for uncle in parent.half_siblings if uncle.is_male])

    @property
    def step_uncles(self):
        return set([uncle for parent in self.step_parents for uncle in parent.step_siblings if uncle.is_male])

    @property
    def adoptive_step_uncles(self):
        return set([uncle for parent in self.adoptive_step_parents for uncle in parent.step_siblings if uncle.is_male])

    # AUNTS

    @property
    def aunts(self):
        return self.full_aunts | self.adoptive_full_aunts | self.half_aunts | self.adoptive_half_aunts | self.step_aunts | self.adoptive_step_aunts

    @property
    def full_aunts(self):
        return set([aunt for parent in self.parents for aunt in parent.full_siblings if aunt.is_female])

    @property
    def adoptive_full_aunts(self):
        return set([aunt for parent in self.adoptive_parents for aunt in parent.full_siblings if aunt.is_female])

    @property
    def half_aunts(self):
        return set([aunt for parent in self.parents for aunt in parent.half_siblings if aunt.is_female])

    @property
    def adoptive_half_aunts(self):
        return set([aunt for parent in self.adoptive_parents for aunt in parent.half_siblings if aunt.is_female])

    @property
    def step_aunts(self):
        return set([aunt for parent in self.step_parents for aunt in parent.step_siblings if aunt.is_female])

    @property
    def adoptive_step_aunts(self):
        return set([aunt for parent in self.adoptive_step_parents for aunt in parent.step_siblings if aunt.is_female])

    # NEPHEWS

    @property
    def nephews(self):
        return self.full_nephews | self.adoptive_nephews | self.half_nephews | self.adoptive_half_nephews | self.step_nephews | self.adoptive_step_nephews

    @property
    def full_nephews(self):
        return set([nephew for sibling in self.full_siblings for nephew in sibling.children if nephew.is_male])

    @property
    def adoptive_nephews(self):
        return set([nephew for sibling in self.adoptive_full_siblings for nephew in sibling.children if nephew.is_male])

    @property
    def half_nephews(self):
        return set([nephew for sibling in self.half_siblings for nephew in sibling.children if nephew.is_male])

    @property
    def adoptive_half_nephews(self):
        return set([nephew for sibling in self.adoptive_half_siblings for nephew in sibling.children if nephew.is_male])

    @property
    def step_nephews(self):
        return set([nephew for sibling in self.step_siblings for nephew in sibling.children if nephew.is_male])

    @property
    def adoptive_step_nephews(self):
        return set([nephew for sibling in self.adoptive_step_siblings for nephew in sibling.children if nephew.is_male])

    # NIECES

    @property
    def nieces(self):
        return self.full_nieces | self.adoptive_nieces | self.half_nieces | self.adoptive_half_nieces | self.step_nieces | self.adoptive_step_nieces

    @property
    def full_nieces(self):
        return set([niece for sibling in self.full_siblings for niece in sibling.children if niece.is_female])

    @property
    def adoptive_nieces(self):
        return set([niece for sibling in self.adoptive_full_siblings for niece in sibling.children if niece.is_female])

    @property
    def half_nieces(self):
        return set([niece for sibling in self.half_siblings for niece in sibling.children if niece.is_female])

    @property
    def adoptive_half_nieces(self):
        return set([niece for sibling in self.adoptive_half_siblings for niece in sibling.children if niece.is_female])

    @property
    def step_nieces(self):
        return set([niece for sibling in self.step_siblings for niece in sibling.children if niece.is_female])

    @property
    def adoptive_step_nieces(self):
        return set([niece for sibling in self.adoptive_step_siblings for niece in sibling.children if niece.is_female])

    # COUSINS

    @property
    def cousins(self):
        return self.full_cousins | self.adoptive_full_cousins | self.half_cousins | self.adoptive_half_cousins | self.step_cousins | self.adoptive_step_cousins

    @property
    def full_cousins(self):
        c = set([cousin for uncle in self.uncles for cousin in uncle.children])
        c | set([cousin for uncle in self.aunts for cousin in uncle.children])
        return c

    @property
    def adoptive_full_cousins(self):
        c = set([cousin for uncle in self.adoptive_full_uncles for cousin in uncle.children])
        c | set([cousin for uncle in self.adoptive_full_aunts for cousin in uncle.children])
        return c

    @property
    def half_cousins(self):
        c = set([cousin for uncle in self.half_uncles for cousin in uncle.children])
        c | set([cousin for uncle in self.half_aunts for cousin in uncle.children])
        return c

    @property
    def adoptive_half_cousins(self):
        c = set([cousin for uncle in self.adoptive_half_uncles for cousin in uncle.children])
        c | set([cousin for uncle in self.adoptive_half_aunts for cousin in uncle.children])
        return c

    @property
    def step_cousins(self):
        c = set([cousin for uncle in self.step_uncles for cousin in uncle.children])
        c | set([cousin for uncle in self.step_aunts for cousin in uncle.children])
        return c

    @property
    def adoptive_step_cousins(self):
        c = set([cousin for uncle in self.adoptive_step_uncles for cousin in uncle.children])
        c | set([cousin for uncle in self.adoptive_step_aunts for cousin in uncle.children])
        return c

    # FAMILY NAMES

    @property
    def get_nephews_names(self):
        return self.get_names_list(self.nephews)

    @property
    def get_nieces_names(self):
        return self.get_names_list(self.nieces)

    @property
    def get_aunts_names(self):
        return self.get_names_list(self.aunts)

    @property
    def get_uncles_names(self):
        return self.get_names_list(self.uncles)

    @property
    def get_siblings_names(self):
        return self.get_names_list(self.siblings)

    @property
    def get_childrens_names(self):
        return self.get_names_list(self.children)

    @property
    def get_underage_childrens_names(self):
        return self.get_names_list(self.underage_children)

    @property
    def get_cousins_names(self):
        return self.get_names_list(self.cousins)

    @property
    def get_grandparents_names(self):
        return self.get_names_list(self.grandparents)

    @classmethod
    def get_names_list(cls, lst):
        if lst is None or len(lst) == 0:
            return "None"
        names_list = [p.name for p in lst]
        if len(lst) == 1:
            return ', '.join(map(str, names_list))
        return ', '.join(map(str, names_list[:-1])) + ' and ' + str(names_list[-1])
