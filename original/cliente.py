import cv2
import pyaudio
import zmq
import struct
import threading
import numpy as np

def audio_streaming_client():
    audio = pyaudio.PyAudio()
    stream = audio.open(format=pyaudio.paInt16,
                        channels=1,
                        rate=44100,
                        output=True,
                        frames_per_buffer=1024)

    context = zmq.Context()
    audio_socket = context.socket(zmq.SUB)
    audio_socket.connect("tcp://localhost:5556")
    audio_socket.setsockopt(zmq.SUBSCRIBE, b"")

    while True:
        audio_data = audio_socket.recv()
        stream.write(audio_data)

    stream.stop_stream()
    stream.close()
    audio.terminate()



if __name__ == "__main__":
    audio_thread_c = threading.Thread(target=audio_streaming_client)
    audio_thread_c.start()
