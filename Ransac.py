import cv2
import numpy as np
from sklearn import linear_model


def ransac(image, left_neighbors_arr, right_neighbors_arr):
    left_lane_x = []
    left_lane_y = []
    right_lane_x = []
    right_lane_y = []

    for y1, x1 in left_neighbors_arr:
        left_lane_x.append([x1])
        left_lane_y.append([y1])

    for y1, x1 in right_neighbors_arr:
        right_lane_x.append([x1])
        right_lane_y.append([y1])
    
    left_ransac_x = np.array(left_lane_x)
    left_ransac_y = np.array(left_lane_y)
    right_ransac_x = np.array(right_lane_x)
    right_ransac_y = np.array(right_lane_y)

    left_ransac = linear_model.RANSACRegressor(linear_model.LinearRegression())
    left_ransac.fit(left_ransac_x, left_ransac_y)
    slope_left = left_ransac.estimator_.coef_
    intercept_left = left_ransac.estimator_.intercept_

    right_ransac = linear_model.RANSACRegressor(linear_model.LinearRegression())
    right_ransac.fit(right_ransac_x, right_ransac_y)
    slope_right = right_ransac.estimator_.coef_
    intercept_right = right_ransac.estimator_.intercept_

    height = image.shape[0]
    width = image.shape[1]
    
    y_limit_min = int(0.95 * height)
    y_limit_max = int(0.62 * height)
    
    if slope_left == 0 or slope_left > 0 or slope_left > -0.4:
        slope_left = [[-0.65335443]]

    y_1 = height
    x_1 = np.abs(int((y_1 - intercept_left) / slope_left))

    y_2 = y_limit_max
    x_2 = np.abs(int((y_2 - intercept_left) / slope_left))
    
    y_3 = y_limit_max
    x_3 = np.abs(int((y_3 - intercept_right) / slope_right))

    y_4 = height
    x_4 = np.abs(int((y_4 - intercept_right) / slope_right))
    
    cv2.line(image, (x_1, y_1), (x_2, y_2), (0, 0, 255), 3)
    cv2.line(image, (x_3, y_3), (x_4, y_4), (0, 0, 255), 3)
    pts = np.array([[x_1, y_1], [x_2, y_2], [x_3, y_3], [x_4, y_4]])
    frame_copy = image.copy()
    cv2.fillPoly(frame_copy, np.int32([pts]), (255, 255, 0))
    cv2.addWeighted(frame_copy, 0.4, image, 0.6, 0, image)
