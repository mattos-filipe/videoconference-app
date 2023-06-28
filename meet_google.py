import zmq
import sys
import text_messaging as tm
import video_streaming as vs
import audio_streaming as us
import pyaudio
 
'''
PORT SCHEME
    [55{id}{type}]
    The {id}   variable indicates the program identifier
    The {type} variable indicates the kind of data
        0: process_communication //deprecated
        1: text_streaming
        2: video_streaming
        3: audio_streaming
'''

ip_list = ['192.168.43.100','192.168.43.241']
for i in ip_list:
    print(i)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print('Número incorreto de parâmetros. Exemplo de uso:\n\n\tpython3 servidor.py [id]\nCom 0 <= [id] <= 7')
        exit()
    if( int(sys.argv[1]) <0 or int(sys.argv[1]) > 7 ):
        print('Id inválido: 0 <= [id] <= 7')
        exit()
    id = int(sys.argv[1])
    
    
    tm.TextMessaging(id, ip_list)
    #vs.VideoStreaming(id, ip_list)
    #us.AudioStreaming(id, ip_list)