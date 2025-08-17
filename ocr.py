import cv2
import pyttsx3
from paddleocr import PaddleOCR
import paho.mqtt.client as mqtt

MQTT_BROKER_HOST = "localhost"
MQTT_OCR_TOPIC = "services/ocr"


def on_connect(client, userdata, flags, reason_code, properties):
    print(f"Connected with result code {reason_code}.")
    client.subscribe(MQTT_OCR_TOPIC)


def on_message(client, userdata, msg):
    print(msg.topic + " " + str(msg.payload))


ocr = PaddleOCR()

cap = cv2.VideoCapture(0)  # 0 = default webcam
print("Press SPACE to capture an image, ESC to quit.")
engine = pyttsx3.init()

mqttc = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
mqttc.enable_logger()
mqttc.on_connect = on_connect
mqttc.on_message = on_message
mqttc.connect(MQTT_BROKER_HOST)
mqttc.loop_start()

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
            alltext = results[0]["rec_texts"]
            print(alltext)
            for text in alltext:
                engine.say(text)
            engine.runAndWait()

    # ESC = exit
    elif key == 27:
        break

mqttc.loop_stop()
mqttc.disconnect()
cap.release()
cv2.destroyAllWindows()
