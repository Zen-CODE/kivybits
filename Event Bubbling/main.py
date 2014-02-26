from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout

Builder.load_string('''
<EventBubbler>:
    orientation: 'vertical'
    Label:
        text: '1'
        on_touch_down: root.printme("label 1 on_touch_up")
    Label:
        text: '2'
        on_touch_down: root.printme("label 2 on_touch_up")
    BoxLayout:
        orientation: 'horizontal'
        on_touch_down: root.printme("box on_touch_up")
        Label:
            text: '3'
            on_touch_down: root.printme("label 3 on_touch_up")
        Label:
            text: '4'
            on_touch_down: root.printme("label 4 on_touch_up")
''')


class EventBubbler(BoxLayout):
    def printme(self, msg):
        print msg


class BubbleApp(App):
    def build(self):
        return EventBubbler()

BubbleApp().run()



