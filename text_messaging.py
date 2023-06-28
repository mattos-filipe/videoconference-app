import zmq
import threading
import numpy as np

class TextMessaging:
    __context = zmq.Context()
    __text_publisher_socket = __context.socket(zmq.PUB)
    __text_server_threads = []
    __text_client_threads = []
    def __init__(self, id, ip_list):
        self.id=id
        self.ip_list = ip_list
        print(f'[{self.id}] Conectado ao chat de texto!')        
        self.text_messaging_server()
        self.text_messaging_client()

    def __format_print(self, sender, message):
        print(f'[id={self.id}] [sender={sender}]: {message}')

    def text_messaging_server(self):
        self.__text_publisher_socket.bind(f"tcp://*:55{self.id}1")
        thread = threading.Thread(target=self.__text_messaging_server_thread, args=())
        self.__text_server_threads.append(thread)
        thread.start()

    def __text_messaging_server_thread(self):
        while True:
            message = input()
            self.__text_publisher_socket.send_string(message)

        
    def text_messaging_client(self):
        for newSocket in range(8):
            context = zmq.Context()
            text_socket = context.socket(zmq.SUB)
            text_socket.connect(f"tcp://{self.ip_list[newSocket]}:55{newSocket}1")
            text_socket.setsockopt(zmq.SUBSCRIBE, b"")
            thread = threading.Thread(target=self.__text_messaging_client_thread, args=(text_socket,newSocket))
            self.__text_client_threads.append(thread)
            thread.start()

    def __text_messaging_client_thread(self, text_socket, sender):
        while True:
            message = text_socket.recv_string()
            self.__format_print( sender, message)