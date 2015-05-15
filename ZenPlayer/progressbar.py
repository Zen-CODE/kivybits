__author__ = "Richard Larkin"

from kivy.uix.progressbar import ProgressBar
from kivy.lang import Builder
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import StringProperty

Builder.load_string('''
<-ImageProgressBar>:
    canvas:
        StencilPush

        Rectangle:
            pos: self.pos
            size: self.width * (self.value / self.max), self.height
        StencilUse

        Rectangle:
            size: self.size
            pos: self.pos
            source: root.source

        StencilUnUse
        StencilPop
''')


class ImageProgressBar(ProgressBar):
    """
    Provides a feature identical yet "prettier" progressbar.
    """
    source = StringProperty('')

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
                                       source="bar1.png",
                                       value=100)
            self.add_widget(self.pb)

            # Animate the value changes
            def set_progress(*args, **_kwargs):
                self.pb.value = _kwargs['value']

            for k, val in enumerate(range(100, -1, -1)):
                Clock.schedule_once(partial(set_progress, value=val),
                                    2 + 0.025 * k)

    class TestApp(App):
        def build(self):
            return MainScreen()

    TestApp().run()
