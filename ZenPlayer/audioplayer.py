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
