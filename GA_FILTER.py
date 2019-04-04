# noinspection PyUnresolvedReferences
import utilityFunctions
from src import Building, GeneticAlgorithmMinecraft as GAM, MapAnalysis as MA

import BuildHouses as BH
from pymclevel import alphaMaterials as am


def perform(level, box, options):
    print("_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _")
    print("_ _ _ _\t\tstart\t\t_ _ _ _")
    print("_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _")

    heightMap = MA.create_two_dimensional_height_map(level, box)
    startingPoint = {"x": box.minx, "z": box.minz}

    gam = GAM.Genetic_Algorithm()
    result = gam.run_genetic_algorithm(heightMap, box.maxx - box.minx, box.maxz - box.minz, startingPoint)
    BH.build(level, box.miny, result)
