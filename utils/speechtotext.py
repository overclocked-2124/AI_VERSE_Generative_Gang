import whisper
import pyaudio
import numpy as np
import tempfile
import wave
import os
import threading
import time
import queue
import webrtcvad
import collections
import struct

class WhisperVAD:
    def __init__(self, model_size="medium", vad_mode=3, sample_rate=16000, frame_duration_ms=30, 
                 padding_duration_ms=300, silence_threshold_ms=1000):
        # Initialize Whisper model
        self.model = whisper.load_model(model_size)
        
        # VAD settings
        self.vad = webrtcvad.Vad(vad_mode)  # 0-3, where 3 is the most aggressive
        self.sample_rate = sample_rate
        self.frame_duration_ms = frame_duration_ms
        self.frame_size = int(sample_rate * frame_duration_ms / 1000)
        self.padding_frames = int(padding_duration_ms / frame_duration_ms)
        self.silence_threshold = int(silence_threshold_ms / frame_duration_ms)
        
        # State variables
        self.audio_queue = queue.Queue()
        self.result_queue = queue.Queue()
        self.running = False
        self.thread = None
        self.is_speaking = False
        self.silence_frames = 0
        self.voiced_frames = []
        self.complete_question = []
        
    def start(self):
        """Start the VAD and transcription process"""
        if self.running:
            return False
            
        self.running = True
        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(
            format=pyaudio.paInt16,
            channels=1,
            rate=self.sample_rate,
            input=True,
            frames_per_buffer=self.frame_size
        )
        
        self.thread = threading.Thread(target=self._process_audio)
        self.thread.daemon = True
        self.thread.start()
        return True
        
    def stop(self):
        """Stop the VAD and transcription process"""
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
    
    def get_transcription_results(self):
        """Get all available transcription results"""
        results = []
        while not self.result_queue.empty():
            results.append(self.result_queue.get())
        return results
    
    def _process_audio(self):
        """Main processing loop that handles VAD and transcription"""
        while self.running:
            # Read audio frame
            audio_data = self.stream.read(self.frame_size, exception_on_overflow=False)
            
            # Check if frame contains speech
            is_speech = False
            try:
                is_speech = self.vad.is_speech(audio_data, self.sample_rate)
            except:
                # Handle potential VAD processing errors
                pass
            
            if is_speech:
                # Reset silence counter and add frame to voiced_frames
                self.silence_frames = 0
                self.voiced_frames.append(audio_data)
                if not self.is_speaking:
                    self.is_speaking = True
                    print("Speech started")
            else:
                # Increment silence counter
                self.silence_frames += 1
                
                # Add some padding frames to avoid cutting off speech
                if self.is_speaking and self.silence_frames < self.padding_frames:
                    self.voiced_frames.append(audio_data)
                
                # If silence exceeds threshold, process the collected speech
                if self.is_speaking and self.silence_frames >= self.silence_threshold:
                    self.is_speaking = False
                    print("Speech ended - processing question")
                    
                    # Process complete question in a separate thread to avoid blocking
                    if self.voiced_frames:
                        speech_data = b''.join(self.voiced_frames)
                        threading.Thread(
                            target=self._transcribe_segment, 
                            args=(speech_data,)
                        ).start()
                        self.voiced_frames = []
    
    def _transcribe_segment(self, speech_data):
        """Transcribe a speech segment and add it to the result queue"""
        try:
            # Save audio to temporary file
            with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp_wav:
                with wave.open(tmp_wav.name, "wb") as wf:
                    wf.setnchannels(1)
                    wf.setsampwidth(2)
                    wf.setframerate(self.sample_rate)
                    wf.writeframes(speech_data)
                
                # Transcribe with Whisper
                result = self.model.transcribe(tmp_wav.name, fp16=False)
                text = result["text"].strip()
                language = result.get("language", "unknown")
                
                # Only add non-empty transcriptions to the queue
                if text:
                    self.result_queue.put({
                        "text": text,
                        "language": language,
                        "timestamp": time.time()
                    })
                    print(f"Transcribed: {text}")
                
                # Clean up temporary file
                os.unlink(tmp_wav.name)
        except Exception as e:
            print(f"Error in transcription: {e}")

    def is_question_complete(self):
        """Check if there's a complete question available"""
        return not self.result_queue.empty()

    def get_next_question(self):
        """Get the next complete question from the queue"""
        if not self.result_queue.empty():
            return self.result_queue.get()
        return None
