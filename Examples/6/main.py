from kivy.app import App
from kivy.lang import Builder
from  kivy.uix.floatlayout import FloatLayout
import webbrowser

Builder.load_string('''
<ActiveLabel>:
    Label:
        markup: True
        text: "Made with [ref=http://kivy.org]Kivy[/ref]"
        on_ref_press: root.openurl(*args)
''')


class ActiveLabel(FloatLayout):
    def openurl(self, *args):
        print "openurl fired"
        webbrowser.open(args[1])


class LabelDemo(App):
    def build(self):
        return ActiveLabel()

if __name__=="__main__":
    LabelDemo().run()

