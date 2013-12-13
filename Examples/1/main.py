from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.vkeyboard import VKeyboard
from kivy.core.window import Window
from kivy.properties import ObjectProperty
from functools import partial
from kivy.uix.button import  Button
from kivy.config import Config
from kivy.logger import Logger

Config.set('kivy', 'keyboard_mode', 'dock')


class KeyboardListener(object):
    """
    This class handles the management of keyboard bindings and callbacks.
    It also exposes a list of available keyboard layouts.
    """
    layouts = []  # List of available keyboard layouts
    _keyboard = None  # Current keyboard layout
    _callback = None  # Current callback

    def __init__(self):
        """ Build a list of available keyboard layouts."""
        super(KeyboardListener, self).__init__()
        self.layouts = [key for key in VKeyboard().available_layouts.keys()]
        #self.layouts.append('numeric.json')

    def set_callback(self, callback, layout):
        """
        Set the function to be called when key presses occur.
        """
        Window.release_all_keyboards()
        self._keyboard = Window.request_keyboard(
            self._keyboard_close,
            self)

        #if self._keyboard.widget:
        Logger.info("main.py: self._keyboard.widget=" +
                    str(self._keyboard.widget))
        #if self._keyboard.widget:
            #vkeyboard = self._keyboard.widget
            #vkeyboard.layout = layout
            #vkeyboard.bind(on_key_down=callback)
        if self._keyboard:
            self._keyboard.layout = layout
            self._keyboard.bind(on_key_down=callback)
            self._callback = callback

    def _keyboard_close(self):
        """The keyboard has been closed. Clean up"""
        if self._callback:
            Logger.info("main.py: Keyboard closed...")
            self._keyboard.unbind(on_key_down=self._callback)
            self._keyboard = None
            self._callback = None

# In your config.ini, in the "kivy" section, add "keyboard_mode = dock"
Builder.load_string(
'''
<KeyboardTest>:
    #TODO: Remove
    display_label: display_label
    kb_container: kb_container

    orientation: 'vertical'
    Label:
        size_hint_y: 0.125
        text: "Please select the keyboard layout."
    BoxLayout:
        id: kb_container
        size_hint_y: 0.125
        orientation: "horizontal"
        padding: 10

    Label:
        id: display_label
        size_hint_y: 0.25
        markup: True
        text: "[b]System info[/b]"
        halign: "center"
    Widget:
        size_hint_y: 0.5
''')


class KeyboardTest(BoxLayout):
    display_label = ObjectProperty()
    kb_container = ObjectProperty()
    kb_listener = None

    def __init__(self, **kwargs):
        super(KeyboardTest, self).__init__(**kwargs)
        self._kb_listener = KeyboardListener()
        self._add_keyboards()

    def _add_keyboards(self):
        """
        Add buttons for each available keyboard layout
        """
        for key in self._kb_listener.layouts:
            button = Button(text=key,
                            on_release=partial(self.on_button_release,
                                               layout=key))
            self.kb_container.add_widget(button)

    def on_button_release(self, instance, layout):
        """ The button has been pressed """
        Logger.info("main.py: Setting keyboard listed to " + layout)
        self._kb_listener.set_callback(self.on_key_press, layout)

    def on_key_press(self, *largs):
        """ A key has been pressed. Display it."""
        self.display_label.text = '[b]Key pressed[/b]\n' + largs[2]


class test(App):
    def build(self):
        return KeyboardTest()

if __name__ == "__main__":
    test().run()
