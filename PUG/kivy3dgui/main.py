from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.textinput import TextInput


class DemoApp(App):
    """
    The App class is a singleton and creates the base of your application.
    """
    @staticmethod
    def get_grid():
        """ Build and return the main grid UI. """
        grid = GridLayout(rows=2, cols=2)
        grid.add_widget(
            Button(text='Click me'))
        grid.add_widget(
            TextInput(text='Click me'))
        grid.add_widget(
            Image(source='audio_icon.png', allow_swtretch=True))
        return grid

    def build(self):
        """ This method returns the root widget of your application. """

        return self.get_grid()

if __name__ == "__main__":
    DemoApp().run()