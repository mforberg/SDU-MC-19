# noinspection PyUnresolvedReferences
import utilityFunctions
from src import MapAnalysis
from src.genetic_algorithm import PrepareBuildingArea, GeneticAlgorithmMinecraft
from src.build_solution import BuildHouses
from src.build_solution import BuildRoads
from src.prepare_solution.deforestation.Deforestation import deforest_area

# noinspection PyUnresolvedReferences
from pymclevel import alphaMaterials as aM
from src.prepare_solution.a_star.PathsForClusters import *
from src.prepare_solution.k_means.KMeansClustering import *
import time

inputs = (("Genetic Algorithm and A*", "label"),
          ("Build solution", True))


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
    centroids = starting_points(3, result)
    clusters = points_to_buildings(centroids, result)


    print "CALL 7"
    start = time.time()
    paths = path_for_clusters(clusters, height_map, box_length, box_width, starting_point)
    print "CALL 8"
    end = time.time()
    print end-start, "TOTAL TIME FOR A-STAR"
    # manhattan_distance(result)
    # blocked_tiles(result)
    # a star
    if options["Build solution"]:
        deforest_area(result, paths, height_map, level)
        # place roads
        BuildRoads.build_roads(paths, level)
        BuildHouses.build(level, height_map, result)
    del list_of_blocked_coordinates[:]
    # TODO: change how we calculate door / connection point location
