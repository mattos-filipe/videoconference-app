import cv2
import time
import numpy as np
import threading
cap = dict()
index = 0
def thread_fuc(index):
    while True:
        cap[index] = cv2.VideoCapture(index)
        
        print("Camera", index, "is opened.")
        ret, frame = cap[index].read()
        encoded_frame = cv2.imencode('.jpg', frame)[1].tobytes()
        frame = cv2.imdecode(np.frombuffer(encoded_frame, dtype=np.uint8), cv2.IMREAD_COLOR)
        cv2.imshow(f'{index}', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        time.sleep(1)

for i in range(2):
    input()
    thread = threading.Thread(target=thread_fuc, args=(i,))
    thread.start()