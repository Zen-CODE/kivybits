from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.core.window import Window
from kivy.uix.vkeyboard import VKeyboard
from kivy.logger import Logger
from kivy import kivy_data_dir
import os
import shutil
from kivy.properties import ObjectProperty
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.factory import Factory


# In your confixg.ini, in the "kivy" section, add "keyboard_mode = dock"
Builder.load_string(
'''
<KeyboardTest>:
    displayLabel: displayLabel
    kbContainer: kbContainer

    orientation: 'vertical'
    Label:
        size_hint_y: 0.25
        text: "Available Keyboard Layouts"
    BoxLayout:
        id: kbContainer
        size_hint_y: 0.25
        orientation: "horizontal"
        padding: 10

    Label:
        id: displayLabel
        size_hint_y: 0.5
        markup: True
        text: "[b]Key pressed[/b] - None"
        halign: "center"
''')


class KeyboardTest(BoxLayout):
    displayLabel = ObjectProperty()
    kbContainer = ObjectProperty()

    def __init__(self, **kwargs):
        super(KeyboardTest, self).__init__(**kwargs)
        #self._add_numeric()
        self._add_keyboards()

    def _add_info(self, text):
        '''Add the supplied text to the display label'''
        self.displayLabel.text += "\n" + text

    # ==========================================================================
    # Note: This method is made redundant in 1.8 as the json file can be loaded
    # from the application folder
    #def _add_numeric(self):
    #    '''Ensure that a copy of the keyboard file exists in the correct place
    #    '''
    #    keyboard_file = kivy_data_dir + "/keyboards/numeric.json"
    #    self._add_info("keyboard directory = " + kivy_data_dir + "/keyboards")
    #    if not os.path.exists(keyboard_file):
    #        shutil.copy("./numeric.json", keyboard_file)
    #        self._add_info("Copied ./numeric.json to this folder.")
    #    else:
    #        self._add_info("numeric.json already copied here.")
    # ==========================================================================

    def _add_keyboards(self):
        '''Add textboxes and labels for each available keyboard layout
        '''
        vk = VKeyboard()
        for key in vk.available_layouts.keys():
            # Add a boxlayout and label for each layout
            bl = BoxLayout(orientation="vertical")
            ti = TextInput()
            ti.bind(on_focus=self.on_text_focus)

            bl.add_widget(Label(text=key))
            bl.add_widget(ti)
            self.kbContainer.add_widget(bl)

    def on_text_focus(self, instance, value, *largs):
        # Window.release_all_keyboards()
        print "hello"
        vk = VKeyboard()
        for key in vk.available_layouts.keys():
            print "Layout ", key, "=", vk.available_layouts[key]

        if value:
            Logger.info('main.py: on_focus_numeric')
            numericVK = VKeyboard(layout="numeric")
            # numericVK = VKeyboard(layout="azerty")
            # numericVK = VKeyboard()
            # numericVK.layout = "azerty"
            Window.set_vkeyboard_class(numericVK)

        else:
            Logger.info('main.py: lost on_focus_numeric')
            Window.set_vkeyboard_class(VKeyboard)

        return True


class test(App):
    def build(self):
        return KeyboardTest()

if __name__ == "__main__":
    test().run()
