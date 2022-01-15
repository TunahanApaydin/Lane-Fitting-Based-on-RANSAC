import cv2
import time
import numpy as np

from Ransac import ransac
from Visualize import visualize_points
from DataPrepocessing import Preprocessing

FORMAT = "image"

class LaneDetection:
    def __init__(self):
        pass
        
    def detect_lanes(self, image_roi):
        #s = time.time()
        stepsizey = 10
        stepsizex = 22
        w_height = 10
        w_width = 22
        left_count = 0
        left_neighbors = []
        right_count = 0
        right_neighbors = []
        img = image_roi
        lane_judgment = [False, False, False]
        
        for x in range(125, 900, stepsizex):
            for y in range(315, 540, stepsizey): 
                lane_judgment = [False, False, False]
                #window = img[y:y+w_height, x:x+w_width]

                src = np.float32([[x, y], [x+w_width, y], [x, y+w_height], [x+w_width, y+w_height]])
                dst = np.float32([[0, 0], [22, 0], [0, 10], [22, 10]])

                matrix = cv2.getPerspectiveTransform(src, dst)
                window = cv2.warpPerspective(img, matrix, (22, 10))
                #cv2.imwrite("/home/tuna/Desktop/Image Processing/project/pt/dw%d.jpg" % count, result)
                
                target_count = np.sum(window == 255)
                target_size = target_count / (window.shape[0] * window.shape[1])
                if 0.2 <= target_size <= 0.7:
                    lane_judgment[0] = True
                
                    min = np.min(window)
                    max = np.max(window)
                    contrast = target_count / (max+min)
                    if 0 < contrast < 1.2:
                        lane_judgment[1] = True
                    
                        sum_ibw = np.sum(window[:,0], axis = 0) # sum of all pixel values of the first column of the binary image in DWs.
                        gx, gy = np.gradient(window)
                        Tg1 = (np.diff(gx) == 127.5).sum()
                        Tg2 = (np.diff(gx) == 255).sum()
                        if ((Tg1 + Tg2) > (0.8 * window.shape[0]) and (sum_ibw < 1500)):
                            lane_judgment[2] = True
                
                if (lane_judgment[0] == True) and (lane_judgment[1] == True) and (lane_judgment[2] == True):

                    center_img_X = np.array((2*x +11)/2) #11 = window.shape[1]/2
                    center_img_Y = np.array(y+5) #5 = window.shape[0]/2
                    nonzero = np.argwhere(img == 255)
                    distances = np.sqrt((nonzero[:,1] - center_img_X) ** 2 + (nonzero[:,0] - center_img_Y) ** 2)
                    sorted_D = np.argsort(distances)
                    indexes = sorted_D[0:25]
        
                    if img.shape[1]/2 > x:    
                        left_neighbors.append(nonzero[indexes])
                        left_neighbors_arr = np.array(left_neighbors)               
                        left_count += 1

                    else:
                        right_neighbors.append(nonzero[indexes])
                        right_neighbors_arr = np.array(right_neighbors)
                        right_count += 1

        left_neighbors_arr = left_neighbors_arr.reshape(25*left_count, 2)
        right_neighbors_arr = right_neighbors_arr.reshape(25*right_count, 2)
        #print(time.time()-s)
        return left_neighbors_arr, right_neighbors_arr 

    def main(self):
        process = Preprocessing()

        if FORMAT == "image": 
            gray, otsu = process.image_prep()
            image, image_roi = process.region_of_interest(gray, otsu)

            left_neighbors_arr, right_neighbors_arr = self.detect_lanes(image_roi)

            ransac(image, left_neighbors_arr, right_neighbors_arr)
            
            cv2.imshow("lanes", image)
            #cv2.imwrite("/home/tuna/Desktop/Image Processing/project/result4.jpg", image)
            if cv2.waitKey(0) & 0xFF == ord('x'):
                cv2.destroyAllWindows()

        else:
            capture = cv2.VideoCapture(process.get_video_path)

            while True:
                ret, frame = capture.read()
                
                if ret:
                    cv2.resize(frame, (960, 540))
                else:
                    break
                    
                gray, otsu = process.frame_prep(frame)
                image, image_roi = process.region_of_interest(gray, otsu)

                left_neighbors_arr, right_neighbors_arr = self.detect_lanes(image_roi)

                ransac(frame, left_neighbors_arr, right_neighbors_arr)
                
                cv2.imshow("lanes", frame)
                if cv2.waitKey(10) & 0xFF == ord('x'):
                    break
            capture.release()
            cv2.destroyAllWindows()
        #visualize_points(image, left_neighbors_arr, right_neighbors_arr)

if __name__ == "__main__":
    ld = LaneDetection()
    ld.main()