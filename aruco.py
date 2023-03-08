import cv2
from pyzbar.pyzbar import decode

while True:
    frame = cv2.imread('test.jpg')

    decoded_objs = decode(frame)

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
        cv2.rectangle(frame, (left, top), (left+width, top+height), (0, 0, 255), 2)

        # Display the barcode data and offsets on the frame
        print( f"Data: {data}", (left, top-10),)
        print( f"X offset: {x_offset:.2f}")
        print( f"Y offset: {y_offset:.2f}")
        #cv2.putText(frame, f"Y offset: {y_offset:.2f}", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

    #cv2.imshow("frame", frame)


#cap.release()
cv2.destroyAllWindows()
