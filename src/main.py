# -*- coding: utf-8 -*-

import sys
import abc
from utilities.statistics import Statistics
from utilities.randomizer import Randomizer
from utilities.compatibility import Compatibility
from life_stage import Baby, Child, Teen, YoungAdult, Adult, Senior
from traits import Names, Professions, Traits, LifeStages
from person_generator import PersonGenerator
from person_developer import PersonDeveloper
from relationship_developer import RelationshipDeveloper
from relationship_generator import RelationshipGenerator
from world import World

# Traits: Names, Professions, Traits and LifeStages
names = Names()
professions = Professions()
traits = Traits()
life_stages = LifeStages()

randomizer = Randomizer()
statistics = Statistics(names, professions, traits, life_stages, randomizer)

developer = PersonDeveloper(
    names, professions, traits, life_stages, randomizer, statistics)
generator = PersonGenerator(
    names, professions, traits, life_stages, statistics, developer)
compatibility = Compatibility()
relationship_developer = RelationshipDeveloper(randomizer, statistics)
relationship_generator = RelationshipGenerator(traits, compatibility, randomizer, statistics, relationship_developer)


world = World(generator, developer, relationship_generator, traits, life_stages, statistics, randomizer, relationship_developer)


world.time_jump()
world.time_jump()
world.time_jump()
world.time_jump()
world.time_jump()
world.time_jump()
world.time_jump()
world.time_jump()
world.time_jump()

for p in world.get_population():
    print(p)

print("length of population: " + str(len(world.living_population)))
print("length of couples: " + str(len(world.couples)))
print("length of romanceable population: " +
      str(len(world.romanceable_outsiders)))
print("length of unromanceable population: " +
      str(len(world.unromanceable_outsiders)))
print("length of partnered population: " + str(len(world.partnered_outsiders)))
print("length of deceased: " + str(len(world.dead_population)))
print("length of total population: " + str(len(world.population)))


def validate_choice(prompt, valid_values):
    '''Validates user input.'''

    error_message = "\nValid commands: " + \
        ", ".join((str(x) for x in valid_values))

    while True:
        choice = input(prompt).lower()
        if choice in str(valid_values) and choice != '':
            return choice
        else:
            print(error_message)

for p in world.population:
    if p.in_love_with_family:
        print("{} is in love with a family member.".format(p.name))


for p in world.living_population:
    attrs = vars(p)
    print(', '.join("%s: %s" % item for item in attrs.items()))
    print()

for c in world.couples:
    attrs = vars(c)
    print(', '.join("%s: %s" % item for item in attrs.items()))
    print()

def time_function():

    for p in world.get_population():
        print(p)

    while True:
        print("Type 't' to time jump or 'q' to exit.")

        choice = validate_choice("\n>> ", ['t', 'q'])

        if choice == "t":
            world.time_jump()
            for p in world.get_population():
                print(p)
            print("length: " + str(len(world.population)))
        if choice == "q":
            sys.exit(0)
            return False


class Shape(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def draw(self, color):
        pass


class Triangle(Shape):
    def draw(self, color):
        print("Drawing Triangle with color " + color)


class Circle(Shape):
    def draw(self, color):
        print("Drawing Circle with color " + color)


class Drawing(Shape):
    def __init__(self):
        self.shapes = []

    def draw(self, color):
        for sh in self.shapes:
            sh.draw(color)

    def add(self, sh):
        self.shapes.append(sh)

    def remove(self, sh):
        self.shapes.remove(sh)

    def clear(self):
        print("Clearing all the shapes from drawing")
        self.shapes = []


def do():
    tri1 = Triangle()
    tri2 = Triangle()
    cir = Circle()

    drawing = Drawing()
    drawing.add(tri1)
    drawing.add(tri2)
    drawing.add(cir)

    drawing.draw("Red")

    drawing.clear()

    drawing.add(tri1)
    drawing.add(cir)
    drawing.draw("Green")


if __name__ == '__main__':
    pass

""" for relationship in world.population:
    attrs = vars(relationship)
    print(', '.join("%s: %s" % item for item in attrs.items()))
    print() """


"""
BUILDING

Building has 4 floors.
Each floor has 4 apartments where 4 different families live, making it a total of 16 apartment flats / families.
Apartment flat names: 1-A, 1-B, 1-C, 1-D | 2-A, 2-B, 2-C, 2-D | 3-A, 3-B, 3-C, 3-D | 4-A, 4-B, 4-C, 4-D

LIFE STAGES

Baby(0 - 4)
Child(5 - 12)
Teen(13 - 17)
Young Adult(18 - 30)
Adult(31 - 59)
Senior(60+)

DEATH
Note: Persons can die from old age, illness, accident or suicide.

Of old age: 50%
Before old age: 50%

Senior: 80%
    Illness: 70%
    Accident: 20%
    Suicide: 10%
Adult: 10%
    Illness: 45%
    Accident: 45%
    Suicide: 10%
Young Adult: 4%
    Illness: 30%
    Accident: 60%
    Suicide: 10%
Teen: 3%
    Illness: 50%
    Suicide: 50%
Child: 2%
    Illness: 100%
Baby: 1%
    Illness: 100%

BABIES

Gender: 50/50 chance of being born male/female.
Number:
    Singleton: 93%
    Twins: 5%
    Triplets: 2%

SEXUAL IDENTITY AND ORIENTATION
Note: Known in the teen stage.

Cisgender: 98%
Transgender: 2%
    50/50 chance of being born transgender

Heterosexual: 93%
Gay/Bisexual: 5%
    50/50 chance of being born gay/bisexual.
Asexual/Graysexual: 2%
    50/50 chance of being born asexual/graysexual
        50/50 chance of being born romantic/aromantic.
            If romantic:
                95 % chance of being heteroromantic.
                5 % chance of being homo/biromantic.
                    50/50 chance of being born homo/biromantic.


MINORITIES ACCEPTANCE
Note: Minorities included: LGBT+, poly relationships and incestuous relationships.

Chance of having a supportive family: 60%
Chance of having a nonsupportive family: 40%
    Consequences:
        Move out(as Young Adult): 50%
        Thrown out(as Young Adult): 40%
        Suicide(as Teen): 10%

PREGNANCY OR ADOPTION
Note: Pregnancy and adoption start in the Young Adult stage.

Can have children: 90%
    Wants children: 70%
        Type:
            Pregnancy: 90%
            Adoption: 10%
        Number of children:
            1: 35%
            2: 35%
            3: 20%
            4: 10%
    Does not want children: 30%

Cannot have children: 10%
    Wants children: 70%
        Type:
            Adoption: 100%
        Number of children:
            1: 50%
            2: 30%
            3: 15%
            4: 5%
    Does not want children: 30%


RELATIONSHIP ORIENTATION

Monogamous: 80%
Polyamorous: 20%

LOVE

Non-incest: 95%
Incest: 5%
    First cousins: 30%
    Siblings: 30%
    Parent/Child: 20%
    Uncle-Aunt/Nephew-Niece: 20%

RELATIONSHIP STATUS
Note: Domestic partnerships and marriages start in the Young Adult stage.

Marriage: 70%
    When:
        Young Adult: 40%
        Adult: 40%
        Senior: 20%
    Divorce:
        Will divorce: 60%
            When:
                Young Adult: 40%
                Adult: 40%
                Senior: 20%
        Will not divorce: 40%

Domestic partnership: 30%
    Separation:
        Will separate: 60%
             When:
                Young Adult: 40%
                Adult: 40%
                Senior: 20%
        Will not separate: 40%

"""
