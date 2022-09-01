import json
import face_recognition
import cv2
import numpy as np
import os

video_capture = cv2.VideoCapture(0)


# video_capture = cv2.VideoCapture('http://172.0.16.45:8080/video')


def face_recognitionn(known_face_encodings, known_face_names):
    face_locations = []
    face_names = []
    process_this_frame = True

    counter = 0
    counter2 = 0

    while True:
        # Grab a single frame of video
        ret, frame = video_capture.read()

        # Resize frame of video to 1/4 size for faster face recognition processing
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25, interpolation=cv2.INTER_CUBIC)

        # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
        rgb_small_frame = small_frame[:, :, ::-1]

        # Only process every other frame of video to save time
        if process_this_frame:
            # Find all the faces and face encodings in the current frame of video
            face_locations = face_recognition.face_locations(rgb_small_frame)
            face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

            face_names = []
            for face_encoding in face_encodings:
                # See if the face is a match for the known face(s)
                matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
                name = "Unknown"

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

            if name != 'Unknown':

                l_json = os.listdir("./jsons/")
                database_json = ""
                for i in l_json:
                    if i.split("__")[0] == name:
                        database_json = i

                f = open(f'./jsons/{database_json}', 'r')
                data = json.load(f)

                counter += 1

                if counter == 10:
                    if int(data['karta_hisob']) > 1400:
                        data['karta_hisob'] = str(int(data['karta_hisob']) - 1400)
                        with open(f"./jsons/{database_json}", "w") as outfile:
                            json.dump(data, outfile)
                    else:
                        counter2 = 404



                elif counter == 200:
                    counter = 0

                cv2.rectangle(frame, (left, top), (right, bottom), (242, 21, 21), 5)
                cv2.rectangle(frame, (left, bottom + 15), (right, bottom), (0, 0, 0), cv2.FONT_ITALIC)
                font = cv2.FONT_ITALIC
                cv2.putText(frame, name, (left + 10, bottom + 15), font, 1.0, (255, 255, 255), 2)

                if counter2 != 404:
                    cv2.putText(frame, "Paid : 1400 summ !", (left + 10, bottom - 260), font, 1.0, (40, 180, 5),
                                2)
                    cv2.putText(frame, f"Balance : {data['karta_hisob']} summ", (left + 10, bottom - 310), font, 1.0,
                                (40, 180, 5), 2)
                else:
                    cv2.putText(frame, "your money isn't enough !", (left - 50, bottom - 260), font, 1.0, (0, 0, 204), 2)
                    cv2.putText(frame, f"balance : {data['karta_hisob']} so'm", (left + 10, bottom - 310), font, 1.0,
                                (0, 0, 204),
                                2)



            else:

                # from pygame import mixer  # Load the popular external library
                #
                # mixer.init()
                # mixer.music.load('./mp3/unknown_person.mp3')
                # mixer.music.play()
                cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 204), 5)
                cv2.rectangle(frame, (left, bottom + 15), (right, bottom), (0, 0, 0), cv2.FONT_ITALIC)
                font = cv2.FONT_ITALIC
                cv2.putText(frame, name, (left + 10, bottom + 15), font, 1.0, (0, 0, 204), 2)
                cv2.putText(frame, "you didn't add to base !!!", (left + 10, bottom - 200), font, 1.0, (0, 0, 204), 2)

        cv2.imshow('Video', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release handle to the webcam
    video_capture.release()
    cv2.destroyAllWindows()


def main():
    into_dir = os.listdir("./photos/")

    known_face_encodings = [face_recognition.face_encodings(face_recognition.load_image_file(f"./photos/{i}"))[0] for i in into_dir]
    known_face_names = [i.split("__")[0] for i in into_dir]

    face_recognitionn(known_face_encodings, known_face_names)


main()
