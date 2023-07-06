import zmq
import threading
import sys
import time


class TextMessaging:
    #Defining the socket for the publisher
    __context = zmq.Context()
    __text_publisher_socket = __context.socket(zmq.PUB)

    #list of threads
    __text_server_threads = []
    __text_client_threads = []

    #class constructor
    def __init__(self, id, ip_list):
        self.id=id
        self.ip_list = ip_list
        print(f'[{self.id}] Conectado ao chat de texto!')

        #calling the method that initiates the publisher thread
        self.text_messaging_server()

        #calling the method that initiates the subscribers threads
        self.text_messaging_client()

    def __format_print(self, sender, message):
        print(f'[id={self.id}] [sender={sender}]: {message}')

    def text_messaging_server(self):
        #bing at port 55{self.id}1
        self.__text_publisher_socket.bind(f"tcp://*:55{self.id}1")
        thread = threading.Thread(target=self.__text_messaging_server_thread, args=())
        self.__text_server_threads.append(thread)
        thread.start()

    def __text_messaging_server_thread(self):
        while True:
            #reads users message and sends through socket
            message = input()
            self.__text_publisher_socket.send_string(message)

        
    def text_messaging_client(self):
        #the user connects to all other ips
        for ip in self.ip_list:
            for newSocket in range(8):
                if(newSocket != self.id):# we dont want our own text feedback
                    context = zmq.Context()
                    text_socket = context.socket(zmq.SUB)
                    
                    #connects to the user
                    text_socket.connect(f"tcp://{ip}:55{newSocket}1")
                    text_socket.setsockopt(zmq.SUBSCRIBE, b"")
                    thread = threading.Thread(target=self.__text_messaging_client_thread, args=(text_socket,newSocket))
                    self.__text_client_threads.append(thread)
                    thread.start()

    def __text_messaging_client_thread(self, text_socket, sender):
        while True:
            #receive string and print it
            message = text_socket.recv_string()
            self.__format_print( sender, message)