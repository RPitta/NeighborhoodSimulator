from traits import Traits
from utilities.randomizer import Randomizer


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

    def move_in(self, person):
        """Returns person's partner's apartment ID to move into."""
        self.display_move_in_message(person)
        return person.house_to_move_in

    @classmethod
    def display_move_in_message(cls, person):
        partner = ""
        for p in person.partners:
            if p.apartment_id == person.house_to_move_in:
                partner = p
        if partner.is_male:
            print("\n{}'s partner {} has moved in with him.".format(partner, person))
            if len(person.underage_children) == 1:
                if person.is_male:
                    print("His underage child {} has also moved in.".format(person.get_underage_childrens_names))
                else:
                    print("Her underage child {} has also moved in.".format(person.get_underage_childrens_names))
            elif len(person.underage_children) > 1:
                if person.is_male:
                    print("His underage children {} have also moved in.".format(person.get_underage_childrens_names))
                else:
                    print("Her underage children {} have also moved in.".format(person.get_underage_childrens_names))
        else:
            print("\n{}'s partner {} has moved in with her.".format(partner, person))
            if len(person.underage_children) == 1:
                if person.is_male:
                    print("His underage child {} has also moved in.".format(person.get_underage_childrens_names))
                else:
                    print("Her underage child {} has also moved in.".format(person.get_underage_childrens_names))
            elif len(person.underage_children) > 1:
                if person.is_male:
                    print("His underage children {} have also moved in.".format(person.get_underage_childrens_names))
                else:
                    print("Her underage children {} have also moved in.".format(person.get_underage_childrens_names))


class ConditionsHandler:
    """Handles each person's conditions / illnesses."""

    @classmethod
    def display_autism_diagnostic_message(cls, baby):
        print(f"\n{baby} has been diagnosed with {Traits.AUTISTIC_DISORDER}.")

    @classmethod
    def display_depression_diagnostic_message(cls, person):
        print(f"\n{person} has fallen into a {Traits.DEPRESSION}.")

    @classmethod
    def display_therapy_start_message(cls, person):
        print(f"\n{person} has started going to therapy.")

    @classmethod
    def recover_from_depression(cls, person):
        if Traits.DEPRESSION not in person.conditions:
            raise Exception("Can't recover from depression if not depressed.")

        person.conditions.remove(Traits.DEPRESSION)
        if person.is_neighbor:
            print(f"\n{person} has recovered from {Traits.DEPRESSION}.")


class CareerHandler:
    """Handles people's careers, education and jobs."""

    def __init__(self, statistics):
        self.statistics = statistics

    def check_employment_and_education_status(self, person):
        """Check each person's education and employment status yearly."""
        if person.education.in_study:
            self.advance_degree(person)
        else:
            if person.job.employment == Traits.EMPLOYED:
                # Logic to at some point get fired / get promoted / get demoted / improve or worsen job performance
                pass
            elif person.job.employment == Traits.UNEMPLOYED and person.age >= Traits.YOUNGADULT.start:
                if not self.will_start_next_degree(person) and person.can_work:
                    person.job.employment = self.statistics.get_employment_chance()
                    if person.job.employment == Traits.EMPLOYED:
                        self.get_job(person)

    def advance_degree(self, person):
        """Advances person's current degree."""
        person.education.advance_degree(person.is_drug_addict, person.is_alcohol_addict)
        if person.is_neighbor and not person.education.in_study:
            self.display_completed_degree_message(person)

    @classmethod
    def display_completed_degree_message(cls, person):
        if person.is_male:
            print("\n{} has successfully completed his {}.".format(person, person.education))
        else:
            print("\n{} has successfully completed her {}.".format(person, person.education))

    @classmethod
    def will_start_next_degree(cls, person):
        """Override parent method with print messages for neighbors."""
        if person.education.available_degree == person.education.BACHELOR and person.will_do_bachelor:
            person.education.start_degree(person.education.BACHELOR)
            if person.is_neighbor:
                print("\n{} has started studying a bachelor's degree in X.".format(person))
        elif person.education.available_degree == person.education.MASTER and person.will_do_master:
            person.education.start_degree(person.education.MASTER)
            if person.is_neighbor:
                print("\n{} has started studying a master's degree in X.".format(person))
        elif person.education.available_degree == person.education.DOCTOR and person.will_do_doctor:
            person.education.start_degree(person.education.DOCTOR)
            if person.is_neighbor:
                print("\n{} has started studying a doctor's degree in X.".format(person))
        else:
            return False
        return True

    def start_school(self, child):
        """Child starts school."""
        child.education.start_degree(child.education.SCHOOL)
        if child.is_neighbor:
            self.display_start_of_school_message(child)

    @classmethod
    def display_start_of_school_message(cls, child):
        print("\n{} has started school.".format(child))

    def get_job(self, person):
        """Assign new job."""
        person.job.get_job(person)
        if person.is_neighbor:
            self.display_new_job_message(person)

    @classmethod
    def display_new_job_message(cls, person):
        print("\n{} has found a job as a {}.".format(person, person.job.title))


class LgbtaHandler:
    """Handles lgbta's coming out."""

    def __init__(self, names, person_developer):
        self.names = names
        self.person_developer = person_developer

    def come_out(self, teen):
        """Lgbta persons come out."""
        if teen.is_trans:
            self.set_transgenders_new_traits(teen)
        if teen.is_neighbor:
            if teen.is_gay:
                self.display_sexual_orientation_message(teen, "gay")
            if teen.is_bi:
                self.display_sexual_orientation_message(teen, "bisexual")
            if teen.is_asexual:
                self.display_sexual_orientation_message(teen, "asexual")
            self.display_family_nonsupport_message(teen)
            self.person_developer.set_coming_out_consequences(teen)

    def set_transgenders_new_traits(self, teen):
        """Switch transgender's gender, assign new name."""
        self.set_new_gender(teen)
        self.set_new_name(teen)

    def set_new_name(self, teen):
        new_name = self.names.get_name(teen)
        if teen.is_neighbor:
            self.display_transgender_message(teen, new_name)
        teen.name = new_name

    @classmethod
    def set_new_gender(cls, person):
        """Reassign gender."""
        if person.is_female:
            person.gender = Traits.MALE
        else:
            person.gender = Traits.FEMALE

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


class DeathHandler:
    """Handles city people's death."""

    def __init__(self, person_developer):
        self.person_developer = person_developer

    def die(self, person, household=None):
        """Set person's status to not alive and remove partners."""
        person.is_alive = False

        if person.is_neighbor:
            self.display_death_message(person)
            self.person_developer.set_depression_for_housemates(person, household)

        # Remove person from their spouses / partners
        self.remove_from_spouses(person)
        self.remove_from_partners(person)

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

    def remove_from_spouses(self, person):
        """Remove person from spouse's spouses list. Set as widowed."""
        for spouse in person.spouses:
            spouse.relationship_status = Traits.WIDOWED
            spouse.deceased_spouses.append(person)
            spouse.spouses = [s for s in spouse.spouses if s != person]
            spouse.partners = [p for p in spouse.partners if p != person]
            self.set_new_love_date_for_widower(spouse)

    def remove_from_partners(self, person):
        """Remove person from partner's partners list. Set as single."""
        for partner in person.partners:
            if not partner.is_married_or_remarried:
                partner.relationship_status = Traits.SINGLE
            partner.deceased_partners.append(person)
            partner.partners = [partner for partner in partner.partners if partner != person]
            self.set_new_love_date_for_widower(partner)
            # Reset move_in_date if applicable
            if partner.house_to_move_in == person.apartment_id and partner.move_in_date >= partner.age:
                partner.move_in_date = -1
                partner.house_to_move_in = -1

    def set_new_love_date_for_widower(self, person):
        """Helper method to set new love date for partner/spouse of dead person."""
        self.person_developer.set_new_love_date(person)


class JobHandler:
    """Handles job and employment activity."""

    def get_job(self, person):
        """Add new job."""
        person.job.get_job(person)
        if person.is_neighbor:
            self.display_new_job_message(person)

    @classmethod
    def display_new_job_message(cls, person):
        vowels = ["a", "e", "i", "o", "u"]
        if person.job.title[0].lower() in vowels:
            print("\n{} has found a job as an {}.".format(person, person.job.title))
        else:
            print("\n{} has found a job as a {}.".format(person, person.job.title))

    def get_fired(self, person):
        """Remove current job."""
        person.job.get_fired()
        if person.is_neighbor:
            self.display_get_fired_message(person)

    @classmethod
    def display_get_fired_message(cls, person):
        if person.is_male:
            print("\n{} has been fired from his job and is now unemployed.".format(person))
        else:
            print("\n{} has been fired from her job and is now unemployed.".format(person))

    @classmethod
    def get_promotion(cls, person):
        """Job promotion."""
        person.job.promotion(1000, True)  # Example only. NEEDS WORK.
        if person.is_neighbor:
            print("\n{} has been promoted.".format(person))

    @classmethod
    def get_demotion(cls, person):
        """Job demotion."""
        person.job.demotion(1000, True)  # Example only. NEEDS WORK.
        if person.is_neighbor:
            print("\n{} has been demoted.".format(person))


class AddictionHandler:
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
            raise Exception("Cannot become an addict if no drugs/alcohol addiction is set.")
        self.person_developer.set_addiction_consequences(person)
        if person.is_neighbor:
            self.display_new_addict_message(person)

    @classmethod
    def display_new_addict_message(cls, person):
        if person.will_become_drug_addict:
            print(f"\n{person} has become a drug addict.")
        elif person.will_become_alcohol_addict:
            print(f"\n{person} has become an alcohol addict.")

    def get_sober(self, person):
        """Recover from addiction if an addict."""
        if person.is_drug_addict:
            person.is_drug_addict = False
            person.was_drug_addict = True
            if person.is_neighbor:
                print(f"\n{person} has spent some time in a rehabilitation centre and is no longer a drug addict.")
        elif person.is_alcohol_addict:
            person.is_alcohol_addict = False
            person.was_alcohol_addict = True
            if person.is_neighbor:
                print(f"\n{person} has spent some time in a rehabilitation centre and is no longer an alcohol addict.")
        else:
            raise Exception("Cannot get sober if not an addict.")
        self.person_developer.relapse_chance(person)

    def relapse(self, person):
        """Become an addict again if an ex-addict."""
        if person.was_drug_addict:
            person.is_drug_addict = True
            if person.is_neighbor:
                print(f"\n{person} has relapsed and has become a drug addict again.")
        elif person.was_alcohol_addict:
            person.is_alcohol_addict = True
            if person.is_neighbor:
                print(f"\n{person} has relapsed and has become an alcohol addict again.")
        else:
            raise Exception("Cannot relapse if not previously an addict.")
        self.person_developer.set_addiction_consequences(person)


class MarriageHandler:
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
        if any(p.is_neighbor for p in couple.persons):
            self.display_new_marriage_message(couple)

    @classmethod
    def set_married_status(cls, couple):
        """Change each person's relationship status to married or remarried."""
        for person in couple.persons:
            if len(person.ex_spouses) > 0 or len(person.deceased_spouses) > 0:
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

    @classmethod
    def display_new_marriage_message(cls, couple):
        print("\n{} {} and {} {} have married. Their surname is now {}.".format(
            couple.person1.name, couple.person1.original_surname, couple.person2.name, couple.person2.original_surname,
            couple.person1.surname))


class DivorceHandler:
    """Handles divorce and separation."""

    def __init__(self):
        self.randomizer = Randomizer()

    def get_divorced(self, couple):
        """Handles couple divorce"""
        self.set_divorced_status(couple)
        self.remove_spouses(couple)
        self.add_to_exspouses(couple)
        self.revert_username(couple)
        if any(p.is_neighbor for p in couple.persons):
            self.display_divorce_message(couple)

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

    @classmethod
    def display_divorce_message(cls, couple):
        print(f"\n{couple.person1} and {couple.person2} have gotten a divorce.")

    def get_separated(self, couple):
        """Handles couple separation"""
        self.set_separated_status(couple)
        self.remove_partners(couple)
        self.add_to_expartners(couple)
        if any(p.is_neighbor for p in couple.persons):
            self.display_separation_message(couple)

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

    @classmethod
    def display_separation_message(cls, couple):
        print(f"\n{couple.person1} and {couple.person2} have separated.")

    def leave_household(self, couple):
        """Returns person who will leave the apartment and the new apartment ID if any."""
        if any(p.move_in_date > 0 for p in couple.persons):
            # If someone had moved in, they'll be the one to move out.
            leaving_person = next(p for p in couple.persons if p.move_in_date > 0)
        else:
            # Else, random person will move out.
            leaving_person = self.randomizer.get_random_item(couple.persons)
        new_apartment_id = self.get_id_from_neighborhood_friends(leaving_person)
        return {"person": leaving_person, "id": new_apartment_id}

    def get_id_from_neighborhood_friends(self, person):
        """Returns None if person has no neighborhood friends, or liberal friend's apartment ID if so."""
        if len(person.neighbor_friends) == 0:
            self.display_left_neighborhood_message(person)
            return None
        else:
            friend = next(friend for friend in person.neighbor_friends)
            self.display_new_household_message(person, friend)
            return friend.apartment_id

    @classmethod
    def display_left_neighborhood_message(cls, person):
        if len(person.children) == 0:
            print("{} has moved out and no longer lives in the neighborhood.".format(person.name))
            return
        children_in_household = [p for p in person.children if p.move_in_date > 0 and p.apartment_id == p.apartment_id]
        if len(children_in_household) == 0:
            print("{} has moved out and no longer lives in the neighborhood.".format(person.name))
        elif len(children_in_household) == 1:
            if person.is_male:
                print("{} and his child have moved out and no longer live in the neighborhood.".format(person.name))
            else:
                print("{} and her child have moved out and no longer live in the neighborhood.".format(person.name))
        else:
            if person.is_male:
                print("{} and his children have moved out and no longer live in the neighborhood.".format(
                    person.name))
            else:
                print("{} and her children have moved out and no longer live in the neighborhood.".format(
                    person.name))

    @classmethod
    def display_new_household_message(cls, person, friend):
        if person.is_male:
            print("{} now lives in his friend {}'s apartment, {}.".format(person.name, friend, friend.apartment_id))
        else:
            print("{} now lives in her friend {}'s apartment, {}.".format(person.name, friend, friend.apartment_id))


class PregnancyHandler:
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
        if any(p.is_neighbor for p in couple.persons):
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
        """Set adoption process to True and set statistical number of expecting children"""
        couple.expecting_num_of_children = self.statistics.get_adoption_num_of_children()
        for person in couple.persons:
            person.is_in_adoption_process = True
        self.pregnancy_and_adoption_validation(couple)
        if any(p.is_neighbor for p in couple.persons):
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
        """Override give birth method to include print messages."""
        if couple.is_pregnant is False:
            raise Exception("Cannot give birth if not pregnant.")

        babies = []
        if couple.expecting_num_of_children == Traits.SINGLETON:
            babies = [self.person_generator.generate_baby(couple)]
            if any(p.is_neighbor for p in couple.persons):
                self.print_singleton_message(couple, babies)
            return babies
        elif couple.expecting_num_of_children == Traits.TWINS:
            for _ in range(couple.expecting_num_of_children):
                new_baby = self.person_generator.generate_baby(couple)
                new_baby.is_twin = True
                babies.append(new_baby)
            if any(p.is_neighbor for p in couple.persons):
                self.print_twins_message(couple, babies)
            return babies
        elif couple.expecting_num_of_children == Traits.TRIPLETS:
            for _ in range(couple.expecting_num_of_children):
                new_baby = self.person_generator.generate_baby(couple)
                new_baby.is_triplet = True
                babies.append(new_baby)
            if any(p.is_neighbor for p in couple.persons):
                self.print_triplets_message(couple, babies)
            return babies
        else:
            raise Exception("Number of births is not permitted.")

    def adopt(self, couple):
        """Override adopt method to include print messages."""
        if not all([p.is_in_adoption_process for p in couple.persons]):
            raise Exception("Couple cannot adopt if not in adoption process.")

        if couple.expecting_num_of_children == Traits.ONE_CHILD:
            child = self.foster_care_system.adopt_child(couple)
            if any(p.is_neighbor for p in couple.persons):
                self.display_adoptions_message(couple, child)
            return child
        elif couple.expecting_num_of_children == Traits.SIBLING_SET:
            children = self.foster_care_system.adopt_sibling_set(couple)
            if any(p.is_neighbor for p in couple.persons):
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

    @classmethod
    def reset_pregnancy(cls, couple):
        """Set woman pregnancy to false and subtract newborns from desired num of children."""
        couple.woman.is_pregnant = False
        couple.desired_children_left -= couple.expecting_num_of_children
        couple.expecting_num_of_children = 0

    @classmethod
    def reset_adoption(cls, couple):
        """Set couple's adoption process to false and subtract adoptions from desired num of children."""
        for person in couple.persons:
            person.is_in_adoption_process = False
        couple.desired_children_left -= couple.expecting_num_of_children
        couple.expecting_num_of_children = 0
