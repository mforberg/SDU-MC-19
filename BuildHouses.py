import utilityFunctions
import numpy as np
import datetime
import GeneticAlgorithmMinecraft as GAM
from multiprocessing import Process
from pymclevel import alphaMaterials, MCSchematic, MCLevel, BoundingBox
from mcplatform import *
from collections import OrderedDict

am = alphaMaterials

"Need a lot of refactoring!!!!"

def build(level, heightMap, boxLength, boxWidth, boxHeight, startingPoint, building):
    dictOfBuildings = GAM.generate_population(heightMap, boxLength, boxWidth, startingPoint, building)
    for key, value in dictOfBuildings.iteritems():
        if value == "blackSmith":
            buildBlackSmith(level, heightMap, boxLength, boxWidth, boxHeight, startingPoint, building, dictOfBuildings)
        else:
            buildFloor(level, boxHeight, building, dictOfBuildings)
            for x in range(key[0], key[0] + building[value]["xLength"]):
                utilityFunctions.setBlockToGround(level, (am.Wood.ID, 0), x, boxHeight+5, key[1],
                                              boxHeight)
                utilityFunctions.setBlockToGround(level, (am.Wood.ID, 0), x, boxHeight+5,
                                              key[1] + building[value]["zWidth"] - 1,
                                              boxHeight)
            for z in range(key[1], key[1] + building[value]["zWidth"]):
                utilityFunctions.setBlockToGround(level, (am.Wood.ID, 0),
                                              key[0] + building[value]["xLength"] - 1, boxHeight+5, z,
                                              boxHeight)
                utilityFunctions.setBlockToGround(level, (am.Wood.ID, 0), key[0], boxHeight+5, z,
                                              boxHeight)

def buildFloor(level, boxHeight, building, dictOfBuildings):
   # dictOfBuildings = GAM.generate_population(heightMap, boxLength, boxWidth, startingPoint, building)
    for key, value in dictOfBuildings.iteritems():
        if value != "blackSmith":
            for x in range(key[0], key[0] + building[value]["xLength"]):
                for z in range(key[1], key[1]+building[value]["zWidth"]):
                    utilityFunctions.setBlock(level, (am.Wood.ID, 0), x, boxHeight, z)
    #return dictOfBuildings

def buildBlackSmith(level, heightMap, boxLength, boxWidth, boxHeight, startingPoint, building, dictOfBuildings):

    for key, value in dictOfBuildings.iteritems():
        if value == "blackSmith":
            for x in range(key[0], key[0] + building[value]["xLength"] - 3):
                utilityFunctions.setBlockToGround(level, (am.Wood.ID, 0), x, boxHeight + 5, key[1],
                                          boxHeight)
            for x in range(key[0], key[0] + building[value]["xLength"]):
                utilityFunctions.setBlockToGround(level, (am.Wood.ID, 0), x, boxHeight + 5,
                                          key[1] + building[value]["zWidth"] - 1,
                                          boxHeight)
            for x in range(key[0] + building[value]["xLength"] - 3, key[0] + building[value]["xLength"]):
                utilityFunctions.setBlockToGround(level, (am.Wood.ID, 0), x, boxHeight + 5,
                                          key[1] + 2,
                                          boxHeight)

            for z in range(key[1], key[1] + building[value]["zWidth"]):
                utilityFunctions.setBlockToGround(level, (am.Wood.ID, 0), key[0], boxHeight + 5, z,
                                          boxHeight)
            for z in range(key[1] + building[value]["zWidth"] - 1, key[1] + 2, -1):
                utilityFunctions.setBlockToGround(level, (am.Wood.ID, 0),
                                          key[0] + building[value]["xLength"] - 1, boxHeight + 5, z,
                                          boxHeight)
            for z in range(key[1], key[1] + 3):
                utilityFunctions.setBlockToGround(level, (am.Wood.ID, 0),
                                          key[0] + building[value]["xLength"] - 3, boxHeight + 5, z,
                                          boxHeight)