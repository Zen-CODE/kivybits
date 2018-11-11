from kivy.app import App
from kivy.lang.builder import Builder
from textwrap import dedent

class Constants:
    """ A class holding declarations of constants. """
    kv = dedent('''
        BoxLayout:
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


class ServiceExample(App):
    def build(self):
        box = Builder.load_string(Constants.kv)
        box.ids.label.text = Constants.info_text
        return box

ServiceExample().run()

