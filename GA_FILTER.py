# noinspection PyUnresolvedReferences
import utilityFunctions
import time
from src import MapAnalysis
from src.genetic_algorithm import PrepareBuildingArea, GeneticAlgorithmMinecraft
from src.build_solution import BuildHouses

# noinspection PyUnresolvedReferences
from pymclevel import alphaMaterials as aM
from src.prepare_solution.a_star.AStar import *
from src.prepare_solution.a_star.PrepareAStar import *
from heapq import *


def perform(level, box, options):
    print("_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _")
    print("_ _ _ _\t\tstart\t\t_ _ _ _")
    print("_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _")
    print "CALL 1"
    height_map = MapAnalysis.create_two_dimensional_height_map(level, box)
    starting_point = {"x": box.minx, "z": box.minz}
    box_width = box.maxz - box.minz
    box_length = box.maxx - box.minx

    print "CALL 2"
    gam = GeneticAlgorithmMinecraft.GeneticAlgorithm()
    # RUN GENETIC ALGORITHM
    print "CALL 3"
    result = gam.run_genetic_algorithm(height_map, box.maxx - box.minx, box.maxz - box.minz, starting_point)
    # LEVEL AREA FOR BUILDINGS
    print "CALL 4"
    PrepareBuildingArea.modify_area(height_map, result, level)
    print "CALL 5"
    # SET PATH CONNECTION POINTS FOR ALL STRUCTURES
    set_all_connections_points(result, height_map)
    print "CALL 6"
    start = time.time()
    neighbors = run(result, height_map, level, box_length, box_width, starting_point)
    print "CALL 7"
    end = time.time()
    print end-start, "TOTAL TIME FOR A-STAR"
    # manhattan_distance(result)
    # blocked_tiles(result)
    # a star
    # deforest(list_of_buildings, a_star)
    # place roads
    BuildHouses.build(level, height_map, result)

    # TODO: add values to width + length to add "buffer" area to modify area
    # TODO: modify how to build house with modifier to subtract "buffer"
    # TODO: change how we calculate door / connection point location
