__author__ = "Richard Larkin aka. ZenCODE"
# http://kivy.org/planet/2014/01/
#   building-a-background-application-on-android-with-kivy/

from time import sleep
from kivy.lib import osc


class OSCServer(object):
    """
    Handles messages received of OSC.
    """
    server_port = 3000
    client_port = 3001

    def __init__(self):
        """ Create a listener and start managing comms. """
        osc.init()
        self.osc_id = osc.listen(ipAddr='127.0.0.1', port=OSCServer.server_port)
        osc.bind(self.osc_id, self.kivy_server, 'kivy_server')

    @staticmethod
    def kivy_server(message, *args):
        """
        Handle SoundLoader messages. Message is a list of:
            [<api_name>, ',s')] + [<function>, <args>, <kwargs>]

        Note: args and kwargs are string literals, but this is not yet
        implemented.
        """
        print("kivy_server : got a message {0}".format(message))
        osc.sendMsg('kivy_client', ['p1', 'p2', 'p3'],
                    port=OSCServer.client_port)

    def wait(self):
        """ Start the loop where we wait for messages. """
        while True:
            osc.readQueue(self.osc_id)
            sleep(.1)

if __name__ == '__main__':
    OSCServer().wait()
