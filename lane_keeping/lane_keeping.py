from lane_keeping import *

def lane_keeping(frame):
            # Detect edges in the video frame
            edges = detect_edges(frame)
            
            # Select region of interest in the video frame
            roi = region_of_interest(edges)

            # Display edges detected in cropped video frame in new window
            cv2.imshow("Edges in roi", roi)
            
            # Detect line segments in the selected region of interest
            line_segments = detect_line_segments(roi)
            
            # Fit line segments to obtain the lane lines
            lane_lines = average_slope_intercept(frame,line_segments)
            
            # Display the lane lines on the video frame
            lane_lines_image = display_lines(frame,lane_lines)
            
            # Calculate the steering angle based on the lane lines
            steering_angle = get_steering_angle(frame, lane_lines)
            
            # Validate the steering angle by comparing it to the last value
            validated_steering_angle = compare_to_last_value(steering_angle)
            
            # Calculate the wheel speeds based on the validated steering angle
            leftSpeed, rightSpeed = calculate_wheel_speeds(validated_steering_angle)
            
            # Control the robot steering based on the calculated wheel speeds
            gpg.steer(rightSpeed, leftSpeed) 
            
            # Display the heading line on the video frame
            heading_image = display_heading_line(lane_lines_image, steering_angle)

            # Display final video with heading line in new window
            cv2.imshow("Heading line", heading_image)
            
            # Output the validated steering angle and wheel speeds to the console
            print('Steering angle:' + str(validated_steering_angle))
            print('Wheel speeds: ' + str(leftSpeed) + str(rightSpeed))
        