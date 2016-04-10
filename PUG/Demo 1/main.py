from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.uix.image import Image


class DemoApp(App):
    """
    The App class is a singleton and creates the base of your application.
    """
    def build(self):
        """ This method returns the root widget of your application. """
        float_layout = FloatLayout()
        button = Button(text='Click me',
                        size_hint=(0.4, 0.2),
                        pos_hint={'center_x': 0.5, 'center_y': 0.8})
        button.bind(on_press=self.button_click)


        self.image = Image(source='1.png',
                           size_hint=(0.2, 0.2),
                           pos_hint={'right': 1, 'top': 1})
        float_layout.add_widget(self.image)

        float_layout.add_widget(button)
        return float_layout

    def button_click(self, button):
        """ Fired, via binding, when the button is clicked. """
        anim = An



if __name__ == "__main__":
    DemoApp().run()