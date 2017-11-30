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


photo_record_mode = True
Test_folder = "2017_11_30-002-world"
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
        if os.path.splitext(file)[-1] != '.jpg':
            continue
        if "2017_11_30-002-world-frame-00000" not in file:
          continue
        photo_name = os.path.splitext(file)[0]
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

        if len(current_markers):
            for i in range(len(current_markers)):
                marker_pos = current_markers[i]['img_pos'][0], current_markers[i]['img_pos'][1]
                s = current_markers[i]['ellipses'][-1][1][0], current_markers[i]['ellipses'][-1][1][1]
                print(current_markers[i]['marker_type'], "marker found. Pos =", marker_pos, s)
        else:
            print("No marker found")

        if photo_record_mode:
            for i in range(len(current_markers)):
                marker_pos = int(current_markers[i]['img_pos'][0]), int(current_markers[i]['img_pos'][1])
                color = (0, 0, 255) if current_markers[i]['marker_type'] == 'Stop' else (0, 255, 0)
                for ellipse in current_markers[i]["ellipses"]:
                    cv2.ellipse(image, ellipse, color=color, thickness=1)
                cv2.circle(image, marker_pos, 2, (0, 0, 255), -1)
            cv2.imwrite(os.path.join(marked_image_folder, "{}.jpg".format(photo_name)), image)

            from circle_detector import edges, img_ellipse, mask_ring, mask_outer, mask_middle, mask_edge

            if edges is not None:
                for i in range(len(edges)):
                    cv2.imwrite(os.path.join(marked_image_folder, "{0}-edges-{1}.jpg".format(photo_name, i)), edges[i])
            if img_ellipse is not None:
                cv2.imwrite(os.path.join(marked_image_folder, "{0}-img_ellipse.jpg".format(photo_name)), img_ellipse)

            if mask_ring is not None and img_ellipse.shape[::-1] == mask_ring.shape[::-1]:
                temp = cv2.add(img_ellipse, mask_ring)
                cv2.imwrite(os.path.join(marked_image_folder, "{0}-mask_ring.jpg".format(photo_name)), temp)
            if mask_middle is not None and img_ellipse.shape[::-1] == mask_middle.shape[::-1]:
                temp = cv2.add(img_ellipse, mask_middle)
                cv2.imwrite(os.path.join(marked_image_folder, "{0}-mask_middle.jpg".format(photo_name)), temp)
            if mask_outer is not None:
                if len(current_markers) and img_ellipse.shape[::-1] == mask_outer.shape[::-1]:
                    temp = cv2.add(img_ellipse, mask_outer)
                    cv2.imwrite(os.path.join(marked_image_folder, "{0}-outer.jpg".format(photo_name)), temp)
                cv2.imwrite(os.path.join(marked_image_folder, "{0}-mask_outer.jpg".format(photo_name)), mask_outer)
            if mask_edge is not None:
                cv2.imwrite(os.path.join(marked_image_folder, "{0}-mask_edge.jpg".format(photo_name)), mask_edge)

Total_duration = np.array(duration).sum()

print("===== RESULT =====")
print("# of images =", image_count)
print("Duration =", round(Total_duration, 2), "s")
print("fps  =", round(image_count / Total_duration, 2))