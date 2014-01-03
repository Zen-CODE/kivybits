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
        #self._add_numeric()  # Please see below
        self._add_keyboards()
        self._keyboard = None

    # =========================================================================
    # Note: This method is made redundant in Kivy 1.8 as the json file can be
    # loaded from the application folder
    # =========================================================================
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
        """
        Add a buttons for each available keyboard layout. When clicked,
        the buttons will change the keyboard layout to the one selected.
        """
        vk = VKeyboard()
        for key in vk.available_layouts.keys():
            # Add a button for each layout
            self.kbContainer.add_widget(
                Button(
                    text=key,
                    on_release=partial(self.set_layout, key)))

    def set_layout(self, layout, button):
        """
        Change the keyboard layout to the one specified by *layout*.
        """
        # Window.release_all_keyboards()
        kb = Window.request_keyboard(
            self._keyboard_close, self)
        if kb.widget:
            Logger.info("main.py: Using keyboard.widget = " + str(kb.widget))
            self._keyboard = kb.widget
        else:
            Logger.info("main.py: keyboard.widget is None, "
                        "falling back to keyboard = " + str(kb))
            self._keyboard = kb

        # TODO: Remove - For debugging
        Logger.info("main.py: dir(kb)=" + str(dir(kb)))
        # TODO: Remove /
        if kb:
            kb.layout = layout
            kb.bind(on_key_down=self.key_down)
            self._keyboard = kb
        else:
            Logger.info("main.py: No keyboard found...")

    def _keyboard_close(self, *args):
        """ The active keyboard is being closed. """
        Logger.info("main.py: Keyboard is being closed.")
        if self._keyboard:
            self._keyboard.unbind(on_key_down=self.key_down)
            self._keyboard = None

    def key_down(self, keyboard, keycode, text, modifiers):
        """
        The callback function that catches keyboard events.
        """
        self.displayLabel.text = "Key pressed - {0}".format(text)


class KeyboardDemo(App):
    def build(self):
        return KeyboardTest()

if __name__ == "__main__":
    KeyboardDemo().run()
