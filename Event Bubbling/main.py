from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout

use_kv = False

if use_kv:
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

    @staticmethod
    def printme(msg):
        print msg

    if not use_kv:
        def __init__(self, **kwargs):
            from kivy.uix.label import Label
            from kivy.uix.boxlayout import BoxLayout

            super(EventBubbler, self).__init__(**kwargs)
            self.orientation = 'vertical'
            self.add_widget(
                Label(
                    text="1",
                    on_touch_down=lambda btn, tch: self.printme("1abel 1")))
            self.add_widget(
                Label(
                    text="2",
                    on_touch_down=lambda btn, tch: self.printme("1abel 2")))
            box = BoxLayout(
                on_touch_down=lambda box, tch: self.printme("box"))
            box.add_widget(
                Label(
                    text="3",
                    on_touch_down=lambda btn, tch: self.printme("1abel 3")))
            box.add_widget(
                Label(
                    text="4",
                    on_touch_down=lambda btn, tch: self.printme("1abel 4")))
            self.add_widget(box)


class BubbleApp(App):
    def build(self):
        return EventBubbler()

BubbleApp().run()



