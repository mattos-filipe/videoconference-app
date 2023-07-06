import socket
import time

import sys
sys.path.append("lib")
import text_messaging as tm
import video_streaming as vs
import audio_streaming as us

 
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

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8", 80))

ip_address = s.getsockname()[0]
hostname = socket.gethostname()

print(ip_address)
print(hostname)

ip_list = [ip_address, '192.168.43.236', '192.168.43.241','192.168.43.45']
for i in ip_list:
    #print(i)
    pass
if __name__ == "__main__":  
    if len(sys.argv) != 2:
        print('Número incorreto de parâmetros. Exemplo de uso:\n\n\tpython3 servidor.py [id]\nCom 0 <= [id] <= 7')
        exit()
    if( int(sys.argv[1]) <0 or int(sys.argv[1]) > 7 ):
        print('Id inválido: 0 <= [id] <= 7')
        exit()
    id = int(sys.argv[1])
    
    tm.TextMessaging(id, ip_list)
    vs.VideoStreaming(id, ip_list)
    us.AudioStreaming(id, ip_list)
        