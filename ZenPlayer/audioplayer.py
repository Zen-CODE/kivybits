import gobject
gobject.threads_init()
import pygst
pygst.require('0.10')
import gst
import gst.interfaces
from kivy.clock import Clock
from kivy.event import EventDispatcher

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
    def __init__(self, filename, **kwargs):
        super(_AudioPlayer, self).__init__(**kwargs)
        self.player = gst.element_factory_make("playbin2", "player")
        #ssfakesink = gst.element_factory_make("fakesink", "fakesink")
        self.bus = self.player.get_bus()
        self.bus.set_sync_handler(self.on_message)
        self.filename = filename

    def on_message(self, bus, message):
        t = message.type
        if t == gst.MESSAGE_EOS:
            self.player.set_state(gst.STATE_NULL)
            #TODO
            #Clock.schedule_once(self.Autoplay_Next)
        elif t == gst.MESSAGE_ERROR:
            self.player.set_state(gst.STATE_NULL)
            err, debug = message.parse_error()
            print "Player Error: %s" % err, debug
        return gst.BUS_PASS

    def play(self):
        self.player.set_property('uri', "file://{0}".format(self.filename))
        self.player.set_state(gst.STATE_PLAYING)

    def playing(self):
        #TODO
        return False


