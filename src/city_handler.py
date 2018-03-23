from traits import Traits
from utilities.randomizer import Randomizer


class PersonalHandler:

    def __init__(self, statistics, person_developer):
        self.statistics = statistics
        self.death_handler = DeathHandler()
        self.person_developer = person_developer

    def age_up(self, person):
        """Most important function: age up person.
        Returns aged up person. May be dead."""
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
        # Set new stage and age
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
        if person.is_female:
            person.gender = Traits.MALE
        else:
            person.gender = Traits.FEMALE

        # Find new name
        new_name = self.statistics.get_name(person)
        if new_name is None:
            raise Exception("Name is null. List must be empty.")

        # Assign new name
        person.name = new_name


class DeathHandler:

    def die(self, person):

        person.is_alive = False

        # Remove person from their partner(s) / spouse
        if person.partner is not None:
            person.partner.relationship_status = Traits.SINGLE
            person.partner.in_love_date = -1
            person.partner.partner = None
        if person.spouse is not None:
            person.spouse.relationship_status = Traits.WIDOWED
            person.spouse.in_love_date = -1
            person.spouse.spouse = None

        if person.partners is not None and len(person.partners) > 0:
            for partner in person.partners:
                partner.partner = None
                partner.partners = [p for p in partner.partners if p != person]
                if len(partner.partners) == 0 and partner.spouse is None:
                    partner.relationship_status = Traits.SINGLE
        return person

class MarriageHandler:

    def __init__(self):
        self.randomizer = Randomizer()

    def get_married(self, couple):

        # If poly person is already married by the time this couple is set to marry, skip.
        for person in couple.persons:
            if person.is_married_or_remarried:
                return couple

        for person in couple.persons:
            if len(person.ex_spouses) > 0:
                person.relationship_status = Traits.REMARRIED
            else:
                person.relationship_status = Traits.MARRIED

        self.replace_partners_with_spouses(couple)
        self.set_shared_surname(couple)
        self.marriage_validation(couple)

        return couple

    def replace_partners_with_spouses(self, couple):
        # Set each other as spouses
        couple.person1.spouse = couple.person2
        couple.person2.spouse = couple.person1
        # Remove partner if mono
        for person in couple.persons:
            person.partner = None
        # Remove person2 from person1's partners if poly
        if couple.person2 in couple.person1.partners:
            couple.person1.partners.remove(couple.person2)
        # Remove person1 from person2's partners if poly
        if couple.person1 in couple.person2.partners:
            couple.person2.partners.remove(couple.person1)

    def set_shared_surname(self, couple):
        # If person is female and is married to a male, take male's surname. Else, 50/50 chance.
        if couple.is_straight:
            couple.woman.surname = couple.man.surname
        else:
            chosen = self.randomizer.get_random_item(
                [couple.person1.surname, couple.person2.surname])
            for person in couple.persons:
                person.surname = chosen

        # Validation
        if couple.person1.surname != couple.person2.surname:
            raise Exception("Married couple does not have the same surname.")

    def marriage_validation(self, couple):
        if not all([couple.persons[0].is_married_or_remarried for p in couple.persons]):
            raise Exception(
                "Married couple is not set as married.")
        if any([couple.persons[0].spouse is None for p in couple.persons]):
            raise Exception("Married couple has no assigned spouse.")
        if couple.marriage_date > couple.oldest.age:
            raise Exception(
                "Married couple has marriage date set in the future.")
        if not all([couple.persons[0].surname == p.surname for p in couple.persons]):
            raise Exception(
                "Married couple does not have the same surname.")


class DivorceHandler:

    def get_divorced(self, couple):
        """Handles couple divorce"""
        for person in couple.persons:
            person.relationship_status = Traits.DIVORCED

        self.remove_spouses(couple)
        self.add_to_exspouses(couple)
        self.revert_username(couple)

        return couple

    def remove_spouses(self, couple):
        for person in couple.persons:
            person.spouse = None

    def add_to_exspouses(self, couple):
        couple.person1.ex_spouses.append(couple.person2)
        couple.person2.ex_spouses.append(couple.person1)

    def revert_username(self, couple):
        for person in couple.persons:
            person.surname = person.original_surname

    def get_separated(self, couple):
        """Handles couple separation"""
        for person in couple.persons:
            if person.is_married_or_remarried is False and len(person.partners) < 2:
                person.relationship_status = Traits.SEPARATED

        self.remove_partners(couple)
        self.add_to_expartners(couple)

        return couple

    def remove_partners(self, couple):
        for person in couple.persons:
            person.partner = None
            if len(person.partners) > 1:
                person.partners = [p for p in person.partners if p != person]

    def add_to_expartners(self, couple):
        couple.person1.ex_partners.append(couple.person2)
        couple.person2.ex_partners.append(couple.person1)


class PregnancyHandler:

    def __init__(self, person_generator, statistics):
        self.person_generator = person_generator
        self.statistics = statistics
        self.randomizer = Randomizer()

    def get_pregnant(self, couple):
        """Set pregnancy to True and set statistical number of expecting children."""

        # If poly woman has already gotten pregnant / had max children with another man ->
        # Reset birth date and skip getting pregnant.
        if couple.woman.is_pregnant or any(person.has_max_num_of_children for person in couple.persons):
            couple.birth_date = -1
            return couple

        couple.expecting_num_of_children = self.statistics.get_pregnancy_num_of_children()
        couple.woman.is_pregnant = True

        # Validation
        self.pregnancy_and_adoption_validation(couple)

        return couple

    def start_adoption_process(self, couple):
        """Set adoption process to True and set statistical number of expecting children"""
        couple.expecting_num_of_children = self.statistics.get_adoption_num_of_children(
            couple)
        for person in couple.persons:
            person.is_in_adoption_process = True

        # Validation
        self.pregnancy_and_adoption_validation(couple)

        return couple

    def pregnancy_and_adoption_validation(self, couple):
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
            if couple.expecting_num_of_children not in Traits.ALLOWED_NUM_OF_ADOPTIONS:
                raise Exception(
                    "Couple's expecting number of adoptions is not permitted.")
            if all([person.can_have_bio_children for person in couple.persons]):
                raise Exception(
                    "Couple can have biological children yet they are adopting.")

    def give_birth(self, couple):
        """Returns newborns from given pregnant couple."""
        # Validation
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

        # Validation
        if babies is None or len(babies) <= 0:
            raise Exception("Babies list is null.")

        return babies

    def reset_pregnancy(self, couple):
        """Set woman pregnancy to false and substract newborns from desired num of children."""
        couple.woman.is_pregnant = False
        couple.desired_children_left -= couple.expecting_num_of_children
        couple.expecting_num_of_children = 0
        return couple

    def adopt(self, couple):
        """Returns adoptions from given couple."""
        # Validation
        if not all([p.is_in_adoption_process for p in couple.persons]):
            raise Exception("Couple cannot adopt if not in adoption process.")

        babies = []
        for _ in range(couple.expecting_num_of_children):
            new_baby = self.person_generator.generate_baby(couple)
            new_baby.is_adopted = True
            babies.append(new_baby)

        # Validation
        if babies is None or len(babies) <= 0:
            raise Exception("Babies list is null.")

        return babies

    def reset_adoption(self, couple):
        """Set couple's adoption process to false and substract adoptions from desired num of children."""
        for person in couple.persons:
            person.is_in_adoption_process = False
        couple.desired_children_left -= couple.expecting_num_of_children
        couple.expecting_num_of_children = 0
        return couple