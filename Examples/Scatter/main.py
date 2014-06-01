from kivy.app import App
from kivy.uix.scatter import Scatter
from kivy.uix.gridlayout import GridLayout
from kivy.properties import ObjectProperty
from kivy.lang import Builder

Builder.load_string('''
<MainWindow>:
    scat1: scat1
    rows: 2
    cols: 2
    Scatter:
        id: scat1
        Image:
            source: "cover.jpg"

    Scatter:
        Image:
            source: "cover.jpg"
    Scatter:
        Image:
            source: "cover.jpg"
    Scatter:
        Image:
            source: "cover.jpg"
''')


class MainWindow(GridLayout):
    scat1 = ObjectProperty()

    def __init__(self, **kwargs):
        super(MainWindow, self).__init__(**kwargs)

        from kivy.graphics.transformation import Matrix
        mat = Matrix().scale(3, 3, 3)
        self.scat1.apply_transform(mat)


class TestApp(App):
    def build(self):
        return MainWindow()

TestApp().run()