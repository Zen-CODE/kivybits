from playlist import PlayList, PlayListScreen
from filebrowser import ZenFileBrowser
from kivy.utils import platform
if platform == 'linux':  # Enable Mp3
    from audioplayer import SoundLoader
else:
    from kivy.core.audio import SoundLoader
from kivy.logger import Logger
from kivy.storage.jsonstore import JsonStore
from kivy.uix.screenmanager import ScreenManager
from playing import PlayingScreen
from audioplayer import Sound
from kivy.clock import Clock


class Controller(object):
    """
    Controls the playing of audio and coordinates the updating of the playlist
    and screen displays
    """
    volume = 100
    advance = True  # This flag indicates whether to advance to the next track
                    # once the currently playing one had ended
    sm = None  # THe ScreenManager

    def __init__(self):
        """ Initialize the screens and the screen manager """
        self.playlist = PlayList()
        self._store = JsonStore("zenplayer.json")
        self.playlist.load(self._store)
        if self._store.exists('state'):
            state = self._store.get("state")
            if "volume" in state.keys():
                self.volume = state["volume"]

        self.sm = ScreenManager()
        self.playing = PlayingScreen(self, name="main")
        self.playing.init_display()
        self.sm.add_widget(self.playing)
        self.sm.current = "main"

        Sound.add_state_callback(self.playing.on_sound_state)
        Sound.add_state_callback(self._on_sound_state)

    def _on_sound_state(self, state):
        print "_on_sound_state fired - " + state
        if state == "stopped" and self.advance:
            Clock.schedule_once(lambda dt: self.play_next())

    def get_current_art(self):
        return self.playlist.get_current_art()

    def get_current_info(self):
        return self.playlist.get_current_info()

    def get_current_file(self):
        return self.playlist.get_current_file()

    @staticmethod
    def get_pos_length():
        return Sound.get_pos_length()

    def play_pause(self):
        self.advance = True
        if Sound.state == "":
            audio_file = self.get_current_file()
            if audio_file:
                Sound.play(audio_file, self.volume)
        elif Sound.state == "playing":
            Sound.stop()
        else:
            Sound.play(volume=self.volume)

    def play_next(self):
        """ Play the next track in the playlist. """
        Logger.info("main.py: PlayingScreen.play_next")
        self.move_next()
        audio_file = self.get_current_file()
        if audio_file:
            Sound.play(audio_file, self.volume)

    def play_previous(self):
        """ Play the previous track in the playlist. """
        self.move_previous()
        audio_file = self.get_current_file()
        if audio_file:
            Sound.play(audio_file, self.volume)

    def move_next(self):
        """ Play the next track in the playlist. """
        self.playlist.move_next()

    def move_previous(self):
        """" Move the current playlist item back one. """
        self.playlist.move_previous()

    def save(self):
        """ Save the state of the the playlist and volume. """
        self.playlist.save(self._store)
        self._store.put("state", volume=self.volume)

    def set_volume(self, value):
        """ Set the volume of the currently playing track if there is one. """
        self.volume = value
        Sound.set_volume(self.volume)

    def show_filebrowser(self):
        """ Switch to the file browser screen """
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
