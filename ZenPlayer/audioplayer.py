import gobject
gobject.threads_init()
import pygst
pygst.require('0.10')
import gst
import gst.interfaces
from kivy.event import EventDispatcher
from kivy.properties import OptionProperty


class SoundLoader():
    """
    And 'kivy.core.audio.SoundPlayer' compatible class with mp3 audio format
    support.
    """
    _player = None

    @staticmethod
    def load(filename):
        """
        Load and start playing the audiofile specified.
        """
        if not SoundLoader._player:
            SoundLoader._player = _AudioPlayer(filename)
        return SoundLoader._player


class _AudioPlayer(EventDispatcher):
    """
    This class mimics the functionality of the 'kivy.core.audio.Sound' class
    but uses an alternative implementation to support mp3 on linux and android.
    """

    state = OptionProperty('stop', options=('stop', 'play'))
    '''State of the sound, one of 'stop' or 'play'.

    :attr:`state` is a read-only :class:`~kivy.properties.OptionProperty`.'''

    def __init__(self, filename, **kwargs):
        super(_AudioPlayer, self).__init__(**kwargs)
        self.player = gst.element_factory_make("playbin2", "player")
        # This was in the original code, but seems unnecessary?
        #ssfakesink = gst.element_factory_make("fakesink", "fakesink")
        self.bus = self.player.get_bus()
        self.bus.set_sync_handler(self._on_message)
        self.filename = filename

    def _on_message(self, bus, message):
        """ Callback for the self.bus.set_sync_handler message handler """
        t = message.type
        if t == gst.MESSAGE_EOS:
            self.player.set_state(gst.STATE_NULL)
            self.state = 'stop'
        elif t == gst.MESSAGE_ERROR:
            self.player.set_state(gst.STATE_NULL)
            err, debug = message.parse_error()
            print "Player Error: %s" % err, debug
        return gst.BUS_PASS

    def play(self):
        self.player.set_property('uri', "file://{0}".format(self.filename))
        self.player.set_state(gst.STATE_PLAYING)
        self.state = 'play'

