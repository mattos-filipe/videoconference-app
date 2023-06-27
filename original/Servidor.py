import cv2
import pyaudio
import zmq
import struct
import threading
import numpy as np

def video_streaming_server():
    context = zmq.Context()
    video_socket = context.socket(zmq.PUB)
    video_socket.bind("tcp://*:5555")

    video_capture = cv2.VideoCapture(0)

    while True:
        ret, frame = video_capture.read()
        encoded_frame = cv2.imencode('.jpg', frame)[1].tobytes()
        video_socket.send(encoded_frame)

    video_capture.release()

def audio_streaming_server():
    audio = pyaudio.PyAudio()
    stream = audio.open(format=pyaudio.paInt16,
                        channels=1,
                        rate=44100,
                        input=True,
                        frames_per_buffer=1024)

    context = zmq.Context()
    audio_socket = context.socket(zmq.PUB)
    audio_socket.bind("tcp://*:5556")

    while True:
        audio_data = stream.read(1024)
        audio_socket.send(audio_data)

    stream.stop_stream()
    stream.close()
    audio.terminate()

def text_messaging_server():
    context = zmq.Context()
    text_socket = context.socket(zmq.REP)
    text_socket.bind("tcp://*:5557")

    while True:
        message = text_socket.recv_string()
        print("Received message:", message)
        response = "Received: " + message
        text_socket.send_string(response)

if __name__ == "__main__":
    video_thread = threading.Thread(target=video_streaming_server)
    audio_thread = threading.Thread(target=audio_streaming_server)
    text_thread = threading.Thread(target=text_messaging_server)
    video_thread.start()
    audio_thread.start()
    text_thread.start()