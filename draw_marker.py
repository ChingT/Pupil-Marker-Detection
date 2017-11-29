"""

To draw Ref marker and Stop marker on A4 paper
(A4 size = 210 x 297 mm)

"""

import cv2
import numpy as np

paper_size = 2100, 2100
center = paper_size[0]//2, paper_size[1]//2

cross_size = 20
normal_marker = np.ones(paper_size)*255
cv2.circle(normal_marker, center, 940, (180, 180, 180), thickness=2)
cv2.circle(normal_marker, center, 600, (0, 0, 0), thickness=-1)
cv2.circle(normal_marker, center, 380, (255, 255, 255), thickness=-1)
cv2.circle(normal_marker, center, 190, (0, 0, 0), thickness=-1)
rectangle_points = (center[0], center[1] - cross_size), (center[0], center[1] + cross_size)
cv2.rectangle(normal_marker, rectangle_points[0], rectangle_points[1], (200, 200, 200), cross_size//2)
rectangle_points = (center[0] - cross_size, center[1]), (center[0] + cross_size, center[1])
cv2.rectangle(normal_marker, rectangle_points[0], rectangle_points[1], (200, 200, 200), cross_size//2)

stop_marker = np.ones(paper_size)*255
cv2.circle(stop_marker, center, 940, (0, 0, 0), thickness=-1)
cv2.circle(stop_marker, center, 600, (255, 255, 255), thickness=-1)
cv2.circle(stop_marker, center, 380, (0, 0, 0), thickness=-1)
cv2.circle(stop_marker, center, 190, (255, 255, 255), thickness=-1)

markers = np.bmat([[normal_marker, normal_marker], [stop_marker, stop_marker]])
cv2.imwrite("New_markers_A4.jpg", markers)
