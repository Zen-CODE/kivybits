__author__ = "Richard Larkin aka. ZenCODE"
# http://kivy.org/planet/2014/01/
#   building-a-background-application-on-android-with-kivy/

from time import sleep
from kivy.lib import osc


class OSCListener(object):
    """
    Handles messages received of OSC.
    """
    server_port = 3000
    client_port = 3001

    def __init__(self):
        """ Create a listener and start managing comms. """
        osc.init()
        osc_id = osc.listen(ipAddr='127.0.0.1', port=OSCListener.server_port)
        osc.bind(osc_id, self.sound_loader, 'sound_loader')
        self.osc_id = osc_id

    def sound_loader(self, message, *args):
        """
        Handle SoundLoader messages. Message is a list of:
            [<api_name>, ',s')] + [<args passed in the call>]

        """
        print("Server: got a message! %s" % message)
        # self.osc.sendMsg('sound_loader', ['p1', 'p2', 'p3'],
        #                 port=OSCListener.server_port)

    def wait(self):
        """ Start the loop where we wait for messages. """
        while True:
            osc.readQueue(self.osc_id)
            sleep(.1)

if __name__ == '__main__':
    OSCListener().wait()
