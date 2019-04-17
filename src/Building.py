import math
from variables import MC_LIBRARY


class Building:
    def __init__(self, x, z, type_of_house):
        self.x = x
        self.z = z
        self.path_connection_point = tuple()
        self.type_of_house = type_of_house
        self.buildingsCopy = MC_LIBRARY.buildings

    def distance_between_building(self, house):
        # find the middle of each building
        this_middle_point = {"x": self.x + (self.buildingsCopy[self.type_of_house]["xLength"] / float(2)),
                             "z": self.z + (self.buildingsCopy[self.type_of_house]["zWidth"] / float(2))}
        house_middle_point = {"x": house.x + (self.buildingsCopy[house.type_of_house]["xLength"] / float(2)),
                              "z": house.z + (self.buildingsCopy[house.type_of_house]["zWidth"] / float(2))}

        """Check if there is overlapping"""
        this_min_x = self.x
        this_max_x = self.x + self.buildingsCopy[self.type_of_house]["xLength"]
        this_min_z = self.z
        this_max_z = self.z + self.buildingsCopy[self.type_of_house]["zWidth"]
        house_min_x = house.x
        house_max_x = house.x + self.buildingsCopy[house.type_of_house]["xLength"]
        house_min_z = house.z
        house_max_z = house.z + self.buildingsCopy[house.type_of_house]["zWidth"]

        overlapping = False
        overlapping_direction_x = False

        """overlapping in form of the houses' points being within one another
        1: if the minimum x value for the house parameter the function is being called with is between min and max
        2: if the maximum x value for the house parameter the function is being called with is between min and max
        3: if the minimum z value for the house parameter the function is being called with is between min and max
        4: if the maximum z value for the house parameter the function is being called with is between min and max
        """
        if this_min_x < house_min_x < this_max_x:
            overlapping = True
            overlapping_direction_x = True
        elif this_min_x < house_max_x < this_max_x:
            overlapping = True
            overlapping_direction_x = True
        elif this_min_z < house_min_z < this_max_z:
            overlapping = True
        elif this_min_z < house_max_z < this_max_z:
            overlapping = True

        """depending on the relation to each other, calculation of distance points changes"""
        right = False
        down = False
        """if this building is more east of the other building"""
        if this_middle_point["x"] > house_middle_point["x"]:
            right = True
        """if this building is more south of the other building"""
        if this_middle_point["z"] > house_middle_point["z"]:
            down = True

        if overlapping:
            points_dict = self.__inside_case(house, this_middle_point, house_middle_point,
                                            overlapping_direction_x)
            calculation_point1 = points_dict["calculation_point1"]
            calculation_point2 = points_dict["calculation_point2"]
        else:
            points_dict = self.__corner_case(house, this_middle_point, house_middle_point, right, down)
            calculation_point1 = points_dict["calculation_point1"]
            calculation_point2 = points_dict["calculation_point2"]

        """the points have now been found, and pythagoras is used to calculate the distance"""
        x = math.pow(calculation_point1["x"] - calculation_point2["x"], 2)
        z = math.pow(calculation_point1["z"] - calculation_point2["z"], 2)
        distance = math.sqrt(x + z)
        return distance

    def __corner_case(self, house, this_middle_point, house_middle_point, right, down):
        calculation_point1 = {}
        calculation_point2 = {}
        if right:
            calculation_point1["x"] = this_middle_point["x"] - (self.buildingsCopy[self.type_of_house]["xLength"] / float(2))
            calculation_point2["x"] = house_middle_point["x"] + (self.buildingsCopy[house.type_of_house]["xLength"] / float(2))
        else:
            calculation_point1["x"] = this_middle_point["x"] + (self.buildingsCopy[self.type_of_house]["xLength"] / float(2))
            calculation_point2["x"] = house_middle_point["x"] - (self.buildingsCopy[house.type_of_house]["xLength"] / float(2))
        if down:
            calculation_point1["z"] = this_middle_point["z"] - (self.buildingsCopy[self.type_of_house]["zWidth"] / float(2))
            calculation_point2["z"] = house_middle_point["z"] + (self.buildingsCopy[house.type_of_house]["zWidth"] / float(2))
        else:
            calculation_point1["z"] = this_middle_point["z"] + (self.buildingsCopy[self.type_of_house]["zWidth"] / float(2))
            calculation_point2["z"] = house_middle_point["z"] - (self.buildingsCopy[house.type_of_house]["zWidth"] / float(2))
        return {"calculation_point1": calculation_point1, "calculation_point2": calculation_point2}

    def __inside_case(self, house, inside_middle_point, outside_middle_point, inside_direction_x):
        calculation_point1 = {}
        calculation_point2 = {}
        if inside_direction_x:
            calculation_point1["x"] = 0
            calculation_point2["x"] = 0
            calculation_point1["z"] = inside_middle_point["z"] - (
                    self.buildingsCopy[self.type_of_house]["zWidth"] / float(2))
            calculation_point2["z"] = outside_middle_point["z"] + (
                    self.buildingsCopy[house.type_of_house]["zWidth"] / float(2))
        else:
            calculation_point1["z"] = 0
            calculation_point2["z"] = 0
            calculation_point1["x"] = inside_middle_point["x"] - (
                    self.buildingsCopy[self.type_of_house]["xLength"] / float(2))
            calculation_point2["x"] = outside_middle_point["x"] + (
                    self.buildingsCopy[house.type_of_house]["xLength"] / float(2))
        return {"calculation_point1": calculation_point1, "calculation_point2": calculation_point2}

    def check_if_house_is_within(self, house):
        this_min_x = self.x
        this_max_x = self.x + self.buildingsCopy[self.type_of_house]["xLength"]
        this_min_z = self.z
        this_max_z = self.z + self.buildingsCopy[self.type_of_house]["zWidth"]

        house_min_x = house.x
        house_max_x = house.x + self.buildingsCopy[house.type_of_house]["xLength"]
        house_min_z = house.z
        house_max_z = house.z + self.buildingsCopy[house.type_of_house]["zWidth"]
        """simply check if any of the four corners are within this house"""
        if this_min_x <= house_min_x <= this_max_x and this_min_z <= house_min_z <= this_max_z:
            return True
        if this_min_x <= house_min_x <= this_max_x and this_min_z <= house_max_z <= this_max_z:
            return True
        if this_min_x <= house_max_x <= this_max_x and this_min_z <= house_min_z <= this_max_z:
            return True
        if this_min_x <= house_max_x <= this_max_x and this_min_z <= house_max_z <= this_max_z:
            return True
        """simply check if any of the four corners of this is within the other house"""
        if house_min_x <= this_min_x <= house_max_x and house_min_z <= this_min_z <= house_max_z:
            return True
        if house_min_x <= this_min_x <= house_max_x and house_min_z <= this_max_z <= house_max_z:
            return True
        if house_min_x <= this_max_x <= house_max_x and house_min_z <= this_min_z <= house_max_z:
            return True
        if house_min_x <= this_max_x <= house_max_x and house_min_z <= this_max_z <= house_max_z:
            return True
        """if we passed all these if statements, we are not within the building"""
        return False


    def set_connection_point(self, well, height_map):
        x = self.x + (MC_LIBRARY.BUFFER)
        z = self.z + (MC_LIBRARY.BUFFER)
        well_z = well.z - (MC_LIBRARY.BUFFER*2)
        if z < well_z:
            z += (self.buildingsCopy[self.type_of_house]["zWidth"] - (MC_LIBRARY.BUFFER*2)) - 1
        x += (self.buildingsCopy[self.type_of_house]["xLength"] - (MC_LIBRARY.BUFFER*2)) / 2
        y = height_map[x,z][0]
        self.path_connection_point = (x, z, y)




