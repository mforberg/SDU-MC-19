# noinspection PyUnresolvedReferences
import utilityFunctions
from src import MapAnalysis as MA
from src.genetic_algorithm import ClearArea as CA, GeneticAlgorithmMinecraft as GAM
from src.build_solution import BuildHouses as BH
# noinspection PyUnresolvedReferences
from pymclevel import alphaMaterials as am
from src.prepare_solution.Deforestation import find_bounds


def perform(level, box, options):
    print("_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _")
    print("_ _ _ _\t\tstart\t\t_ _ _ _")
    print("_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _")
    height_map = MA.create_two_dimensional_height_map(level, box)
    starting_point = {"x": box.minx, "z": box.minz}

    gam = GAM.Genetic_Algorithm()
    result = gam.run_genetic_algorithm(height_map, box.maxx - box.minx, box.maxz - box.minz, starting_point)
    # set connection points
    # a star
    # deforest(list_of_buildings, a_star)
    CA.modify_area(height_map, result, level)
    # place roads
    BH.build(level, height_map, result)
