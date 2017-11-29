"""

To extract the frames from videos

"""

import cv2
import os

interval = 5

for root, dirs, files in os.walk("."):
    if "Done" in root:
        continue
    for file in files:
        if os.path.splitext(file)[-1] == '.mp4':
            if not "2017_11_28-000-world" in file:
                continue
            file_path = os.path.join(root, os.path.splitext(file)[0])
            print(file_path)
            if not os.path.exists(file_path):
                os.makedirs(file_path)
            cap = cv2.VideoCapture(os.path.join(root, file))
            count = 0

            while cap.isOpened():
                if count % interval == 0:
                    _, frame = cap.read()
                    if frame is None:
                        break
                    photo_name = "{0}-frame-{number:05}.jpg".format(os.path.splitext(file)[0], number=count)
                    cv2.imwrite(os.path.join(file_path, photo_name), frame)
                    print(photo_name)
                else:
                    if cap.grab() is None:
                        break
                count = count + 1
                # if cv2.waitKey(10) & 0xFF == ord('q'):
                #     break

            cap.release()
            cv2.destroyAllWindows()