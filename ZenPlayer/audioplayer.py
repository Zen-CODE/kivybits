import gobject
#gobject.threads_init()
#import pygst
#pygst.require('0.10')
from kivy.core.audio.audio_pygst import SoundPyGst

class SoundLoader():
    """
    And 'kivy.core.audio.SoundPlayer' compatible class with mp3 audio format
    support.
    """

    @staticmethod
    def load(filename):
        """
        Load and start playing the specified *filename*.
        """
        return SoundPyGst(source=filename)
