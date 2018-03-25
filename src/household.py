
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
            if person.partner in self.members:
                desc += "\nPartner: {}".format(person.partner)
            if person.spouse in self.members:
                desc += "\nSpouse: {}".format(person.spouse)
            if len(person.partners) == 1 and person.spouse is None:
                desc += "\nPartner: {}".format(person.partners[0])
            for child in person.children:
                if child in self.members:
                    desc += "\nChild: {}".format(child)
            if person.father in self.members:
                desc += "\nFather: {}".format(person.father)
            if person.mother in self.members:
                desc += "\nMother: {}".format(person.mother)
            for sibling in person.full_siblings:
                if sibling in self.members:
                    desc += "\nSibling: {}".format(sibling)
            for half_sibling in person.half_siblings:
                if half_sibling in self.members:
                    desc += "\nHalf-Sibling: {}".format(half_sibling)
            for grandchild in person.grandchildren:
                if grandchild in self.members:
                    desc += "\nGrandchild: {}".format(grandchild)
            for uncle in person.uncles:
                if uncle in self.members:
                    desc += "\nUncle: {}".format(uncle)
            for aunt in person.aunts:
                if aunt in self.members:
                    desc += "\nAunt: {}".format(aunt)
            for nephew in person.nephews:
                if nephew in self.members:
                    desc += "\nnNephew: {}".format(nephew)
            for niece in person.nieces:
                if niece in self.members:
                    desc += "\nNiece: {}".format(niece)
            print(desc)

    def household_validation(self):
        if len(set(self.members)) != len(self.members):
            raise Exception("List of household members contains duplicates.")