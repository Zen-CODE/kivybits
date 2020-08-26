from kivy.app import App
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.gridlayout import GridLayout
from kivy.properties import ObjectProperty
from kivy.lang import Builder

Builder.load_string('''
<DemoScatter>:
    img: img
    scat: scat
    Scatter:
        id: scat
        Image:
            id: img
            source: "cover.jpg"

<MainWindow>:
    scat1: scat1
    rows: 2
    cols: 2
    DemoScatter:
        id: scat1
    DemoScatter:
    DemoScatter:
    DemoScatter:
''')


class DemoScatter(RelativeLayout):
    img = ObjectProperty()
    scat = ObjectProperty()

    def on_touch_down(self, touch):
        ret = super(DemoScatter, self).on_touch_down(touch)
        if self.collide_point(*touch.pos):
            return True
        else:
            # Continue bubbling event
            return ret

    def apply_transform(self, trans):
        return self.scat.apply_transform(trans)


class MainWindow(GridLayout):
    scat1 = ObjectProperty()

    def __init__(self, **kwargs):
        super(MainWindow, self).__init__(**kwargs)

        from kivy.graphics.transformation import Matrix
        mat = Matrix().scale(3, 3, 3)
        self.scat1.apply_transform(mat)
        print "Transform applied"


class TestApp(App):
    def build(self):
        return MainWindow()

TestApp().run()