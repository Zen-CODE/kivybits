from random import sample
from string import ascii_lowercase
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout


kv = """
#: import CAMIMenuRow camimenu.CAMIMenuRow
#: import CAMIMenu camimenu.CAMIMenu
#: import Window kivy.core.window.Window
#: set row_height 0.1 * Window.height

<Test>:
    canvas:
        Color:
            rgba: 0.3, 0.3, 0.3, 1
        Rectangle:
            size: self.size
            pos: self.pos
    rv: rv
    orientation: 'vertical'
    GridLayout:
        cols: 3
        rows: 2
        size_hint_y: None
        height: dp(108)
        padding: dp(8)
        spacing: dp(16)
        Button:
            text: 'Populate list'
            on_press: root.populate()
        Button:
            text: 'Sort list'
            on_press: root.sort()
        Button:
            text: 'Clear list'
            on_press: root.clear()
        BoxLayout:
            spacing: dp(8)
            Button:
                text: 'Insert new item'
                on_press: root.insert(new_item_input.text)
            TextInput:
                id: new_item_input
                size_hint_x: 0.6
                hint_text: 'value'
                padding: dp(10), dp(10), 0, 0
        BoxLayout:
            spacing: dp(8)
            Button:
                text: 'Update first item'
                on_press: root.update(update_item_input.text)
            TextInput:
                id: update_item_input
                size_hint_x: 0.6
                hint_text: 'new value'
                padding: dp(10), dp(10), 0, 0
        Button:
            text: 'Remove first item'
            on_press: root.remove()

    CAMIMenu:
        id: rv
"""

Builder.load_string(kv)


class Test(BoxLayout):

    def callback(self, *args):
        print("Callback fired with {0}".format(args))

    def populate(self):
        self.rv.data = [{'text': ''.join(sample(ascii_lowercase, 6)),
                        'callback': lambda y=x: self.callback(y),
                        'post_icons': [
                            {'source': 'graphics/trophy.png',
                             'callback': lambda y=x: self.callback(
                                "trophy " + str(x))},
                            {'source': 'graphics/group.png',
                             'callback': lambda y=x: self.callback(
                                 "group " + str(x))}
                        ],
                        'number': x}
                        for x in range(50)]

    def sort(self):
        self.rv.data = sorted(self.rv.data, key=lambda x: x['text'])

    def clear(self):
        self.rv.data = []

    def insert(self, value):
        self.rv.data.insert(0, {'text': value or 'default value'})

    def update(self, value):
        if self.rv.data:
            self.rv.data[0]['text'] = value or 'default new value'
            self.rv.refresh_from_data()

    def remove(self):
        if self.rv.data:
            self.rv.data.pop(0)


class TestApp(App):
    def build(self):
        return Test()


if __name__ == '__main__':
    TestApp().run()
