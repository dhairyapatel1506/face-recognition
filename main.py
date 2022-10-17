import cv2
import numpy as np
from tkinter import *
from tkinter import ttk
from PIL import ImageTk, Image, ImageDraw
from tkinter import filedialog
import face_recognition
import os
import shutil
import ffmpeg

def clear_screen():
    count = 0
    # Destroys all widgets except the background image Label
    for widget in root.winfo_children():
        if str(widget).startswith(".!label") and count != 0:
                widget.destroy()
                count += 1

def image_recognition():
    global my_image
    clear_screen()

    # Opens File Dialog Box
    root.filename = filedialog.askopenfilename(initialdir="/home/dhairyapatel/Pictures", title="Select an image", filetypes=(("Image files", "*.jpg *.jpeg *.png *.webp *.avif"), ("All files", "*.*")))

    if(root.filename):
        
        # Loads selected image
        unknown_image = face_recognition.load_image_file(root.filename)

        # Locates all faces in the image
        face_locations = face_recognition.face_locations(unknown_image)

        # Generates Encodings
        unknown_encodings = face_recognition.face_encodings(unknown_image, face_locations)

        # Converts image to a PIL-format image so that it can be drawn on with the Pillow library
        pil_image = Image.fromarray(unknown_image)

        # Creates a Pillow ImageDraw Draw instance to draw with
        draw = ImageDraw.Draw(pil_image)
        
        # Loops through each face found in the unknown image
        for (top, right, bottom, left), unknown_encoding in zip(face_locations, unknown_encodings):

            # Looks for a match from the known face(s)
            results = face_recognition.compare_faces(known_face_encodings, unknown_encoding, 0.45)

            name = "Unknown"

            face_distances = face_recognition.face_distance(known_face_encodings, unknown_encoding)
            best_match_index = np.argmin(face_distances)
            if results[best_match_index]:
                name = known_face_names[best_match_index]

            # Draws a box around the face using the Pillow module
            draw.rectangle(((left, top), (right, bottom)), outline=(0, 0, 255))

            # Draws a label with the name below the face
            text_width, text_height = draw.textsize(name)
            draw.rectangle(((left, bottom - text_height - 10), (right, bottom)), fill=(0, 0, 255), outline=(0, 0, 255))
            draw.text((left + 6, bottom - text_height - 5), name, fill=(255, 255, 255, 255))

        # Removes the drawing library from memory
        del draw

        # Displays and saves the resulting image
        pil_image.show()
        pil_image.save("output.jpg")

def image_add():
    clear_screen()
    root.filename = filedialog.askopenfilename(initialdir="/home/dhairyapatel", title="Select an image", filetypes=(("Image files", "*.jpg *.jpeg *.png *.webp *.avif"), ("All files", "*.*")))
    if(root.filename):
        
        # Copies the selected image to the Database
        shutil.copy(root.filename, "Database")

        my_label = Label(root, text="The image was added to the Database").grid(row=1, column=1)

def webcam_recognition():

    # Gets a reference to webcam #0 (default)
    video_capture = cv2.VideoCapture(0)

    while True:

        # Grabs a single frame of the video
        ret, frame = video_capture.read()

        # Converts the image from BGR color (used by OpenCV) to RGB color (used by face_recognition)
        rgb_frame = frame[:, :, ::-1]

        # Finds all the faces in the frame and generates Encodings
        face_locations = face_recognition.face_locations(rgb_frame)
        unknown_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

        # Loops through each face in the frame
        for (top, right, bottom, left), unknown_encoding in zip(face_locations, unknown_encodings):
            # Looks for a match from the known face(s)
            matches = face_recognition.compare_faces(known_face_encodings, unknown_encoding, 0.50)

            name = "Unknown"

            face_distances = face_recognition.face_distance(known_face_encodings, unknown_encoding)
            best_match_index = np.argmin(face_distances)
            if matches[best_match_index]:
                name = known_face_names[best_match_index]

            # Draws a box around the face
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

            # Draws a label with the name below the face
            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

        # Displays the resulting frame
        cv2.imshow('Video', frame)

        # Exits on pressing 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Releases webcam handle
    video_capture.release()
    cv2.destroyAllWindows()

def video_recognition():
    rotateCode = 0
    root.filename = filedialog.askopenfilename(initialdir="/home/dhairyapatel/Videos", title="Select a video", filetypes=(("Video files", "*.mp4"), ("All files", "*.*")))

    if(root.filename):

        # Opens the input movie file
        input_movie = cv2.VideoCapture(root.filename)

        length = int(input_movie.get(cv2.CAP_PROP_FRAME_COUNT))
        fps = int(input_movie.get(cv2.CAP_PROP_FPS))

        # Gets metadata of the file
        meta_dict = ffmpeg.probe(root.filename)

        # Checks if metadata contains rotate tag
        if 'rotate' in meta_dict['streams'][0]['tags']:
            rotateCode = 1

        ret, frame = input_movie.read()
        height, width, channels = frame.shape
            
        # Creates an output movie file
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        output_movie = cv2.VideoWriter('output.avi', fourcc, fps, (width, height))

        # Initializes some variables
        face_locations = []
        face_encodings = []
        face_names = []
        frame_number = 0
        
        while True:

            # Grabs a single frame of the video
            if(frame_number>1):
                ret, frame = input_movie.read()

            # Flips the frame by 180 degrees if rotateCode equals 1
            if rotateCode:
                frame = cv2.flip(frame, flipCode=-1)

            frame_number += 1

            # Quit when the input video file ends
            if not ret:
                break

            # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
            rgb_frame = frame[:, :, ::-1]

            # Find all the faces and face encodings in the current frame of video
            face_locations = face_recognition.face_locations(rgb_frame)
            face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

            face_names = []
            for face_encoding in face_encodings:

                # Look for a match from the known faces
                results = face_recognition.compare_faces(known_face_encodings, face_encoding)

                name = None
                
                face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
                best_match_index = np.argmin(face_distances)
                if results[best_match_index]:
                    name = known_face_names[best_match_index]
                                
                face_names.append(name)

            # Labels the results
            for (top, right, bottom, left), name in zip(face_locations, face_names):
                if not name:
                    continue

                # Draws a box around the face
                cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

                # Draws a label with a name below the face
                cv2.rectangle(frame, (left, bottom - 25), (right, bottom), (0, 0, 255), cv2.FILLED)
                font = cv2.FONT_HERSHEY_DUPLEX
                cv2.putText(frame, name, (left + 6, bottom - 6), font, 0.5, (255, 255, 255), 1)

            # Writes the resulting image to the output video file
            print("Writing frame {} / {}".format(frame_number, length))
            output_movie.write(frame)
            if(frame_number==length):
                break

        # All done!
        input_movie.release()
        cv2.destroyAllWindows()

root = Tk()
root.resizable(height = None, width = None)
root.geometry("1294x800")
root.title("Facial Recognition System")
background=Image.open('bg.png')
my_background=ImageTk.PhotoImage(background)
my_label=ttk.Label(root, image=my_background)
my_label.place(x=0, y=0, relwidth=1, relheight=1)
known_face_names = []
known_face_encodings = []

# Creates arrays of known face Encodings and their names
for file in os.listdir("Database"):
    known_image = face_recognition.load_image_file(f"Database/{file}")
    known_encoding = face_recognition.face_encodings(known_image)[0]
    known_face_encodings.append(known_encoding)
    known_face_names.append(file.split(".")[0].title())

imageRecognitionButton = Button(root, text="Image Recognition", command=image_recognition).place(relx=0.2, rely=0.5, anchor=CENTER)
webcamRecognitionButton = Button(root, text="Live Webcam Recognition", command=webcam_recognition).place(relx=0.5, rely=0.5, anchor=CENTER)
videoRecognitionButton = Button(root, text="Video Recognition", command=video_recognition).place(relx=0.8, rely=0.5, anchor=CENTER)

root.mainloop()
