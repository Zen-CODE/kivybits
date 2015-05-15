__author__ = "Richard Larkin"

from kivy.uix.progressbar import ProgressBar
from kivy.lang import Builder
from kivy.uix.floatlayout import FloatLayout

Builder.load_string('''
<-ImageProgressBar>:
    canvas:
        # Color:
        #     rgba: 1, 1, 0, 0.25
        Rectangle:
            size: self.width * (self.value / self.max), self.height
            pos: self.pos
            source: "bar1.png"
''')


class ImageProgressBar(ProgressBar):
    """
    Provides a feature identical yet "prettier" progressbar.
    """


if __name__ == "__main__":
    from kivy.app import App
    from kivy.clock import Clock
    from functools import partial

    class MainScreen(FloatLayout):
        def __init__(self, **kwargs):
            super(MainScreen, self).__init__(**kwargs)
            self.pb = ImageProgressBar(size_hint=(0.6, 0.2),
                                       pos_hint={"center_x": 0.5,
                                                 "center_y": 0.5},
                                       value=100)
            self.add_widget(self.pb)

            def set_progess(*args, **kwargs):
                print "setting to {0}".format(kwargs['value'])
                self.pb.value = kwargs['value']

            for k, val in enumerate(range(100, -10, -10)):
                print "l, val = {0}, {1}".format(k, val)
                #Clock.schedule_once(lambda x: partial(set_progess, val), 0.1 * k)
                Clock.schedule_once(partial(set_progess, value=val), 2 + 0.05 * k)



    class TestApp(App):
        def build(self):
            return MainScreen()

    TestApp().run()

