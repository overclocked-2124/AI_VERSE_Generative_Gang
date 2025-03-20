import torch
import simpleaudio as sa
from transformers import AutoModelForSpeechSeq2Seq,AutoProcessor,pipeline
def text_speech(text):
    
    model_name=""
    model=AutoModelForSpeechSeq2Seq.from_pretrained(model_name,torch_dtype=torch.float16)
    processor=AutoProcessor.from_pretrained(model_name)
    tts_pipeline=pipeline("text_to_speech",model=model,processor=processor,device=0)
    output=tts_pipeline(text)
    return output