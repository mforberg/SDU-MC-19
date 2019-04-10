# noinspection PyUnresolvedReferences
import utilityFunctions
from src import GeneticAlgorithmMinecraft as GAM, MapAnalysis as MA, ClearArea as CA
import BuildHouses as BH
# noinspection PyUnresolvedReferences
from pymclevel import alphaMaterials as am


def perform(level, box, options):
    print("_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _")
    print("_ _ _ _\t\tstart\t\t_ _ _ _")
    print("_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _")
    height_map = MA.create_two_dimensional_height_map(level, box)
    starting_point = {"x": box.minx, "z": box.minz}

    gam = GAM.Genetic_Algorithm()
    result = gam.run_genetic_algorithm(height_map, box.maxx - box.minx, box.maxz - box.minz, starting_point)
    CA.modify_area(height_map, result, level)
    BH.build(level, height_map, result)
