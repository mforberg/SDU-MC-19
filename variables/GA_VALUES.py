"""The amount of houses in a single solution"""
GENE_SIZE = 10
"""The percent chance of crossover"""
CROSSOVER_RATE = 0.05  # 5%
"""The percent chance of mutation"""
MUTATION_RATE = float(1)/GENE_SIZE  # TODO: Mikkel fix
"""The amount of "solutions" in a population"""
POPULATION_SIZE = 100
"""The amount of generations the algorithm should be run"""
GENERATIONS = 1
"""The top percentage of the population who should just continue to next"""
ELITES_PERCENTAGE = 0.1  # 10%

"""Fitness weights"""
WATER_WEIGHT = 6    # for each water-block found
AREA_WEIGHT = 1  # multiply the blocks modified
DISTANCE_WEIGHT = 0.5  # What the distance score should be multiplied with
DISTANCE_TO_WELL_WEIGHT = 2  # The distance to the well multiplied
VARIANCE_WEIGHT = 2  # How much the variance score should be multiplied

"""Extra variables"""
CHANGED_BLOCK_PER_POINT = 10  # how many blocks needs to be changed to count as a point

"""Fitness Max Scores"""
VARIANCE_MAX_SCORE = 1000  # max score for the variance in buildings
AREA_MAX_SCORE = 100  # contains both water and blocks modified

"""Quadratic Equation in Fitness"""
A = float(-4) / 45
B = float(16) / 3
C = 0
