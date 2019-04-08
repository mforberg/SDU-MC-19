import utilityFunctions
import numpy as np
import datetime
from src import GeneticAlgorithmMinecraft as GAM
from variables.MC_LIBRARY import buildings as building_copy
from multiprocessing import Process
from pymclevel import alphaMaterials, MCSchematic, MCLevel, BoundingBox
from mcplatform import *
from collections import OrderedDict

am = alphaMaterials

def build(level, box_height, xbuildings):
    buildings = xbuildings[0]


    for building in buildings:
        print building_copy[building.typeOfHouse]
        if building.typeOfHouse == "well":
            print "here"
            well_x = building.x
            well_z = building.z

    for building in buildings:

        height_of_building = building_copy[building.typeOfHouse]["yHeight"]
        length_of_building = building_copy[building.typeOfHouse]["xLength"]
        width_of_building = building_copy[building.typeOfHouse]["zWidth"]

        print building_copy[building.typeOfHouse], " this"
        houseType = building_copy[building.typeOfHouse]["floorAndRoof"]

        if building.typeOfHouse == "blackSmith":
            build_floor_bs(level, length_of_building, width_of_building, height_of_building, box_height, building)
            build_black_smith(level, length_of_building, width_of_building, height_of_building, box_height, building)
        else:
            for x in range(building.x, building.x + length_of_building):
                utilityFunctions.setBlockToGround(level, (am.Wood.ID, 0), x, height_of_building + box_height, building.z,
                                                  box_height)
                utilityFunctions.setBlockToGround(level, (am.Wood.ID, 0), x, height_of_building + box_height,
                                                  building.z + width_of_building - 1,
                                                  box_height)
            for z in range(building.z, building.z + width_of_building):
                utilityFunctions.setBlockToGround(level, (am.Wood.ID, 0), building.x + length_of_building - 1,
                                                  height_of_building + box_height, z,
                                                  box_height)
                utilityFunctions.setBlockToGround(level, (am.Wood.ID, 0), building.x, height_of_building + box_height, z,
                                                  box_height)
            if houseType:
                build_floor(level, length_of_building, width_of_building, height_of_building, box_height, building)
                choose_x = building.x
                print well_x
                if building.x > well_x:
                    choose_x = building.x + length_of_building

                build_door(level, length_of_building, box_height, choose_x, building)



def build_floor(level, length_of_building, width_of_building, height_of_building, box_height, building):
    for x in range(building.x, building.x + length_of_building):
        for z in range(building.z, building.z + width_of_building):
            utilityFunctions.setBlock(level, (am.Wood.ID, 0), x, box_height, z)
            utilityFunctions.setBlock(level, (am.Obsidian.ID, 0), x, box_height + height_of_building, z)

def build_black_smith(level, length_of_building, width_of_building, height_of_building, box_height, building):

    removeTopSquareX = building.x + length_of_building - 3
    removeTopSquareZ = building.z + 2

    for x in range(building.x, removeTopSquareX):
            utilityFunctions.setBlockToGround(level, (am.Wood.ID, 0), x, height_of_building + box_height, building.z,
                                              box_height)
    for x in range(building.x, building.x + length_of_building):
            utilityFunctions.setBlockToGround(level, (am.Wood.ID, 0), x, height_of_building + box_height,
                                              building.z + width_of_building - 1,
                                              box_height)
    for x in range(removeTopSquareX, building.x + length_of_building):
            utilityFunctions.setBlockToGround(level, (am.Wood.ID, 0), x, height_of_building + box_height,
                                              removeTopSquareZ,
                                              box_height)

    for z in range(building.z, building.z + width_of_building):
            utilityFunctions.setBlockToGround(level, (am.Wood.ID, 0), building.x, height_of_building + box_height, z,
                                              box_height)
    for z in range(building.z, removeTopSquareZ + 1):
            utilityFunctions.setBlockToGround(level, (am.Wood.ID, 0),
                                              removeTopSquareX, height_of_building + box_height, z,
                                              box_height)
    for z in range(building.z + width_of_building - 1, removeTopSquareZ, -1):
            utilityFunctions.setBlockToGround(level, (am.Wood.ID, 0), building.x + length_of_building - 1,
                                              height_of_building + box_height, z, box_height)

def build_floor_bs(level, length_of_building, width_of_building, height_of_building, box_height, building):
    for x in range(building.x, building.x + length_of_building - 2):
        for z in range(building.z, building.z + width_of_building):
            utilityFunctions.setBlock(level, (am.Wood.ID, 0), x, box_height, z)
            utilityFunctions.setBlock(level, (am.Obsidian.ID, 0), x, box_height + height_of_building, z)
    for x in range(building.x + length_of_building - 2, building.x + length_of_building):
        for z in range(building.z + width_of_building - 1, building.z + 1, -1):
            utilityFunctions.setBlock(level, (am.Wood.ID, 0), x, box_height, z)
            utilityFunctions.setBlock(level, (am.Obsidian.ID, 0), x, box_height + height_of_building, z)

def build_door(level, length_of_building, box_height, choose_x, building):
    door_position = length_of_building / 2
    for i in range(2):
        utilityFunctions.setBlock(level, (64, 1), choose_x + door_position, box_height + i, building.z)
