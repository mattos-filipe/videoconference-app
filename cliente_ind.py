import cv2
import zmq
import threading
import numpy as np
from collections import deque

def __video_streaming_client_thread(socket, sender):
        windowName = f'Video [id={id}] [sender={sender}]'
        while True:
            encoded_frame = socket.recv()
            frame = cv2.imdecode(np.frombuffer(encoded_frame, dtype=np.uint8), cv2.IMREAD_COLOR)
            #data_deque_dict[self.id].append(frame)
            

            cv2.imshow(windowName, frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        cv2.destroyWindow(windowName)

context = zmq.Context()
socket = context.socket(zmq.SUB)
socket.connect(f"tcp://localhost:5502")
socket.setsockopt(zmq.SUBSCRIBE, b"")
thread = threading.Thread(target=__video_streaming_client_thread, args=(socket,1,))
thread.start()