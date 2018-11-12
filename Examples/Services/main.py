from os import path
from kivy.app import App
from kivy.lang.builder import Builder
from textwrap import dedent
from kivy.uix.boxlayout import BoxLayout
from kivy.logger import Logger
from kivy.utils import platform

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

class OS(object):
    """ A convenience class for handling OS specific sunctionality."""
    def get_user_path():
        """
        Return a path that is writable by the current process and can
        be used to store app data.
        """

        if platform == "android":
            from jnius import autoclass, cast
            PythonActivity = autoclass('org.kivy.android.PythonActivity')
            Environment = autoclass('android.os.Environment')
            context = cast('android.content.Context', PythonActivity.mActivity)
            ret = context.getExternalFilesDir(
                Environment.getDataDirectory().getAbsolutePath()
            ).getAbsolutePath()
        else:
            root = path.expanduser("~")
            if platform == "ios":
                # iOS does not seems to allow for sub-folder creation?
                # Documents seems to the the place to put it
                # https://groups.google.com/forum/#!topic/kivy-users/sQXAOecthmE
                ret = path.join(root, "Documents")
            else:
                ret = path.join(root, ".KivyServices")
        return ret



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
        service = autoclass("speedtest.maths.camiweb.com.ServiceCamiapps")
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

