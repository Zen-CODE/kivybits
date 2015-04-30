"""
ZenCODE's Music Library Checker
===============================

This module checks that the specified albums has properly structured music
albums using the following conventions:

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

    albums = ListProperty([])
    '''
    A list of dictionaries containing data for each album found. Entries are as
    follows:

        'folder': the full folder path

    This is the minimum it will contain. Once processed it contains:

        'tracks': a list of sorted file names
        'images': a list of images found
        'warning': a list list of warnings found
    '''
    max_albums = 10

    def __init__(self, **kwargs):
        """ The class constructor. """
        super(MusicLib, self).__init__(**kwargs)
        self.albums = MusicLib._get_albums(MusicLib.source,
                                            [],
                                            MusicLib.max_albums)

    @staticmethod
    def _get_albums(folder, albums, max_albums):
        """
        Process the *folder*, appending to the *albums* list adding only
        *max_albums* + 1 albums.
        """
        if len(albums) > max_albums:
            return albums

        for root, sub_albums, files in walk(folder):
            for i in sub_albums:
                MusicLib._get_albums(path.join(folder, i), albums, max_albums)

            if len(sub_albums) == 0 and len(files) > 0:
                if root not in albums:
                    albums.append({'folder': root})

                if len(albums) > max_albums:
                    return albums
        return albums

    def get_row_item(self, index):
        """
        Give a formatted DisplayItem for the folder.
        """
        folder = self.albums[index]['folder']
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
        # Clock.schedule_interval(lambda dt: self.show_next(), 10)

    def show_album(self, advance=None):
        """
        Begins the timed display of albums. If *advance* is True, the next item
        is shown. If False, it moves back. If not specified, the current album
        is shown.
        """
        albums = self.music_lib.albums
        if advance is not None:
            if advance:
                if self.current_index < len(albums):
                    self.current_index = (
                        self.current_index + 1) % len(albums)
            else:
                if 0 < self.current_index:
                    self.current_index = (
                        len(albums) + self.current_index - 1) %\
                        len(albums)

        container = self.ids.row_container
        container.clear_widgets()
        if len(albums) > self.current_index:
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
