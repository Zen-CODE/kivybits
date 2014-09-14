import gobject
from kivy.core.audio.audio_pygst import SoundPyGst
from kivy.logger import Logger


class SoundLoader(object):
    """
    Supplies the Gst Sound class capable of playing Mp3 files.
    """

    @staticmethod
    def load(filename):
        """
        Load and start playing the specified *filename*.
        """
        return SoundPyGst(source=filename)


class Sound(object):
    """
    This class manages the playing audio as a Singleton
    """
    state = ""  # options= "", "stopped" or "playing", "finished"
    _state_callbacks = []
    _sound = None  # The underlying Sound instance

    @staticmethod
    def _on_stop(*args):
        Logger.info("main.py: sound has stopped. state=" + str(Sound.state))
        if Sound.state != "stopped":
            Sound._set_state("finished")

    @staticmethod
    def _set_state(state):
        """ Set the state value and fire all attached callbacks """
        if state != Sound.state:
            Sound.state = state
            for func in Sound._state_callbacks:
                func(state)

    @staticmethod
    def add_state_callback(callback):
        """ Add a callback to be fired when the state changes """
        Sound._state_callbacks.append(callback)

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
            Sound._set_state("stopped")
            Sound._sound.stop()

    @staticmethod
    def play(filename="", volume=100):
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
            Sound._sound.volume = volume
            Sound._set_state("playing")
        else:
            Sound._set_state("")

    @staticmethod
    def set_volume(value):
        """
        The the volume of the currently playing sound if appropriate
        """
        if Sound._sound:
            Sound._sound.volume = value
