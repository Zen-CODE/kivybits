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
from playlist import PlayList, PlayListScreen
from kivy.clock import Clock
from filebrowser import ZenFileBrowser
from kivy.utils import platform
if platform == 'linux':  # Enable Mp3
    from audioplayer import SoundLoader
else:
    from kivy.core.audio import SoundLoader
#from kivy.core.audio import SoundLoader

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
    volume: volume
    progress: progress
    info_label1: info_label1
    info_label2: info_label2
    info_label3: info_label3
    time_label: time_label

    album_image: album_image
    BoxLayout:
        BoxLayout:
            orientation: "vertical"
            size_hint_x: 0.1
            padding: 10
            spacing: 10
            Slider:
                id: progress
                size_hint_y: 0.9
                orientation: "vertical"
                max: 1
                #on_value: root.set_volume()
            Image:
                size_hint_y: 0.075
                source: 'images/progress.png'
        BoxLayout:
            # Center column
            size_hint_x: 0.8
            orientation: "vertical"
            padding: 10, 10, 10, 10
            BoxLayout:
                size_hint_y: 0.05
                Image:
                    source: 'images/add.png'
                    on_touch_down: self.collide_point(*args[1].pos) and root.show_filebrowser()
                Image:
                    source: 'images/zencode.jpg'
                Image:
                    source: 'images/playlist.png'
                    on_touch_down: self.collide_point(*args[1].pos) and root.show_playlist()
            Label:
                id: info_label1
                size_hint_y: 0.05
            Label:
                id: info_label2
                size_hint_y: 0.05
            Label:
                id: info_label3
                size_hint_y: 0.05
            BoxLayout:
                size_hint_y: 0.65
                padding: 10, 10, 10, 10
                Image:
                    id: album_image
                    source: "images/zencode.jpg"
            Label:
                id: time_label
                size_hint_y: 0.05
            BoxLayout:
                size_hint_y: 0.075
                orientation: "horizontal"
                MediaButton:
                    id: previous
                    source: 'images/previous.png'
                    on_click: root.play_previous()
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
                    on_click: root.play_next()

        BoxLayout:
            # Right sidebar
            orientation: "vertical"
            size_hint_x: 0.1
            padding: 10
            spacing: 10
            Slider:
                id: volume
                size_hint_y: 0.9
                orientation: "vertical"
                max: 1
                on_value: root.set_volume()
            Image:
                size_hint_y: 0.075
                source: 'images/speaker.png'
''')


class PlayingScreen(Screen):
    """
    The main screen that shows whats currently playing
    """
    #TODO : Document properties once stable
    album_image = ObjectProperty()
    sound = None
    advance = True  # This flag indicates whether to advance to the next track
                    # once the currently playing one had ended
    playlist = PlayList()
    but_previous = ObjectProperty()
    but_stop = ObjectProperty()
    but_playpause = ObjectProperty()
    but_next = ObjectProperty()
    info_label = ObjectProperty()
    volume = ObjectProperty()
    progress = ObjectProperty()
    time_label = ObjectProperty()

    def __init__(self, sm, **kwargs):
        self.sm = sm
        super(PlayingScreen, self).__init__(**kwargs)
        Clock.schedule_interval(self._update_progress, 1/25)
        self.playlist.load()

    def init(self):
        """ Initialize the display """
        self.album_image.source = self.playlist.get_current_art()
        info = self.playlist.get_current_info()
        if info:
            self.info_label1.text = info["artist"]
            self.info_label2.text = info["album"]
            self.info_label3.text = info["file"]
            self.volume.value = 0.5   # TODO: Initialize to half or previous

    def playpause(self):
        """ Start playing any audio if nothing is playing """
        if not self.sound:
            audiof = self.playlist.get_current_file()
            if audiof:
                print "playing ", audiof
                self.sound = SoundLoader.load(audiof)
                self.sound.bind(on_stop=self._on_sound_stop)
                self.sound.play()
                self.init()
                self.but_playpause.source = "images/pause.png"
                self.sound.volume = self.volume.value
        elif self.sound.state == "play":
            self.advance = False
            self.sound.stop()
            self.but_playpause.source = "images/play.png"
        else:
            self.sound.play()
            self.but_playpause.source = "images/pause.png"
            self.sound.volume = self.volume.value

    def play_next(self):
        """ Play the next track. """
        print "PlayingScreen.play_next"
        if self.sound:
            self.stop()
            self.sound = None
        self.playlist.move_next()
        print "self.playlist.move_next()=", self.playlist.get_current_file()
        if self.playlist.get_current_file():
            self.init()
            self.playpause()

    def play_previous(self):
        """ Ply the previous track. """
        if self.sound:
            self.stop()
            self.sound = None
        self.playlist.move_previous()
        print "self.playlist.move_previous()=", self.playlist.get_current_file()
        if self.playlist.get_current_file():
            self.init()
            self.playpause()

    def stop(self):
        """ Stop any playing audio """
        self.advance = False
        if self.sound:
            self.sound.stop()
            self.but_playpause.source = "images/play.png"
            self.sound = None
            self.advance = True

    def save(self):
        """ Save the current playlist state """
        self.playlist.save()

    def set_volume(self):
        """ Set the volume of the currently playing track if there is one. """
        if self.sound:
            self.sound.volume = self.volume.value

    def show_playlist(self):
        """ Switch to the playlist screen """
        if "playlist" not in self.sm.screen_names:
            self.sm.add_widget(PlayListScreen(self.sm,
                                              self.playlist,
                                              name="playlist"))
        self.sm.current = "playlist"

    def show_filebrowser(self):
        """ Switch to the playlist screen """
        if "filebrowser" not in self.sm.screen_names:
            self.sm.add_widget(ZenFileBrowser(self.sm,
                                              self.playlist,
                                              name="filebrowser"))
        self.sm.current = "filebrowser"

    def _on_sound_stop(self, *args):
        print "sound has stopped. args=", str(args)
        self.sound = None
        if self.advance:
            self.playlist.move_next()
            self.init()
            self.playpause()

    def _update_progress(self, dt):
        """ Update the progressbar  """
        if self.sound:
            #self.progress.value = self.sound.get_pos()
            length = self.sound._get_length()
            if length > 0:
                self.progress.value = self.sound.get_pos() / length

                mins, secs = int(length / 60), int(length % 60)
                self.time_label.text = "{0}s / {1}m {2:02d}s".format(
                    int(self.sound.get_pos()),
                    mins,
                    secs)


class ZenPlayer(App):
    """
    The App initialisation class
    """
    playing = None  # Reference to the main screen (for saving)


    def on_pause(self):
        # Enable support for pause
        return True

    def on_resume(self):
        # Enable support for resume
        pass

    def build(self):
        sm = ScreenManager()
        self.playing = PlayingScreen(sm, name="main")
        self.playing.init()
        sm.add_widget(self.playing)
        sm.current = "main"
        return sm

    def on_stop(self):
        """The app is closing. Save the state."""
        self.playing.save()

ZenPlayer().run()
