# noinspection PyUnresolvedReferences
import utilityFunctions
from src import GeneticAlgorithmMinecraft as GAM, MapAnalysis as MA
# noinspection PyUnresolvedReferences
from pymclevel import alphaMaterials as am


def perform(level, box, options):
    print("_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _")
    print("_ _ _ _\t\tstart\t\t_ _ _ _")
    print("_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _")

    heightMap = MA.create_two_dimensional_height_map(level, box)
    startingPoint = {"x": box.minx, "z": box.minz}

    gam = GAM.Genetic_Algorithm()
    result = gam.run_genetic_algorithm(heightMap, box.maxx - box.minx, box.maxz - box.minz, startingPoint)

    """result = list of buildings (Type = Building)"""
    """Monika code is called under here (should use result):"""


    #utilityFunctions.setBlock(level, (64, 1), box.minx, 10, box.minz)
    #utilityFunctions.setBlock(level, (64, 1), box.minx, 11, box.minz)
