from kivy.app import App
from kivy.lang import Builder
from kivy.lib import osc
from kivy.clock import Clock
from server import OSCServer


kv = '''
Button:
    text: 'push me!'
    on_press: app.ping()
'''


class OSCClient(object):
    """ Handles the client side of comms with the OSCServer class. """
    def __init__(self):
        super(OSCClient, self).__init__()
        osc.init()
        osc_id = osc.listen(ipAddr='127.0.0.1', port=OSCServer.client_port)
        osc.bind(osc_id, OSCClient.kivy_client, 'kivy_client')
        Clock.schedule_interval(lambda *x: osc.readQueue(osc_id), 0)

    @staticmethod
    def kivy_client(message, * args):
       print("Client: got a message! %s" % message)

    @staticmethod
    def send_message(args, kwargs):
        osc.sendMsg('kivy_server', [args, kwargs],
                    port=OSCServer.server_port)


class ServiceApp(App):
    def build(self):
        # if platform == 'android':
        #     from android import AndroidService
        #     service = AndroidService('my pong service', 'running')
        #     service.start('service started')
        #     self.service = service
        OSCClient()
        return Builder.load_string(kv)

    def ping(self):
        OSCClient.send_message('args1', 'kwargs1')


if __name__ == '__main__':
    ServiceApp().run()