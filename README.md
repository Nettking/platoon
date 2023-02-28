# platoon
Platooning project

This repository provides a collection of code files for a project involving autonomous vehicles. Using computer vision methods, the project entails recognizing and following roadway lanes. The repository's primary scripts utilize OpenCV and NumPy to receive video input from a front-mounted camera, recognize lane lines in the picture, and produce steering instructions to control the car's movement.

This repository provides code for the GoPiGo3 robot, an educational and experimental robot based on the Raspberry Pi. The code contains capabilities for identifying and following lane lines in a video stream, as well as calculating and adjusting wheel speeds depending on steering angle. The code for lane identification utilizes OpenCV, while the code for robot control uses the GoPiGo3 library. This code is intended for use with the GoPiGo3 robot, but it is adaptable for use with other robots and applications.

This research demonstrates the use of computer vision and machine learning in real-world applications, such as autonomous driving. It may be used as a jumping off point for similar projects or as a resource for studying computer vision and machine learning methods.

## Getting started
To get started with the project, you'll need to clone the repository and install the required packages:<br />
```sh
git clone https://github.com/Nettking/platoon.git
```
```sh
sudo apt update && sudo apt install -y cmake g++ wget unzip
```
First, you need to make sure that your GoPiGo3 has a Raspberry Pi board and that it is connected to the internet.<br />

Open a terminal window on your GoPiGo3 and type the following command to update the packages:<br />


sudo apt-get update
```

Install the dependencies required to build OpenCV:

```sh
sudo apt-get install build-essential cmake pkg-config
sudo apt-get install libjpeg-dev libtiff5-dev libjasper-dev libpng-dev libavcodec-dev libavformat-dev libswscale-dev libv4l-dev libxvidcore-dev libx264-dev libgtk-3-dev libcanberra-gtk* libatlas-base-dev gfortran python3-dev
```

Download the OpenCV source code:


wget -O opencv.zip https://github.com/opencv/opencv/archive/4.3.0.zip
unzip opencv.zip

Create a build directory and navigate to it:

```sh
mkdir build
cd build
```

Run the following command to configure the build with the required options:

```sh
cmake -D CMAKE_BUILD_TYPE=RELEASE -D CMAKE_INSTALL_PREFIX=/usr/local -D OPENCV_EXTRA_MODULES_PATH=../opencv_contrib-4.5.4/modules -D ENABLE_NEON=ON -D ENABLE_VFPV3=ON -D BUILD_TESTS=OFF -D INSTALL_PYTHON_EXAMPLES=OFF -D BUILD_EXAMPLES=OFF ..
```

Build and install OpenCV:

```sh
make -j4
sudo make install
sudo ldconfig
```

Verify that OpenCV is installed by running a Python script that uses OpenCV:

```sh
python3
import cv2
print(cv2.__version__)
```
If everything is working correctly, you should see the version number of OpenCV printed on the screen.

```sh
pip install -r requirements.txt
```
You can then run the run.py script to retrieve the historical data and train the machine learning model:
```sh
python run.py
```
