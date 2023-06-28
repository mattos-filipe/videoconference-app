import zmq
import threading
import soundcard as sc
import numpy as np

class AudioStreaming:
    __context = zmq.Context()
    __audio_publisher_socket = __context.socket(zmq.PUB)
    __audio_server_threads = []
    __audio_client_threads = []
    def __init__(self, id):
        self.id=id
        self.mic = sc.default_microphone()
        self.spk = sc.default_speaker()
        print(f'[{self.id}] Conectado à audiotransmissao!')        
        self.audio_streaming_server()
        self.audio_streaming_client()

    def __format_print(self, sender, message):
        print(f'[id={self.id}] [sender={sender}]: {message}')

    def audio_streaming_server(self):
        self.__audio_publisher_socket.bind(f"tcp://*:55{self.id}3")
        thread = threading.Thread(target=self.__audio_streaming_server_thread, args=())
        self.__audio_server_threads.append(thread)
        thread.start()

    def __audio_streaming_server_thread(self):
        with self.mic.recorder(samplerate=48000,channels=1) as mic:
            while True:
                data = mic.record(numframes=1024)
                data_bytes = data.tobytes()
                self.__audio_publisher_socket.send(data_bytes)
        '''recorder.stop()'''

    def audio_streaming_client(self):
        for newSocket in range(8):
            if(self.id == newSocket):
                context = zmq.Context()
                socket = context.socket(zmq.SUB)
                socket.connect(f"tcp://localhost:55{newSocket}3")
                socket.setsockopt(zmq.SUBSCRIBE, b"")
                thread = threading.Thread(target=self.__audio_streaming_client_thread, args=(socket,newSocket))
                self.__audio_client_threads.append(thread)
                thread.start()

    def __audio_streaming_client_thread(self, socket, sender):
        while True:
            with self.spk.player(samplerate=48000, channels=1) as sp:
                data_bytes = socket.recv()
                data = np.frombuffer(data_bytes, dtype=np.float32)
                sp.play(data)