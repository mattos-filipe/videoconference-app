import soundcard

# Seleciona o dispositivo de entrada de áudio (microfone)
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

# Inicia a gravação e reprodução de áudio
with recorder, player:
    print("Iniciando gravação e reprodução de áudio...")

    while True:
        # Captura o áudio do microfone
        audio_data = recorder.record(numframes=buffer_size)

        # Reproduz o áudio nos alto-falantes
        player.play(audio_data)