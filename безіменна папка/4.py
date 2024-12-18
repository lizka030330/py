class AudioDecoder:
    def decode(self, filename):
        print(f"Decoding audio file: {filename}")

class FileReader:
    def read(self, filename):
        print(f"Reading audio file: {filename}")

class Equalizer:
    def set_equalizer(self):
        print("Setting equalizer to default settings")

class AudioPlayer:
    def play(self):
        print("Playing audio...")

class AudioFacade:
    def __init__(self):
        self.decoder = AudioDecoder()
        self.reader = FileReader()
        self.equalizer = Equalizer()
        self.player = AudioPlayer()
    
    def play_audio(self, filename):
        self.reader.read(filename)
        self.decoder.decode(filename)
        self.equalizer.set_equalizer()
        self.player.play()

if __name__ == "__main__":
    audio_facade = AudioFacade()
    audio_facade.play_audio("song.mp3")
