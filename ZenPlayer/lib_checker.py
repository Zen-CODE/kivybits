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
from os import sep, listdir, path, walk
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
    # source = u'/media/richard/ZenUno/Zen/Music/CD'

    @staticmethod
    def get_row_item(folder, files):
        """
        Give a formatted display to the folder.
        """
        parts = folder.split(sep)
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
        self.box = self.ids.box
        self.folders = self._load_albums(MusicLib.source, [], 1)

        print "albums = " + str(self.folders)

    def _load_albums(self, folder, folders, max_folders):
        """
        Process the *folder*, appending to the *folders* list, our *folders* list with albums in the *folder*.
        """
        if len(folders) > max_folders:
            return folders

        for root, subfolders, files in walk(folder):
            for i in subfolders:
                self._load_albums(path.join(folder, i), folders, max_folders)

            if len(subfolders) == 0 and len(files) > 0:
                if root not in folders:
                    folders.append(root)

                if len(folders) > max_folders:
                    return folders
        return folders


class FolderChecker(App):
    def build(self):
        return MainScreen()

if __name__ == '__main__':
    FolderChecker().run()

