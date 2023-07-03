import zmq
import threading
import sys
import time


class TextMessaging:
    __context = zmq.Context()
    __text_publisher_socket = __context.socket(zmq.PUB)
    __text_server_threads = []
    __text_client_threads = []
    def __init__(self, id, ip_list):
        self.lock = False
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
            if(message == 'quit'):
                self.lock = True
                return
            self.__text_publisher_socket.send_string(message)

        
    def text_messaging_client(self):
        for ip in self.ip_list:
            for newSocket in range(8):
                if(newSocket != self.id):
                    context = zmq.Context()
                    text_socket = context.socket(zmq.SUB)
                    text_socket.connect(f"tcp://{ip}:55{newSocket}1")
                    text_socket.setsockopt(zmq.SUBSCRIBE, b"")
                    thread = threading.Thread(target=self.__text_messaging_client_thread, args=(text_socket,newSocket))
                    self.__text_client_threads.append(thread)
                    thread.start()

    def __text_messaging_client_thread(self, text_socket, sender):
        while True:
            if(self.lock):
                return  
            message = text_socket.recv_string()
            self.__format_print( sender, message)

    def delete(self):
        time.sleep(1)
        sys.exit(0)