# noinspection PyUnresolvedReferences
import utilityFunctions
from src import Building, GeneticAlgorithmMinecraft as GAM, MapAnalysis as MA
from variables import GA_VALUES as GAV
from variables.MC_LIBRARY import *

def perform(level, box, options):
    print("start")
    """Depending on the size of the box, different amount of buildings needs to be added. x-size = z-size"""

    heightMap = MA.create_two_dimensional_height_map(level, box)
    startingPoint = {"x": box.minx, "z": box.minz}


    gam = GAM.Genetic_Algorithm(GAV.GENE_SIZE, GAV.CROSSOVER_RATE, GAV.MUTATION_RATE, GAV.POPULATION_SIZE)
    #gam.run_genetic_algorithm(heightMap, box.maxx - box.minx, box.maxz - box.minz, startingPoint, MC_LIBRARY.buildings)
    building1 = Building.Building(10, 10, "church")
    building2 = Building.Building(8, 0, "well")
    print(building1.distance_between_building(building2))
    print("HERE")
    print(buildingsCopy().__class__)
    print(buildingsCopy().__class__)
    print(buildingsCopy().__class__)
    print(totalprobability())
    #test = MC_LIBRARY.total_probability()

    #for key in coor.keys():
    #    print(key)
        #utilityFunctions.setBlock(level, (am.DiamondOre.ID, 0), key[0], coor[key][1], key[1])
