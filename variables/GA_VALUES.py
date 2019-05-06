USE_SIZE_FOR_TYPE_MUTATION = False
"""The percent chance of crossover"""
CROSSOVER_RATE = 0.05  # 5%
"""The amount of "solutions" in a population"""
POPULATION_SIZE = 100
"""The amount of generations the algorithm should be run"""
GENERATIONS = 100
"""The top percentage of the population who should just continue to next"""
ELITES_PERCENTAGE = 0.1  # 10%
"""Percentage of solution that should be normal houses"""
NORMAL_HOUSE_PERCENTAGE = 0.33  # 33%
"""Mutation rate is calculated by (1 / (gene_size * MUTATION_RATE_MODIFIER))"""
MUTATION_RATE_MODIFIER = 1  # x time as unlikely to mutate

"""Fitness weights"""
WATER_AND_LAVA_WEIGHT = 15  # For each water/lava-block found
AREA_WEIGHT = 1  # Multiply the blocks modified
#DISTANCE_WEIGHT = 1  # What the distance score should be multiplied with
DISTANCE_TO_WELL_WEIGHT = 2  # The distance to the well multiplied
VARIANCE_WEIGHT = 2  # How much the variance score should be multiplied
NORMAL_HOUSE_WEIGHT = 1  # How much the amount of normal houses should be multiplied with
Y_DIFFERENCE_WEIGHT = 1  # How much the y difference should be multiplied with
AVG_AREA_COVERAGE_WEIGHT = 2  # How much the average area coverage score should be multiplied with

"""Extra variables"""
POINTS_PER_DIFFERENCE_IN_Y = 10  # how many points a single difference in height gives
CHANGED_BLOCKS_PERCENTAGE = 0.1  # how big the percentage of changed block (depending on size) is allowed
AREA_COVERAGE_POINTS_PER_UNIT = 4
#FIT_AREA_COVERAGE_TO_DISTANCE_QUADRATIC_EQUATION = -10  # self explanatory

"""Fitness Max Scores"""
VARIANCE_MAX_SCORE = 1000  # max score for the variance in buildings
AREA_MAX_SCORE = 200  # contains both water and blocks modified (score per building)
NORMAL_HOUSE_MAX_SCORE = 1000  # max score for the right amount of houses
Y_MAX_SCORE = 1000  # max score for the difference in y coordinate
DISTANCE_MAX_SCORE = 100  # max score for distance to other houses
AVG_AREA_COVERAGE_MAX_SCORE = 1000  # max score for average area coverage

"""Length of solution variables"""
# 10 buildings = 6902
# 21 buildings = 8757
DECREASE_PER_EXTRA_BUILDING = 150  # 168 the average number of fitness points decreased per building after min length


"""FI2POP variables"""
USE_FI2POP = True
COLLISION_MAX_SCORE = 1000
COLLISION_WEIGHT = 4
WITHIN_BOX_MAX_SCORE = 1000
WITHIN_BOX_WEIGHT = 1
NOT_WITHIN_BOX_MINUS_PER_HOUSE = 250


"""Quadratic Equation in Fitness (distance)"""
A = float(-4) / 45
B = float(16) / 3
C = 0
MAX_VALUE_QE = 80
VALUE_CUT_FOR_MAX = 70


def get_minimum_amount_of_houses(box_x, box_z):
    minimum_amount_of_houses = round((box_z * box_x) / 6200)
    return minimum_amount_of_houses


def get_maximum_amount_of_houses(box_x, box_z):
    maximum_amount_of_houses = round((box_z * box_x) / 3100)
    return maximum_amount_of_houses
