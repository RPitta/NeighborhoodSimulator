import random
import operator


class Randomizer:

    def get_random_dict_key(self, d):
        """Returns a random key from dictionary based on given percentages."""

        # Dict validation
        if d is None or len(d) < 2:
            raise Exception("Unexpected error occurred. Given dict is wrong.")
        if sum(list(d.values())) != 100:
            raise Exception(
                "Unexpected error occurred. Given dict values do not add up to 100.")

        dict_values = list(d.values())
        ordered_dict = sorted(d.items(), key=operator.itemgetter(1))
        ordered_list = sorted(dict_values, key=int)

        # Random number from 1 to 100 (included)
        random_num = random.randint(1, 100)

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
        raise Exception("Unexpected error occurred. Key not found in dict.")

    def get_random_list_item(self, lst):
        """Returns a completely random item from list."""
        if lst is None or len(lst) <= 0:
            raise Exception("Unexpected error occurred. Given list is empty.")

        return random.choice(lst)
