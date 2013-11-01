"""
A experiment exploring how to broadcast property change to all instances of a
widget.
"""
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.properties import StringProperty


class CustomButton(Button):
    common_text = StringProperty()
    _index = 0  # Just used to store an arb value
    _instances = []

    def __init__(self, **kwargs):
        super(CustomButton, self).__init__(**kwargs)
        CustomButton._instances.append(self)

    @staticmethod
    def on_common_text(instance, value):
        """ For each instance of this class, change it's text """
        for button in CustomButton._instances:
            button.text = value

    def on_release(self):
        self.common_text = "Click me! " + str(self._index)


class TestApp(App):
    def build(self):
        layout = BoxLayout(orientation="vertical")
        for i in range(0, 6):
            but = CustomButton(text="Click me!")
            but._index = i
            layout.add_widget(but)
        return layout

if __name__ == "__main__":
    TestApp().run()