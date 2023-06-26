import arcade
import time

class BGM:
    def __init__(self, song_index):
        self.music_list = ["bgm/MainMenu2.mp3", "bgm/GameMusic2.mp3", "bgm/GameOver.mp3", "bgm/Chomp.mp3",
                           "bgm/Death.mp3", "bgm/Switch.mp3", "bgm/mirror.mp3", "bgm/diamond.mp3", "bgm/Click.wav"]
        self.current_song_index = song_index
        self.player = None
        self.music = None

    def play_music(self, volume, loop):
        self.music = arcade.Sound(self.music_list[self.current_song_index], streaming=True)
        self.player = self.music.play(volume=volume, loop=loop)
        time.sleep(0.03)

    def stop_audio(self):
        if self.player:
            self.player.pause()