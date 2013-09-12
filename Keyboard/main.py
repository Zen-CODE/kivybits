from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.core.window import Window
from kivy.uix.vkeyboard import VKeyboard
from kivy.logger import Logger
import kivy
import os
import shutil
from kivy.uix.textinput import TextInput

Builder.load_string(
'''
<KeyboardTest>:
    orientation: 'vertical'
    Label:
        size_hint_y: 0.25
        text: "I'm glad to see you Dave."
    BoxLayout:
        size_hint_y: 0.25
        orientation: "horizontal"
        TextInput:
            id: numericInput
            on_focus: root.on_focus_numeric(*args)
        TextInput:
            id: normalInputs
    Widget:
        size_hint_y: 0.5
''')

# In your confixg.ini, in the "kivy" section, add "keyboard_mode = dock"


class KeyboardTest(BoxLayout):
    def __init__(self, **kwargs):
        super(KeyboardTest, self).__init__(**kwargs)
        self._check_keyboard_exists()

    def _check_keyboard_exists(self):
        '''Ensure that a copy of the keyboard file exists in the correct place
        '''
        keyboard_file = kivy.kivy_data_dir + "/keyboards/numeric.json"
        if not os.path.exists(keyboard_file):
            # You will need to place your json file in the same folder
            shutil.copy("./numeric.json", keyboard_file)
            Logger.info("main.py: copying ./numeric.json to " + keyboard_file)

    def on_focus_numeric(self, instance, value, *largs):
        # Window.release_all_keyboards()
        # Window.keyboards = {}
        # for kb in Window.keyboards.keys():
         #   Logger.info("main.py: keyboard installed = " + kb)

        if value:
            print 'on_focus_numeric'
            numericVK = VKeyboard(layout="numeric")
            # numericVK = VKeyboard(layout="azerty")
            # numericVK = VKeyboard()
            # numericVK.layout = "azerty"
            # Window.set_vkeyboard_class(numericVK)

        else:
            print 'not on_focus_numeric'
            Window.set_vkeyboard_class(VKeyboard)

        # return instance.on_focus(instance, value, *largs)
        # return super(TextInput, instance).on_focus(value, *largs)
        return True
        # return instance.on_focus.dispatch()


class test(App):
    def build(self):
        return KeyboardTest()

if __name__ == "__main__":
    test().run()
