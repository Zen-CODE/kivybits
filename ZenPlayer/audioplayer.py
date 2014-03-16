import gobject
gobject.threads_init()
import pygst
pygst.require('0.10')
import gst
import gst.interfaces
from kivy.clock import Clock


class AudioPlayer(object):
    def __init__(self, **kwargs):
        super(AudioPlayer, self).__init__(**kwargs)
        self.player = gst.element_factory_make("playbin2", "player")
        fakesink = gst.element_factory_make("fakesink", "fakesink")
        self.bus = self.player.get_bus()
        self.bus.set_sync_handler(self.on_message)

    def on_message(self, bus, message):
        t = message.type
        if t == gst.MESSAGE_EOS:
            self.player.set_state(gst.STATE_NULL)
            Clock.schedule_once(self.Autoplay_Next)
        elif t == gst.MESSAGE_ERROR:
            self.player.set_state(gst.STATE_NULL)
            err, debug = message.parse_error()
            print "Player Error: %s" % err, debug
        return gst.BUS_PASS

    def start(self, filename):
        self.player.set_property('uri', "file://{0}".format(filename))
        self.player.set_state(gst.STATE_PLAYING)

    def playing(self):
        #TODO
        return False


