# Description
The world's simplest GUI-based Facial Recognition System built using the <a href="https://github.com/ageitgey/face_recognition">face_recognition</a> library.
<p align="center"> <img src="https://github.com/dhairyapatel1506/facial-recognition/assets/101339040/df7a5291-20ab-4004-a3cb-ee252bb38186"> </p>

# Features
- Can recgonize faces through images.
- Can recognize faces in real-time through a webcam.
- Can recognize faces through video.

<!--# Requirements & Setup
- First, refer <a href="https://github.com/ageitgey/face_recognition/#installation">this</a> for the requirements and to install all the basic dependencies.
- Then, install ffmpeg (Video Recognition won't work without this) and you should be good to go:
   - ```sudo apt install ffmpeg```
-->
# Requirements & Setup

- First, refer to [this guide](https://github.com/ageitgey/face_recognition/#installation) for installing `dlib`, which is a dependency for `face_recognition`.

- Then, install the following system dependencies:
  ```bash
  sudo apt update
  sudo apt install python3-pip
  sudo apt install ffmpeg         # Required for video recognition
  sudo apt install python3-tk     # Required for tkinter GUI support
  ```

- Install the required Python packages:
  ```bash
  pip install opencv-python-headless  # For cv2
  pip install numpy                   # For numerical operations
  pip install pillow                  # For image processing with PIL
  pip install face_recognition        # For face recognition
  pip install ffmpeg-python           # Wrapper for ffmpeg
  ```

# Usage
<p align="center"> <img src="https://github.com/dhairyapatel1506/facial-recognition/assets/101339040/8f11f10b-54d3-4394-8fdb-d70266a10c7c"> </p>

I've included 4 sample files with the project—3 images and 1 video, all labelled _unknown_. You can use these to test the program. 

<p align="center"> <img src="https://github.com/dhairyapatel1506/facial-recognition/assets/101339040/def1e1a9-6fb9-4901-8693-e9b45c0f5e13"> </p>

_Image Database_ is the folder that stores the images of the people you want the system to recognize. I've also included 2 sample images in here, of Biden and Obama. You can add your own images to this folder and save them with the name that you want the system to identify that person with.
<br></br>

Run: ```python main.py```

# ToDo
  <p>☐ Implement multi-threading/multi-processing to increase video processing speeds.</p>
  <p>☐ Implement feature to add new images through the user interface.</p>
  <p>☐ Display the time taken in completing a functionality.</p>
  
