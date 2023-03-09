import cv2
from pyzbar.pyzbar import decode

def locateQR(frame):
        decoded_objs = decode(frame)
        if decoded_objs == None:
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
            cv2.rectangle(frame, (left, top), (left+width, top+height), (0, 0, 255), 2)
            # Display the barcode data and offsets on the frame
            #print("Data: {}".format(data), (left, top-10))
            #print("X offset: {:.2f}".format(x_offset))
            #print("Y offset: {:.2f}".format(y_offset))
            return data, x_offset, y_offset
        


if __name__ == '__main__':

    video = cv2.VideoCapture(0)
    while True:
        frame = video.read()
        data, x_offset, y_offset = locateQR(frame)    
        print('Data: ')
        print(str(data))
        print('X_offset: ')
        print(str(x_offset))
        print('Y_offset: ')
        print(str(y_offset))
        key = cv2.waitKey(1)
        if key == 27:
            break
        #cv2.imshow("frame", frame)


    #cap.release()
    cv2.destroyAllWindows()
