from random import SystemRandom
import operator


class Randomizer:
    """Utility class used for returning random values."""
    def __init__(self):
        self.random = SystemRandom()

    def get_random_dict_key(self, d):
        """Returns a random key from dictionary based on given percentages."""
        if d is None or len(d) < 2 or sum(list(d.values())) not in [99.9, 100]:
            raise Exception(
                "Given dict has less than 2 items or dict values do not add up to 100.")

        dict_values = list(d.values())
        ordered_dict = sorted(d.items(), key=operator.itemgetter(1))
        ordered_list = sorted(dict_values, key=int)

        random_num = self.random.randint(1, 100)

        # Loop through the list and return the dictionary key of value
        sum_so_far = 0
        for i in range(len(ordered_list)):
            if random_num <= (ordered_list[i] + sum_so_far):
                if ordered_dict[i][0] is None or ordered_dict[i][0] not in d.keys():
                    raise Exception(
                        "Unexpected error occurred. Key not found in dict.")

                return ordered_dict[i][0]
            sum_so_far += ordered_list[i]

        # Raise exception if no matching value
        raise Exception("Key not found in dict.")

    def get_random_item(self, lst):
        """Returns a completely random item from given list."""
        if lst is None or len(lst) <= 0:
            raise Exception("Given list is empty.")
        return self.random.choice(lst)
