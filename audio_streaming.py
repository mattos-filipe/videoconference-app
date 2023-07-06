import time
import zmq
import threading
import numpy as np
import pyaudio

class AudioStreaming:
    #Defining the socket for the publisher
    __context = zmq.Context()
    __audio_publisher_socket = __context.socket(zmq.PUB)

    #list of threads
    __audio_server_threads = []
    __audio_client_threads = []
    audio = pyaudio.PyAudio()

    #class constructor
    def __init__(self, id, ip_list):
        self.id=id
        self.ip_list = ip_list
        print(f'[{self.id}] Conectado à audiotransmissao!')

        #calling the method that initiates the publisher thread
        self.audio_streaming_server()

        #calling the method that initiates the subscribers threads
        self.audio_streaming_client()

    def __format_print(self, sender, message):
        print(f'[id={self.id}] [sender={sender}]: {message}')

    def audio_streaming_server(self):
        #bing at port 55{self.id}1
        self.__audio_publisher_socket.bind(f"tcp://*:55{self.id}3")
        thread = threading.Thread(target=self.__audio_streaming_server_thread)
        self.__audio_server_threads.append(thread)
        thread.start()

    def __audio_streaming_server_thread(self):
        audio = pyaudio.PyAudio()
        #open microphone
        stream = audio.open(format=pyaudio.paInt16,
                            channels=1,
                            rate=44100,
                            input=True,
                            frames_per_buffer=5120)
        
        while True:
            #record micrhophone audio
            audio_data = stream.read(5120)
            #send record
            self.__audio_publisher_socket.send(audio_data)
            time.sleep(0.05)


    def audio_streaming_client(self):
        #the user connects to all other ips
        for ip in self.ip_list:
            for newSocket in range(8):
                if newSocket != self.id: #we dont want our own audio feedback
                    context = zmq.Context()
                    socket = context.socket(zmq.SUB)

                    #connects to the user
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
            #receive audio
            audio_data = socket.recv()
            time.sleep(0.05)
            #play audio
            stream.write(audio_data)
        