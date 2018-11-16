from kivy.app import App
from kivy.lang.builder import Builder
from textwrap import dedent
from kivy.uix.boxlayout import BoxLayout
from kivy.logger import Logger
from kivy.properties import BooleanProperty


kv = dedent('''
    #: import Popup kivy.uix.popup.Popup
    #: import Label kivy.uix.label.Label
    <ServiceUI>:
        orientation: "vertical"
        padding: [20, 10, 20, 10]
        Label:
            id: label
            markup: True
            halign: "center"
        Button:
            id: btn1
            text: ("Start" if root.service_one else "Stop") + " service one"
            on_press: root.start_service_one() 
        Button:
            id: btn2
            text: ("Start" if root.service_two else "Stop") + " service two"
            on_press:
                Popup(title="Not implemented",
                content=Label(text="Not yet implemented"),
                size_hint=(0.5, 0.3)).open()

    ''')


class ServiceUI(BoxLayout):

    service_one = BooleanProperty(False)
    """ Indicates the running status of Serviceone"""

    service_two = BooleanProperty(False)
    """ Indicates the running status of Servicetwo"""

    def __init__(self, **kwargs):
        super(ServiceUI, self).__init__(**kwargs)
        self.ids.label.text = "[b]Service Example[/b]\n\n"\
            "In Kivy, Android services are separate, independent processes."\
            " This differs from typical Android services."

    def start_service_one(self):
        """ Start the service """
        self._start_android_service("Serviceone")

    def _start_android_service(self, name):
        """ Toggle the android service on and off """

        from jnius import autoclass
        srv_name = "service.demo.zencode.kivy.org.Service" + name
        Logger.info("main.py: Starting service {0}".format(srv_name))
        service = autoclass(srv_name)
        mActivity = autoclass(
            'org.kivy.android.PythonActivity').mActivity
        service.start(mActivity, "")

        # param = '{"user_path": "' + OS.get_user_path() + '"}'
        # Logger.info("main.py: service param = {0}".format(param))
        # service.start(mActivity, param)


class ServiceExample(App):
    def build(self):
        Builder.load_string(kv)
        return ServiceUI()


ServiceExample().run()
