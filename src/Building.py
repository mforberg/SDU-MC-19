import math
import LIBRARY

class Building:
    def __init__(self, x, z, typeOfHouse):
        self.x = x
        self.z = z
        self.typeOfHouse = typeOfHouse
        self.buildingsCopy = LIBRARY.buildings

    def distance_between_building(self, house):
        # find the middle of each building
        thisMiddlePoint = {"x": self.x + (self.buildingsCopy[self.typeOfHouse]["xLength"] / float(2)),
                           "z": self.z + (self.buildingsCopy[self.typeOfHouse]["zWidth"] / float(2))}
        houseMiddlePoint = {"x": house.x + (self.buildingsCopy[house.typeOfHouse]["xLength"] / float(2)),
                            "z": house.z + (self.buildingsCopy[house.typeOfHouse]["zWidth"] / float(2))}

        """Check if there is overlapping"""
        thisMinX = self.x
        thisMaxX = self.x + self.buildingsCopy[self.typeOfHouse]["xLength"]
        thisMinZ = self.z
        thisMaxZ = self.z + self.buildingsCopy[self.typeOfHouse]["zWidth"]
        houseMinX = house.x
        houseMaxX = house.x + self.buildingsCopy[house.typeOfHouse]["xLength"]
        houseMinZ = house.z
        houseMaxZ = house.z + self.buildingsCopy[house.typeOfHouse]["zWidth"]

        overlapping = False
        #houseInside = False
        #thisInside = False
        #insideDirectionX = False
        overlappingDirectionX = False

        """overlapping in form of the houses' points being within one another
        1: if the minimum x value for the house parameter the function is being called with is between min and max
        2: if the maximum x value for the house parameter the function is being called with is between min and max
        3: if the minimum z value for the house parameter the function is being called with is between min and max
        4: if the maximum z value for the house parameter the function is being called with is between min and max
        """
        if thisMinX < houseMinX < thisMaxX:
            overlapping = True
            overlappingDirectionX = True
        elif thisMinX < houseMaxX < thisMaxX:
            overlapping = True
            overlappingDirectionX = True
        elif thisMinZ < houseMinZ < thisMaxZ:
            overlapping = True
        elif thisMinZ < houseMaxZ < thisMaxZ:
            overlapping = True


        # """overlapping in form of one house being "inside" the other
        # 1: if the house the function is being called on is within the other one (x)
        # 2: if the house the function is being called on is within the other one (z)
        # 3: if the house parameter the function is being called with is within the other one (x)
        # 4: if the house parameter the function is being called with is within the other one (z)
        # """
        # if thisMinX > houseMinX and thisMaxX < houseMaxX:
        #     thisInside = True
        #     insideDirectionX = True
        # elif thisMinZ > houseMinZ and thisMaxZ < houseMaxZ:
        #     thisInside = True
        # elif houseMinX > thisMinX and houseMaxX < thisMaxX:
        #     houseInside = True
        #     insideDirectionX = True
        # elif houseMinZ > thisMinZ and houseMaxZ < thisMaxZ:
        #     houseInside = True

        """depending on the relation to each other, calculation of distance points changes"""
        right = False
        down = False
        """if this building is more east of the other building 
        else if they are the same"""
        if thisMiddlePoint["x"] > houseMiddlePoint["x"]:
            print("right")
            right = True
        """if this building is more south of the other building
         else if they are the same"""
        if thisMiddlePoint["z"] > houseMiddlePoint["z"]:
            down = True

        if overlapping:
            pointsDict = self.__inside_case(house, thisMiddlePoint, houseMiddlePoint,
                                            overlappingDirectionX)
            calculationPoint1 = pointsDict["calculationPoint1"]
            calculationPoint2 = pointsDict["calculationPoint2"]
        # elif houseInside:
        #     right = not right
        #     down = not down
        #     pointsDict = self.__inside_case(house, self, buildingsCopy, houseMiddlePoint, thisMiddlePoint,
        #                                     overlappingDirectionX)
        #     calculationPoint1 = pointsDict["calculationPoint1"]
        #     calculationPoint2 = pointsDict["calculationPoint2"]
        else:
            pointsDict = self.__corner_case(house, thisMiddlePoint, houseMiddlePoint, right, down)
            calculationPoint1 = pointsDict["calculationPoint1"]
            calculationPoint2 = pointsDict["calculationPoint2"]

        """the points have now been found, and pythagoras is used to calculate the distance"""
        x = math.pow(calculationPoint1["x"] - calculationPoint2["x"], 2)
        z = math.pow(calculationPoint1["z"] - calculationPoint2["z"], 2)
        distance = math.sqrt(x + z)
        return distance

    def __corner_case(self, house, thisMiddlePoint, houseMiddlePoint, right, down):
        calculationPoint1 = {}
        calculationPoint2 = {}
        if right:
            calculationPoint1["x"] = thisMiddlePoint["x"] - (self.buildingsCopy[self.typeOfHouse]["xLength"] / float(2))
            calculationPoint2["x"] = houseMiddlePoint["x"] + (self.buildingsCopy[house.typeOfHouse]["xLength"] / float(2))
        else:
            calculationPoint1["x"] = thisMiddlePoint["x"] + (self.buildingsCopy[self.typeOfHouse]["xLength"] / float(2))
            calculationPoint2["x"] = houseMiddlePoint["x"] - (self.buildingsCopy[house.typeOfHouse]["xLength"] / float(2))
        if down:
            calculationPoint1["z"] = thisMiddlePoint["z"] - (self.buildingsCopy[self.typeOfHouse]["zWidth"] / float(2))
            calculationPoint2["z"] = houseMiddlePoint["z"] + (self.buildingsCopy[house.typeOfHouse]["zWidth"] / float(2))
        else:
            calculationPoint1["z"] = thisMiddlePoint["z"] + (self.buildingsCopy[self.typeOfHouse]["zWidth"] / float(2))
            calculationPoint2["z"] = houseMiddlePoint["z"] - (self.buildingsCopy[house.typeOfHouse]["zWidth"] / float(2))
        return {"calculationPoint1": calculationPoint1, "calculationPoint2": calculationPoint2}

    def __inside_case(self, house, insideMiddlePoint, outsideMiddlePoint, insideDirectionX):
        calculationPoint1 = {}
        calculationPoint2 = {}
        if insideDirectionX:
            calculationPoint1["x"] = 0
            calculationPoint2["x"] = 0
            calculationPoint1["z"] = insideMiddlePoint["z"] - (
                    self.buildingsCopy[self.typeOfHouse]["zWidth"] / float(2))
            calculationPoint2["z"] = outsideMiddlePoint["z"] + (
                    self.buildingsCopy[house.typeOfHouse]["zWidth"] / float(2))
        else:
            calculationPoint1["z"] = 0
            calculationPoint2["z"] = 0
            calculationPoint1["x"] = insideMiddlePoint["x"] - (
                    self.buildingsCopy[self.typeOfHouse]["xLength"] / float(2))
            calculationPoint2["x"] = outsideMiddlePoint["x"] + (
                    self.buildingsCopy[house.typeOfHouse]["xLength"] / float(2))
        return {"calculationPoint1": calculationPoint1, "calculationPoint2": calculationPoint2}




"""calculationPoint1 = {}
        calculationPoint2 = {}
        if insideDirectionX:
            calculationPoint1["x"] = 0
            calculationPoint2["x"] = 0
            if down:
                calculationPoint1["z"] = insideMiddlePoint["z"] - (
                        buildingsCopy[insideHouse.typeOfHouse]["zWidth"] / float(2))
                calculationPoint2["z"] = outsideMiddlePoint["z"] + (
                        buildingsCopy[outsideHouse.typeOfHouse]["zWidth"] / float(2))
            else:
                calculationPoint1["z"] = insideMiddlePoint["z"] + (
                        buildingsCopy[insideHouse.typeOfHouse]["zWidth"] / float(2))
                calculationPoint2["z"] = outsideMiddlePoint["z"] - (
                        buildingsCopy[outsideHouse.typeOfHouse]["zWidth"] / float(2))
        else:
            calculationPoint1["z"] = 0
            calculationPoint2["z"] = 0
            if right:
                calculationPoint1["x"] = insideMiddlePoint["x"] - (
                        buildingsCopy[insideHouse.typeOfHouse]["xLength"] / float(2))
                calculationPoint2["x"] = outsideMiddlePoint["x"] + (
                        buildingsCopy[outsideHouse.typeOfHouse]["xLength"] / float(2))
            else:
                calculationPoint1["x"] = insideMiddlePoint["x"] + (
                        buildingsCopy[insideHouse.typeOfHouse]["xLength"] / float(2))
                calculationPoint2["x"] = outsideMiddlePoint["x"] - (
                        buildingsCopy[outsideHouse.typeOfHouse]["xLength"] / float(2))"""