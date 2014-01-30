from kivy.app import App
from kivy.lang import Builder
from kivy.properties import ObjectProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.core.window import Window
from kivy.uix.vkeyboard import VKeyboard
from kivy.logger import Logger
from kivy.properties import ObjectProperty
from kivy.uix.button import Button
from functools import partial
from kivy.config import Config
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import Screen, ScreenManager
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

<ModeScreen>:
    center_label: center_label
    FloatLayout:
        BoxLayout:
            orientation: "vertical"
            size_hint: 0.8, 0.8
            pos_hint: {"x": 0.1, "y": 0.1}
            padding: "5sp"
            spacing: "5sp"
            Label:
                canvas:
                    Color:
                        rgba: 0, 0, 1, 0.3
                    Rectangle:
                        pos: self.pos
                        size: self.size

                text: "Keyboard demo"
                size_hint_y: 0.1
            Label:
                id: center_label
                markup: True
                size_hint_y: 0.8
            BoxLayout:
                orientation: "horizontal"
                size_hint_y: 0.1
                Button:
                    text: "Exit"
                    on_release: exit()
                Button:
                    text: "Set to 'dock'"
                    on_release: root.set_mode('dock')
                Button:
                    text: "Set to ''"
                    on_release: root.set_mode('')
                Button:
                    text: "Continue"
                    on_release: root.next()

''')


class ModeScreen(Screen):
    """
    Present the option to change keyboard mode and warn of system-wide
    consequences.
    """
    center_label = ObjectProperty()
    keyboard_mode = ""

    def on_pre_enter(self, *args):
        """
        Detect the current keyboard mode and set the text of the main
        label accordingly.
        """
        self.keyboard_mode = Config.get("kivy", "keyboard_mode")
        p1 = "Current keyboard mode: '{0}'\n\n".format(self.keyboard_mode)
        if self.keyboard_mode == "dock":
            p2 = "You have the right setting to use this demo.\n\n"
        elif self.keyboard_mode == "":
            p2 = "You need the keyboard mode to 'dock' (below) in order for\n" \
                 "this demo to run.\n\n"
        else:
            p2 = "Custom setting detected! To use the demo, you must set the " \
                 "keyboard mode to dock but will\nneed to restore your" \
                " setting manually.\n\n"
        p3 = "[b][color=#ff0000]Warning:[/color][/b] This is a system-wide " \
            "setting and will affect all Kivy apps. Please\nuse this app" \
            " to reset this value."

        self.center_label.text = "".join([p1, p2, p3])

    def set_mode(self, mode):
        """ Sets the keyboard mode to the one specified """
        Config.set("kivy", "keyboard_mode", mode)
        Config.write()
        self.center_label.text = "Please restart the application for this\n" \
            "setting to take effect."

    def next(self):
        """ Continue to the main screen """
        print "manager=", str(self.manager)


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
        sm = ScreenManager()
        sm.switch_to(ModeScreen())
        return sm

if __name__ == "__main__":
    KeyboardDemo().run()
