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
            id: box
            spacing: "20dp"
            orientation: 'vertical'
            size_hint_y: None
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
        ri = RowItem()
        parts = folder.split(sep)
        header = u"[b][color=#FFFF00]{0} - by {1}[/color][/b]".format(
            parts[-1],
            parts[-2])

        full_path = path.join(*reversed(parts[::-1]))
        source = "images/album.png"
        count = 0
        warnings = []

        # Gather data
        for my_file in sorted(files):
            ext = my_file[-4:]
            if ext in [".jpg", ".png", ".gif"]:
                source = path.join(folder, my_file)
            elif ext == ".mp3":
                # print(my_file[0:-4:])
                count += 1
            else:
                warnings.append(u"Unrecognized file {0}".format(my_file))

        # Now create and return the row_tem
        footer = ""
        for warning in warnings:
            footer += "[color=#FF0000]{0}[/color]".format(warning)

        ri.add_widget(Image(source=source, size_hint=(0.3, 1)))
        ri.add_widget(
            Label(
                text=u"{0}\n\nTracks: {1}\n{2}".format(
                    header, count, footer),
                markup=True,
                size_hint=(0.7, 1),
                halign="center"))
        return ri


class RowItem(BoxLayout):
    """ This class represent an individual album found in the search. """
    # def __init__(self):
    #     super(RowItem, self).__init__()
    #     self.add_widget(Label(text="Object {0}".format(self)))


class MainScreen(BoxLayout):
    """"
    The main screen showing a list of albums found.
    """
    box = None

    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)
        self.max_folders = 10
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
        self.box.add_widget(row_item)


class FolderChecker(App):
    def build(self):
        return MainScreen()

if __name__ == '__main__':
    FolderChecker().run()

