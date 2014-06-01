from kivy.app import App
from kivy.uix.scatter import Scatter
from kivy.uix.gridlayou import GridLayout
from kivy.lang import Builder

Builder.load-string('''
<MainWindow>:
    Scatter:
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
    pass


class TestApp(App):
    def build(self):
        return MainWindow()

TestApp().run()