from kivy.app import App
from kivy.lang.builder import Builder
from textwrap import dedent
from kivy.uix.boxlayout import BoxLayout
from kivy.logger import Logger
from kivy.properties import BooleanProperty
import zipfile
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from os.path  import exists


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
            text: "Open zip in service"
            on_press: root.start_service_one() 
        Button:
            id: btn2
            text: "Open zip"
            on_press: root.open_zip()

    ''')


class ServiceUI(BoxLayout):

    service_one = BooleanProperty(False)
    """ Indicates the running status of Serviceone"""

    def __init__(self, **kwargs):
        super(ServiceUI, self).__init__(**kwargs)
        self.ids.label.text = "[b]Service Example[/b]\n\n"\
            "The process can open the zip. The service cannot."

        # self.ids.label.text = "[b]Service Example[/b]\n\n"\
        #     "In Kivy, Android services are separate, independent processes."\
        #     " This differs from typical Android services."

    def open_zip(self):
        """ Open the zip file that cannot be opened by the service. """
        file_name = "service_one/main.zip"

        if not exists(file_name):
            Logger.info("main.py: Zip not found. Aborting...")
            return
        else:
            Logger.info("main.py: Zip found. About to open as binary.")

        my_zip = zipfile.ZipFile(file_name, "r")
        msg = "zip opened . contains {0}".format(my_zip.filelist[0].filename)
        # with open(file_name, 'rb') as f:
        #     text = str(f.read(10))
        # msg = "Text read = " + text

        Popup(title="Zip file",
              content=Label(text=msg),
              size_hint=(0.9, 0.5)).open()
        Logger.info("main.py: About to open zip file from service.")

    def start_service_one(self):
        """ Start the service """
        self._start_android_service("Serviceone")

    def _start_android_service(self, name):
        """ Toggle the android service on and off """
        srv_name = "service.demo.zencode.kivy.org.Service" + name
        Logger.info("main.py: Starting service {0}".format(srv_name))

        from jnius import autoclass
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
