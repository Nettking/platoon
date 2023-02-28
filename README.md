# platoon
Platooning project

This repository provides a collection of code files for a project involving autonomous vehicles. Using computer vision methods, the project entails recognizing and following roadway lanes. The repository's primary scripts utilize OpenCV and NumPy to receive video input from a front-mounted camera, recognize lane lines in the picture, and produce steering instructions to control the car's movement.

This repository provides code for the GoPiGo3 robot, an educational and experimental robot based on the Raspberry Pi. The code contains capabilities for identifying and following lane lines in a video stream, as well as calculating and adjusting wheel speeds depending on steering angle. The code for lane identification utilizes OpenCV, while the code for robot control uses the GoPiGo3 library. This code is intended for use with the GoPiGo3 robot, but it is adaptable for use with other robots and applications.

This research demonstrates the use of computer vision and machine learning in real-world applications, such as autonomous driving. It may be used as a jumping off point for similar projects or as a resource for studying computer vision and machine learning methods.

## Getting started
To get started with the project, you'll need to clone the repository and install the required packages:<br />
```sh
git clone https://github.com/Nettking/python_ml.git
```
```sh
pip install -r requirements.txt
```
You can then run the run.py script to retrieve the historical data and train the machine learning model:
```sh
python run.py
```
