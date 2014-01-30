from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.core.window import Window
from kivy.uix.vkeyboard import VKeyboard
from kivy.logger import Logger
from kivy.properties import ObjectProperty
from kivy.uix.button import Button
from functools import partial
from kivy.config import Config
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import Screen
from kivy import require

# This example uses features introduced in Kivy 1.8.0
#require("1.8.0")

Builder.load_string(
'''
<KeyboardScreen>:
    displayLabel: displayLabel
    kbContainer: kbContainer
    BoxLayout:
        orientation: 'vertical'
        Label:
            size_hint_y: 0.15
            text: "Available Keyboard Layouts"
        BoxLayout:
            id: kbContainer
            size_hint_y: 0.2
            orientation: "horizontal"
            padding: 10

        Label:
            id: displayLabel
            size_hint_y: 0.15
            markup: True
            text: "[b]Key pressed[/b] - None"
            halign: "center"

        Widget:
            # Just a space taker to allow for the popup keyboard
            size_hint_y: 0.5

''')


class ModeTest(Popup):
    """
    Present the option to change keyboard mode and warn of system-wide
    consequences.
    """
    def __init__(self, **kwargs):
        super(ModeTest, self).__init__(
            title="Keyboard mode",
            content=Button(text="Test"),
            size_hint=(0.8, 0.8),
            size=(500, 400),
            auto_dismiss=False)


        #TODO: Remove or document?
        Logger.info("main.py: keyboard_mode=" +
                    Config.get("kivy", "keyboard_mode"))
        Config.set("kivy", "keyboard_mode", "")
        Config.write()
        Logger.info("main.py: 2. keyboard_mode=" +
                    Config.get("kivy", "keyboard_mode"))
        #TODO: Remove or document?

    pass


class KeyboardScreen(Screen):
    displayLabel = ObjectProperty()
    kbContainer = ObjectProperty()

    def __init__(self, **kwargs):
        super(KeyboardScreen, self).__init__(**kwargs)
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
        layouts = VKeyboard().available_layouts.keys()
        layouts.append("numeric.json")  # Add the file in our app directory
        for key in layouts:
            # Add a button for each layout
            self.kbContainer.add_widget(
                Button(
                    text=key,
                    on_release=partial(self.set_layout, key)))

    def set_layout(self, layout, button):
        """
        Change the keyboard layout to the one specified by *layout*.
        """
        #TODO: Remove - These properties now seem to be required?
        #self.password = ""
        #self.keyboard_suggestions = None
        #TODO: Remove

        kb = Window.request_keyboard(
            self._keyboard_close, self)
        if kb.widget:
            # If the current configuration supports Virtual Keyboards, this
            # widget will be a kivy.uix.vkeyboard.VKeyboard instance.
            self._keyboard = kb.widget
            self._keyboard.layout = layout
        else:
            self._keyboard = kb

        self._keyboard.bind(on_key_down=self.key_down,
                            on_key_up=self.key_up)

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

    def key_up(self, keyboard, keycode, text, modifiers):
        """
        The callback function that catches keyboard events.
        """
        self.displayLabel.text += ", up {0}".format(text)


class KeyboardDemo(App):
    def build(self):
        return KeyboardScreen()

if __name__ == "__main__":
    KeyboardDemo().run()
