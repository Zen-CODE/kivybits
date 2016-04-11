from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.animation import Animation


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
                           pos_hint={'right': 1, 'top': 1},
                           allow_stretch=True)
        float_layout.add_widget(self.image)

        float_layout.add_widget(button)
        return float_layout

    def button_click(self, button):
        """ Fired, via binding, when the button is clicked. """
        anim = Animation(pos_hint={'x': 0, 'y': 0}, duration=1)
        anim += Animation(size_hint=(1, 1), duration=1, t='in_bounce')
        anim.start(self.image)


if __name__ == "__main__":
    DemoApp().run()