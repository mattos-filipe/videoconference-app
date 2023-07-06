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
    The {id}   variable indicates the program identifier, the parameter the users inputs before the execution
    The {type} variable indicates the channel's type of data
        1: text_streaming
        2: video_streaming
        3: audio_streaming
'''

#Identifying user's ip
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8", 80))
ip_address = s.getsockname()[0] #user ip
hostname = socket.gethostname()

'''CHANGE THE CODE HERE:
    1 - Never remove {ip_addres} from ip_list, just add the users ip as shown above
    2 - There are two operation mode listed below, uncomment how u want to run and comment the other
'''

#UNCOMMENT THE LINE BELOW IF THE PROGRAMS WILL BE EXECUTED ON MORE THAN ONE COMPUTER
ip_list = [ip_address, '192.168.43.236', '192.168.43.241','192.168.43.45']

#UNCOMMENT THE LINE BELOW IF THE PROGRAMS WILL BE EXECUTED ON A SINGLE COMPUTER
#ip_list = [ip_address]

if __name__ == "__main__":  
    #Checking if the user input the {id} parameter
    if len(sys.argv) != 2:
        print('Número incorreto de parâmetros. Exemplo de uso:\n\n\tpython3 servidor.py [id]\nCom 0 <= [id] <= 7')
        exit()
    if( int(sys.argv[1]) <0 or int(sys.argv[1]) > 7 ):
        print('Id inválido: 0 <= [id] <= 7')
        exit()

    #program identifier
    id = int(sys.argv[1])
    
    #Initiating the text messaging class
    tm.TextMessaging(id, ip_list)

    #Initiating the video streaming class
    vs.VideoStreaming(id, ip_list)

    #Initiating the audio streaming class
    us.AudioStreaming(id, ip_list)
        