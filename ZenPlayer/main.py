"""
ZenPlayer
=========

ZenPlayer is a minimal audio/video player that explores the ability of the
Kivy framework.

"""
__author__ = 'ZenCODE'

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty
from os import path, listdir
from kivy.core.audio import SoundLoader
#from audioplayer import SoundLoader

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
    queue = []
    advance = True  # This flag indicates whether to advance to the next track
                    # once the currently playing one had ended

    def play_folder(self, folder):
        self._set_albumart(folder)
        self._add_to_queue(folder)
        if not self.sound:
            self._start_play()

    def stop(self):
        """ Stop any playing audio """
        if self.sound:
            self.advance = False
            self.sound.stop()

    def _set_albumart(self, folder):
        """
        Extracts the image from the folder and displays any cover images in the
        center image placeholder
        """
        for file in ["cover.jpg", "cover.png", "cover.bmp", "cover.jpeg"]:
            full_name = path.join(folder, file)
            if path.exists(full_name):
                self.album_image.source = full_name
                break

    def _add_to_queue(self, folder):
        """
        Add any suitable files to the queue for playback when done
        """
        for file in listdir(folder):
            if ".mp3" in file or ".ogg" in file or ".wav" in file:
                self.queue.append(path.join(folder, file))

    def _start_play(self):
        """
        Start playing any files in the queue
        """
        if len(self.queue) > 0:
            print "playing ", self.queue[0]
            self.sound = SoundLoader.load(self.queue[0])
            self.sound.bind(on_stop=self._on_stop)
            self.sound.play()

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
        playing.play_folder('/media/Zen320/Zen/Music/MP3/Ace of base/Da capo')

        def stop(dt):
            print "About to stop"
            playing.stop()

        #from kivy.clock import Clock
        #Clock.schedule_once(stop, 5.0)

        #TODO: Remove

        sm.switch_to(playing)
        return sm

ZenPlayer().run()


