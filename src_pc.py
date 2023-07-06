
context_pc = zmq.Context()
process_communication_socket = context_pc.socket(zmq.REP)
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