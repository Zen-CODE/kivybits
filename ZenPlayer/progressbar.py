__author__ = "Richard Larkin"

from kivy.uix.progressbar import ProgressBar
from kivy.lang import Builder
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import OptionProperty

Builder.load_string('''
<-ImageProgressBar>:
    canvas:

        # PushMatrix
        # Translate:
        #     xy: self.center_x, self.center_y
        # Rotate:
        #     angle: 90 if root.orientation == 'horizontal' else 0
        #     axis: 0, 0, 1
        # Translate:
        #     xy: -self.center_x, -self.center_y

        # Color:
        #     rgba: 1, 1, 0, 0.25
        StencilPush

        Rectangle:
            pos: self.pos
            size: self.width * (self.value / self.max) if root.orientation == 'horizontal' else self.width, \
                  self.height if root.orientation == 'horizontal' else self.height * (self.value / self.max)
        StencilUse

        Rectangle:
            size: self.size
            pos: self.pos
            source: "bar1.png"

        StencilUnUse
        StencilPop
#        PopMatrix

''')


class ImageProgressBar(ProgressBar):
    """
    Provides a feature identical yet "prettier" progressbar.
    """
    orientation = OptionProperty('horizontal', options=['horizontal', 'vertical'])


if __name__ == "__main__":
    from kivy.app import App
    from kivy.clock import Clock
    from functools import partial

    class MainScreen(FloatLayout):
        def __init__(self, **kwargs):
            super(MainScreen, self).__init__(**kwargs)
            self.pb = ImageProgressBar(size_hint=(0.5, 0.5),
                                       pos_hint={"center_x": 0.5,
                                                 "center_y": 0.5},
                                       value=100,
                                       orientation='vertical')
            self.add_widget(self.pb)

            def set_progess(*args, **kwargs):
                print "setting to {0}".format(kwargs['value'])
                self.pb.value = kwargs['value']

            for k, val in enumerate(range(100, -1, -1)):
                print "l, val = {0}, {1}".format(k, val)
                # Clock.schedule_once(lambda x: partial(set_progess, val), 0.1 * k)
                Clock.schedule_once(partial(set_progess, value=val), 2 + 0.025 * k)



    class TestApp(App):
        def build(self):
            return MainScreen()

    TestApp().run()

