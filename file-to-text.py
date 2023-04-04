import os
from google.cloud import speech
import time
import json


speech_client = speech.SpeechClient()

def File_to_text(file_name,speech_client):
    ## Step 1. Load the media files
    with open(file_name, 'rb') as f2:
        byte_data_wav = f2.read()
    audio_wav = speech.RecognitionAudio(content=byte_data_wav)

    config_wav = speech.RecognitionConfig(
        sample_rate_hertz=44100,
        enable_automatic_punctuation=True,
        language_code='vi-VN',
        audio_channel_count=2
    )


    response_standard_wav = speech_client.recognize(
        config=config_wav,
        audio=audio_wav
    )
    return response_standard_wav.results[0].alternatives[0].transcript


if __name__=='__main__':
    list_file={}
    to_text=[]
    ls = os.listdir('output-records')
    for i in ls:
        os.remove('output-records/'+i)
    while True:
        try:
            last_element = os.listdir('output-records')[-1]
            if last_element in list_file:
                continue
            response=File_to_text('output-records/'+last_element,speech_client)
            list_file[last_element]=1
            # text_re=json.loads(str(response))
            print(response.results[0].alternatives[0].transcript)
            time.sleep(2)
        except:
            print('nothing has been changed')
            time.sleep(2)
            

    
    
