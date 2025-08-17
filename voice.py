import queue
import sounddevice as sd
import sys

from vosk import Model, KaldiRecognizer

q = queue.Queue()
model = Model(lang="en-us")
samplerate = sd.query_devices(kind="input")["default_samplerate"]


def callback(indata, frames, time, status):
    if status:
        print(status, file=sys.stderr)
    q.put(bytes(indata))


try:
    with sd.RawInputStream(callback=callback, dtype="int16", samplerate=samplerate):
        rec = KaldiRecognizer(model, samplerate)
        print("ok")
        while True:
            if rec.AcceptWaveform(q.get()):
                print(rec.Result())

except KeyboardInterrupt:
    print("bye bye 👋")

except Exception as e:
    print(f"uh oh 🙀 {e}")
