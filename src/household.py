class Household:

    def __init__(self, apartment_id):
        self.apartment_id = apartment_id
        self.members_list = []
        self.pets_list = []

    @property
    def members(self):
        return self.members_list

    @property
    def pets(self):
        return self.pets_list

    def add_member(self, person):
        """Add member and set matching apartment IDs."""
        person.apartment_id = self.apartment_id
        self.members_list.append(person)

    def remove_member(self, person):
        """Remove member and their apartment id."""
        if person not in self.members_list:
            raise Exception("Can't remove a person who wasn't a household member.")

        person.apartment_id = -1
        self.members_list = [member for member in self.members if member != person]

    def add_pet(self, pet):
        """Add pet and set matching apartment IDs."""
        self.pets_list.append(pet)
        pet.apartment_id = self.apartment_id

    def remove_pet(self, pet):
        """Remove pet and its apartment id."""
        pet.apartment_id = self.apartment_id
        self.pets_list.remove(pet)

    def display(self):
        print("\n***** Apartment ID " + str(self.apartment_id) + " ********")
        for person in self.members:
            desc = "\nApartment ID: {}\nName: {}\nSurname: {}\nGender: {}\nAge: {}\nSocial Class: {}\nCivil Status: {}\nProfession: {}\nEmployment: {}".format(
                person.apartment_id,
                person.name,
                person.surname,
                person.gender,
                person.age,
                person.social_class,
                person.relationship_status,
                person.occupation,
                person.employment
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
                    desc += "\nParent: {}".format(child)
            for parent in person.adoptive_parents:
                if parent in self.members:
                    desc += "\nParent: {}".format(child)
            for step_parent in person.step_parents:
                if step_parent in self.members:
                    desc += "\nStep-parent: {}".format(child)
            for sibling in person.siblings:
                if sibling in self.members:
                    desc += "\nSibling: {}".format(sibling)
            print(desc)

    def household_validation(self):
        """Validation of household members."""
        for member in self.members:
            print(member)
        if len(set(self.members)) != len(self.members):
            raise Exception("List of household members contains duplicates.")
