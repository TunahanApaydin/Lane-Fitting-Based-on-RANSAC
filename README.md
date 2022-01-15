# Lane-Fitting-Based-on-RANSAC
This project is an article application.(https://ieeexplore.ieee.org/document/7984519)
DW(Detection Window) is used for lane detection. Various operations are performed on each DW shifted in the ROI. In the related article, three conditions are required for a point to be a stripe.
a. Target size.
b. Target contrast.
c. Target morphology.

Let's review the steps.

Input data:
![frame126](https://user-images.githubusercontent.com/79514917/149625512-aa3fc418-ee0f-4198-88bd-8dee1e7dee99.jpg)
