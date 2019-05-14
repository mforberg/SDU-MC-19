import math

USE_SIZE_FOR_TYPE_MUTATION = False
"""The percent chance of crossover"""
CROSSOVER_RATE = 0.05  # 5%
"""The amount of "solutions" in a population"""
POPULATION_SIZE = 100
"""The amount of generations the algorithm should be run"""
GENERATIONS = 100
"""The top percentage of the population who should just continue to next"""
ELITES_PERCENTAGE = 0.1  # 10%
# """Percentage of solution that should be normal houses"""
# NORMAL_HOUSE_PERCENTAGE = 0.33  # 33%
"""Mutation rate is calculated by (1 / (gene_size * MUTATION_RATE_MODIFIER))"""
MUTATION_RATE_MODIFIER = 1  # x time as unlikely to mutate
"""Fitness Max Scores"""
MAX_SCORE = 1000

"""Fitness weights"""
WATER_AND_LAVA_WEIGHT = 10  # For each water/lava-block found, how much does it cost to use that area
AREA_WEIGHT = 1.5  # Multiply the blocks modified
DISTANCE_TO_WELL_WEIGHT = 1  # The distance to the well multiplied
# VARIANCE_WEIGHT = 0.5  # How much the variance score should be multiplied
# NORMAL_HOUSE_WEIGHT = 0.5  # How much the amount of normal houses should be multiplied with
Y_DIFFERENCE_WEIGHT = 0.5  # How much the y difference should be multiplied with
COVERAGE_WEIGHT = 1  # How much the score for the area covered is multiplied with
FORCE_PROBABILITY_WEIGHT = 0.3

"""Extra variables"""
POINTS_PER_DIFFERENCE_IN_Y = 10  # how many points a single difference in height gives
ALLOWED_CHANGED_BLOCKS_PERCENTAGE = 0.1  # how big the percentage of changed block (depending on size) is allowed
# AREA_COVERAGE_POINTS_PER_UNIT = 2  # how many points is subtracted for every unit
# AREA_COVERAGE_ZERO_SCORE = 200  # average coverage distance for zero points

"""Length of solution variables"""
DECREASE_PER_EXTRA_BUILDING = -30  # Positive number increases the chance of smaller solution (Negative for bigger)

"""FI2POP variables"""
USE_FI2POP = True
COLLISION_MAX_SCORE = 1000
COLLISION_WEIGHT = 4
WITHIN_BOX_MAX_SCORE = 1000
WITHIN_BOX_WEIGHT = 1
NOT_WITHIN_BOX_MINUS_PER_HOUSE = 250

"""Quadratic Equation in Fitness (distance to well)"""
Q_A = float(-3) / 140
Q_B = float(23) / 14
Q_C = 50
Q_D = math.pow(Q_B, 2) - (4 * Q_A * Q_C)
VERTEX_Y = -Q_D / (4 * Q_A)
VERTEX_X = -Q_B / (2 * Q_A)
PERCENTAGE_FOR_MAX_VALUE_QE = 0.1

"""Linea Equation in Fitness (distance to well)"""
y_1 = 0
y_2 = VERTEX_Y
x_1 = 0
x_2 = VERTEX_X
L_A = (y_2 - y_1) / (x_2 - x_1)


def get_minimum_amount_of_houses(box_x, box_z):
    minimum_amount_of_houses = round((box_z * box_x) / 6200)
    return minimum_amount_of_houses


def get_maximum_amount_of_houses(box_x, box_z):
    maximum_amount_of_houses = round((box_z * box_x) / 3100)
    return maximum_amount_of_houses
