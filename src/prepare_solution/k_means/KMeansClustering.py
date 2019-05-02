from sklearn.cluster import KMeans


def starting_points(amount_of_clusters, list_of_buildings):
    list_of_starting_points = list()
    for building in list_of_buildings:
        if building.type_of_house == "well":
            continue
        coords_for_building = building.path_connection_point

        list_of_starting_points.append([coords_for_building[0], coords_for_building[1] + building.buffer_direction] )
    list_of_centroids = k_means_clustering(amount_of_clusters, list_of_starting_points)
    return list_of_centroids

def k_means_clustering(amount_of_clusters, list_of_starting_points):
    list_of_centroids = list()
    k = amount_of_clusters
    kmeans = KMeans(n_clusters=k, init="k-means++")
    kmeans = kmeans.fit(list_of_starting_points)
    labels = kmeans.predict(list_of_starting_points)
   # print list_of_starting_points
    print labels
    centroids = kmeans.cluster_centers_
    for centroid in centroids:
        list_of_centroids.append([int(i) for i in centroid])
    return list_of_centroids