import cv2
import zmq
import threading
import numpy as np
import time


class VideoStreaming:
    #Defining the socket for the publisher
    __context = zmq.Context()
    __video_publisher_socket = __context.socket(zmq.PUB)

    #list of threads
    __video_server_threads = []
    __video_client_threads = []

    #class constructor
    def __init__(self, id, ip_list):
        self.id=id
        self.ip_list = ip_list


        print(f'[{self.id}] Conectado à videotransmissao!')

        #calling the method that initiates the publisher thread
        self.video_streaming_server()

        #calling the method that initiates the subscribers threads
        self.video_streaming_client()

    def __format_print(self, sender, message):
        print(f'[id={self.id}] [sender={sender}]: {message}')

    def video_streaming_server(self):
        #bing at port 55{self.id}1
        self.__video_publisher_socket.bind(f"tcp://*:55{self.id}2")
        thread = threading.Thread(target=self.__video_streaming_server_thread, args=())
        self.__video_server_threads.append(thread)
        thread.start()

    def __video_streaming_server_thread(self):
        #capture image from camera
        video_capture = cv2.VideoCapture(0)
        while True:
            ret, frame = video_capture.read()
            #encode
            encoded_frame = cv2.imencode('.jpg', frame)[1].tobytes()
            #send through socket
            self.__video_publisher_socket.send(encoded_frame)
            time.sleep(0.05)
            
        video_capture.release()

    def video_streaming_client(self):
        #the user connects to all other ips
        for ip in self.ip_list:
            for newSocket in range(8):
                #if(newSocket != self.id) we want our own video feedback
                context = zmq.Context()
                socket = context.socket(zmq.SUB)
                
                #connects to the user
                socket.connect(f"tcp://{ip}:55{newSocket}2")
                socket.setsockopt(zmq.SUBSCRIBE, b"")
                thread = threading.Thread(target=self.__video_streaming_client_thread, args=(socket,newSocket))
                self.__video_client_threads.append(thread)
                thread.start()

    def __video_streaming_client_thread(self, socket, sender):
        #setting window's name
        windowName = f'Video [id={self.id}] [sender={sender}]'
        while True:
            #receive frame
            encoded_frame = socket.recv()
            frame = cv2.imdecode(np.frombuffer(encoded_frame, dtype=np.uint8), cv2.IMREAD_COLOR)

            #open window to show image
            cv2.imshow(windowName, frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        cv2.destroyWindow(windowName)