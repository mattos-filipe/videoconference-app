import cv2
import pyaudio
import zmq
import struct
import threading
import numpy as np
import sys
import time
#text_publisher_socket  = None
context = zmq.Context()
text_publisher_socket = context.socket(zmq.PUB)
context_pc = zmq.Context()
process_communication_socket = context_pc.socket(zmq.REP)

text_server_threads = []
text_client_threads = []

def format_print(programId, sender, message):
    print(f'[id={programId}] [sender={sender}]: {message}')
    
'''
PORT SCHEME
TO DO:atualizar descrições
    [55{id}{type}]
    The {id}   variable indicates the program identifier
    The {type} variable indicates the kind of data
        0: process_communication
        1: text_streaming
        2: video_streaming
        3: audio_streaming
'''
def process_communication_server_thread(programId:int):
    newProcessId = -1           # to avoid threads duplication
    while True:
        message = process_communication_socket.recv_string()
        process_communication_socket.send_string("")
        newProcessId = int(message)
        print(f'|{newProcessId}|')
        if newProcessId >= 0:
            context = zmq.Context()
            socket = context.socket(zmq.SUB)
            socket.connect(f"tcp://localhost:55{newProcessId}1")
            socket.setsockopt(zmq.SUBSCRIBE, b"")
            thread = threading.Thread(target=text_messaging_client_thread, args=(socket,newProcessId,programId))
            text_client_threads.append(thread)
            thread.start()
            print(text_client_threads)
            newProcessId = -1

def process_communication_server(programId:int):
    process_communication_socket.bind(f"tcp://*:55{programId}0")
    thread = threading.Thread(target=process_communication_server_thread, args=(programId,))
    thread.start()

def process_communication_client(programId):
    context = zmq.Context()
    socket = context.socket(zmq.REQ)
    socket.connect(f"tcp://localhost:55{programId}0")
    socket.send_string(f'{programId}')
    socket.close()

############ SERVER ############
def text_messaging_server(programId):
    text_publisher_socket.bind(f"tcp://*:55{programId}1")
    thread = threading.Thread(target=text_messaging_server_thread, args=(programId,))
    text_server_threads.append(thread)
    thread.start()

def text_messaging_server_thread(programId):
    while True:
        #message = input(f"[{programId}] Enter message: ")
        message = input()
        text_publisher_socket.send_string(message)
        
        
############ CLIENT ############
def text_messaging_client(programId):
    for newSocket in range(8):
        context = zmq.Context()
        text_socket = context.socket(zmq.SUB)
        text_socket.connect(f"tcp://localhost:55{newSocket}1")
        text_socket.setsockopt(zmq.SUBSCRIBE, b"")
        thread = threading.Thread(target=text_messaging_client_thread, args=(text_socket,newSocket,programId))
        text_client_threads.append(thread)
        thread.start()

def text_messaging_client_thread(text_socket, sender:int, programId:int):
    while True:
        #format_print(programId, sender, '89: teste')
        message = text_socket.recv_string()
        #print(f'socket: {text_socket}')
        format_print(programId, sender, message)
        


    

def video_streaming_server(id):
    context = zmq.Context()
    video_socket = context.socket(zmq.PUB)
    video_socket.bind(f"tcp://*:55{id}8")

    video_capture = cv2.VideoCapture(0)

    while True:
        ret, frame = video_capture.read()
        encoded_frame = cv2.imencode('.jpg', frame)[1].tobytes()
        video_socket.send(encoded_frame)

    video_capture.release()

def audio_streaming_server(id):
    audio = pyaudio.PyAudio()
    stream = audio.open(format=pyaudio.paInt16,
                        channels=1,
                        rate=44100,
                        input=True,
                        frames_per_buffer=1024)

    context = zmq.Context()
    audio_socket = context.socket(zmq.PUB)
    audio_socket.bind(f"tcp://*:55{id}9")

    while True:
        audio_data = stream.read(1024)
        audio_socket.send(audio_data)

    stream.stop_stream()
    stream.close()
    audio.terminate()



if __name__ == "__main__":
    if len(sys.argv) != 2:
        print('Número incorreto de parâmetros. Exemplo de uso:\n\n\tpython3 servidor.py [id]\nCom 0 <= [id] <= 7')
        exit()
    if( int(sys.argv[1]) <0 or int(sys.argv[1]) > 7 ):
        print('Id inválido: 0 <= [id] <= 7')
        exit()
    id = int(sys.argv[1])
    print(f'[{id}] Conectado à videoconferência!')
    #video_thread = threading.Thread(target=video_streaming_server)
    #audio_thread = threading.Thread(target=audio_streaming_server)
    #video_thread.start()
    #audio_thread.start()

    text_messaging_server(id)
    text_messaging_client(id)
    #process_communication_server(id)
    '''for oldChannel in range(id):
        process_communication_client(oldChannel)'''
    
    