import gobject
from kivy.core.audio.audio_pygst import SoundPyGst


class SoundLoader():
    """
    Supplies the Gst Sound class capable of playing Mp3 files.
    """

    @staticmethod
    def load(filename):
        """
        Load and start playing the specified *filename*.
        """
        return SoundPyGst(source=filename)

