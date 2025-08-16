import cv2
from paddleocr import PaddleOCR
import pyttsx3

ocr = PaddleOCR()

cap = cv2.VideoCapture(0)  # 0 = default webcam
print("Press SPACE to capture an image, ESC to quit.")
engine = pyttsx3.init()

while True:
    ret, frame = cap.read()
    if not ret:
        print("Failed to access webcam.")
        break

    cv2.imshow("Webcam - Press SPACE to capture", frame)

    key = cv2.waitKey(1)

    # SPACE = capture image
    if key == 32:
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        results = ocr.predict(rgb)
        
        for res in results:
            alltext = results[0]['rec_texts']
            print(alltext)
            for text in alltext:
                engine.say(text)
            engine.runAndWait()

    # ESC = exit
    elif key == 27:
        break

cap.release()
cv2.destroyAllWindows()