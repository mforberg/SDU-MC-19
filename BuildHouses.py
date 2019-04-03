import utilityFunctions
import numpy as np
import datetime
from src import GeneticAlgorithmMinecraft as GAM
from variables.MC_LIBRARY import buildings as buildingCopy
from multiprocessing import Process
from pymclevel import alphaMaterials, MCSchematic, MCLevel, BoundingBox
from mcplatform import *
from collections import OrderedDict

am = alphaMaterials

"Need a lot of refactoring!!!!"

def build(level, boxHeight, buildings):
    for building in buildings:
        if building.typeOfHouse == "well":
            wellX = building.x
            wellZ = building.z

    listof = list()
    for building in buildings:

        heightOfBuilding = buildingCopy[building.typeOfHouse]["yHeight"]
        lengthOfBuilding = buildingCopy[building.typeOfHouse]["xLength"]
        widthOfBuilding = buildingCopy[building.typeOfHouse]["zWidth"]
        houseType = buildingCopy[building.typeOfHouse]["floorAndRoof"]

        if building.typeOfHouse == "blackSmith":
            buildFloorBS(level, lengthOfBuilding, widthOfBuilding, heightOfBuilding, boxHeight, building)
            buildBlackSmith(level, lengthOfBuilding, widthOfBuilding, heightOfBuilding, boxHeight, building)
        else:
            if houseType:
                buildFloor(level, lengthOfBuilding, widthOfBuilding, heightOfBuilding, boxHeight, building)
            for x in range(building.x, building.x + lengthOfBuilding):
                utilityFunctions.setBlockToGround(level, (am.Wood.ID, 0), x, heightOfBuilding + boxHeight, building.z,
                                              boxHeight)
                utilityFunctions.setBlockToGround(level, (am.Wood.ID, 0), x, heightOfBuilding + boxHeight,
                                              building.z + widthOfBuilding - 1,
                                              boxHeight)
            for z in range(building.z, building.z + widthOfBuilding):
                utilityFunctions.setBlockToGround(level, (am.Wood.ID, 0), building.x + lengthOfBuilding - 1,
                                                  heightOfBuilding + boxHeight, z,
                                              boxHeight)
                utilityFunctions.setBlockToGround(level, (am.Wood.ID, 0), building.x, heightOfBuilding + boxHeight, z,
                                              boxHeight)

    print listof


def buildFloor(level, lengthOfBuilding, widthOfBuilding, heightOfBuilding, boxHeight, building):
        for x in range(building.x, building.x + lengthOfBuilding):
            for z in range(building.z,  building.z + widthOfBuilding):
                utilityFunctions.setBlock(level, (am.Wood.ID, 0), x, boxHeight, z)
                utilityFunctions.setBlock(level, (am.Obsidian.ID, 0), x, boxHeight + heightOfBuilding, z)

def buildBlackSmith(level, lengthOfBuilding, widthOfBuilding, heightOfBuilding, boxHeight, building):
        for x in range(building.x, building.x + lengthOfBuilding - 3):
            utilityFunctions.setBlockToGround(level, (am.Wood.ID, 0), x, heightOfBuilding + boxHeight, building.z,
                                          boxHeight)
        for x in range(building.x, building.x + lengthOfBuilding):
            utilityFunctions.setBlockToGround(level, (am.Wood.ID, 0), x, heightOfBuilding + boxHeight,
                                          building.z + widthOfBuilding - 1,
                                          boxHeight)
        for x in range(building.x + lengthOfBuilding - 3, building.x + lengthOfBuilding):
            utilityFunctions.setBlockToGround(level, (am.Wood.ID, 0), x, heightOfBuilding + boxHeight,
                                          building.z + 2,
                                          boxHeight)

        for z in range(building.z, building.z + widthOfBuilding):
            utilityFunctions.setBlockToGround(level, (am.Wood.ID, 0), building.x, heightOfBuilding + boxHeight, z,
                                          boxHeight)
        for z in range(building.z, building.z + 3):
            utilityFunctions.setBlockToGround(level, (am.Wood.ID, 0),
                                          building.x + lengthOfBuilding - 3, heightOfBuilding + boxHeight, z,
                                          boxHeight)
        for z in range(building.z + widthOfBuilding - 1, building.z + 2, -1):
            utilityFunctions.setBlockToGround(level, (am.Wood.ID, 0), building.x + lengthOfBuilding - 1,
                                        heightOfBuilding + boxHeight, z, boxHeight)

def buildFloorBS(level, lengthOfBuilding, widthOfBuilding, heightOfBuilding, boxHeight, building):
    for x in range(building.x, building.x + lengthOfBuilding - 2):
        for z in range(building.z, building.z + widthOfBuilding):
            utilityFunctions.setBlock(level, (am.Wood.ID, 0), x, boxHeight, z)
            utilityFunctions.setBlock(level, (am.Obsidian.ID, 0), x, boxHeight + heightOfBuilding, z)
    for x in range(building.x + lengthOfBuilding - 2, building.x + lengthOfBuilding):
        for z in range(building.z + widthOfBuilding -1, building.z + 1, -1):
            utilityFunctions.setBlock(level, (am.Wood.ID, 0), x, boxHeight, z)
            utilityFunctions.setBlock(level, (am.Obsidian.ID, 0), x, boxHeight + heightOfBuilding, z)
