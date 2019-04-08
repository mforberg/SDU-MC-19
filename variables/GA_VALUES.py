"""The amount of houses in a single solution"""
GENE_SIZE = 10
"""The percent chance of crossover"""
CROSSOVER_RATE = 0.05  # 5%
"""The percent chance of mutation"""
MUTATION_RATE = float(1)/GENE_SIZE
"""The amount of "solutions" in a population"""
POPULATION_SIZE = 100
"""The amount of generations the algorithm should be run"""
GENERATIONS = 100
"""The top percentage of the population who should just continue to next"""
ELITES_PERCENTAGE = 0.1  # 10%
