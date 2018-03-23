# -*- coding: utf-8 -*-

import sys
import abc
from statistics import Statistics
from traits import Setup, LifeStages
from baby_generator import BabyGenerator
from person_developer import PersonDeveloper
from couple_developer import CoupleDeveloper
from couple_creator import CoupleCreator
from city_couple_creator import CityCoupleCreator
from city import City
from neighborhood import Neighborhood

# Initialize Names, Professions and LifeStages
setup = Setup()
life_stages = LifeStages()

# Initialize statistics with names, professions, stages
statistics = Statistics(setup, life_stages)

# Initialize person generator
baby_generator = BabyGenerator(life_stages, statistics)
person_developer = PersonDeveloper(setup, life_stages, statistics)
city_couple_creator = CityCoupleCreator()
couple_creator = CoupleCreator()
couple_developer = CoupleDeveloper(statistics)

# Initialize city, at last
city = City(baby_generator, person_developer, city_couple_creator,
            life_stages, couple_developer, statistics)

# First time jumps to remove first older generation (the one without parents)
for _ in range(20):
    city.time_jump_city()

# Now populate neighborhood
neighborhood = Neighborhood(baby_generator, person_developer, couple_creator,
                            life_stages, couple_developer, statistics)
neighborhood.populate_neighborhood(city.living_population, city.city_couples)

# Display their stats (debugging purposes)
neighborhood.display_households()

print()
for _ in range(10):
    city.time_jump_city()
    neighborhood.time_jump_neighborhood(city.romanceable_outsiders)

for neighbor in neighborhood.neighbors:
    # Update city population with neighborhood newborns
    if neighbor not in city.population:
        city.population.append(neighbor)
    # Then remove dead neighbors from neighbors list and their assigned household
    if neighbor.is_alive is False:
        for household in neighborhood.households:
            if neighbor.apartment_id == household.apartment_id:
                household.remove_member(neighbor)
        neighborhood.neighbors.remove(neighbor)

print("\nStats, for debugging purposes:\n")
for p in neighborhood.neighbors:
    attrs = vars(p)
    print(', '.join("%s: %s" % item for item in attrs.items()))
    print()

print("\nlength of living city+neighborhood population: " +
      str(len(city.living_population)))
print("length of living city population: " + str(len(city.living_outsiders)))
print("length of neighbors: " + str(len(neighborhood.neighbors)))
print("length of city couples: " + str(len(city.city_couples)))
print("length of neighbor couples: " + str(len(neighborhood.neighbor_couples)))
print("length of deceased: " + str(len(city.dead_population)))
print("length of total living+dead population: " +
      str(len(city.population)) + "\n")
