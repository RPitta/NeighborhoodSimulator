# -*- coding: utf-8 -*-

import sys
import abc
from statistics import Statistics
from traits import Names, Professions, LifeStages
from person_generator import PersonGenerator
from person_developer import PersonDeveloper
from couple_developer import CoupleDeveloper
from couple_creator import CoupleCreator
from city import City
from neighborhood import Neighborhood

# Initialize Names, Professions and LifeStages
names = Names()
professions = Professions()
life_stages = LifeStages()

# Initialize statistics with names, professions, stages
statistics = Statistics(names, professions, life_stages)

# Initialize person generator
baby_generator = PersonGenerator(life_stages, statistics)
person_developer = PersonDeveloper(names, professions, life_stages, statistics)
couple_creator = CoupleCreator()
couple_developer = CoupleDeveloper(statistics)

# Initialize city, at last
city = City(baby_generator, person_developer, couple_creator,
            life_stages, couple_developer, statistics)

# First time jumps to remove first older generation (the one without parents)
for _ in range(20):
    city.time_jump()

# Now populate neighboorhood
neighborhood = Neighborhood()
neighborhood.populate_neighborhood(city.living_population)

# Display their stats (debugging purposes)
neighborhood.display_households()

print("\nlength of city population: " + str(len(city.living_population)))
print("length of couples: " + str(len(city.couples)))
print("length of neighbors: " + str(len(neighborhood.neighbors)))
print("length of deceased: " + str(len(city.dead_population)))
print("length of total city population: " + str(len(city.population)) + "\n")

print("\nNeighbors:\n")
for p in neighborhood.neighbors:
    print(p)

print("\nStats, for debugging purposes:\n")
for p in neighborhood.neighbors:
    attrs = vars(p)
    print(', '.join("%s: %s" % item for item in attrs.items()))
    print()
