import threading
from array import array
from queue import Queue, Full
import time
import wave
import sys

import pyaudio

FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
RECORD_SECONDS = 5
WAVE_OUTPUT_FILENAME = "voice.wav"

CHUNK_SIZE = 1024
MIN_VOLUME = 2600
white_frame = 3
max_file = 100
BUF_MAX_SIZE = CHUNK_SIZE * 10
dict_output='output-records/'

def main():
    stopped = threading.Event()
    q = Queue(maxsize=int(round(BUF_MAX_SIZE / CHUNK_SIZE)))
    stop_thread = False
    listen_t = threading.Thread(target=listen, args=(stopped, q))
    listen_t.start()
    record_t = threading.Thread(target=record, args=(stopped, q , 0))
    record_t.start()

    try:
        while True:
            listen_t.join(0.1)
            record_t.join(0.1)
    except KeyboardInterrupt:
        stopped.set()
    
    

def record(stopped, q,output_count):
    st=time.time()
    frames=[]
    count_avai = 0
    while True:
        if stopped.wait(timeout=0):
            break
        chunk = q.get()
        vol = max(chunk)

        frames.append(chunk)
        if vol >= MIN_VOLUME:
            # TODO: write to file
            # print ("O")
            print(vol)
            count_avai=count_avai+1
            # if (count_avai > 3):
            st=time.time()
        else:
            if time.time()-st> white_frame:
                print(time.time()-st)
                break
            # print ("-")
            count_avai=0
    print(dict_output +  str(output_count) + '.wav')
    wf = wave.open(dict_output +  str(output_count) + '.wav', 'wb')
    wf.setnchannels(2)
    wf.setsampwidth(pyaudio.PyAudio().get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()
    output_count=output_count+1
    if output_count < max_file:
        record(stopped, q,output_count)


def listen(stopped, q):
    stream = pyaudio.PyAudio().open(
        format=pyaudio.paInt16,
        channels=2,
        rate=44100,
        input=True,
        frames_per_buffer=1024,
    )

    while True:
        if stopped.wait(timeout=0):
            break
        try:
            q.put(array('h', stream.read(CHUNK_SIZE)))
        except Full:
            pass  # discard


if __name__ == '__main__':
    main()