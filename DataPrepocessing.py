import cv2
import numpy as np

class Preprocessing:
    def __init__(self):
        self.img_path = "/home/tuna/Desktop/Image Processing/project/7.jpg"
        self.video_path = "/home/tuna/Desktop/Image Processing/project/solidWhiteRight.mp4"
        self.image = cv2.resize(cv2.imread(self.img_path), (960, 540))
        #cv2.imwrite("/home/tuna/Desktop/Image Processing/project/image.jpg", self.image)
        self.left_bottom = []
        self.right_bottom = []
        self.apex_left = []
        self.apex_right = []
        #cv2.imshow("f", self.image)
        #cv2.waitKey(0)
    
    def image_prep(self):
        gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        _, otsu = cv2.threshold(gray, 50, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        #cv2.imwrite("/home/tuna/Desktop/Image Processing/project/gray.jpg", gray)
        #cv2.imwrite("/home/tuna/Desktop/Image Processing/project/otsu.jpg", otsu)
        #cv2.imshow("otsu", otsu)
        return gray, otsu

    def frame_prep(self, frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        _, otsu = cv2.threshold(gray, 50, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

        return gray, otsu

    @property
    def get_image(self):
        return self.image

    @property
    def get_video_path(self):  
        return self.video_path


    def region_of_interest(self, gray, otsu):
        width = self.image.shape[1]
        height = self.image.shape[0]
        # self.left_bottom = [((width/2) - 380), height]
        # self.right_bottom = [width, height]
        # self.apex_left = [((width/2) - 60), ((height/2) + 60)]
        # self.apex_right = [((width/2) + 50), ((height/2) + 50)]

        self.left_bottom = [0, height]
        self.right_bottom = [width, height]
        self.apex_left = [50, (height/2)]
        self.apex_right = [(width-50), (height/2)]

        roi_corners = np.array([[self.left_bottom, self.apex_left, self.apex_right, self.right_bottom]], dtype = np.int32)
        mask_color = 255
        mask_roi = np.zeros(gray.shape, dtype = np.uint8)
        cv2.fillPoly(mask_roi, roi_corners, mask_color)
        image_roi = cv2.bitwise_and(otsu, mask_roi)
        #cv2.imshow("roi", image_roi)
        #cv2.imwrite("/home/tuna/Desktop/Image Processing/project/ROI.jpg", image_roi)
        return self.image, image_roi