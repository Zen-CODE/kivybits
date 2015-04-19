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
from kivy.properties import NumericProperty, ListProperty
from kivy.clock import Clock

Builder.load_file('lib_checker.kv')


class MusicLib(object):
    """
    This class houses metadata about our music collection.
    """
    # source = u'/media/ZenOne/Zen/Music/CD'
    source = u'/media/richard/ZenUno/Zen/Music/CD'

    @staticmethod
    def get_row_item(folder):
        """
        Give a formatted display to the folder.
        """
        parts = folder.split(sep)
        # full_path = path.join(*reversed(parts[::-1]))
        files = [file_name for file_name in listdir(folder)]

        lines = [u"[b][color=#FFFF00]{0} : {1}[/color][/b]".format(
            parts[-2],
            parts[-1])]
        images = []

        # Gather data
        for my_file in sorted(files):
            ext = my_file[-4:]
            if ext in [".jpg", ".png", ".gif", "jpeg"]:
                images.append(path.join(folder, my_file))
            elif ext in [".mp3", "ogg"]:
                lines.append(my_file[0:-4:])
            else:
                lines.append(
                    u"[color=#FF0000]Unrecognized file {0}[/color]".format(
                        my_file))

        # Now create and return the row_tem
        di = DisplayItem()
        if len(images) == 0:
            di.ids.images.add_widget(Image(source="images/album.png"))
        else:
            for image in images:
                di.ids.images.add_widget(Image(source=image))

        for line in lines:
            di.ids.labels.add_widget(
                PlaylistLabel(text=line))
        return di

    @staticmethod
    def get_albums(folder, folders, max_folders):
        """
        Process the *folder*, appending to the *folders* list adding only
        *max_folders* + 1 folders.
        """
        if len(folders) > max_folders:
            return folders

        for root, sub_folders, files in walk(folder):
            for i in sub_folders:
                MusicLib.get_albums(path.join(folder, i), folders, max_folders)

            if len(sub_folders) == 0 and len(files) > 0:
                if root not in folders:
                    folders.append(root)

                if len(folders) > max_folders:
                    return folders
        return folders


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
    folders = ListProperty([])

    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)
        self.folders = MusicLib.get_albums(MusicLib.source, [], 10)
        self.show_album()
        Clock.schedule_interval(lambda dt: self.show_next(), 10)

    def show_album(self):
        """
        Begins the timed display of folders
        """
        container = self.ids.row_container
        container.clear_widgets()
        container.add_widget(MusicLib.get_row_item(
            self.folders[self.current_index]))

    def show_next(self):
        """ Show the next album. """
        self.current_index = (self.current_index + 1) % len(self.folders)
        self.show_album()

    def show_previous(self):
        """ Show the next album. """
        self.current_index = (
            len(self.folders) + self.current_index - 1) % len(self.folders)
        self.show_album()


class FolderChecker(App):
    def build(self):
        return MainScreen()

if __name__ == '__main__':
    FolderChecker().run()
