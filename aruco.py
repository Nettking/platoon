import cv2
from pyzbar.pyzbar import decode

# set up camera
cap = cv2.VideoCapture(0)

while True:
    # capture frame-by-frame
    ret, frame = cap.read()

    # check if the frame was correctly captured
    if not ret:
        continue

    # convert the frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # decode QR code or barcode
    decoded_objs = decode(gray)

    # display the decoded objects on the frame
    for obj in decoded_objs:
        cv2.putText(frame, str(obj.data), (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
        cv2.rectangle(frame, (obj.rect.left, obj.rect.top), (obj.rect.left + obj.rect.width, obj.rect.top + obj.rect.height), (0, 255, 0), 2)

    # display the resulting frame
    cv2.imshow('frame', frame)

    # exit if the 'q' key is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# release the camera and close all windows
cap.release()
cv2.destroyAllWindows()
