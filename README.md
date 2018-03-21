# NeighborhoodSimulator

Neighborhood Simulator is, as the name suggests, a simulator of a neighborhood (a small-sized apartment building) based on real-life statistics. For example, what'd be the ratio of males/females or heterosexuals/homosexuals or married/divorced people in a neighborhood of 30 people? What are the chances that you'll see a couple give birth to twins? Or that a polyamorous person will date two persons at the same time? What if a teen comes out as transgender, or an adult couple turns out to also be full-siblings? How will the families and neighbors react to one another's life choices and developments? Which neighbors are going to be friends and which will not be able to stand each other? How will they deal with a death in the family / neighborhood, and what are the chances of a newborn dying or a teen committing suicide?

We'll assume two facts: first, the building is located a bit far from the city, so neighbors will be friendlier/closer to each other than they normally would be if they lived in a large city. And two, the location will likely be New Jersey, as very few other US states allow legal consanguinamory.

So before the user starts a new game, we first populate the city with a big number of random people, and time jump until the first generation (the one that is born without parents) is dead.
Then, we populate the neighborhood by choosing 10 (or whichever number of households the building has) random unrelated adults, and move them and their families to each apartment.
So now the game can begin for the user. We start by presenting him/her the neighborhood (who lives in each household and their basic info) and then the user can time jump at any moment so that he/she can see the neighbors growing up and their life developments year by year.

**RULES**

(always modifiable if needed, and many haven't been implemented yet)

HOUSEHOLD
* Each apartment/household has an ID (example: 1A, 1B, 1C - 2A, 2B, 2C, - 3A, 3B, 3C...)
* Each household can have a number of pets (cats, dogs, fish, rabbits, hamsters, birds).
* Pets have their own lifespan and will die once old age is reached.
* Empty households will be refilled (with either another neighbor household that is full, or with outsiders)
* If parents and any other persons within a household die, and an underage child remains, he/she will move out to live with a relative (or be taken from social services if no relatives)

BABIES
* Newborns are aged "0" (referring to being only days alive and having not reached yet 12 months)
* Newborns take their father's surname (regardless of whether the parents are married or not) unless adopted by a single female.
* Newborns have the same social class as their parents.
* Babies aged 3 can become autistic (high-functioning or not). If not high-functioning, autistic persons will be undateable and will always live with parents/siblings.

DEATH
* Death can happen at any age starting from age 1. Old age set at 80 at the moment, but should be increased.
* Possible death causes depend on age: if baby/child, it can only be from an illness. Otherwise, it can be from an illness, (road) accident, suicide, overdose, or old age.
* A dead family member can cause their parent/sibling/child/partner to become depressed; they will either recover through therapy, or commit suicide.
* If one person from an unmarried couple dies, the other one will have a civil status of Single. If married, they will be Widowed.
* Death in the neighborhood will cause reactions / funeral attendance by the neighbors.

PROFESSIONS
* Persons can start working at 18. They will decide to either go to university, work, or live off their parents (if upperclass)
* Persons will choose a random profession (but akin to their personality)
* Persons will be intermittently employed/unemployed throughout life.
* If unemployed for a long time and the person lives alone or is otherwise the only family provider, and their social class was middle/low to begin with, they may stop paying rent and become homeless / move out of the neighborhood. 
* Persons who have a specific profession such as actors or politicians will be able to get rich / famous and may cause reactions among the neighborhood.

ADDICTIONS
* Persons over 18 can become drug or alcohol addicts. 
* They will eventually either be sent to a rehabilitation facility, or overdose.
* They can relapse after years being sober.

RELATIONSHIPS
* Persons can start getting into committed relationships once young adults (18). Teenage "crushes" not implemented (yet?).
* Persons realize their relationship orientation (monoamorous/polyamorous) at 18+.
* Poly persons can only date 2 persons at the same time. (Should increase this in the future?)
* Intergenerational relationships are considered to be relationships with at least a 20-year age difference (youngest must always be of age).
* Throuples (or triads) are considered to be relationships between three poly persons all romantically involved with each other.
* Consanguineous relationships are considered to be relationships between adult relatives (by blood or adoption); sibling/sibling or half-sibling/half-sibling, parent/child, cousin/cousin and uncle-aunt/niece-nephew. Grandparent/grandchild not allowed due to its extreme rarity. Romantic relationships between step-relatives and in-laws count as typical straight/gay but may also be subject to family/neighborhood reactions.
* Who can have committed relationships: everyone except aromantic asexuals (and those who wish to be single, obviously).
* Who can get married: straight/gay couples. Throuples and consang couples can't legally marry AFAIK.

PREGNANCY AND ADOPTION
* Couples can only have childen if both want to.
* Couples can only have biological children if neither were born infertile. Otherwise, they'll resort to adoption.
* Pregnancy and adoption can happen from age 19 until the end of the young adult stage (39). Teenage pregnancy not implemented (yet?).
* Pregnant women can only have 1 child, twins or triplets.
* Only 1 or 2 children can be adopted at the same time.
* Who can have biological children: straight couples (excluding infertile couples), two (m/f) persons from a throuple (but all three will be the child's parents),  and consanguineous couples (who will have a slightly increased chance of having a disabled child). Transgender persons and asexual persons (regardless or romantic orientation) cannot.
* Who can adopt: everyone (single persons and couples). However, only single persons who want children but do not want a committed relationship will adopt. Throuples will "officially" adopt as couples (but all three will be the child's parents), and consanguineous couples will "officially" adopt as single persons (but both will be the child's parents). 

DIVORCE
* Couples can get divorced/separated at any point in time from one year after getting together, up until old age.
* One of the two (the man if straight couple) will move to another apartment in the neighborhood if available, or move out of the building.
* Underage children will remain with the mother.
* Each person will be added to each other's list of ex-partners / ex-spouses and there will be a chance of getting back together eventually.
* Divorced persons who marry a second (or third) time will have a civil status of Remarried.
* Divorced/separated persons who start dating another person who has children, will become step-parents. 
* New partners / spouses will move into the household.
* Step-children will also move in if the new partner is their mother, or the children's mother is dead. Adult children will only move in if single and unemployed.

MINORITIES
* Persons within minority groups (LGBTA persons, poly persons and consanguinamorous persons) are liberal by default, as are persons who at any point have an intergenerational relationship.
* Persons within minority groups and intergenerationals will be subjected to their families and beighbors (positive and/or negative) reactions.
* LGBTA persons can only come out during their teenage years (13-17).
* Conservative families of LGBTA teens may throw them out or these teens may move out at 18 or commit suicide.
* Relationships between minority and non-minority (for example, between transgender/cisgender or mono/poly, can only happen if the non-minority person is liberal)

NEIGHBORHOOD
* Neighbors can date each other, become friends, enemies, or neutral (by default). Will depend on age, personality and other traits. 
* If two kids from two different households become friends, there's a good chance that their parents will also become friends.
* If two households do not stand each other and their kids become friends/lovers, the families may oppose it (and either succeed in breaking them up, or fail and either learn to accept the relationship or watch them move out)
* Neighbors may attend one another's weddings/funerals and may react to one another's life choices. Neighbors who are friends can do activities together if shared hobbies such as tennis competitions or going to their community-shared swimming pool.
* Two neighbors from different households who are single and are friends, can choose to live together in the same apartment. They will be added to each other's family list if they remain single and living together throughout the years.

PENDING TO BE IMPLEMENTED:

* Setting option for users: realistic statistics and custom statistics (user can modify for example the statistical chance for male/female to a 20/80 ratio instead of default 50/50)
* Save/Load game system
* Statistics need to be further researched and adjusted to be as close to real-life as possible.

Bugs:

* Too many to list... Project needs bug cheking, error handling / debugging ASAP. Also, it's currently SLOW as fuck.

Contribution:

Please anyone feel free to create a branch and contribute regardless of programming/python skill level, as long as you know what you're doing and won't just make a mess of things lol. I am a beginner myself! :)
