from kivy.app import App
from kivy.graphics.svg import Svg
from kivy.uix.boxlayout import BoxLayout
from kivy.graphics import Scale
from kivy.uix.relativelayout import RelativeLayout
from kivy.properties import StringProperty


class SvgWidget(RelativeLayout):
    filename = StringProperty()

    def __init__(self, **kwargs):
        super(SvgWidget, self).__init__(**kwargs)
        with self.canvas:
            self.scale = Scale(1, 1, 1)
            self.svg = Svg(kwargs['filename'])

        self.bind(size=self._do_scale)

    def _do_scale(self, *args):
        self.scale.xyz = (self.width / self.svg.width,
                          self.height / self.svg.height,
                          1)


class SvgApp(App):
    def build(self):
        root = BoxLayout()
        root.add_widget(SvgWidget(filename='fox.svg'))
        root.add_widget(SvgWidget(filename='refresh.svg'))
        return root


if __name__ == '__main__':
    SvgApp().run()
