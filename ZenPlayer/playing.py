from kivy.lang import Builder
from kivy.properties import ObjectProperty
from playlist import PlayList, PlayListScreen
from kivy.clock import Clock
from filebrowser import ZenFileBrowser
from kivy.utils import platform
if platform == 'linux':  # Enable Mp3
    from audioplayer import SoundLoader
else:
    from kivy.core.audio import SoundLoader
from kivy.logger import Logger
from kivy.storage.jsonstore import JsonStore
from kivy.uix.screenmanager import Screen


class Controller(object):
    """
    Controls the playing of audio and coordinates the updating of the playlist
    and screen displays
    """
    volume = 100
    advance = True  # This flag indicates whether to advance to the next track
                    # once the currently playing one had ended
    sm = None  # THe ScreenManager

    def __init__(self, sm):
        self.sm = sm
        self.playlist = PlayList()
        self._store = JsonStore("zenplayer.json")
        self.playlist.load(self._store)
        if self._store.exists('state'):
            state = self._store.get("state")
            if "volume" in state.keys():
                self.volume = state["volume"]

    def _on_sound_stop(self, *args):
        Logger.info("main.py: sound has stopped. args=" + str(args))
        if self.advance:
            self.move_next()
            #self.init_display()
            self.play_pause()

    def get_current_art(self):
        return self.playlist.get_current_art()

    def get_current_info(self):
        return self.playlist.get_current_info()

    def get_current_file(self):
        return self.playlist.get_current_file()

    def play_pause(self):
        self.advance = True
        if not Sound.state:
            audiof = self.get_current_file()
            if audiof:
                Logger.info("main.py: playing " + audiof)
                Sound.play(audiof, self._on_sound_stop)
                #self.init_display()
                #self.but_playpause.source = "images/pause.png"
                Sound.set_volume(self.volume)
        elif Sound.state == "playing":
            Sound.stop()
            #self.but_playpause.source = "images/play.png"
        else:
            Sound.play()
            #self.but_playpause.source = "images/pause.png"
            Sound.set_volume(self.volume_slider.value)

    def play_next(self):
        Logger.info("main.py: PlayingScreen.play_next")
        self.move_next()
        audiofile = self.get_current_file()
        if audiofile:
            #self.init_display()
            Sound.play(audiofile)

    def play_previous(self):
        """ Ply the previous track. """
        self.move_previous()
        audiofile = self.get_current_file()
        if audiofile:
            #self.init_display()
            Sound.play(audiofile)

    def move_next(self):
        self.playlist.move_next()

    def move_previous(self):
        self.playlist.move_previous()

    def save(self):
        self.playlist.save(self._store)
        self._store.put("state", volume=self.volume)

    def set_volume(self, value):
        """ Set the volume of the currently playing track if there is one. """
        self.volume = value
        Sound.set_volume(value)

    def show_filebrowser(self):
        """ Switch to the playlist screen """
        if "filebrowser" not in self.sm.screen_names:
            self.sm.add_widget(ZenFileBrowser(self.sm,
                                              self.playlist,
                                              name="filebrowser"))
        self.sm.current = "filebrowser"

    def show_playlist(self):
        """ Switch to the playlist screen """
        if "playlist" not in self.sm.screen_names:
            self.sm.add_widget(PlayListScreen(self.sm,
                                              self.playlist,
                                              name="playlist"))
        self.sm.current = "playlist"


    def stop(self):
        """ Stop any playing audio """
        self.advance = False
        Sound.stop()
        #self.but_playpause.source = "images/play.png"

Builder.load_string('''
<PlayingScreen>:
    # Define the buttons
    but_previous: previous
    but_stop: stop
    but_playpause: playpause
    but_next: next
    volume_slider: volume
    progress_slider: progress
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
                    on_touch_down: self.collide_point(*args[1].pos) and \
                                   root.show_filebrowser()
                Image:
                    source: 'images/zencode.jpg'
                Image:
                    source: 'images/playlist.png'
                    on_touch_down: self.collide_point(*args[1].pos) and \
                                   root.show_playlist()
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
                    on_click: root.play_pause()
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
                value: 0.5
                max: 1
                on_value: root.set_volume()
            Image:
                size_hint_y: 0.075
                source: 'images/speaker.png'
''')


class Sound():
    """
    This class manages the playing audio as a Singleton
    """
    state = ""  # One of "", "stopped", "playing"
    _sound = None  # The underlying Sound instance

    @staticmethod
    def _on_stop(*args):
        Logger.info("main.py: sound has stopped. args=" + str(args))
        Sound.state = "stopped"

    @staticmethod
    def get_pos_length():
        """ Return a tuple of the length and position, or return 0, 0"""
        sound = Sound._sound
        if sound:
            return sound.get_pos(), sound._get_length()
        else:
            return 0, 0

    @staticmethod
    def stop():
        """ Stop any playing audio """
        if Sound._sound:
            Sound._sound.stop()
            Sound.state = "stopped"

    @staticmethod
    def play(filename="", on_stop=None):
        """
        Play the file specified by the filename. If on_stop is passed in,
        this function is called when the sound stops
        """
        if Sound._sound is not None:
            Sound._sound.stop()

        if filename:
            Sound._sound = SoundLoader.load(filename)
        if Sound._sound:
            Sound._sound.bind(on_stop=Sound._on_stop)
            Sound._sound.play()
            Sound.state = "playing"

    @staticmethod
    def set_volume(value):
        """
        The the volume of the currently playing sound if appropriate
        """
        if Sound._sound:
            Sound._sound.volume = value


class PlayingScreen(Screen):
    """
    The main screen that shows whats currently playing
    """
    #TODO : Document properties once stable
    album_image = ObjectProperty()
    but_previous = ObjectProperty()
    but_stop = ObjectProperty()
    but_playpause = ObjectProperty()
    but_next = ObjectProperty()
    info_label = ObjectProperty()
    volume_slider = ObjectProperty()
    progress_slider = ObjectProperty()
    time_label = ObjectProperty()
    ctrl = None  #Controller()

    def __init__(self, sm, **kwargs):
        self.ctrl = Controller(sm)
        super(PlayingScreen, self).__init__(**kwargs)
        Clock.schedule_interval(self._update_progress, 1/25)
        self.volume_slider.value = self.ctrl.volume

    def init_display(self):
        """ Initialize the display """
        self.album_image.source = self.ctrl.get_current_art()
        info = self.ctrl.get_current_info()
        if info:
            self.info_label1.text = info["artist"]
            self.info_label2.text = info["album"]
            self.info_label3.text = info["file"]

    def play_pause(self):
        """ Start playing any audio if nothing is playing """
        self.ctrl.play_pause()

    def play_next(self):
        """ Play the next track. """
        self.ctrl.play_next()

    def play_previous(self):
        """ Ply the previous track. """
        self.ctrl.play_previous()

    def stop(self):
        """ Stop any playing audio """
        self.ctrl.stop()

    def save(self):
        """ Save the current playlist state """
        self.ctrl.save()

    def set_volume(self):
        """ Set the volume of the currently playing track if there is one. """
        self.ctrl.set_volume(self.volume_slider.value)

    def show_playlist(self):
        """ Switch to the playlist screen """
        self.ctrl.show_playlist()

    def show_filebrowser(self):
        """ Switch to the playlist screen """
        self.ctrl.show_filebrowser()

    def _update_progress(self, dt):
        """ Update the progressbar  """
        if Sound.state == "playing":
            pos, length = Sound.get_pos_length()
            if length > 0:
                self.progress_slider.value = pos / length

                self.time_label.text = "{0}m {1:02d}s / {2}m {3:02d}s".format(
                    int(pos / 60),
                    int(pos % 60),
                    int(length / 60),
                    int(length % 60))
