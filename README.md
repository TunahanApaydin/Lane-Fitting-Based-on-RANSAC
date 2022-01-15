# Lane-Fitting-Based-on-RANSAC
This project is an article application.(https://ieeexplore.ieee.org/document/7984519)

DW(Detection Window) is used for lane detection. Various operations are performed on each DW shifted in the ROI. In the related article, three conditions are required for a point to be a stripe.
a. Target size.
b. Target contrast.
c. Target morphology.

Let's review the steps.

Input data:
![frame126](https://user-images.githubusercontent.com/79514917/149625512-aa3fc418-ee0f-4198-88bd-8dee1e7dee99.jpg)
- Input data size: (960, 540)
- Each input image is resized in the data preprocessing(DataPrepocessing.py) part.

BGR to Gray:
![gray](https://user-images.githubusercontent.com/79514917/149625823-4913d61a-4117-4a35-8b97-bb4acb7174e8.jpg)

Otsu Thresholding:
![otsu](https://user-images.githubusercontent.com/79514917/149625867-7ea412f0-23f6-4bcb-9db7-59deb834f001.jpg)
- Threshold: 50.

ROI:

![image](https://user-images.githubusercontent.com/79514917/149625916-8bc31531-216c-4f8d-bfc5-517fb29bf809.png)

DW:

![DW](https://user-images.githubusercontent.com/79514917/149625981-739cc053-22a4-4733-8bd2-81f49a3b3120.jpg)

RANSAC:
![ransac](https://user-images.githubusercontent.com/79514917/149626062-7500b3f8-b9d0-43a9-b46b-e04e6e3d845d.png)

Result:
![result](https://user-images.githubusercontent.com/79514917/149626111-30f8553e-0321-414b-ad36-e07e802d5a0e.jpg)

Sample Results:
![results](https://user-images.githubusercontent.com/79514917/149626173-aed2c2a1-ad6f-42de-9a50-041ffc68cf41.png)
