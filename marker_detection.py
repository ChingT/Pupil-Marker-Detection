"""

Find the center by circle_tracker.update()
Write the debugs images
calculate the fps

"""

import cv2
import numpy as np
import os
import timeit
from circle_detector import CircleTracker
from circle_detector import edges, img_ellipse, mask_ring_dot, mask_outer, mask_middle

photo_record_mode = True
Test_folder = "2017_11_28-000-world"
if photo_record_mode:
    marked_image_folder = "{0}/{0}-marked".format(Test_folder)
    if not os.path.exists(marked_image_folder):
        os.makedirs(marked_image_folder)

circle_tracker = CircleTracker(wait_interval=1)

duration = []
image_count = 0

for root, dirs, files in os.walk(Test_folder):
    if "marked" in root:
        continue
    files.sort()
    for file in files:
        if os.path.splitext(file)[-1] == '.jpg':
            if "2017_11_28-000-world-frame-" not in file:
              continue
            photo_name = file
            photo_path = os.path.join(root, file)
            image = cv2.imread(photo_path)
            img_size = image.shape[::-1][1]
            gray_img = cv2.imread(photo_path, 0)
            print(photo_name)
            image_count += 1

            start_time = timeit.default_timer()
            current_markers = circle_tracker.update(gray_img)
            end_time = timeit.default_timer()
            duration.append(end_time - start_time)

            if photo_record_mode:
                for i in range(len(current_markers)):
                    marker_pos = current_markers[i]['img_pos']
                    print(current_markers[i]['marker_type'], "marker found. Pos =", marker_pos)
                    color = (0, 0, 255) if current_markers[i]['marker_type'] == 'Stop' else (0, 255, 0)
                    for x in range(len(current_markers[i]["ellipses"])):
                        cv2.ellipse(image, current_markers[i]["ellipses"][x], color=color, thickness=1)
                    cv2.circle(image, (int(marker_pos[0]), int(marker_pos[1])), 2, (0, 0, 255), -1)
                cv2.imwrite(os.path.join(marked_image_folder, photo_name), image)

                if edges is not None:
                    for ii in range(len(edges)):
                        cv2.imwrite(os.path.join(marked_image_folder, "{0}-edges-{1}.jpg".format(os.path.splitext(file)[0], ii)), edges[ii])
                if mask_ring_dot is not None:
                    temp = cv2.add(img_ellipse, mask_ring_dot)
                    cv2.imwrite(os.path.join(marked_image_folder, "{0}-mask_ring.jpg".format(os.path.splitext(file)[0])), temp)
                if mask_middle is not None:
                    temp = cv2.add(img_ellipse, mask_middle)
                    cv2.imwrite(os.path.join(marked_image_folder, "{0}-mask_middle.jpg".format(os.path.splitext(file)[0])), temp)
                if mask_outer is not None:
                    temp = cv2.add(img_ellipse, cv2.bitwise_not(mask_outer))
                    cv2.imwrite(os.path.join(marked_image_folder, "{0}-outer.jpg".format(os.path.splitext(file)[0])), temp)
                    cv2.imwrite(os.path.join(marked_image_folder, "{0}-mask_outer.jpg".format(os.path.splitext(file)[0])), mask_outer)
                if img_ellipse is not None:
                    cv2.imwrite(os.path.join(marked_image_folder, "{0}-img_ellipse.jpg".format(os.path.splitext(file)[0])), img_ellipse)

Total_duration = np.array(duration).sum()

print("===== RESULT =====")
print("# of images =", image_count)
print("Duration =", Total_duration)
print("fps  =", image_count / Total_duration)