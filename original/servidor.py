import cv2
import pyaudio
import zmq
import struct
import threading
import numpy as np
import time

def audio_streaming_server():
    audio = pyaudio.PyAudio()
    stream = audio.open(format=pyaudio.paInt16,
                        channels=1,
                        rate=44100,
                        input=True,
                        frames_per_buffer=5120)

    context = zmq.Context()
    audio_socket = context.socket(zmq.PUB)
    audio_socket.bind("tcp://*:5556")

    while True:
        audio_data = stream.read(5120)
        #print('enviado')
        audio_socket.send(audio_data)
        time.sleep(0.05)
        

    stream.stop_stream()
    stream.close()
    audio.terminate()

def audio_streaming_client():
    audio =  pyaudio.PyAudio()
    stream = audio.open(format=pyaudio.paInt16,
                        channels=1,
                        rate=44100,
                        output=True,
                        frames_per_buffer=5120)

    context = zmq.Context()
    audio_socket = context.socket(zmq.SUB)
    audio_socket.connect("tcp://localhost:5556")
    audio_socket.setsockopt(zmq.SUBSCRIBE, b"")

    while True:
        audio_data = audio_socket.recv()
        #print('recebido')
        time.sleep(0.05)
        stream.write(audio_data)

    stream.stop_stream()
    stream.close()
    audio.terminate()

if __name__ == "__main__":
    audio = pyaudio.PyAudio()
    audio_thread_s = threading.Thread(target=audio_streaming_server)
    audio_thread_s.start()

    audio_thread_c = threading.Thread(target=audio_streaming_client)
    audio_thread_c.start()