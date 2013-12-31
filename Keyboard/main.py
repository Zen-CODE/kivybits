from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.core.window import Window
from kivy.uix.vkeyboard import VKeyboard
from kivy.logger import Logger
from kivy.properties import ObjectProperty
from kivy.uix.button import Button
from functools import partial

# In your config.ini, in the "kivy" section, add "keyboard_mode = dock"
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

    # ==========================================================================
    # Note: This method is made redundant in 1.8 as the json file can be loaded
    # from the application folder
    # ==========================================================================
    #from kivy import kivy_data_dir
    #import os
    #import shutil
    #def _add_numeric(self):
    #    '''Ensure that a copy of the keyboard file exists in the correct place
    #    '''
    #    keyboard_file = kivy_data_dir + "/keyboards/numeric.json"
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
            # Add a button for each layout
            button = Button(
                text=key,
                on_release=partial(self.set_layout, key))
            self.kbContainer.add_widget(button)

    def set_layout(self, layout, button):
        # Window.release_all_keyboards()
        print "set_layout ", layout
        return

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
