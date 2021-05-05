import face_recognition
import cv2
import numpy as np
import glob
import time
import matplotlib.pyplot as plt

# This is a demo of running face recognition on live video from your webcam. It's a little more complicated than the
# other example, but it includes some basic performance tweaks to make things run a lot faster:
#   1. Process each video frame at 1/4 resolution (though still display it at full resolution)
#   2. Only detect faces in every other frame of video.

# PLEASE NOTE: This example requires OpenCV (the `cv2` library) to be installed only to read from your webcam.
# OpenCV is *not* required to use the face_recognition library. It's only required if you want to run this
# specific demo. If you have trouble installing it, try any of the other demos that don't require it instead.

# Load a sample picture and learn how to recognize it.
me_image = face_recognition.load_image_file("me.jpg")
known_face_encoding0 = face_recognition.face_encodings(me_image)[0]

# Load a sample picture and learn how to recognize it.
me_image2 = face_recognition.load_image_file("me2.jpg")
known_face_encoding1 = face_recognition.face_encodings(me_image2)[0]

# Create arrays of known face encodings and their names
known_face_encodings = [
    known_face_encoding0,
    known_face_encoding1
]
known_face_names = [
    "me",
    "me2"
]

# Initialize some variables
face_locations = []
face_encodings = []
face_names = []
process_this_frame = True

me = 0
unknown = 0
count = 0
face_distance_thresholds = [0.4, 0.5, 0.6]
accuracies = []
name = "Unknown"

imagelist = glob.glob('/home/pi/face_recognition/examples/images/*.png')

t0 = time.time()

for face_distance_threshold in face_distance_thresholds:
    for image in imagelist:
        print(count)
        count += 1
        # Grab a single frame of video
        frame = cv2.imread(image)

        # Resize frame of video to 1/4 size for faster face recognition processing
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

        # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
        rgb_small_frame = small_frame[:, :, ::-1]

        # Find all the faces and face encodings in the current frame of video
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

        name = "Unknown"
        face_names = []
        for face_encoding in face_encodings:
            # See if the face is a match for the known face(s)
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding, face_distance_threshold)

            # Or instead, use the known face with the smallest distance to the new face
            face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
            best_match_index = np.argmin(face_distances)
            if matches[best_match_index]:
                name = known_face_names[best_match_index]

            face_names.append(name)

        if name == 'me':
            me += 1
        else:
            unknown += 1

    accuracy = (1 - me / (me + unknown))*100
    accuracies.append(accuracy)

t1 = time.time()
print(t1-t0)

print(accuracies)

plt.plot(face_distance_thresholds, accuracies)
plt.xlabel('FaceDistance')
plt.ylabel('FaceAccuracy(%)')
plt.xticks(np.arange(0.4, 0.7, 0.1))
plt.yticks(np.arange(95, 101, 1))
# plt.text(0.395, 99.5, "100%")
# plt.text(0.49, 99, "99.7%")
# plt.text(0.59, 96, "95.3%")
plt.show()
