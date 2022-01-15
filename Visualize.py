import numpy as np
import matplotlib.pyplot as plt

def visualize_points(image, left_neighbors_arr, right_neighbors_arr):
    point_arr = np.concatenate((left_neighbors_arr, right_neighbors_arr))
    plt.imshow(image)
    for i in range(len(point_arr)):
        plt.scatter(point_arr[i][1], point_arr[i][0], s=1) 
    plt.show()