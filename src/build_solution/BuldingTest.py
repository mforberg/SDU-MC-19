# noinspection PyUnresolvedReferences
import utilityFunctions
from variables.MC_LIBRARY import *
# noinspection PyUnresolvedReferences
from pymclevel import alphaMaterials as am
# noinspection PyUnresolvedReferences
from mcplatform import *


def build_points(level, solution):
    for point in solution:
        utilityFunctions.setBlock(level, (am.Wood.ID, 0), point[1][0], point[1][2], point[1][1])