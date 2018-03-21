
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
        self.members_list.append(person)

    def remove_member(self, person):
        self.members_list.remove(person)

    def add_pet(self, pet):
        self.pets_list.append(pet)

    def remove_pet(self, pet):
        self.pets_list.remove(pet)
