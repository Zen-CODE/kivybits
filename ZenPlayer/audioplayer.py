import gobject
gobject.threads_init()
import pygst
pygst.require('0.10')
import gst
import gst.interfaces
from kivy.core.audio import Sound


class SoundLoader():
    """
    And 'kivy.core.audio.SoundPlayer' compatible class with mp3 audio format
    support.
    """
    _player = None

    @staticmethod
    def load(filename):
        """
        Load and start playing the specified *filename*.
        """
        if not SoundLoader._player:
            SoundLoader._player = _AudioPlayer(filename)
        return SoundLoader._player


class _AudioPlayer(Sound):
    """
    This class mimics the functionality of the 'kivy.core.audio.Sound' class
    but uses an alternative implementation to support mp3 on linux and android.

    Please see from kivy.core.audio.Sound class for details
    """
    def __init__(self, filename, **kwargs):
        super(_AudioPlayer, self).__init__(**kwargs)
        self.player = gst.element_factory_make("playbin2", "player")
        # This was in the original code, but seems unnecessary?
        ssfakesink = gst.element_factory_make("fakesink", "fakesink")
        self.bus = self.player.get_bus()
        self.bus.set_sync_handler(self._on_message)
        self.source = filename
        print "playbin has", dir(self.player)

    def _on_message(self, bus, message):
        """ Callback for the self.bus.set_sync_handler message handler """
        t = message.type.numerator
        print "t=", str(t)
        print "state=", self.state

        #t = message.type
        #print "t=", str(t)
        # t= <flags GST_MESSAGE_EOS of type GstMessageType>
        if t == gst.MESSAGE_EOS:  # MESSAGE_EOS = 1
            print 'stopping'
            #self.player.set_state(gst.STATE_NULL)
            #self.state = 'stop'
            self.stop()
            #from kivy.clock import Clock
            #Clock.schedule_once(lambda dt: self.stop(), 1)
        elif t == gst.MESSAGE_ERROR:
            print 'error'
            self.player.set_state(gst.STATE_NULL)
            err, debug = message.parse_error()
            print "Player Error: %s" % err, debug
        else:
            print 'niether'
        return gst.BUS_PASS

    def play(self):
        self.player.set_property('uri', "file://{0}".format(self.source))
        self.player.set_state(gst.STATE_PLAYING)
        self.state = 'play'

    def stop(self):
        """ Stop any currently playing audio"""
        self.player.set_state(gst.STATE_NULL)
        self.state = 'stop'

    def on_state(self, widget, value):
        """ Respond to a change of state """
        print "on_state=", value

    def on_volume(self, widget, value):
        """ Respond to a change of volume """
        self.player.set_property("volume", value)
