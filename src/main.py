# -*- coding: utf-8 -*-

import sys
import abc
from statistics import Statistics
from traits import Names, Professions, LifeStages
from person_generator import PersonGenerator
from person_developer import PersonDeveloper
from couple_developer import CoupleDeveloper
from couple_creator import CoupleCreator
from world import World

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

# Initialize world, at last
world = World(baby_generator, person_developer, couple_creator,
              life_stages, couple_developer, statistics)

#  First time jumps to remove first older generation (the one without parents)
for _ in range(80):
    world.time_jump()

# Now populate neighboorhood
world.populate_neighborhood()

# Display their stats (debugging purposes)
for p in world.display_households():
    print(p)

print("\nlength of population: " + str(len(world.living_population)))
print("length of couples: " + str(len(world.couples)))
print("length of neighbors: " + str(len(world.neighbors)))
print("length of deceased: " + str(len(world.dead_population)))
print("length of total population: " + str(len(world.population)) + "\n")

print("\nNeighbors:")
for p in world.neighbors:
    print(p)

print("\nStats, for debugging purposes:\n")
for p in world.neighbors:
    attrs = vars(p)
    print(', '.join("%s: %s" % item for item in attrs.items()))
    print()
