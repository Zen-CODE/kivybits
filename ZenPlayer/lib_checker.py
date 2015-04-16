"""
ZenCODE's Music Library Checker
===============================

This module checks that the specified folders has properly structured music
folders using the following conventions:

    <Artists>\<Album>\<Track> - <Title>.<ext>
"""
__author__ = 'Richard Larkin a.k.a. ZenCODE'


from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
from kivy.uix.label import Label
from kivy.metrics import sp

Builder.load_string('''
<RowItem>:
    orientation: 'horizontal'
    size_hint: 1, None
    height: "100sp"

<MainScreen>:
    orientation: 'vertical'
    Label:
        canvas.before:
            Color:
                rgba: 0, 0, 1, 0.2
            Rectangle:
                pos: self.pos
                size: self.size
        text: "Music Library"
        size_hint_y: 0.1
    ScrollView:
        BoxLayout:
            id: row_box
            orientation: 'vertical'
            size_hint_y: None
''')


class RowItem(BoxLayout):
    """ This class represent an individual album found in the search. """
    def __init__(self):
        super(RowItem, self).__init__()
        self.add_widget(Label(text="Object {0}".format(self)))


class MainScreen(BoxLayout):
    """" The main screen showing a list of albums found. """
    box = None

    def __init__(self):
        super(MainScreen, self).__init__()
        num_rows = 10
        self.box = self.ids.row_box

        for k in range(0, num_rows):
            self.add_row(RowItem())

        self.box.height = num_rows * sp(100)

    def add_row(self, row_item):
        """ Add the row_item to the main display. """
        self.box.add_widget(row_item)


class FolderChecker(App):
    def build(self):
        return MainScreen()

if __name__ == '__main__':
    FolderChecker().run()

