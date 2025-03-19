import whisper
import pyaudio
import numpy as np
import tempfile
import wave
import os

model = whisper.load_model("medium")

p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=4000)

audio_buffer = []

try:
    while True:
        audio_data = stream.read(4000)
        audio_buffer.append(audio_data)

        if len(audio_buffer) >= 10:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp_wav:
                with wave.open(tmp_wav.name, "wb") as wf:
                    wf.setnchannels(1)
                    wf.setsampwidth(2)
                    wf.setframerate(16000)
                    wf.writeframes(b"".join(audio_buffer))

                result = model.transcribe(tmp_wav.name, fp16=False)
                print("Text", result["text"])
                print("Detected Language:", result.get("language", "unknown"))

                os.unlink(tmp_wav.name)
                audio_buffer = []

except KeyboardInterrupt:
    stream.stop_stream()
    stream.close()
    p.terminate()