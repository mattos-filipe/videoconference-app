import soundcard
import soundfile as sf

# Seleciona o dispositivo de entrada de áudio (microfone)
microphones = soundcard.all_microphones()
print(microphones)

microphone = soundcard.default_microphone()

# Seleciona o dispositivo de saída de áudio (alto-falante)
speaker = soundcard.default_speaker()

# Configura a taxa de amostragem e o número de canais
samplerate = 44100
channels = 1

# Define o tamanho do buffer de áudio
buffer_size = 1024

# Cria um gravador de áudio
recorder = microphone.recorder(samplerate=samplerate, channels=channels, blocksize=buffer_size)

# Cria um player de áudio
player = speaker.player(samplerate=samplerate, channels=channels, blocksize=buffer_size)

# Nome do arquivo de áudio para salvar
filename = "audio_gravado.wav"

# Inicia a gravação, reprodução e salvamento de áudio
with recorder, player:
    print("Iniciando gravação e reprodução de áudio...")

    # Cria o arquivo WAV para salvar o áudio gravado
    file = sf.SoundFile(filename, mode='w', samplerate=samplerate, channels=channels)
    
    while True:
        # Captura o áudio do microfone
        audio_data = recorder.record(numframes=buffer_size)

        # Reproduz o áudio nos alto-falantes
        player.play(audio_data)

        

        # Verifica se a gravação deve ser interrompida
        if input("Pressione 'q' para parar: ").strip().lower() == "q":
            break
        # Salva o áudio gravado no arquivo
        file.write(audio_data)

    # Fecha o arquivo de áudio
    file.close()

print(f"Áudio gravado salvo em {filename}")
