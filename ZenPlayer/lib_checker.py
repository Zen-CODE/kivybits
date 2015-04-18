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
from kivy.metrics import sp
from os import sep, listdir, path
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.clock import Clock

Builder.load_string('''
<DisplayItem>:
    orientation: 'horizontal'
    BoxLayout:
        id: images
        spacing: "20dp"
        orientation: 'vertical'
    BoxLayout:
        id: labels
        orientation: 'vertical'

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
    DisplayItem:
            id: box
            size_hint_y: 0.9
''')


class MusicLib(object):
    """
    This class houses metadata about our music collection.
    """
    source = u'/media/ZenOne/Zen/Music/CD'

    @staticmethod
    def get_row_item(folder, files):
        """
        Give a formatted display to the folder.
        """
        parts = folder.split(sep)
        source = "images/album.png"
        full_path = path.join(*reversed(parts[::-1]))

        lines = [u"[b][color=#FFFF00]{0} : {1}[/color][/b]".format(
            parts[-2],
            parts[-1])]
        images = []

        # Gather data
        for my_file in sorted(files):
            ext = my_file[-4:]
            if ext in [".jpg", ".png", ".gif", "jpeg"]:
                images.append(path.join(folder, my_file))
            elif ext == ".mp3":
                lines.append(my_file[0:-4:])
            else:
                lines.append(
                    u"[color=#FF0000]Unrecognized file {0}[/color]".format(
                        my_file))

        # Now create and return the row_tem
        di = DisplayItem()
        if len(images) == 0:
            di.ids.images.add_widget(Image(source="data/album.png"))
        else:
            for image in images:
                di.ids.images.add_widget(Image(source=image))

        for line in lines:
            di.ids.labels.add_widget(
                Label(text=line,
                      markup=True,
                      halign="center"))
        return di


class DisplayItem(BoxLayout):
    """ This class represent an individual album found in the search. """


class MainScreen(BoxLayout):
    """"
    The main screen showing a list of albums found.
    """
    box = None

    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)
        self.max_folders = 50
        self.folder_count = 0
        self.box = self.ids.box
        self.start()

    def start(self):
        self.box = self.ids.box
        self.build_contents(MusicLib.source)
        self.box.height = self.folder_count * sp(100)

    def build_contents(self, folder):
        """ Populate our main display with row items."""
        contents = listdir(folder)
        for item in contents:
            if self.folder_count >= self.max_folders:
                return

            full_path = path.join(folder, item)
            if path.isdir(full_path):
                self.build_contents(full_path)
            else:
                self.add_row(MusicLib.get_row_item(folder, contents))
                self.folder_count += 1

                break

    def add_row(self, row_item):
        """ Add the row_item to the main display. """
        self.box.clear_widgets()
        self.box.add_widget(row_item)


class FolderChecker(App):
    def build(self):
        return MainScreen()

if __name__ == '__main__':
    FolderChecker().run()

