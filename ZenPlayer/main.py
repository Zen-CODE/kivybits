"""
ZenPlayer
=========

ZenPlayer is a minimal audio/video player that explores the ability of the
Kivy framework.

"""
__author__ = 'ZenCODE'

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty
from os import path, listdir
#from kivy.core.audio import SoundLoader
from audioplayer import SoundLoader

Builder.load_string('''
<PlayingScreen>:
    album_image: album_image
    BoxLayout:
        orientation: "horizontal"
        BoxLayout:
            orientation: "vertical"
            size_hint_x: 0.1
        Image:
            id: album_image
            size_hint_x: 0.8
        BoxLayout:
            orientation: "vertical"
            size_hint_x: 0.1
''')


class PlayingScreen(Screen):
    """
    The main screen that shows whats currently playing
    """
    #TODO : Document properties once stable
    album_image = ObjectProperty()
    sound = None
    queue = []  # contains a list of (filename, albumart) pairs
    advance = True  # This flag indicates whether to advance to the next track
                    # once the currently playing one had ended

    def add_folder(self, folder):
        """ Add the specified folder to the queue """
        artwork = self._get_albumart(folder)
        for f in listdir(folder):
            if ".mp3" in f or ".ogg" in f or ".wav" in f:
                self.queue.append([path.join(folder, f), artwork])

    def play(self, index=0):
        if not self.sound:
            self._start_play()

    def stop(self):
        """ Stop any playing audio """
        if self.sound:
            self.advance = False
            self.sound.stop()

    def _get_albumart(self, folder):
        """
        Return the full image filename from the folder
        """
        for file in ["cover.jpg", "cover.png", "cover.bmp", "cover.jpeg"]:
            full_name = path.join(folder, file)
            if path.exists(full_name):
                return full_name
        return ""


    def _start_play(self):
        """
        Start playing any files in the queue
        """
        if len(self.queue) > 0:
            print "playing ", self.queue[0][0]
            self.sound = SoundLoader.load(self.queue[0][0])
            self.sound.bind(on_stop=self._on_stop)
            self.sound.play()
            self.album_image.source = self.queue[0][1]

    def _on_stop(self, *args):
        print "sound has stopped. args=", str(args)
        if self.advance:
            self.queue.pop(0)
            self._start_play()
        # output: sound has stopped. args=
        # (<kivy.core.audio.audio_pygame.SoundPygame object at 0xa106a7c>,)


class ZenPlayer(App):
    def build(self):
        sm = ScreenManager()
        playing = PlayingScreen()
        #TODO: Remove
        #playing.play_folder('/media/Zen320/Zen/Music/MP3/In Flames/Colony')
        playing.add_folder('/media/Zen320/Zen/Music/MP3/Ace of base/Da capo')
        playing.play()

        def stop(dt):
            print "About to stop"
            playing.stop()

        #from kivy.clock import Clock
        #Clock.schedule_once(stop, 5.0)

        #TODO: Remove

        sm.switch_to(playing)
        return sm

ZenPlayer().run()


