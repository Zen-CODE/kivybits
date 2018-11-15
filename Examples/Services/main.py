from kivy.app import App
from kivy.lang.builder import Builder
from textwrap import dedent
from kivy.uix.boxlayout import BoxLayout
from kivy.logger import Logger


kv = dedent('''
        <ServiceUI>:
            orientation: "vertical"
            padding: [20, 10, 20, 10]
            Label:
                id: label
                markup: True
                halign: "center"
            Button:
                id: btn1
                text: "Start service 1"
                on_press: root.toggle_service(1)
            Button:
                id: btn2
                text: "Start service 2"
                on_press: root.toggle_service(2)

    ''')


class ServiceUI(BoxLayout):


    def __init__(self, **kwargs):
        super(ServiceUI, self).__init__(**kwargs)
        self.ids.label.text = "[b]Service Example[/b]\n\n"\
            "In Kivy, Android services are separate, independant processes."\
            "differs from typical Android services."

    def toggle_service(self, number):
        """ Start/Stop the specified server """
        # print("Start/stop service {0}".format(number))
        # # For "android_new", now just "android" toolchain

    def _android_service(self):
        """ Toggle the android service on and off """

        from jnius import autoclass
        service = autoclass("service.demo.zencode.kivy.org.ServiceServicedemo")
        mActivity = autoclass(
            'org.kivy.android.PythonActivity').mActivity
            
        param = '{"user_path": "' + OS.get_user_path() + '"}'
        Logger.info("main.py: service param = {0}".format(param))
        service.start(mActivity, param)        


class ServiceExample(App):
    def build(self):
        Builder.load_string(kv)
        return ServiceUI()

ServiceExample().run()

