from traits import Traits
from utilities.randomizer import Randomizer


class CityPersonalHandler:

    def __init__(self, names, person_developer):
        self.names = names
        self.person_developer = person_developer
        self.death_handler = CityDeathHandler()

    def age_up(self, person):
        """Returns aged up person. May be dead."""
        if person.age == person.stage.end:
            if person.stage.next_stage is False:
                person = self.death_handler.die(person)
            else:
                self.set_new_stage(person)
        else:
            person.age += 1

        if person.is_death_date:
            person = self.death_handler.die(person)
        return person

    def set_new_stage(self, person):
        """Set up new stage if reached."""
        person.stage = person.stage.next_stage
        person.age += 1
        # Set new stage traits
        self.person_developer.set_new_stage_traits(person)

    def come_out(self, teen):
        """Lgbta persons come out."""
        if teen.is_trans:
            self.set_transgenders_new_traits(teen)
        return teen

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

    def set_new_name(self, person):
        """Find new name"""
        new_name = self.names.get_name(person)
        person.name = new_name


class PersonalHandler(CityPersonalHandler):
    def __init__(self, names, person_developer):
        CityPersonalHandler.__init__(self, names, person_developer)

    def set_new_stage(self, person):
        super().set_new_stage(person)
        self.display_new_stage_message(person)

    @classmethod
    def display_new_stage_message(cls, person):
        print("\n{} is now {}.\n".format(person, person.age))
        print("\n{} is now a {}.\n".format(person.fullname, person.stage))

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
        return teen

    def set_new_name(self, person):
        new_name = self.names.get_name(person)
        self.display_transgender_message(person, new_name)
        person.name = new_name

    @classmethod
    def display_transgender_message(cls, person, new_name):
        if person.is_male:
            print("\n{} has come out as transgender. His new chosen name is {}.".format(
                person, new_name))
        else:
            print("\n{} has come out as transgender. Her new chosen name is {}.".format(
                person, new_name))

    @classmethod
    def display_sexual_orientation_message(cls, person, orientation):
        print("\n{} has come out as {}.".format(person, orientation))


class CityDeathHandler:

    def die(self, person):
        """Set person's status to not alive and remove partners."""
        person.is_alive = False

        # Remove person from their partners / spouses
        if len(person.partners) > 0:
            if len(person.spouses) > 0:
                for spouse in person.spouses:
                    spouse.relationship_status = Traits.WIDOWED
                    spouse.ex_spouses.append(person)
                    spouse.spouses = [spouse for spouse in spouse.spouses if spouse != person]
            for partner in person.partners:
                if partner not in person.spouses and not partner.is_married_or_remarried:
                    partner.relationship_status = Traits.SINGLE
                    partner.ex_partners.append(person)
                    partner.spouses = [partner for partner in partner.partners if partner != person]
        return person

class DeathHandler(CityDeathHandler):

    def die(self, person):
        super().die(person)
        self.display_death_message(person)
        return person

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
        return self.person_developer.set_addiction_consequences(person)

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
        return self.person_developer.relapse_chance(person)

    def relapse(self, person):
        """Become an addict again if an ex-addict."""
        if person.was_drug_addict:
            person.is_drug_addict = True
        elif person.was_alcohol_addict:
            person.is_alcohol_addict = True
        else:
            raise Exception("Cannot relapse if not previously an addict.")
        # Set possible consequences (overdose / rehab)
        return self.person_developer.set_addiction_consequences(person)


class AddictionHandler(CityAddictionHandler):
    """Adds print messages to addiction handler."""

    def __init__(self, person_developer):
        CityAddictionHandler.__init__(self, person_developer)

    def become_an_addict(self, person):
        if person.will_become_drug_addict:
            print("\n{} has become a drug addict.".format(person))
        elif person.will_become_alcohol_addict:
            print("\n{} has become an alcohol addict.".format(person))
        return super().become_an_addict(person)

    def get_sober(self, person):
        if person.is_drug_addict:
            print("\n{} has spent some time in a rehabilitation centre and is no longer a drug addict.".format(person))
        elif person.is_alcohol_addict:
            print("\n{} has spent some time in a rehabilitation centre and is no longer an alcohol addict.".format(
                person))
        return super().get_sober(person)

    def relapse(self, person):
        if person.was_drug_addict:
            print("\n{} has relapsed and has become a drug addict again.".format(person))
        elif person.was_alcohol_addict:
            print("\n{} has relapsed and has become an alcohol addict again.".format(person))
        return super().relapse(person)


class CityMarriageHandler:
    """Handles marriage."""

    def __init__(self):
        self.randomizer = Randomizer()

    def get_married(self, couple):
        """Marriage."""
        if any(p.is_married_or_remarried for p in couple.persons):  # Skip if poly person is already married
            return couple
        self.set_married_status(couple)
        self.replace_partners_with_spouses(couple)
        self.set_shared_surname(couple)
        self.marriage_validation(couple)
        return couple

    @classmethod
    def set_married_status(cls, couple):
        for person in couple.persons:
            if len(person.ex_spouses) > 0:
                person.relationship_status = Traits.REMARRIED
            else:
                person.relationship_status = Traits.MARRIED

    @classmethod
    def replace_partners_with_spouses(cls, couple):
        """Set each other as spouses."""
        couple.person1.spouses.append(couple.person2)
        couple.person2.spouses.append(couple.person1)

    def set_shared_surname(self, couple):
        """If person is female and is married to a male, take male's surname. Else, 50/50 chance."""
        if couple.is_straight:
            couple.woman.surname = couple.man.surname
        else:
            chosen = self.randomizer.get_random_item(
                [couple.person1.surname, couple.person2.surname])
            for person in couple.persons:
                person.surname = chosen

    @classmethod
    def marriage_validation(cls, couple):
        if not all([p.is_married_or_remarried for p in couple.persons]):
            raise Exception(
                "Married couple is not set as married.")
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
        return couple

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
        return couple

    @classmethod
    def set_divorced_status(cls, couple):
        for person in couple.persons:
            person.relationship_status = Traits.DIVORCED

    @classmethod
    def remove_spouses(cls, couple):
        for person in couple.persons:
            person.spouses = []

    @classmethod
    def add_to_exspouses(cls, couple):
        couple.person1.ex_spouses.append(couple.person2)
        couple.person2.ex_spouses.append(couple.person1)

    @classmethod
    def revert_username(cls, couple):
        for person in couple.persons:
            person.surname = person.original_surname

    def get_separated(self, couple):
        """Handles couple separation"""
        self.set_separated_status(couple)
        self.remove_partners(couple)
        self.add_to_expartners(couple)
        return couple

    @classmethod
    def set_separated_status(cls, couple):
        for person in couple.persons:
            if person.is_married_or_remarried is False and len(person.partners) < 2:
                person.relationship_status = Traits.SEPARATED

    @classmethod
    def remove_partners(cls, couple):
        for person in couple.persons:
            person.partners = [p for p in person.partners if p != person]

    @classmethod
    def add_to_expartners(cls, couple):
        couple.person1.ex_partners.append(couple.person2)
        couple.person2.ex_partners.append(couple.person1)


class DivorceHandler(CityDivorceHandler):
    """Adds print messages to divorce handler."""

    def get_divorced(self, couple):
        self.display_divorce_message(couple)
        return super().get_divorced(couple)

    @classmethod
    def display_divorce_message(cls, couple):
        print("\n{} and {} have gotten a divorce.".format(
            couple.person1, couple.person2))

    def get_separated(self, couple):
        self.display_separation_message(couple)
        return super().get_separated(couple)

    @classmethod
    def display_separation_message(cls, couple):
        print("\n{} and {} have separated.".format(
            couple.person1, couple.person2))


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
            return couple
        couple.expecting_num_of_children = self.statistics.get_pregnancy_num_of_children()
        couple.woman.is_pregnant = True
        self.pregnancy_and_adoption_validation(couple)
        return couple

    def start_adoption_process(self, couple):
        """Set adoption process to True and set statistical number of expecting children"""
        couple.expecting_num_of_children = self.statistics.get_adoption_num_of_children()
        for person in couple.persons:
            person.is_in_adoption_process = True
        self.pregnancy_and_adoption_validation(couple)
        return couple

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
        return couple

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
        return couple


class PregnancyHandler(CityPregnancyHandler):
    def __init__(self, person_generator, statistics, foster_care_system):
        CityPregnancyHandler.__init__(self, person_generator, statistics, foster_care_system)

    def get_pregnant(self, couple):
        super().get_pregnant(couple)
        self.print_expecting_num_of_bio_children(couple)
        return couple

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
        return couple

    @classmethod
    def print_expecting_num_of_adoptions(cls, couple):
        """Display number of adoptions that couple is expecting."""
        if couple.expecting_num_of_children == Traits.ONE_CHILD:
            print("\n{} and {} have began the process to adopt a child.".format(
                couple.person1, couple.person2))
        elif couple.expecting_num_of_children in Traits.SIBLING_SET:
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
            print("\n{} and {} have adopted a {} aged {}: {}.".format(
                couple.person1, couple.person2, child.baby_gender, child.age, child.name))
            return [child]
        elif couple.expecting_num_of_children == Traits.SIBLING_SET:
            children = self.foster_care_system.adopt_sibling_set(couple)
            print("\n{} and {} have adopted a sibling set:".format(couple.person1, couple.person2))
            for child in children:
                print("{} ({}, age {})".format(child.name, child.baby_gender, child.age))
            return children
        else:
            raise Exception("Wrong number of adoptions.")

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
