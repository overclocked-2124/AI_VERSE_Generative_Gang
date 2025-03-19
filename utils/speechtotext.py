import whisper
import pyaudio
import numpy as np
import tempfile
import wave
import os
import threading
import time

class WhisperTranscriber:
    def __init__(self, model_size="small", chunk_size=4000, sample_rate=16000, buffer_chunks=10):
        self.model = whisper.load_model(model_size)
        self.chunk_size = chunk_size
        self.sample_rate = sample_rate
        self.buffer_chunks = buffer_chunks
        self.running = False
        self.audio_buffer = []
        self.p = None
        self.stream = None
        self.thread = None
        self.transcription_callback = None
        
    def start(self, callback=None):
        """Start the transcription process"""
        if self.running:
            return False
            
        self.transcription_callback = callback
        self.running = True
        self.audio_buffer = []
        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(
            format=pyaudio.paInt16, 
            channels=1, 
            rate=self.sample_rate, 
            input=True, 
            frames_per_buffer=self.chunk_size
        )
        
        self.thread = threading.Thread(target=self._transcribe_loop)
        self.thread.daemon = True
        self.thread.start()
        return True
        
    def stop(self):
        """Stop the transcription process"""
        if not self.running:
            return False
            
        self.running = False
        if self.thread:
            self.thread.join(timeout=2)
        if self.stream:
            self.stream.stop_stream()
            self.stream.close()
        if self.p:
            self.p.terminate()
        return True
        
    def _transcribe_loop(self):
        while self.running:
            try:
                audio_data = self.stream.read(self.chunk_size)
                self.audio_buffer.append(audio_data)
                
                if len(self.audio_buffer) >= self.buffer_chunks:
                    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp_wav:
                        with wave.open(tmp_wav.name, "wb") as wf:
                            wf.setnchannels(1)
                            wf.setsampwidth(2)
                            wf.setframerate(self.sample_rate)
                            wf.writeframes(b"".join(self.audio_buffer))
                        
                        result = self.model.transcribe(tmp_wav.name, fp16=False)
                        text = result["text"]
                        language = result.get("language", "unknown")
                        
                        if self.transcription_callback:
                            self.transcription_callback(text, language)
                        else:
                            print("Text:", text)
                            print("Detected Language:", language)
                            
                        os.unlink(tmp_wav.name)
                        self.audio_buffer = []
            except Exception as e:
                print(f"Error in transcription loop: {e}")
                if not self.running:
                    break
                time.sleep(0.1)
