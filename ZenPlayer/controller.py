from playlist import PlayList, PlayListScreen
from filebrowser import ZenFileBrowser
from kivy.storage.jsonstore import JsonStore
from kivy.uix.screenmanager import ScreenManager
from playing import PlayingScreen
from audioplayer import Sound
from kivy.core.window import Window
from kivy.properties import NumericProperty
from kivy.event import EventDispatcher
from kivy.utils import platform
from kivy.clock import Clock


class Controller(EventDispatcher):
    """
    Controls the playing of audio and coordinates the updating of the playlist
    and screen displays
    """
    volume = NumericProperty(1.0)
    advance = True  # This flag indicates whether to advance to the next track
                    # once the currently playing one had ended
    sm = None  # THe ScreenManager
    pos = 0

    def __init__(self, **kwargs):
        """ Initialize the screens and the screen manager """
        self._store = JsonStore("zenplayer.json")
        self.playlist = PlayList(self._store)

        self.sm = ScreenManager()
        self.playing = PlayingScreen(self, name="main")
        self.sm.add_widget(self.playing)
        self.sm.current = "main"

        if platform not in ['ios', 'android']:
            self.kb_listener = ZenKeyboardListener(self)
        Sound.add_state_callback(self.playing.on_sound_state)
        Sound.add_state_callback(self._on_sound_state)

        super(Controller, self).__init__(**kwargs)
        if self._store.exists('state'):
            state = self._store.get("state")
            if "volume" in state.keys():
                self.volume = state["volume"]

    def _on_sound_state(self, state):
        """ The sound state has changed. If the track played to the end,
        move to the next track."""
        if state == "finished" and self.advance:
            self.play_next()

    def get_current_art(self):
        return self.playlist.get_current_art()

    def get_current_info(self):
        return self.playlist.get_current_info()

    def get_current_file(self):
        return self.playlist.get_current_file()

    @staticmethod
    def get_pos_length():
        return Sound.get_pos_length()

    def on_key_down(self, keyboard, keycode, text, modifiers):
        """ React to the keypress event """
        key_name = keycode[1]
        if key_name == "up":
            self.volume += 0.05
        elif key_name == "down":
            self.volume -= 0.05
        elif key_name == "x":
            self.play_pause()
        elif key_name == "z":
            self.move_previous()
        elif key_name == "v":
            self.stop()
        elif key_name == "b":
            self.play_next()

        return True

    def on_volume(self, widget, value):
        """ Set the volume of the currently playing sound """
        if 0.0 > value:
            self.volume = 0.0
        elif value > 1.0:
            self.volume = 1.0
        else:
            Sound.set_volume(value)
            self.playing.volume_slider.value = value

    def play_pause(self):
        """ Play or pause the currently playing track """
        self.advance = True
        if Sound.state == "playing":
            self.pos, x = Sound.get_pos_length()
            Sound.stop()
        else:
            audio_file = self.get_current_file()
            if audio_file:
                Sound.play(audio_file, self.volume)
                if self.pos > 0:
                    Clock.schedule_once(lambda dt: Sound.seek(self.pos), 0.1)

    def play_next(self):
        """ Play the next track in the playlist. """
        Sound.stop()
        self.playlist.move_next()
        self.play_pause()

    def play_previous(self):
        """ Play the previous track in the playlist. """
        Sound.stop()
        self.playlist.move_previous()
        self.play_pause()

    def save(self):
        """ Save the state of the the playlist and volume. """
        self.playlist.save(self._store)
        self._store.put("state", volume=self.volume)
        if "filebrowser" in self.sm.screen_names:
            self.sm.get_screen("filebrowser").save(self._store)

    def show_filebrowser(self):
        """ Switch to the file browser screen """
        if "filebrowser" not in self.sm.screen_names:
            self.sm.add_widget(ZenFileBrowser(self,
                                              self.playlist,
                                              self._store,
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


class ZenKeyboardListener(EventDispatcher):
    """
    This class handles the management of keypress to control volume, play,
    stop, next etc.
    """
    def __init__(self, ctrl, **kwargs):
        super(ZenKeyboardListener, self).__init__(**kwargs)
        self._keyboard = Window.request_keyboard(
            self._keyboard_closed, self, 'text')
        self._keyboard.bind(on_key_down=ctrl.on_key_down)

    def _keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard = None
