import math
import numpy as np
from easygopigo3 import EasyGoPiGo3
from cv2 import cvtColor, GaussianBlur, Canny, HoughLinesP, line, addWeighted, resize, imshow, fillPoly, bitwise_and, VideoCapture, rectangle, CAP_PROP_FRAME_WIDTH, CAP_PROP_FRAME_HEIGHT, COLOR_BGR2GRAY, waitKey, destroyAllWindows
from pyzbar.pyzbar import decode as decode_qr
import requests
import paho.mqtt.client as mqtt
import subprocess

class PlatoonVehicle:
    def __init__(self, speed=0, distance=100, MQTT_TOPIC_SUB = "test/in", MQTT_TOPIC_PUB = "test/out", MQTT_BROKER_PORT = 1883):
        
        # Speed of the vehicle
        self.speed = speed

        # Distance of the vehicle from the vehicle in front of it
        self.distance = distance

        # Unique IP address of the vehicle
        response = requests.get('https://api.ipify.org')
        public_ip_address = response.text
        self.unique_ip = str(public_ip_address)
        self.gpg = EasyGoPiGo3()
        gpg = self.gpg

        self.distance_sensor = gpg.init_distance_sensor()
        self.distance = 10
        self.last_angle = 90
        gpg.set_speed(0)

        # Initialize video capture and set resolution
        self.video = VideoCapture(0)
        self.video.set(CAP_PROP_FRAME_WIDTH,320)
        self.video.set(CAP_PROP_FRAME_HEIGHT,240)

        self.MQTT_BROKER_PORT = MQTT_BROKER_PORT
        self.MQTT_TOPIC_SUB = MQTT_TOPIC_SUB
        self.MQTT_TOPIC_PUB = MQTT_TOPIC_PUB
    
    def error_handling(self, exc_type, exc_value, exc_traceback):
        print("Traceback (most recent call last):")
        while exc_traceback:
            print("  File \"{}\", line {}, in {}".format(exc_traceback.tb_frame.f_code.co_filename,
                                                         exc_traceback.tb_lineno,
                                                         exc_traceback.tb_frame.f_code.co_name))
            exc_traceback = exc_traceback.tb_next

    ####################################################################
    ##### MQTT
    ####################################################################
    def send_message(client, MQTT_TOPIC_SUB, message = "Hello, world!"):
        # Publish a message to the specified topic
        client.publish(MQTT_TOPIC_SUB, message)
        print("Published message: " + message)

    # Define the callback function for receiving MQTT messages
    def on_message(self, client, MQTT_TOPIC_PUB, message):
        # Decode the message payload from bytes to string
        payload = message.payload.decode()
        response = "Received: " + payload
        print(response)
        # Publish a response message back to the specified topic
        self.send_message(client, MQTT_TOPIC_PUB, message = response)
        
    def establish_connection(self, MQTT_BROKER_ADDR, MQTT_BROKER_PORT,MQTT_TOPIC_SUB, MQTT_TOPIC_PUB, message = "Hello, world!"):
        # Set up the MQTT client and connect to the broker
        client = mqtt.Client()
        client.connect(MQTT_BROKER_ADDR, MQTT_BROKER_PORT)

        # Set up the callback function for receiving messages
        client.on_message = self.on_message(client, MQTT_TOPIC_PUB, message)
        # Subscribe to the specified topic
        client.subscribe(MQTT_TOPIC_SUB)
        
        self.send_message(client, MQTT_TOPIC_SUB, message = message)

        # Start the MQTT client loop to process incoming messages
        #client.loop_start()
        client.loop(timeout=0.01)


    def connect_to_all_brokers(self):
        # Define the MQTT broker address and port
        MQTT_BROKER_PORT = 1883

        # Define the MQTT topics to subscribe and publish to
        MQTT_TOPIC_SUB = "test/in"
        MQTT_TOPIC_PUB = "test/out"
        common_ip = "158.39.162."
        unique_ip = ["127","157","181","197"]
        
        for ip in unique_ip:
            full_ip = common_ip + ip
            if self.unique_ip != full_ip:
                try:
                    self.establish_connection(full_ip, MQTT_BROKER_PORT,MQTT_TOPIC_SUB, MQTT_TOPIC_PUB, self.unique_ip)
                except Exception as e:
                    print('Error connecting to: ' + full_ip)
                    #self.error_handling(type(e), e, e.__traceback__)
    
    def start_script_on_other_vehicle(self, remote_ip):
        username = "pi"   # Replace with your remote machine's username
        password = "gopigo"   # Replace with your remote machine's password
        remote_script_path = "/home/pi/platoon/run.py"  # Replace with the path to the Python script on the remote machine

        # Construct the SSH command
        command = "sshpass -p '{}' ssh {}@{} sudo python3 {}".format(password, username, remote_ip, remote_script_path)

        # Execute the command using subprocess
        result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        # Check if the command was successful
        if result.returncode == 0:
            print("Script executed successfully on remote machine {}".format(remote_ip))
            print("Output:")
            print(result.stdout.decode("utf-8"))
        else:
            print("Error executing script on remote machine {}".format(remote_ip))
            print("Error message:")
            print(result.stderr.decode("utf-8"))

    
    
    
    
    @staticmethod
    def locateQR(frame):
       
        decoded_objs = decode_qr(frame)
        imshow('QR Detection', frame)
        if decoded_objs == None:
            print('decoded_objs == None')
            raise Exception
        for obj in decoded_objs:
            # Get the barcode's data and type
            data = obj.data.decode("utf-8")
            
            barcode_type = obj.type
            
            # Get the barcode's bounding box and calculate the center
            left, top, width, height = obj.rect
            center_x = left + (width / 2)
            center_y = top + (height / 2)
            
            # Calculate the horizontal and vertical offsets from the center of the frame
            x_offset = center_x - (frame.shape[1] / 2)
            y_offset = center_y - (frame.shape[0] / 2)
            
            # Draw a red rectangle around the barcode
            rectangle(frame, (left, top), (left+width, top+height), (0, 0, 255), 2)
            imshow('QR Detection', frame)
            
            
            return data, x_offset, y_offset

    @staticmethod
    def make_points(frame, line):
        # Get the height and width of the input frame
        height, width, _ = frame.shape

        # Unpack the slope and intercept of the line
        slope, intercept = line

        # Calculate the y-coordinates of the endpoints of the line
        y1 = height  # bottom of the frame
        y2 = int(y1 / 2)  # make points from middle of the frame down

        # Handle the case where the slope is zero
        if slope == 0:
            slope = 0.1
            
        # Calculate the x-coordinates of the endpoints of the line using the
        # slope-intercept form of a line
        x1 = int((y1 - intercept) / slope)
        x2 = int((y2 - intercept) / slope)

        # Return the endpoints of the line as a list of two points
        return [[x1, y1, x2, y2]]

    def compare_to_last_angle(self, angle):
        # Calculate the difference between the input value and the last stored value
        diff = abs(self.last_angle - angle)
        
        # Compare the difference to a threshold of 100
        if diff < 100:
            # Store the input value as the last value
            self.last_angle = angle
            # Return the input value
            return angle
        
        if diff > 100:
            # Store the input value as the last value
            self.last_angle = angle
            # Return the last stored value
            return self.last_angle
        
    @staticmethod
    def detect_edges(frame):

        # Convert the color image to grayscale
        img = cvtColor(frame, COLOR_BGR2GRAY)

        # Apply Gaussian blur to the grayscale image
        blur = GaussianBlur(img, (5,5), 0)

        # Apply Canny edge detection to the blurred image
        edges = Canny(blur, 100, 200)

        return edges

    @staticmethod
    def region_of_interest(edges):

        # Get the height and width of the input image
        height, width = edges.shape
        
        # Create a mask with the same shape as the input image
        mask = np.zeros_like(edges)

        # Define a polygon that outlines the lower half of the image
        polygon = np.array([[
            (0, height),
            (0,  height/3),
            (width , height/3),
            (width , height),
        ]], np.int32)
        
        # Fill the polygon with white color
        fillPoly(mask, polygon, 255)
        
        # Apply the mask to the input image using bitwise AND operation
        cropped_edges = bitwise_and(edges, mask)
        
        return cropped_edges

    @staticmethod
    def detect_line_segments(cropped_edges):

        # Set the distance resolution of the Hough grid in pixels
        rho = 1
        
        # Set the angle resolution of the Hough grid in radians
        theta = np.pi / 180  
        
        # Set the threshold for line detection in Hough space
        min_threshold = 10  
        
        # Apply the probabilistic Hough transform to the input image to detect line segments
        line_segments = HoughLinesP(cropped_edges, rho, theta, min_threshold, 
                                        np.array([]), minLineLength=40, maxLineGap=80)
        
        return line_segments

    #@staticmethod            
    def average_slope_intercept(self, frame, line_segments):
        
        # Initialize the list of lane lines
        lane_lines = []
        
        # If no line segments were detected, stop the robot and return an empty list of lane lines
        if line_segments is None:
            print("no line segments detected")
            return lane_lines

        # Get the height and width of the input image
        height, width, _ = frame.shape
        
        # Initialize the lists of left and right line fits
        left_fit = []
        right_fit = []
        
        # Define the region of interest for the left and right lane lines
        boundary = 1/2
        # The left region of interest is the left half of the image
        left_region_boundary = width * (1 - boundary)
        # Oppsite for right region of interest
        right_region_boundary = width * boundary

        # Iterate over all line segments and fit a line to each segment
        for line_segment in line_segments:
            
            # Iterate over the endpoints of the line segment
            for x1, y1, x2, y2 in line_segment:
                
                # Skip vertical lines (slope = infinity)
                if x1 == x2:
                    print("skipping vertical lines (slope = infinity")
                    continue
                
                # Fit a line to the line segment using linear regression
                #fit = np.polyfit((x1, x2), (y1, y2), 1)
                # Calculate the slope and intercept of the line
                slope = (y2 - y1) / (x2 - x1)
                
                # Calculate the intercept of the line
                intercept = y1 - (slope * x1)
                
                # Classify the line segment as left or right based on the slope and x-coordinate of endpoints
                if slope < 0:
                    # If the slope is negative, the line segment is on the left side of the image
                    if x1 < left_region_boundary and x2 < left_region_boundary:
                        left_fit.append((slope, intercept))
                else:
                    # If the slope is positive, the line segment is on the right side of the image
                    if x1 > right_region_boundary and x2 > right_region_boundary:
                        right_fit.append((slope, intercept))
        
        # Calculate the average slope and intercept for the left and right line fits
        left_fit_average = np.average(left_fit, axis=0)
        # If there are no left line fits, return an empty list of lane lines
        if len(left_fit) > 0:
            # Calculate the endpoints of the left lane line
            lane_lines.append(self.make_points(frame, left_fit_average))

        # Repeat for the right lane line
        right_fit_average = np.average(right_fit, axis=0)
        if len(right_fit) > 0:
            lane_lines.append(self.make_points(frame, right_fit_average))

        return lane_lines


    def display_lines(self, frame, lines, line_color=(0, 255, 0), line_width=6):
        

        line_image = np.zeros_like(frame)
        
        # Draw lines on the line image using the OpenCV line() function.
        if lines is not None:
            for line_piece in lines:
                
                for x1, y1, x2, y2 in line_piece:
                    # Draw the line on the line image using OpenCV.
                    line(line_image, (x1, y1), (x2, y2), line_color, line_width)
            
        # Combine the line image with the original frame using the OpenCV addWeighted() function.
        line_image = addWeighted(frame, 0.8, line_image, 1, 1)
    
        return line_image

    @staticmethod
    def display_heading_line(frame, steering_angle, line_color=(0, 0, 255), line_width=5 ):

        heading_image = np.zeros_like(frame)  # Create a black image of the same size as the input frame.
        height, width, _ = frame.shape  # Get the height and width of the input frame.

        # Convert the steering angle from degrees to radians.
        steering_angle_radian = steering_angle / 180.0 * math.pi

        # Calculate the endpoints of the heading line using basic trigonometry.
        x1 = int(width / 2)  # The starting x-coordinate is the center of the frame.
        y1 = height  # The starting y-coordinate is the bottom of the frame.
        x2 = int(x1 - height / 2 / math.tan(steering_angle_radian))  # The ending x-coordinate is determined by the steering angle.
        y2 = int(height / 2)  # The ending y-coordinate is the middle of the frame.

        # Draw the heading line on the black image using OpenCV.
        line(heading_image, (x1, y1), (x2, y2), line_color, line_width)

        # Add the heading line image to the input frame using alpha blending.
        heading_image = addWeighted(frame, 0.8, heading_image, 1, 1)

        # Return the output video frame with the heading line displayed.
        return heading_image


    @staticmethod
    def calculate_wheel_speeds(steering_angle, wheelbase = 0.117, max_speed = 100, min_speed = 60):
        
        # Validate steering angle input
        if not 0 <= steering_angle <= 180:
            raise ValueError("Steering angle must be between 0 and 180 degrees")

        # Convert steering angle to radians
        steering_angle_rad = math.radians(steering_angle)

        if abs(steering_angle - 90) < 5:
            # Straight ahead
            left_speed = max_speed
            right_speed = max_speed
        else:
            # Calculate turning radius using small-angle approximation
            turning_radius = wheelbase / steering_angle_rad

            # Calculate turn rate
            k = 0.95
            turnrate = abs(k * ((turning_radius - wheelbase / 2) / turning_radius) / 2)
            #print('Turnrate:' + str(turnrate))

            # Calculate wheel speeds based on turning radius
            if steering_angle < 90:
                # Turn right
                if steering_angle > 60:
                    k = 0.6
                    turnrate = abs(k * ((turning_radius - wheelbase / 2) / turning_radius) / 2)
                elif steering_angle > 75:
                    k = 0.4
                    turnrate = abs(k * ((turning_radius - wheelbase / 2) / turning_radius) / 2)
                else:
                    k = 1.1
                    turnrate = abs(k * ((turning_radius - wheelbase / 2) / turning_radius) / 2)

                left_speed = max_speed * (1 + turnrate)
                right_speed = max_speed * (1 - turnrate)
            else:
                # Turn left
                if steering_angle < 120:
                    k = 0.6
                    turnrate = abs(k * ((turning_radius - wheelbase / 2) / turning_radius) / 2)

                elif steering_angle < 105:
                    k = 0.4
                    turnrate = abs(k * ((turning_radius - wheelbase / 2) / turning_radius) / 2)
                else:
                    k = 1.1
                    turnrate = abs(k * ((turning_radius - wheelbase / 2) / turning_radius) / 2)

                right_speed = max_speed * (1 + turnrate)
                left_speed = max_speed * (1 - turnrate)

            # Apply speed limits
            left_speed = max(min_speed, min(left_speed, max_speed))
            right_speed = max(min_speed, min(right_speed, max_speed))

        # Return wheel speeds
        return left_speed, right_speed

    
    def get_steering_angle(self, frame, lane_lines):
        
        #print('Last Angle: ' + str(self.last_angle))
        height, width, _ = frame.shape
        
        if len(lane_lines) == 2:
            # Get the end points of both lane lines
            _, _, left_x2, _ = lane_lines[0][0]
            _, _, right_x2, _ = lane_lines[1][0]
            # Get the horizontal center of the image
            mid = int(width / 2)
            # Calculate the x offset from the center of the lane
            x_offset = (left_x2 + right_x2) / 2 - mid
            y_offset = int(height / 2)
            
        elif len(lane_lines) == 1:
            # Get the end points of the lane line
            x1, _, x2, _ = lane_lines[0][0]
            # Calculate the x offset from the center of the lane
            x_offset = x2 - x1
            y_offset = int(height / 2)
            
        elif len(lane_lines) == 0:
            # No lane lines detected, use the previous angle
            x_offset = 0
            y_offset = int(height / 2)
            
        # Calculate the angle to the center of the lane
        angle_to_mid_radian = math.atan(x_offset / y_offset)
        angle_to_mid_deg = int(angle_to_mid_radian * 180.0 / math.pi)  
        steering_angle = angle_to_mid_deg + 90
        
        # Smooth the steering angle
        smooth_angle = (self.last_angle*2 + steering_angle)/3
        self.last_angle = smooth_angle
        
        return smooth_angle

    def steer_robot(self, steering_angle, gpg):
        # Validate the steering angle by comparing it to the last value
        validated_steering_angle = self.compare_to_last_angle(steering_angle)
        
        # Calculate the wheel speeds based on the validated steering angle
        leftSpeed, rightSpeed = self.calculate_wheel_speeds(validated_steering_angle)
        
        # Control the robot steering based on the calculated wheel speeds
        gpg.steer(rightSpeed, leftSpeed)

    
    def follow_lane(self, frame, gpg):
        
        # Resize to 1/2 to use for lane keeping
        #resized_frame = frame#resize(frame, (0, 0), fx=0.5, fy=0.5)
        
        # Detect edges in the video frame
        edges = self.detect_edges(frame)
        
        # Select region of interest in the video frame
        roi = self.region_of_interest(edges)
        
        # Detect line segments in the selected region of interest
        line_segments = self.detect_line_segments(roi)
        
        # Fit line segments to obtain the lane lines
        lane_lines = self.average_slope_intercept(frame,line_segments)
        
        # Display the lane lines on the video frame
        #lane_lines_image = self.display_lines(frame,lane_lines)
        
        
        # Calculate the steering angle based on the lane lines
        steering_angle = self.get_steering_angle(frame, lane_lines)
        
        # Validate the steering angle by comparing it to the last value
        validated_steering_angle = self.compare_to_last_angle(steering_angle)
        
        # Calculate the wheel speeds based on the validated steering angle
        #leftSpeed, rightSpeed = self.calculate_wheel_speeds(validated_steering_angle)
        #if leftSpeed == None:
            #print('No wheelspeed found')
        self.steer_robot(validated_steering_angle, gpg)
        
        # Display the heading line on the video frame
        #heading_image = self.display_heading_line(lane_lines_image, steering_angle)
        
        # Display final video with heading line in new window
        #imshow("Heading line", heading_image)

        # Output the validated steering angle and wheel speeds to the console
        #print('Steering angle:' + str(validated_steering_angle))
        #print('Wheel speeds: ' + str(leftSpeed) + str(rightSpeed))

    
    def get_distance(self, distance_sensor):
        
        try:
            distance_in_mm = str(distance_sensor.read_mm())
            self.distance = distance_in_mm
            return distance_in_mm
        except:
            print("Distance sensor reading error")
            return None


    def control_speed(self, gpg, distance_sensor, stop_distance=100, slow_distance=200):
        
        # Get distance and adjust speed if too close
        distance = self.get_distance(distance_sensor)
        gpg.set_speed(100)
        if distance is not None:
            #print('Distance: ' + distance)
            if int(distance) < stop_distance:
                gpg.set_speed(0)
            elif int(distance) < slow_distance:
                gpg.set_speed(50)
            else:
                gpg.set_speed(100)
        else:
            gpg.set_speed(0)


    @staticmethod
    def calculate_steering_angle(x_offset, wheelbase=0.117):
        k = 0
        if abs(x_offset) > 10: k=0.1
        elif abs(x_offset) > 50: k=0.4
        elif abs(x_offset) > 100: k=0.9
        
        steering_angle = x_offset * k

        # Limit the steering angle to a maximum of 180 degrees
        steering_angle = min(max(steering_angle, -90), 90)

        # Add 90 degrees to convert it to the 0-180 degrees range
        steering_angle += 90

        return steering_angle
    
    def printQRData(self, data, x_offset, y_offset):
        
        print('Data: ')
        print(str(data))
        print('X_offset: ')
        print(str(x_offset))
        print('Y_offset: ')
        print(str(y_offset))
        print('Steering Angle: ')
        steering_angle = self.calculate_steering_angle(x_offset)
        print(str(steering_angle))

    def kill(gpg, video):
        # Stop the robot when the loop is ended
        gpg.set_speed(0)

        # Release the video capture and close all windows
        video.release()
        destroyAllWindows()

    def follow_qr(self, frame, gpg):
        data, x_offset, y_offset = self.locateQR(frame)
        self.printQRData(data, x_offset, y_offset)
        steering_angle = self.calculate_steering_angle(x_offset)
        self.steer_robot(steering_angle, gpg)

    




