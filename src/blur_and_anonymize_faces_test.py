import cv2

cap = cv2.VideoCapture(0)
face_detection = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

mode = "None"

while True:
    _, frame = cap.read()

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    face = face_detection.detectMultiScale(gray, 1.2, 3)

    for (x, y, w, h) in face:
        face_frame = frame[y: y + h, x: x + w]

        if mode == 'blur':
            face_proc = cv2.GaussianBlur(face_frame, (55, 55), 30)
        elif mode == 'pixelation':
            temp = cv2.resize(face_frame, (w // 10, h // 10), interpolation=cv2.INTER_LINEAR)
            face_proc = cv2.resize(temp, (w, h), interpolation=cv2.INTER_NEAREST)
        elif mode == 'both':
            blur = cv2.GaussianBlur(face_frame, (55, 55), 30)
            temp = cv2.resize(blur, (w // 10, h // 10), interpolation=cv2.INTER_LINEAR)
            face_proc = cv2.resize(temp, (w, h), interpolation=cv2.INTER_NEAREST)
        else:
            face_proc = face_frame
        frame[y: y + h, x: x + w] = face_proc

    cv2.imshow('Frame', frame)
    key = cv2.waitKey(1)
    if key == ord('b'):
        mode = 'blur'
    elif key == ord('p'):
        mode = 'pixelation'
    elif key == ord('m'):
        mode = 'both'
    elif key == ord('n'):
        mode = 'none'
    elif key == ord('q'):
        break

cv2.destroyAllWindows()
cap.release()