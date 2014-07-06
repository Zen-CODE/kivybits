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

    def __init__(self):
        self.playlist = PlayList()
        self.store = JsonStore("zenplayer.json")
        self.playlist.load(self.store)
        if self.store.exists('state'):
            state = self.store.get("state")
            if "volume" in state.keys():
                self.volume = state["volume"]

    def get_current_art(self):
        return self.playlist.get_current_art()

    def get_current_info(self):
        return self.playlist.get_current_info()

    def get_current_file(self):
        return self.playlist.get_current_file()

    def move_next(self):
        self.playlist.move_next()

    def move_previous(self):
        self.playlist.move_previous()

    def save(self):
        self.playlist.save(self.store)
        self.store.put("state", volume=self.volume)


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
                value: 0.5
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
    but_previous = ObjectProperty()
    but_stop = ObjectProperty()
    but_playpause = ObjectProperty()
    but_next = ObjectProperty()
    info_label = ObjectProperty()
    volume_slider = ObjectProperty()
    progress_slider = ObjectProperty()
    time_label = ObjectProperty()
    ctrl = Controller()

    def __init__(self, sm, **kwargs):
        self.sm = sm
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

    def playpause(self):
        """ Start playing any audio if nothing is playing """
        self.advance = True
        if not self.sound:
            audiof = self.ctrl.get_current_file()
            if audiof:
                Logger.info("main.py: playing " + audiof)
                self.sound = SoundLoader.load(audiof)
                self.sound.bind(on_stop=self._on_sound_stop)
                self.sound.play()
                self.init_display()
                self.but_playpause.source = "images/pause.png"
                self.sound.volume = self.volume_slider.value
        elif self.sound.state == "play":
            self.sound.stop()
            self.but_playpause.source = "images/play.png"
        else:
            self.sound.play()
            self.but_playpause.source = "images/pause.png"
            self.sound.volume = self.volume_slider.value

    def play_next(self):
        """ Play the next track. """
        Logger.info("main.py: PlayingScreen.play_next")
        if self.sound:
            self.stop()
            self.sound = None
        self.ctrl.move_next()
        if self.ctrl.get_current_file():
            self.init_display()
            self.playpause()

    def play_previous(self):
        """ Ply the previous track. """
        if self.sound:
            self.stop()
            self.sound = None
        self.ctrl.move_previous()
        if self.ctrl.get_current_file():
            self.init_display()
            self.playpause()

    def stop(self):
        """ Stop any playing audio """
        self.advance = False
        if self.sound:
            self.sound.stop()
            self.but_playpause.source = "images/play.png"
            self.sound = None

    def save(self):
        """ Save the current playlist state """
        self.ctrl.save()

    def set_volume(self):
        """ Set the volume of the currently playing track if there is one. """
        if self.sound:
            self.sound.volume = self.volume_slider.value

    def show_playlist(self):
        """ Switch to the playlist screen """
        if "playlist" not in self.sm.screen_names:
            self.sm.add_widget(PlayListScreen(self.sm,
                                              self.ctrl.playlist,
                                              name="playlist"))
        self.sm.current = "playlist"

    def show_filebrowser(self):
        """ Switch to the playlist screen """
        if "filebrowser" not in self.sm.screen_names:
            self.sm.add_widget(ZenFileBrowser(self.sm,
                                              self.ctrl.playlist,
                                              name="filebrowser"))
        self.sm.current = "filebrowser"

    def _on_sound_stop(self, *args):
        Logger.info("main.py: sound has stopped. args=" + str(args))
        self.sound = None
        if self.advance:
            self.ctrl.move_next()
            self.init_display()
            self.playpause()

    def _update_progress(self, dt):
        """ Update the progressbar  """
        if self.sound:
            length = self.sound._get_length()
            if length > 0:
                pos = self.sound.get_pos()
                self.progress_slider.value = pos / length

                self.time_label.text = "{0}m {1:02d}s / {2}m {3:02d}s".format(
                    int(pos / 60),
                    int(pos % 60),
                    int(length / 60),
                    int(length % 60))
