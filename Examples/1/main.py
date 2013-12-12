from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.vkeyboard import VKeyboard
from kivy.core.window import Window
from kivy.properties import ObjectProperty
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from functools import partial
from kivy.config import Config


Config.set('kivy', 'keyboard_mode', 'dock')


class KeyboardListener(object):
    """
    Handles the management of keyboard bindings and callbacks
    """
    layouts = []  # List of available keyboard layouts
    _keyboard = None  # Current keyboard layout
    _callback = None  # Current callback

    def __init__(self):
        """ Build a list of available keyboard layouts """
        super(KeyboardListener, self).__init__()
        self.layouts = [key for key in VKeyboard().available_layouts.keys()]
        self.layouts.append('numeric.json')

    def set_callback(self, callback, text_input, layout):
        """
        Set the function to be called when key presses occur
        """
        #Window.release_all_keyboards()
        self._keyboard = Window.request_keyboard(
            self._keyboard_close,
            text_input)

        #if self._keyboard.widget:
        if self._keyboard:
            self._keyboard.layout = layout
            self._keyboard.bind(on_key_down=callback)
            self._callback = callback

    def _keyboard_close(self):
        """The keyboard has been closed. Clean up"""
        if self._callback:
            print "Keyboard closed..."
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
        size_hint_y: 0.25
        text: "I'm glad to see you Dave."
    BoxLayout:
        id: kb_container
        size_hint_y: 0.25
        orientation: "horizontal"
        padding: 10

    Label:
        id: display_label
        size_hint_y: 0.5
        markup: True
        text: "[b]System info[/b]"
        halign: "center"
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
        Add TextInputs and labels for each available keyboard layout
        """
        for key in self._kb_listener.layouts:
            # Add a BoxLayout, a text input and label for each layout
            bl = BoxLayout(orientation="vertical")
            ti = TextInput()
            ti.bind(focus=partial(self.on_text_focus, layout=key))

            bl.add_widget(Label(text=key))
            bl.add_widget(ti)
            self.kb_container.add_widget(bl)

    def on_text_focus(self, instance, value, layout):
        if value:
            print "Setting keyboard listed to ", layout
            self._kb_listener.set_callback(self.on_key_press, instance, layout)
        return False

    def on_key_press(self, *largs):
        print "largs = ", str(largs)
        self.display_label.text = '[b]Key pressed[/b]\n' + largs[2]
        return True


class test(App):
    def build(self):
        return KeyboardTest()

if __name__ == "__main__":
    test().run()
