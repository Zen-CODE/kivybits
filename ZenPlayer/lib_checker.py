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
from os import sep, listdir, path, walk
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.properties import NumericProperty, ListProperty, ObjectProperty
from kivy.clock import Clock
from kivy.event import EventDispatcher

Builder.load_file('lib_checker.kv')


class MusicLib(EventDispatcher):
    """
    This class houses metadata about our music collection.
    """
    # source = u'/media/ZenOne/Zen/Music/CD'  # PC. Linux
    # source = u'/media/richard/ZenUno/Zen/Music/MP3'  Laptop, linux
    source = r"d:\Zen\Music\MP3"  # PC, Windows

    folders = ListProperty([])
    max_folders = 10

    def __init__(self, **kwargs):
        """ The class constructor. """
        super(MusicLib, self).__init__(**kwargs)
        self.folders = MusicLib._get_albums(MusicLib.source,
                                            [],
                                            MusicLib.max_folders)

    @staticmethod
    def _get_albums(folder, folders, max_folders):
        """
        Process the *folder*, appending to the *folders* list adding only
        *max_folders* + 1 folders.
        """
        if len(folders) > max_folders:
            return folders

        for root, sub_folders, files in walk(folder):
            for i in sub_folders:
                MusicLib._get_albums(path.join(folder, i), folders, max_folders)

            if len(sub_folders) == 0 and len(files) > 0:
                if root not in folders:
                    folders.append(root)

                if len(folders) > max_folders:
                    return folders
        return folders

    def get_row_item(self, index):
        """
        Give a formatted DisplayItem for the folder.
        """
        folder = self.folders[index]
        parts = folder.split(sep)
        # full_path = path.join(*reversed(parts[::-1]))
        files = [file_name for file_name in listdir(folder)]
        di = DisplayItem()
        add_label = di.ids.labels.add_widget

        add_label(Label(
            text=u"[b][color=#FFFF00]{0} : {1}[/color][/b]".format(
                 parts[-2], parts[-1]),
            markup=True))
        images = []

        # Gather data
        for my_file in sorted(files):
            ext = my_file[-4:]
            if ext in [".jpg", ".png", ".gif", "jpeg"]:
                images.append(Image(source=path.join(folder, my_file),
                                    allow_stretch=True))
            elif ext in [".mp3", ".ogg"]:
                add_label(PlaylistLabel(text=my_file[0:-4:]))
            else:
                add_label(Label(
                    text=u"[color=#FF0000]Unrecognized file {0}[/color]".format(
                        my_file)))

        # Now create and return the row_tem
        if len(images) == 0:
            di.ids.images.add_widget(Image(source="images/album.png"))
        else:
            [di.ids.images.add_widget(image) for image in images]

        return di


class DisplayItem(BoxLayout):
    """ This class represent an individual album found in the search. """


class PlaylistLabel(Label):
    """
    This class is used to represent each playlist item.
    """


class MainScreen(BoxLayout):
    """"
    The main screen showing a list of albums found.
    """
    current_index = NumericProperty(0)
    music_lib = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)
        self.music_lib = MusicLib()
        self.show_album()
        Clock.schedule_interval(lambda dt: self.show_next(), 10)

    def show_album(self, advance=None):
        """
        Begins the timed display of folders. If *advance* is True, the next item
        is shown. If False, it moves back. If not specified, the current album
        is shown.
        """
        folders = self.music_lib.folders
        if advance is not None:
            if advance:
                if self.current_index < len(folders):
                    self.current_index = (
                        self.current_index + 1) % len(folders)
            else:
                if 0 < self.current_index:
                    self.current_index = (
                        len(folders) + self.current_index - 1) %\
                        len(folders)

        container = self.ids.row_container
        container.clear_widgets()
        if len(folders) > self.current_index:
            container.add_widget(
                self.music_lib.get_row_item(self.current_index))
        else:
            container.add_widget(Label(text="No albums found"))

    def show_next(self):
        """ Show the next album. """
        self.show_album(True)

    def show_previous(self):
        """ Show the next album. """
        self.show_album(False)


class FolderChecker(App):
    def build(self):
        return MainScreen()

if __name__ == '__main__':
    FolderChecker().run()
