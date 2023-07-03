import time
import zmq
import threading
import soundcard as sc
import numpy as np
import pyaudio

class AudioStreaming:
    __context = zmq.Context()
    __audio_publisher_socket = __context.socket(zmq.PUB)
    __audio_server_threads = []
    __audio_client_threads = []
    audio = pyaudio.PyAudio()
    def __init__(self, id, ip_list):
        self.id=id
        self.ip_list = ip_list
        print(f'[{self.id}] Conectado à audiotransmissao!')
        self.audio_streaming_server()
        self.audio_streaming_client()

    def __format_print(self, sender, message):
        print(f'[id={self.id}] [sender={sender}]: {message}')

    def audio_streaming_server(self):
        self.__audio_publisher_socket.bind(f"tcp://*:55{self.id}3")
        thread = threading.Thread(target=self.__audio_streaming_server_thread)
        self.__audio_server_threads.append(thread)
        thread.start()

    def __audio_streaming_server_thread(self):
        audio = pyaudio.PyAudio()
        stream = audio.open(format=pyaudio.paInt16,
                            channels=1,
                            rate=44100,
                            input=True,
                            frames_per_buffer=5120)
        while True:
            audio_data = stream.read(5120)
            #print('enviado')
            self.__audio_publisher_socket.send(audio_data)
            time.sleep(0.05)


    def audio_streaming_client(self):
        for ip in self.ip_list:
            for newSocket in range(8):
                if newSocket != self.id:
                    context = zmq.Context()
                    socket = context.socket(zmq.SUB)
                    socket.connect(f"tcp://{ip}:55{newSocket}3")
                    socket.setsockopt(zmq.SUBSCRIBE, b"")
                    thread = threading.Thread(target=self.__audio_streaming_client_thread, args=(socket,newSocket))
                    self.__audio_client_threads.append(thread)
                    thread.start()

    def __audio_streaming_client_thread(self, socket, sender):
        audio =  pyaudio.PyAudio()
        stream = audio.open(format=pyaudio.paInt16,
                            channels=1,
                            rate=44100,
                            output=True,
                            frames_per_buffer=5120)
        while True:
            audio_data = socket.recv()
            #print('recebido')
            time.sleep(0.05)
            stream.write(audio_data)

    def __del__(self):
        for th in self.__audio_client_threads:
            th.join()
        for th in self.__audio_server_threads:
            th.join()
        print('Desconectando da audiotransmissao!')
        