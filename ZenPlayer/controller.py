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


class Controller(object):
    """
    Controls the playing of audio and coordinates the updating of the playlist
    and screen displays
    """
    volume = 100
    advance = True  # This flag indicates whether to advance to the next track
                    # once the currently playing one had ended
    sm = None  # THe ScreenManager
    state = ""

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
        self.playing.on_state()
        self.sm.add_widget(self.playing)
        self.sm.current = "main"

    def _on_sound_stop(self, *args):
        Logger.info("main.py: sound has stopped. args=" + str(args))
        if self.advance:
            self.move_next()
            self.play_pause()
            self.playing.on_state()

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
        if not Sound.state:
            audiof = self.get_current_file()
            if audiof:
                Logger.info("main.py: playing " + audiof)
                Sound.play(audiof, self._on_sound_stop)
                self.playing.on_state()
                Sound.set_volume(self.volume)
                #self.but_playpause.source = "images/pause.png"
        elif Sound.state == "playing":
            Sound.stop()
            #self.but_playpause.source = "images/play.png"
        else:
            Sound.play()
            #self.but_playpause.source = "images/pause.png"
            Sound.set_volume(self.volume)

    def play_next(self):
        """ Play the next track in the playlist. """
        Logger.info("main.py: PlayingScreen.play_next")
        self.move_next()
        audiofile = self.get_current_file()
        if audiofile:
            Sound.play(audiofile)
            Sound.set_volume(self.volume)
            self.playing.on_state()

    def play_previous(self):
        """ Play the previous track in the playlist. """
        self.move_previous()
        audiofile = self.get_current_file()
        if audiofile:
            Sound.play(audiofile)
            Sound.set_volume(self.volume)
            self.playing.on_state()


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
        #self.but_playpause.source = "images/play.png"


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
