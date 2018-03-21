# NeighborhoodSimulator

Neighborhood Simulator is, as the name suggests, a simulator of a neighborhood (a small-sized apartment building) based on real-life statistics. For example, what'd be the ratio of males/females or heterosexuals/homosexuals or married/divorced people in a neighborhood of 30 people? What are the chances that you'll see a couple give birth to twins? Or that a polyamorous person will date two persons at the same time? What if a teen comes out as transgender, or an adult couple turns out to also be full-siblings? How will the families and neighbors react to one another's life choices and developments? Which neighbors are going to be friends and which will not be able to stand each other? How will they deal with a death in the family / neighborhood, and what are the chances of a newborn dying or a teen committing suicide?

We'll assume two facts: first, the building is located a bit far from the city, so neighbors will be friendlier/closer to each other than they normally would be if they lived in a large city. And two, the location will likely be New Jersey, as very few other US states allow legal consanguinamory.

So before the user starts a new game, we first populate the city with a big number of random people, and time jump until the first generation (the one that is born without parents) is dead.
Then, we populate the neighborhood by choosing 10 (or whichever number of households the building has) random unrelated adults, and move them and their families to each apartment.
So now the game can begin for the user. We start by presenting him/her the neighborhood (who lives in each household and their basic info) and then the user can time jump at any moment so that he/she can see the neighbors growing up and their life developments year by year.

Pending:
* Empty household must be handled
* Empty household except for underage child must be handled
* Pets for each household (statistical chance, statistical number and type of pets).
* Neighborhood friendship/enmity system
* Upper class / Middle class / Lower class for each person (statistical chance)
* Disabilities such as autistic kids (statistical chance)
* Addictions such as drug / alcohol addict (statistical chance), and rehabilitation options
* Step-families
* Gay adoption
* Throuple biological / adopted children (?)
* Consang biological / adopted children (?)
* Consequences of coming out if conservative family (statistical chance for being thrown out / moving out / suicide)
* Intermittent employment (statistical chance)
* Once young adult: university vs working vs not doing anything (statistical chance, and also may depend on class)
* Personality and hobbies for neighbors
* Setting option for users: realistic statistics and custom statistics (user can modify for example the statistical chance for male/female to a 20/80 ratio instead of default 50/50)
* Save/Load game system
* Statistics need to be further researched and adjusted to be as close to real-life as possible.

Bugs:
* Too many to list... Project needs bug cheking, error handling / debugging ASAP. Also, it's currently SLOW as fuck.

Contribution:
Please anyone feel free to create a branch and contribute regardless of programming/python skill level, as long as you know what you're doing and won't just make a mess of things lol. I am a beginner myself! :)
