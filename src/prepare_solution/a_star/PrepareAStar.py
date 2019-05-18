# def set_all_connections_points(list_of_buildings, height_map):
#     for building in list_of_buildings:  # find the well
#         if building.type_of_house == "well":
#             well = building
#             break
#
#     for building in list_of_buildings:  # set connection points for all buildings
#         if building.type_of_house == well:  # don't set connection point for well to begin with
#             continue
#         building.set_connection_point(well, height_map)
