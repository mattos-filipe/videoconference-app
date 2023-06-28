import cv2
import pyaudio
import zmq
import struct
import threading
import numpy as np

def video_streaming_client():
    context = zmq.Context()
    video_socket = context.socket(zmq.SUB)
    video_socket.connect("tcp://localhost:5555")
    video_socket.setsockopt(zmq.SUBSCRIBE, b"")

    while True:
        encoded_frame = video_socket.recv()
        frame = cv2.imdecode(np.frombuffer(encoded_frame, dtype=np.uint8), cv2.IMREAD_COLOR)
        cv2.imshow("Video", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cv2.destroyAllWindows()

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

def text_messaging_client():
    context = zmq.Context()
    text_socket = context.socket(zmq.REQ)
    text_socket.connect("tcp://localhost:5557")

    while True:
        message = input("Enter message: ")
        text_socket.send_string(message)
        response = text_socket.recv_string()
        print("Server response:", response)

if __name__ == "__main__":
    video_thread = threading.Thread(target=video_streaming_client)
    #audio_thread = threading.Thread(target=audio_streaming_client)
    #text_thread = threading.Thread(target=text_messaging_client)
    video_thread.start()
    #audio_thread.start()
    #text_thread.start()