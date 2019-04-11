# noinspection PyUnresolvedReferences
import utilityFunctions
# noinspection PyUnresolvedReferences
from pymclevel import alphaMaterials



def deforest_area(list_of_buildings, list_of_roads, heightmap, level):
    print "do stuff"
    find_bounds(list_of_buildings)


def find_bounds(list_of_buildings):
    for b in list_of_buildings:
        print b.typeOfHouse
    min_x = list_of_buildings[0].x
    max_x = list_of_buildings[0].x

    min_z = list_of_buildings[0].z
    max_z = list_of_buildings[0].z

    for building in list_of_buildings:

        if building.x < min_x:
            min_x = building.x
        if building.x > max_x:
            max_x = building.x
        if building.z < min_z:
            min_z = building.z
        if building.z > max_z:
            max_z = building.z

    print min_x, max_x, min_z, max_z