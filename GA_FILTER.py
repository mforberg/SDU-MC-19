# noinspection PyUnresolvedReferences
import utilityFunctions
from src import MapAnalysis as MA
from src.genetic_algorithm import ClearArea as CA, GeneticAlgorithmMinecraft as GAM
from src.build_solution import BuildHouses as BH
from src.build_solution import BuldingTest as BT
# noinspection PyUnresolvedReferences
from pymclevel import alphaMaterials as am
from src.prepare_solution.a_star.AStar import *
from src.prepare_solution.a_star.PrepareAStar import *
from heapq import *


def perform(level, box, options):
    print("_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _")
    print("_ _ _ _\t\tstart\t\t_ _ _ _")
    print("_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _")
    height_map = MA.create_two_dimensional_height_map(level, box)
    starting_point = {"x": box.minx, "z": box.minz}
    box_width = box.maxz - box.minz
    box_length = box.maxx - box.minx

    gam = GAM.Genetic_Algorithm()
    result = gam.run_genetic_algorithm(height_map, box_length, box_width, starting_point)
    CA.modify_area(height_map, result, level)
    set_all_connections_points(result, height_map)
    start = time.time()
    neighbors = run(result, height_map, level, box_length, box_width, starting_point)
    end = time.time()

    print end-start, "TOTAL TIME FOR A-STAR"
    """"""
    # a star
    # deforest(list_of_buildings, a_star)
    # place roads
    #BH.build(level, height_map, result)

    # TODO: add values to width + length to add "buffer" area to modify area
    # TODO: modify how to build house with modifier to subtract "buffer"
    # TODO: change how we calculate door / connection point location