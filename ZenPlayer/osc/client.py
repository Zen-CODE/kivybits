from kivy.app import App
from kivy.lang import Builder
from kivy.lib import osc
from kivy.clock import Clock
from server import OSCListener

activityport = 3001


def some_api_callback(message, *args):
   print("Client: got a message! %s" % message)

kv = '''
Button:
    text: 'push me!'
    on_press: app.ping()
'''


class ServiceApp(App):
    def build(self):
        # if platform == 'android':
        #     from android import AndroidService
        #     service = AndroidService('my pong service', 'running')
        #     service.start('service started')
        #     self.service = service

        osc.init()
        oscid = osc.listen(ipAddr='127.0.0.1', port=activityport)
        osc.bind(oscid, some_api_callback, 'sound_loader')
        Clock.schedule_interval(lambda *x: osc.readQueue(oscid), 0)

        return Builder.load_string(kv)

    def ping(self):
        #osc.sendMsg('/some_api', ['ping', ], port=someotherport)
        osc.sendMsg('sound_loader', ['p1', 'p2', 'p3'], port=OSCListener.port)


if __name__ == '__main__':
    ServiceApp().run()