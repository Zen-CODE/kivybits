__author__ = "Richard Larkin aka. ZenCODE"
# http://kivy.org/planet/2014/01/
#   building-a-background-application-on-android-with-kivy/

from time import sleep
from kivy.lib import osc


class OSCListener(object):
    """
    Handles messages received of OSC.
    """
    port = 3000

    @staticmethod
    def sound_loader(message, *args):
        """
        Handle SoundLoader messages. Message is a list of:
            [<api_name>, ',s')] + [<args passed in the call>]

        """
        print("Server: got a message! %s" % message)


if __name__ == '__main__':
    osc.init()
    osc_id = osc.listen(ipAddr='127.0.0.1', port=OSCListener.port)
    osc.bind(osc_id, OSCListener.sound_loader, 'sound_loader')

    while True:
        osc.readQueue(osc_id)
        sleep(.1)