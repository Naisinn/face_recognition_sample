# システム全体のパッケージ（apt でインストールされた picamera2 も含む）を仮想環境内で利用できるように
import sys
sys.path.append("/usr/lib/python3/dist-packages")

import face_recognition
import cv2
import numpy as np
from dispFps import DispFps
import csv

# 追加：Picamera2 と time のインポート
from picamera2 import Picamera2
import time

# Get a reference to webcam #0 (the default one)
# 変更：cv2.VideoCapture(0) の代わりに Picamera2 を使用
picam2 = Picamera2()
config = picam2.create_preview_configuration(main={"format": "XRGB8888", "size": (640, 480)})
picam2.configure(config)
picam2.start()
time.sleep(1)

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

csvdata = []
dispFps = DispFps()

while True:
    # Grab a single frame of video
    # 変更：Picamera2 で1フレームを取得（numpy.ndarray形式）し、4チャンネル(XRGB8888)→RGB→BGRに変換
    frame_4ch = picam2.capture_array("main")
    rgb_image = frame_4ch[:, :, 1:]  # 最初のチャンネルを捨てて RGB を得る
    frame = cv2.cvtColor(rgb_image, cv2.COLOR_RGB2BGR)  # OpenCV 表示用に BGR に変換

    # Resize frame of video to 1/4 size for faster face recognition processing
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

    # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
    rgb_small_frame = small_frame[:, :, ::-1]
    # 追加：face_recognition で正しく処理できるように C-contiguous な配列に変換
    rgb_small_frame = np.ascontiguousarray(rgb_small_frame)

    # Only process every other frame of video to save time
    if process_this_frame:
        # Find all the faces and face encodings in the current frame of video
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

        face_names = []
        for face_encoding in face_encodings:
            # See if the face is a match for the known face(s)
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding, 0.4)
            name = "Unknown"

            # # If a match was found in known_face_encodings, just use the first one.
            # if True in matches:
            #     first_match_index = matches.index(True)
            #     name = known_face_names[first_match_index]

            # Or instead, use the known face with the smallest distance to the new face
            face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
            best_match_index = np.argmin(face_distances)
            if matches[best_match_index]:
                name = known_face_names[best_match_index]

            face_names.append(name)

    process_this_frame = not process_this_frame


    # Display the results
    for (top, right, bottom, left), name in zip(face_locations, face_names):
        # Scale back up face locations since the frame we detected in was scaled to 1/4 size
        top *= 4
        right *= 4
        bottom *= 4
        left *= 4

        # Draw a box around the face
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

        # Draw a label with a name below the face
        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

    time, fps, cpu_temp = dispFps.disp(frame)
    fps = fps.replace('FPS: ', '')
    cpu_temp = cpu_temp.replace('\'C', '')
    csvdata.append([time, fps, cpu_temp])

    # Display the resulting image
    cv2.imshow('Video', frame)

    # Hit 'q' on the keyboard to quit!
    if cv2.waitKey(1) & 0xFF == ord('q'):
        header = [['time(s)', 'FPS(1/s)', 'CPU Temperature(\'C)']]
        with open("csvdata.csv", "w") as f:
            writer = csv.writer(f, lineterminator="\n")
            csvdata = header + csvdata
            writer.writerows(csvdata)
        break

# Release handle to the webcam
# 変更：cv2.VideoCapture の代わりに picamera2 の停止処理
picam2.stop()
cv2.destroyAllWindows()