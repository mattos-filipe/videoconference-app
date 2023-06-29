import soundcard as sc
#import threading



default_speaker = sc.default_speaker()
default_mic = sc.default_microphone()



#data = default_mic.record(samplerate=48000, numframes=48000)
#default_speaker.play(data/numpy.max(data), samplerate=48000)

# alternatively, get a `Recorder` and `Player` object
# and play or record continuously:
def audio_streaming_server_thread():
    with default_mic.recorder(samplerate=48000) as mic, \
        default_speaker.player(samplerate=48000) as sp:
        while True:
            data = mic.record(numframes=1024)
            sp.play(data)

#thread = threading.Thread(target=audio_streaming_server_thread, args=())
#thread.start()
with default_mic.recorder(samplerate=48000) as mic, \
        default_speaker.player(samplerate=48000) as sp:
        while True:
            data = mic.record(numframes=1024)
            sp.play(data)
