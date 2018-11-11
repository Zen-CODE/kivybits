from kivy.app import App
from kivy.lang.builder import Builder
from textwrap import dedent
from kivy.uix.boxlayout import BoxLayout

kv = dedent('''
        <ServiceUI>:
            orientation: "vertical"
            padding: [20, 10, 20, 10]
            Label:
                id: label
                markup: True
                halign: "center"
            Button:
                text: "Start service 1"
            Button:
                text: "Start service 2"

    ''')

info_text = '''[b]Service Example[/b]\n\n'''\
    '''In Kivy, Android services are separate, independant processes.'''\
    '''differs from typical Android services.'''

class ServiceUI(BoxLayout):
    def __init__(self, **kwargs):
        super(ServiceUI, self).__init__(**kwargs)
        self.ids.label.text = info_text


class ServiceExample(App):
    def build(self):
        Builder.load_string(kv)
        return ServiceUI()

ServiceExample().run()

