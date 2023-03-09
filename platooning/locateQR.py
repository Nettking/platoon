import cv2
from pyzbar.pyzbar import decode
from platooning import *

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

            return data, x_offset, y_offset
        


if __name__ == '__main__':
    from platooning import *
    video = cv2.VideoCapture(0)
    while True:
        frame = video.read()
        data, x_offset, y_offset = locateQR(frame)    
        printQRData(data,x_offset,y_offset)
        #cv2.imshow("frame", frame)
        key = cv2.waitKey(1)
        if key == 27:
            break
    
    cv2.destroyAllWindows()
