"""
ZenPlayer
=========

ZenPlayer is a minimal audio/video player that explores the ability of the
Kivy framework.

"""
__author__ = 'ZenCODE'

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty, StringProperty
from os import path, listdir
from kivy.core.audio import SoundLoader
#from audioplayer import SoundLoader

Builder.load_string('''
<MediaButton>:
    image: image
    Image:
        id: image
        pos_hint: {'x': 0, 'y': 0}
        size_hint: 1, 1
        on_touch_down: self.collide_point(*args[1].pos) and root.dispatch('on_click')
''')


class MediaButton(FloatLayout):
    """
    A pretty, shiny button showing the player controls
    """
    source = StringProperty('')
    image = ObjectProperty()

    def __init__(self, **kwargs):
        """ Override the constructor so we can register an event """
        super(MediaButton, self).__init__(**kwargs)
        self.register_event_type("on_click")

    def on_source(self, widget, value):
        """ The 'source' property for the image has changed. Change it. """
        self.image.source = value

    def on_click(self):
        """ The button has been clicked. """
        pass


Builder.load_string('''

<PlayingScreen>:
    # Define the buttons
    but_previous: previous
    but_stop: stop
    but_playpause: playpause
    but_next: next

    album_image: album_image
    BoxLayout:
        orientation: "horizontal"
        BoxLayout:
            # Left Sidebar
            orientation: "vertical"
            size_hint_x: 0.1
        BoxLayout:
            # Center column
            size_hint_x: 0.8
            orientation: "vertical"
            padding: 10, 10, 10, 10
            Image:
                size_hint_y: 0.9
                id: album_image
            BoxLayout:
                size_hint_y: 0.1
                orientation: "horizontal"
                MediaButton:
                    id: previous
                    source: 'images/previous.png'
                MediaButton:
                    id: stop
                    source: 'images/stop.png'
                    on_click: root.stop()
                MediaButton:
                    id: playpause
                    source: 'images/play.png'
                    on_click: root.playpause()
                MediaButton:
                    id: next
                    source: 'images/next.png'

        BoxLayout:
            # Right sidebar
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
    current = 0  # The index of the currently playing track in the queue
    but_previous = ObjectProperty()
    but_stop = ObjectProperty()
    but_playpause = ObjectProperty()
    but_next = ObjectProperty()

    def init(self):
        """ Initialize the display """
        if len(self.queue) > self.current:
            self.album_image.source = self.queue[self.current][1]

    def add_folder(self, folder):
        """ Add the specified folder to the queue """
        artwork = self._get_albumart(folder)
        for f in listdir(folder):
            if ".mp3" in f or ".ogg" in f or ".wav" in f:
                self.queue.append((path.join(folder, f), artwork))

    def playpause(self):
        """ Start playing any audio if nothing is playing """
        if not self.sound:
            if len(self.queue) > self.current:
                print "playing ", self.queue[self.current][0]
                self.sound = SoundLoader.load(self.queue[self.current][0])
                self.sound.bind(on_stop=self._on_stop)
                self.sound.play()
                self.album_image.source = self.queue[self.current][1]
                self.but_playpause.source = "images/pause.png"
        elif self.sound.state == "play":
            self.advance = False
            self.sound.stop()
            self.but_playpause.source = "images/play.png"
        else:
            self.sound.play()
            self.but_playpause.source = "images/pause.png"

    def stop(self):
        """ Stop any playing audio """
        if self.sound:
            self.advance = False
            self.sound.stop()
            self.but_playpause.source = "images/play.png"

    @staticmethod
    def _get_albumart(folder):
        """
        Return the full image filename from the folder
        """
        for f in ["cover.jpg", "cover.png", "cover.bmp", "cover.jpeg"]:
            full_name = path.join(folder, f)
            if path.exists(full_name):
                return full_name
        return ""

    def _on_stop(self, *args):
        print "sound has stopped. args=", str(args)
        if self.advance:
            self.queue.pop(0)
            self.playpause()
        # output: sound has stopped. args=
        # (<kivy.core.audio.audio_pygame.SoundPygame object at 0xa106a7c>,)


class ZenPlayer(App):
    def build(self):
        sm = ScreenManager()
        playing = PlayingScreen()
        #TODO: Remove
        #playing.play_folder('/media/Zen320/Zen/Music/MP3/In Flames/Colony')
        playing.add_folder('/media/Zen320/Zen/Music/MP3/Ace of base/Da capo')
        playing.init()
        #playing.play()

        #def stop(dt):
        #    print "============= About to stop"
        #    playing.stop()

        #from kivy.clock import Clock
        #Clock.schedule_once(stop, 5.0)

        #TODO: Remove

        sm.switch_to(playing)
        return sm

ZenPlayer().run()
