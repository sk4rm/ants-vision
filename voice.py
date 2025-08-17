import json
import paho.mqtt.client as mqtt
import queue
import sounddevice as sd
import sys

from vosk import Model, KaldiRecognizer

MQTT_BROKER_HOST = "localhost"
MQTT_VOICE_TOPIC = "services/voice"
q = queue.Queue()


def callback(indata, frames, time, status):
    if status:
        print(status, file=sys.stderr)
    q.put(bytes(indata))


def on_connect(client, userdata, flags, reason_code, properties):
    if reason_code == mqtt.MQTT_ERR_SUCCESS:
        print(f"Successfully connected to MQTT broker.")
        client.subscribe(MQTT_VOICE_TOPIC)


def on_message(client, userdata, msg):
    print(msg.topic + " " + str(msg.payload))


model = Model(lang="en-us")
samplerate = sd.query_devices(kind="input")["default_samplerate"]

mqttc = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
mqttc.on_connect = on_connect
mqttc.on_message = on_message

try:
    mqttc.connect(MQTT_BROKER_HOST)
    mqttc.loop_start()

    with sd.RawInputStream(callback=callback, dtype="int16", samplerate=samplerate):
        rec = KaldiRecognizer(model, samplerate)

        print("Started recording microphone. Press Ctrl-C to stop.")
        while True:
            if rec.AcceptWaveform(q.get()):
                result = json.loads(rec.Result())
                text = result["text"]
                print(text if text != "" else "🤫")

except KeyboardInterrupt:
    print("bye bye 👋")

except Exception as e:
    print(f"uh oh 🙀 {e}")

mqttc.loop_stop()
mqttc.disconnect()