from traits import Traits
from utilities.randomizer import Randomizer
from education import Education


class PersonalHandler:
    """Handles city and neighborhood persons' individual actions."""

    def __init__(self, person_developer):
        self.person_developer = person_developer

    def age_up(self, person):
        """Increase person's age by 1."""
        if person.age != person.stage.end:
            person.age += 1
        else:
            if person.stage.next_stage is False:
                person.death_date = person.age
            else:
                self.set_new_stage(person)

    def set_new_stage(self, person):
        """Set new stage if reached."""
        person.stage = person.stage.next_stage
        person.age += 1
        # Set new stage traits
        self.person_developer.set_new_stage_traits(person)


class CityCareerHandler:
    """City career handler."""

    def __init__(self, statistics):
        self.statistics = statistics

    def check_employment_and_education_status(self, person):
        """Check each person's education and employment status yearly."""
        if person.education.in_study:
            self.advance_degree_process(person)
        else:
            if person.job.employment == Traits.EMPLOYED:
                # Logic to at some point get fired / get promoted / get demoted / improve or worsen job performance
                pass
            elif person.job.employment == Traits.UNEMPLOYED and person.age >= Traits.YOUNGADULT.start:
                if not self.will_start_next_degree(person):
                    person.job.employment = self.statistics.get_employment_chance()
                    if person.job.employment == Traits.EMPLOYED:
                        self.get_job(person)

    @classmethod
    def advance_degree_process(cls, person):
        """Advances person's current degree."""
        person.education.advance_degree_process()

    @classmethod
    def start_school(cls, child):
        """Child starts school."""
        child.education.start_degree(child.education.SCHOOL)

    @classmethod
    def will_start_next_degree(cls, person):
        """Person starts next degree if applicable."""
        if person.education.available_degree == person.education.BACHELOR and person.will_do_bachelor:
            person.education.start_degree(person.education.BACHELOR)
        elif person.education.available_degree == person.education.MASTER and person.will_do_master:
            person.education.start_degree(person.education.MASTER)
        elif person.education.available_degree == person.education.DOCTOR and person.will_do_doctor:
            person.education.start_degree(person.education.DOCTOR)
        else:
            return False
        return True

    @classmethod
    def get_job(cls, person):
        person.job.get_job(person.education.current_degree)


class CareerHandler(CityCareerHandler):
    """Neighborhood career handler."""

    def __init__(self, statistics):
        CityCareerHandler.__init__(self, statistics)

    def start_school(self, child):
        super().start_school(child)
        self.display_start_of_school_message(child)

    @classmethod
    def display_start_of_school_message(cls, child):
        print("{} has started school.".format(child))

    def advance_degree_process(self, person):
        super().advance_degree_process(person)
        if not person.education.in_study:
            self.display_completed_degree_message(person)

    @classmethod
    def display_completed_degree_message(cls, person):
        if person.is_male:
            print("\n{} has successfully completed his {}.".format(person, person.education))
        else:
            print("\n{} has successfully completed her {}.".format(person, person.education))

    def get_job(self, person):
        super().get_job(person)
        self.display_new_job_message(person)

    @classmethod
    def display_new_job_message(cls, person):
        print("\n{} has found a job as a {}.".format(person, person.job.title))

    @classmethod
    def will_start_next_degree(cls, person):
        """Override parent method with print messages for neighbors."""
        if person.education.available_degree == person.education.BACHELOR and person.will_do_bachelor:
            person.education.start_degree(person.education.BACHELOR)
            print("\n{} has started studying a bachelor's degree in X.".format(person))
        elif person.education.available_degree == person.education.MASTER and person.will_do_master:
            person.education.start_degree(person.education.MASTER)
            print("\n{} has started studying a master's degree in X.".format(person))
        elif person.education.available_degree == person.education.DOCTOR and person.will_do_doctor:
            person.education.start_degree(person.education.DOCTOR)
            print("\n{} has started studying a doctor's degree in X.".format(person))
        else:
            return False
        return True


class CityLgbtaHandler:
    """Handles lgbta's coming out."""

    def __init__(self, names):
        self.names = names

    def come_out(self, teen):
        """Lgbta persons come out."""
        if teen.is_trans:
            self.set_transgenders_new_traits(teen)

    def set_transgenders_new_traits(self, person):
        """Switch transgender's gender, assign new name."""
        self.set_new_gender(person)
        self.set_new_name(person)

    @classmethod
    def set_new_gender(cls, person):
        """Reassign gender."""
        if person.is_female:
            person.gender = Traits.MALE
        else:
            person.gender = Traits.FEMALE

    def set_new_name(self, teen):
        """Find new name."""
        new_name = self.names.get_name(teen)
        teen.name = new_name


class LgbtaHandler(CityLgbtaHandler):
    """Neighborhood lgbta handler."""

    def __init__(self, names, person_developer):
        CityLgbtaHandler.__init__(self, names)
        self.person_developer = person_developer

    def come_out(self, teen):
        if teen.is_trans:
            super().set_new_gender(teen)
            self.set_new_name(teen)
        if teen.is_gay:
            self.display_sexual_orientation_message(teen, "gay")
        if teen.is_bi:
            self.display_sexual_orientation_message(teen, "bisexual")
        if teen.is_asexual:
            self.display_sexual_orientation_message(teen, "asexual")

        # Print unsupportive family's message if applicable
        self.display_family_nonsupport_message(teen)
        # Set coming out consequences if applicable
        self.person_developer.set_coming_out_consequences(teen)

    def set_new_name(self, teen):
        new_name = self.names.get_name(teen)
        self.display_transgender_message(teen, new_name)
        teen.name = new_name

    @classmethod
    def display_transgender_message(cls, teen, new_name):
        if teen.is_male:
            print("\n{} has come out as transgender. His new chosen name is {}.".format(
                teen, new_name))
        else:
            print("\n{} has come out as transgender. Her new chosen name is {}.".format(
                teen, new_name))

    @classmethod
    def display_family_nonsupport_message(cls, teen):
        if teen.is_male and teen.has_conservative_parents:
            print("His conservative family is having a hard time coping with it.")
        elif teen.is_female and teen.has_conservative_parents:
            print("Her conservative family is having a hard time coping with it.")

    @classmethod
    def display_sexual_orientation_message(cls, teen, orientation):
        if teen.is_trans and teen.is_male:
            print("He has also come out as {}.".format(orientation))
        elif teen.is_trans and teen.is_female:
            print("She has also come out as {}.".format(orientation))
        else:
            print("\n{} has come out as {}.".format(teen, orientation))

    def get_thrown_out(self, person):
        """Person is thrown out of their home. Returns None or new household ID."""
        self.display_thrown_out_message(person)
        return self.get_id_from_neighborhood_friends(person)

    @classmethod
    def display_thrown_out_message(cls, person):
        if person.is_male:
            print("\n{} has been thrown out of his home by his unsupportive family.".format(person))
        else:
            print("\n{} has been thrown out of her home by her unsupportive family.".format(person))

    def move_out(self, person):
        """Person moves out of their home. Returns None or new household ID."""
        self.display_move_out_message(person)
        return self.get_id_from_neighborhood_friends(person)

    @classmethod
    def display_move_out_message(cls, person):
        """Prints person's decision to move out for coming out in a conservative family."""
        if person.is_male:
            print("\n{} has moved out of his home due to his unsupportive family.".format(person))
        else:
            print("\n{} has moved out of her home due to her unsupportive family.".format(person))

    def get_id_from_neighborhood_friends(self, person):
        """Returns None if person has no neighborhood friends, or liberal friend's apartment ID if so."""
        if len(person.neighbor_friends) == 0:
            self.display_left_neighborhood_message(person)
            return None
        else:
            friend = next(friend for friend in person.neighbor_friends if friend.is_liberal)
            self.display_new_household_message(person, friend)
            return friend.apartment_id

    @classmethod
    def display_left_neighborhood_message(cls, person):
        if person.is_male:
            print("He no longer lives in the neighborhood.")
        else:
            print("She no longer lives in the neighborhood.")

    @classmethod
    def display_new_household_message(cls, person, friend):
        if person.is_male:
            print("He now lives in his friend {}'s apartment, {}.".format(friend, friend.apartment_id))
        else:
            print("She now lives in her friend {}'s apartment, {}.".format(friend, friend.apartment_id))


class CityDeathHandler:
    """Handles city people's death."""

    def __init__(self, person_developer):
        self.person_developer = person_developer

    def die(self, person):
        """Set person's status to not alive and remove partners."""
        person.is_alive = False

        # Remove person from their spouses / partners
        self.remove_from_spouses(person)
        self.remove_from_partners(person)

    def remove_from_spouses(self, person):
        """Remove person from spouse's spouses list. Set as widowed."""
        for spouse in person.spouses:
            spouse.relationship_status = Traits.WIDOWED
            spouse.ex_spouses.append(person)
            spouse.spouses = [s for s in spouse.spouses if s != person]
            spouse.partners = [p for p in spouse.partners if p != person]
            self.set_new_love_date_for_widower(spouse)

    def remove_from_partners(self, person):
        """Remove person from partner's partners list. Set as single."""
        for partner in person.partners:
            if not partner.is_married_or_remarried:
                partner.relationship_status = Traits.SINGLE
            partner.ex_partners.append(person)
            partner.partners = [partner for partner in partner.partners if partner != person]
            self.set_new_love_date_for_widower(partner)

    def set_new_love_date_for_widower(self, person):
        """Helper method to set new love date for partner/spouse of dead person."""
        self.person_developer.set_new_love_date(person)


class DeathHandler(CityDeathHandler):
    """Adds print messages for neighborhood people's death."""

    def die(self, person):
        super().die(person)
        self.display_death_message(person)

    @classmethod
    def display_death_message(cls, person):
        if person.death_cause == Traits.ILLNESS:
            print("\n{} has died of an illness.".format(person))
        if person.death_cause == Traits.SUICIDE:
            print("\n{} has committed suicide.".format(person))
        if person.death_cause == Traits.ACCIDENT:
            print("\n{} has died in a road accident.".format(person))
        if person.death_cause == Traits.DRUG_OVERDOSE:
            print("\n{} has died from drug overdose.".format(person))
        if person.death_cause == Traits.ALCOHOL_OVERDOSE:
            print("\n{} has died from alcohol overdose.".format(person))
        if person.death_cause is False:
            print("\n{} has died of old age.".format(person))


class CityJobHandler:
    """Handles job and employment activity."""

    def add_job(self, person, job):
        """Add new job."""
        if person.current_job is not None:
            person.job_history.append(person.current_job)
        person.current_job = job
        self.update_employment_status(person, Traits.EMPLOYED)

    def get_fired(self, person):
        """Remove current job."""
        if person.current_job is None or person.career.employment == Traits.UNEMPLOYED:
            raise Exception("Cannot get fired if unemployed.")

        person.job_history.append(person.current_job)
        person.current_job = None
        self.update_employment_status(person, Traits.UNEMPLOYED)

    @classmethod
    def update_employment_status(cls, person, status):
        """Replace unemployed status with employed."""
        person.career.employment = status

    @classmethod
    def get_promotion(cls, person):
        """Job promotion."""
        person.current_job.promotion(1000, True)  # Example only

    @classmethod
    def get_demotion(cls, person):
        """Job demotion."""
        person.current_job.demotion(1000, True)  # Example only


class JobHandler(CityJobHandler):
    """Adds print messages to city job handler class."""

    def add_job(self, person, job):
        print("{} has found a job as a {}.".format(person, job.title))
        super().add_job(person, job)

    def get_fired(self, person):
        print("{} has been fired.".format(person))
        super().get_fired(person)

    @classmethod
    def get_promotion(cls, person):
        print("{} has been promoted.")
        super().get_promotion(person)

    @classmethod
    def get_demotion(cls, person):
        print("{} has been demoted.")
        super().get_demotion(person)


class CityAddictionHandler:
    """Handles addiction."""

    def __init__(self, person_developer):
        self.person_developer = person_developer

    def become_an_addict(self, person):
        """Become a drug or alcohol addict."""
        if person.will_become_drug_addict:
            person.is_drug_addict = True
        elif person.will_become_alcohol_addict:
            person.is_alcohol_addict = True
        else:
            raise Exception("Cannot become an addict if no drugs/alcohol addiction set.")
        # Set possible consequences (overdose / rehab)
        self.person_developer.set_addiction_consequences(person)

    def get_sober(self, person):
        """Recover from addiction if an addict."""
        if person.is_drug_addict:
            person.is_drug_addict = False
            person.was_drug_addict = True
        elif person.is_alcohol_addict:
            person.is_alcohol_addict = False
            person.was_alcohol_addict = True
        else:
            raise Exception("Cannot get sober if not an addict.")
        # Set relapse date if applicable
        self.person_developer.relapse_chance(person)

    def relapse(self, person):
        """Become an addict again if an ex-addict."""
        if person.was_drug_addict:
            person.is_drug_addict = True
        elif person.was_alcohol_addict:
            person.is_alcohol_addict = True
        else:
            raise Exception("Cannot relapse if not previously an addict.")
        # Set possible consequences (overdose / rehab)
        self.person_developer.set_addiction_consequences(person)


class AddictionHandler(CityAddictionHandler):
    """Adds print messages to addiction handler."""

    def __init__(self, person_developer):
        CityAddictionHandler.__init__(self, person_developer)

    def become_an_addict(self, person):
        if person.will_become_drug_addict:
            print("\n{} has become a drug addict.".format(person))
        elif person.will_become_alcohol_addict:
            print("\n{} has become an alcohol addict.".format(person))
        super().become_an_addict(person)

    def get_sober(self, person):
        if person.is_drug_addict:
            print("\n{} has spent some time in a rehabilitation centre and is no longer a drug addict.".format(person))
        elif person.is_alcohol_addict:
            print("\n{} has spent some time in a rehabilitation centre and is no longer an alcohol addict.".format(person))
        super().get_sober(person)

    def relapse(self, person):
        if person.was_drug_addict:
            print("\n{} has relapsed and has become a drug addict again.".format(person))
        elif person.was_alcohol_addict:
            print("\n{} has relapsed and has become an alcohol addict again.".format(person))
        super().relapse(person)


class CityMarriageHandler:
    """Handles marriage."""

    def __init__(self):
        self.randomizer = Randomizer()

    def get_married(self, couple):
        """Marriage."""
        if any(p.is_married_or_remarried for p in couple.persons):  # Skip if poly person is already married
            return
        self.set_married_status(couple)
        self.set_as_spouses(couple)
        self.set_shared_surname(couple)
        self.marriage_validation(couple)

    @classmethod
    def set_married_status(cls, couple):
        for person in couple.persons:
            if len(person.ex_spouses) > 0:
                person.relationship_status = Traits.REMARRIED
            else:
                person.relationship_status = Traits.MARRIED

    @classmethod
    def set_as_spouses(cls, couple):
        """Set each other as spouses."""
        for person in couple.persons:
            spouses = [p for p in couple.persons if p != person]
            for spouse in spouses:
                person.spouses.append(spouse)

    def set_shared_surname(self, couple):
        """If person is female and is married to a male, take male's surname. Else, 50/50 chance."""
        if couple.is_straight:
            couple.woman.surname = couple.man.surname
        else:
            surnames = []
            for p in couple.persons:
                surnames.append(p.surname)
            chosen = self.randomizer.get_random_item(surnames)
            for person in couple.persons:
                person.surname = chosen

    @classmethod
    def marriage_validation(cls, couple):
        if any([p.is_married_or_remarried is False for p in couple.persons]):
            raise Exception("Married couple is not set as married.")
        if any([len(p.spouses) == 0 for p in couple.persons]):
            raise Exception("Married couple has no assigned spouse.")
        if couple.marriage_date > couple.oldest.age:
            raise Exception(
                "Married couple has marriage date set in the future.")
        if not all([couple.persons[0].surname == p.surname for p in couple.persons]):
            raise Exception(
                "Married couple does not have the same surname.")


class MarriageHandler(CityMarriageHandler):
    """Adds print messages to marriage handler."""

    def get_married(self, couple):
        super().get_married(couple)
        self.display_new_marriage_message(couple)

    @classmethod
    def display_new_marriage_message(cls, couple):
        print("\n{} {} and {} {} have married. Their surname is now {}.".format(
            couple.person1.name, couple.person1.original_surname, couple.person2.name, couple.person2.original_surname,
            couple.person1.surname))


class CityDivorceHandler:
    """Handles divorce and separation."""

    def get_divorced(self, couple):
        """Handles couple divorce"""
        self.set_divorced_status(couple)
        self.remove_spouses(couple)
        self.add_to_exspouses(couple)
        self.revert_username(couple)

    @classmethod
    def set_divorced_status(cls, couple):
        for person in couple.persons:
            person.relationship_status = Traits.DIVORCED

    @classmethod
    def remove_spouses(cls, couple):
        for person in couple.persons:
            person.spouses = [spouse for spouse in person.spouses if spouse not in couple.persons]
            person.partners = [partner for partner in person.partners if partner not in couple.persons]

    @classmethod
    def add_to_exspouses(cls, couple):
        for person in couple.persons:
            exes = [ex for ex in couple.persons if ex != person]
            for ex in exes:
                person.ex_spouses.append(ex)

    @classmethod
    def revert_username(cls, couple):
        for person in couple.persons:
            person.surname = person.original_surname

    def get_separated(self, couple):
        """Handles couple separation"""
        self.set_separated_status(couple)
        self.remove_partners(couple)
        self.add_to_expartners(couple)

    @classmethod
    def set_separated_status(cls, couple):
        for person in couple.persons:
            if person.is_married_or_remarried is False and len(person.partners) < 2:
                person.relationship_status = Traits.SEPARATED

    @classmethod
    def remove_partners(cls, couple):
        for person in couple.persons:
            person.partners = [partner for partner in person.partners if partner not in couple.persons]

    @classmethod
    def add_to_expartners(cls, couple):
        for person in couple.persons:
            exes = [ex for ex in couple.persons if ex != person]
            for ex in exes:
                person.ex_partners.append(ex)


class DivorceHandler(CityDivorceHandler):
    """Adds print messages to divorce handler."""
    def __init__(self):
        self.randomizer = Randomizer()

    def get_divorced(self, couple):
        self.display_divorce_message(couple)
        super().get_divorced(couple)

    @classmethod
    def display_divorce_message(cls, couple):
        print("\n{} and {} have gotten a divorce.".format(
            couple.person1, couple.person2))

    def get_separated(self, couple):
        self.display_separation_message(couple)
        super().get_separated(couple)

    @classmethod
    def display_separation_message(cls, couple):
        print("\n{} and {} have separated.".format(
            couple.person1, couple.person2))

    def leave_household(self, couple):
        """Returns person who will leave the apartment and the new apartment ID if any."""
        leaving_person = self.randomizer.get_random_item(couple.persons)
        new_apartment_id = self.get_id_from_neighborhood_friends(leaving_person)
        return {"person" : leaving_person, "id" : new_apartment_id}

    def get_id_from_neighborhood_friends(self, person):
        """Returns None if person has no neighborhood friends, or liberal friend's apartment ID if so."""
        if len(person.neighbor_friends) == 0:
            self.display_left_neighborhood_message(person)
            return None
        else:
            friend = next(friend for friend in person.neighbor_friends if friend.is_liberal)
            self.display_new_household_message(person, friend)
            return friend.apartment_id

    @classmethod
    def display_left_neighborhood_message(cls, person):
        print("{} has moved out and no longer lives in the neighborhood.".format(person.name))

    @classmethod
    def display_new_household_message(cls, person, friend):
        if person.is_male:
            print("{} now lives in his friend {}'s apartment, {}.".format(person.name, friend, friend.apartment_id))
        else:
            print("{} now lives in her friend {}'s apartment, {}.".format(person.name, friend, friend.apartment_id))


class CityPregnancyHandler:
    """Handles pregnancy and adoption."""

    def __init__(self, person_generator, statistics, foster_care_system):
        self.person_generator = person_generator
        self.statistics = statistics
        self.foster_care_system = foster_care_system

    def get_pregnant(self, couple):
        """Set pregnancy to True and set statistical number of expecting children."""
        if couple.woman.is_pregnant or any(person.has_max_num_of_children for person in couple.persons):
            couple.birth_date = -1
            return
        couple.expecting_num_of_children = self.statistics.get_pregnancy_num_of_children()
        couple.woman.is_pregnant = True
        self.pregnancy_and_adoption_validation(couple)

    def start_adoption_process(self, couple):
        """Set adoption process to True and set statistical number of expecting children"""
        couple.expecting_num_of_children = self.statistics.get_adoption_num_of_children()
        for person in couple.persons:
            person.is_in_adoption_process = True
        self.pregnancy_and_adoption_validation(couple)

    @classmethod
    def pregnancy_and_adoption_validation(cls, couple):
        if couple.oldest.is_young_adult is False:
            raise Exception(
                "Couple set out to have children cannot be outside young adult's stage.")
        if any(person.has_max_num_of_children for person in couple.persons):
            raise Exception(
                "Couple set out to have children are already full.")
        if couple.desired_num_of_children <= 0 or couple.desired_children_left <= 0:
            raise Exception("Couple set out to have children do not wish so.")
        if couple.will_get_pregnant:
            if couple.expecting_num_of_children not in Traits.ALLOWED_NUM_OF_CHILDREN_PER_PREGNANCY:
                raise Exception(
                    "Couple's expecting number of children is not permitted.")
            if all([person.can_have_bio_children is False for person in couple.persons]):
                raise Exception(
                    "Couple cannot have biological children yet they are getting pregnant.")
        if couple.will_adopt:
            if all([person.can_have_bio_children for person in couple.persons]):
                raise Exception(
                    "Couple can have biological children yet they are adopting.")

    def give_birth(self, couple):
        """Returns newborns from given pregnant couple."""
        if couple.is_pregnant is False:
            raise Exception("Cannot give birth if not pregnant.")

        babies = []
        if couple.expecting_num_of_children == Traits.SINGLETON:
            babies = [self.person_generator.generate_baby(couple)]
        elif couple.expecting_num_of_children == Traits.TWINS:
            for _ in range(couple.expecting_num_of_children):
                new_baby = self.person_generator.generate_baby(couple)
                new_baby.is_twin = True  # Set as twin
                babies.append(new_baby)
        elif couple.expecting_num_of_children == Traits.TRIPLETS:
            for _ in range(couple.expecting_num_of_children):
                new_baby = self.person_generator.generate_baby(couple)
                new_baby.is_triplet = True  # Set as triplet
                babies.append(new_baby)
        else:
            raise Exception("Number of births is not permitted.")

        return babies

    @classmethod
    def reset_pregnancy(cls, couple):
        """Set woman pregnancy to false and subtract newborns from desired num of children."""
        couple.woman.is_pregnant = False
        couple.desired_children_left -= couple.expecting_num_of_children
        couple.expecting_num_of_children = 0

    def adopt(self, couple):
        """Returns adoptions from given couple."""
        if not all([p.is_in_adoption_process for p in couple.persons]):
            raise Exception("Couple cannot adopt if not in adoption process.")

        if couple.expecting_num_of_children == Traits.ONE_CHILD:
            return self.foster_care_system.adopt_child(couple)
        elif couple.expecting_num_of_children == Traits.SIBLING_SET:
            return self.foster_care_system.adopt_sibling_set(couple)
        else:
            raise Exception("Wrong number of adoptions.")

    @classmethod
    def reset_adoption(cls, couple):
        """Set couple's adoption process to false and subtract adoptions from desired num of children."""
        for person in couple.persons:
            person.is_in_adoption_process = False
        couple.desired_children_left -= couple.expecting_num_of_children
        couple.expecting_num_of_children = 0


class PregnancyHandler(CityPregnancyHandler):
    """Neighborhood pregnancy handler."""

    def __init__(self, person_generator, statistics, foster_care_system):
        CityPregnancyHandler.__init__(self, person_generator, statistics, foster_care_system)

    def get_pregnant(self, couple):
        super().get_pregnant(couple)
        self.print_expecting_num_of_bio_children(couple)

    @classmethod
    def print_expecting_num_of_bio_children(cls, couple):
        """Display number of pregnancy children that couple is expecting."""
        if couple.expecting_num_of_children == Traits.SINGLETON:
            print("\n{} and {} are pregnant with a child.".format(
                couple.man, couple.woman))
        elif couple.expecting_num_of_children == Traits.TWINS:
            print("\n{} and {} are pregnant with twins.".format(
                couple.man, couple.woman))
        elif couple.expecting_num_of_children == Traits.TRIPLETS:
            print("\n{} and {} are pregnant with triplets.".format(
                couple.man, couple.woman))
        else:
            raise Exception("Number of pregnancy children not permitted.")

    def start_adoption_process(self, couple):
        super().start_adoption_process(couple)
        self.print_expecting_num_of_adoptions(couple)

    @classmethod
    def print_expecting_num_of_adoptions(cls, couple):
        """Display number of adoptions that couple is expecting."""
        if couple.expecting_num_of_children == Traits.ONE_CHILD:
            print("\n{} and {} have began the process to adopt a child.".format(
                couple.person1, couple.person2))
        elif couple.expecting_num_of_children == Traits.SIBLING_SET:
            print("\n{} and {} have began the process to adopt a sibling set.".format(
                couple.person1, couple.person2))
        else:
            raise Exception("Number of adoptions is not permitted.")

    def give_birth(self, couple):
        """Override give birth method to include print messages."""
        if couple.is_pregnant is False:
            raise Exception("Cannot give birth if not pregnant.")

        babies = []
        if couple.expecting_num_of_children == Traits.SINGLETON:
            babies = [self.person_generator.generate_baby(couple)]
            self.print_singleton_message(couple, babies)
        elif couple.expecting_num_of_children == Traits.TWINS:
            for _ in range(couple.expecting_num_of_children):
                new_baby = self.person_generator.generate_baby(couple)
                new_baby.is_twin = True  # Set as twin
                babies.append(new_baby)
            self.print_twins_message(couple, babies)
        elif couple.expecting_num_of_children == Traits.TRIPLETS:
            for _ in range(couple.expecting_num_of_children):
                new_baby = self.person_generator.generate_baby(couple)
                new_baby.is_triplet = True  # Set as triplet
                babies.append(new_baby)
            self.print_triplets_message(couple, babies)
        else:
            raise Exception("Number of births is not permitted.")

        return babies

    def adopt(self, couple):
        """Override adopt method to include print messages."""
        if not all([p.is_in_adoption_process for p in couple.persons]):
            raise Exception("Couple cannot adopt if not in adoption process.")

        if couple.expecting_num_of_children == Traits.ONE_CHILD:
            child = self.foster_care_system.adopt_child(couple)
            self.display_adoptions_message(couple, child)
            return child
        elif couple.expecting_num_of_children == Traits.SIBLING_SET:
            children = self.foster_care_system.adopt_sibling_set(couple)
            self.display_adoptions_message(couple, children)
            return children
        else:
            raise Exception("Wrong number of adoptions.")

    @classmethod
    def display_adoptions_message(cls, couple, children):
        if len(children) > 1:
            print("\n{} and {} have adopted a sibling set:".format(couple.person1, couple.person2))
            for child in children:
                print("{} ({}, age {})".format(child.name, child.baby_gender, child.age))
        else:
            print("\n{} and {} have adopted a {} aged {}: {}.".format(
                couple.person1, couple.person2, children[0].baby_gender, children[0].age, children[0].name))

    @classmethod
    def print_singleton_message(cls, couple, babies):
        print("\n{} and {} have given birth to a baby {}: {}.".format(
            couple.man, couple.woman, babies[0].baby_gender, babies[0].name))

    @classmethod
    def print_twins_message(cls, couple, babies):
        print("\n{} and {} have given birth to twins {} ({}) and {} ({}).".format(
            couple.person1, couple.person2, babies[0].name, babies[0].baby_gender, babies[1].name,
            babies[1].baby_gender))

    @classmethod
    def print_triplets_message(cls, couple, babies):
        print("\n{} and {} have given birth to triplets {} ({}), {} ({}) and {} ({}).".format(
            couple.person1, couple.person2, babies[0].name, babies[0].baby_gender, babies[1].name,
            babies[1].baby_gender, babies[2].name, babies[2].baby_gender))
