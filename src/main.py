import cv2


class Faces:
    def __init__(self, mode='node'):
        self.mode = mode

    def blur_and_anon_faces(self):
        cap = cv2.VideoCapture(0)

        face_detection = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

        while True:
            _, frame = cap.read()

            cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
            cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = face_detection.detectMultiScale(gray, 1.2, 3)

            for (x, y, w, h) in faces:
                face_frame = frame[y: y + h, x: x + w]

                if self.mode == 'blur':
                    face_proc = cv2.GaussianBlur(face_frame, (55, 55), 30)
                elif self.mode == 'pixelate':
                    temp = cv2.resize(face_frame, (w // 10, h // 10), interpolation=cv2.INTER_LINEAR)
                    face_proc = cv2.resize(temp, (w, h), interpolation=cv2.INTER_NEAREST)
                elif self.mode == 'both':
                    blur = cv2.GaussianBlur(face_frame, (55, 55), 30)
                    temp = cv2.resize(blur, (w // 10, h // 10), interpolation=cv2.INTER_LINEAR)
                    face_proc = cv2.resize(temp, (w, h), interpolation=cv2.INTER_NEAREST)
                else:
                    face_proc = face_frame
                frame[y: y + h, x: x + w] = face_proc

            _, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()

            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
