# noinspection PyUnresolvedReferences
import utilityFunctions
from src import MapAnalysis as MA
from src.genetic_algorithm import ClearArea as CA, GeneticAlgorithmMinecraft as GAM
from src.build_solution import BuildHouses as BH
# noinspection PyUnresolvedReferences
from pymclevel import alphaMaterials as am
from src.prepare_solution.a_star.AStar import *
from src.prepare_solution.a_star.PrepareAStar import *


def perform(level, box, options):
    print("_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _")
    print("_ _ _ _\t\tstart\t\t_ _ _ _")
    print("_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _")
    height_map = MA.create_two_dimensional_height_map(level, box)
    starting_point = {"x": box.minx, "z": box.minz}

    gam = GAM.Genetic_Algorithm()
    result = gam.run_genetic_algorithm(height_map, box.maxx - box.minx, box.maxz - box.minz, starting_point)    # RUN GENETIC ALGORITHM
    CA.modify_area(height_map, result, level)                                                                   # LEVEL AREA FOR BUILDINGS
    set_all_connections_points(result, height_map)                                                              # SET PATH CONNECTION POINTS FOR ALL STRUCTURES
    #manhattan_distance(result)
    #blocked_tiles(result)
    # a star
    # deforest(list_of_buildings, a_star)
    # place roads
    BH.build(level, height_map, result)

    # TODO: add values to width + length to add "buffer" area to modify area
    # TODO: modify how to build house with modifier to subtract "buffer"
    # TODO: change how we calculate door / connection point location