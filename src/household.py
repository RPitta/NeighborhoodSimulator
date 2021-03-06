from traits import Traits


class Household:
    """Household base class."""

    CHILD_IMPACT_FOR_INCOME = 0.1  # value from 0 to 1

    # household financial stage
    SAFE = 0
    BROKE = 1
    HOMELESS = 2

    def __init__(self, apartment_id):
        self.apartment_id = apartment_id
        self.members_list = []
        self.pets_list = []
        self.finance_status = self.SAFE

    @property
    def members(self):
        return self.members_list

    @property
    def pets(self):
        return self.pets_list

    @property
    def household_income(self):
        """Returns average household income from all employed adults."""
        total_salary = 0
        total_working_age_member = 0
        for p in self.members:
            total_salary += p.job.salary
            total_working_age_member += 1 if p.age >= Traits.YOUNGADULT.start else self.CHILD_IMPACT_FOR_INCOME
        if total_working_age_member == 0:
            return 0
        return total_salary / total_working_age_member

    @property
    def social_class(self):
        """Returns social class which is within household's income."""
        for social_class in Traits.SOCIAL_CLASSES:
            if social_class.belongs_to(self.household_income):
                return social_class
        raise Exception("No matching social class within given household income.")

    @property
    def is_neighbor(self):
        """check if member is one of neighborhood"""
        return self.members_list[0].is_neighbor

    def set_living_inside(self):
        """set all member move to the neighborhood"""
        for p in self.members_list:
            p.is_neighbor = True

    def set_living_outside(self):
        """set all member leaving the neighborhood"""
        for p in self.members_list:
            p.is_neighbor = False

    def add_member(self, person):
        """Add member and set matching apartment IDs."""
        person.apartment_id = self.apartment_id
        person.is_neighbor = True
        self.members_list.append(person)

    def remove_member(self, person):
        """Remove member and their apartment id."""
        if person not in self.members:
            raise Exception("Can't remove a person who wasn't a household member.")

        person.apartment_id = -1
        person.is_neighbor = False
        self.members_list = [p for p in self.members if p != person]

    def add_pet(self, pet):
        """Add pet and set matching apartment IDs."""
        pet.apartment_id = self.apartment_id
        self.pets_list.append(pet)

    def remove_pet(self, pet):
        """Remove pet and its apartment id."""
        pet.apartment_id = self.apartment_id
        self.pets_list.remove(pet)

    def display(self):
        print("\n***** Apartment ID " + str(self.apartment_id) + " ********")

        for person in self.members:
            desc = "\nApartment ID: {}\nName: {}\nSurname: {}\nGender: {}\nAge: {}\nSocial Class: {}\nCivil Status: {}\nLatest Education: {}\nProfession: {}\nEmployment: {}\nSalary per Year: {} [{}]".format(
                person.apartment_id,
                person.name,
                person.surname,
                person.gender,
                person.age,
                self.social_class.name,
                person.relationship_status,
                person.education,
                person.job.title,
                person.job.employment,
                person.job.salary,
                person.social_class.name,
            )
            for spouse in person.spouses:
                desc += "\nSpouse: {}".format(spouse)
            for partner in person.partners:
                if partner not in person.spouses and partner in self.members:
                    desc += "\nPartner: {}".format(partner)
            for child in person.children:
                if child in self.members:
                    desc += "\nChild: {}".format(child)
            for child in person.adoptive_children:
                if child in self.members:
                    desc += "\nChild: {}".format(child)
            for parent in person.parents:
                if parent in self.members:
                    desc += "\nParent: {}".format(parent)
            for parent in person.adoptive_parents:
                if parent in self.members:
                    desc += "\nParent: {}".format(parent)
            for step_parent in person.step_parents:
                if step_parent in self.members:
                    desc += "\nStep-parent: {}".format(step_parent)
            for sibling in person.siblings:
                if sibling in self.members:
                    desc += "\nSibling: {}".format(sibling)
            print(desc)

    def household_validation(self):
        """Validation of household members."""
        if any(p.is_alive is False for p in self.members):
            raise Exception("Household member is dead.")
        if len(set(self.members)) != len(self.members):
            raise Exception("List of household members contains duplicates.")
        if any(p.apartment_id != self.apartment_id for p in self.members):
            raise Exception("Household member has a wrongly assigned apartment ID.")
