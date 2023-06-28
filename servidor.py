import cv2
import pyaudio
import zmq
import sys
import text_messaging as tm
import video_streaming as vs
 
'''
PORT SCHEME
    [55{id}{type}]
    The {id}   variable indicates the program identifier
    The {type} variable indicates the kind of data
        0: process_communication //depracated
        1: text_streaming
        2: video_streaming
        3: audio_streaming
'''
def audio_streaming_server(id):
    audio = pyaudio.PyAudio()
    stream = audio.open(format=pyaudio.paInt16,
                        channels=1,
                        rate=44100,
                        input=True,
                        frames_per_buffer=1024)

    context = zmq.Context()
    audio_socket = context.socket(zmq.PUB)
    audio_socket.bind(f"tcp://*:55{id}3")

    while True:
        audio_data = stream.read(1024)
        audio_socket.send(audio_data)

    stream.stop_stream()
    stream.close()
    audio.terminate()



if __name__ == "__main__":
    if len(sys.argv) != 2:
        print('Número incorreto de parâmetros. Exemplo de uso:\n\n\tpython3 servidor.py [id]\nCom 0 <= [id] <= 7')
        exit()
    if( int(sys.argv[1]) <0 or int(sys.argv[1]) > 7 ):
        print('Id inválido: 0 <= [id] <= 7')
        exit()
    id = int(sys.argv[1])
    
    
    tm.TextMessaging(id)
    vs.VideoStreaming(id)