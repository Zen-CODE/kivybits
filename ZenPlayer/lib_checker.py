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
from kivy.properties import (NumericProperty, ListProperty, ObjectProperty,
                             BooleanProperty)
from kivy.graphics import Color, Rectangle
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

        'artist': the artist
        'album': the album
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

        def is_not_in_albums(_folder, _albums):
            return all([_folder != album['folder'] for album in _albums])

        for root, sub_albums, files in walk(folder):
            for i in sub_albums:
                MusicLib._get_albums(path.join(folder, i), albums, max_albums)

            if len(sub_albums) == 0 and len(files) > 0:
                if is_not_in_albums(root, albums):
                    albums.append({'folder': root})

                if len(albums) > max_albums:
                    return albums
        return albums

    @staticmethod
    def _populate_album(album):
        """
        Populates the indexed *folders" dictionary with album info and data.
        """
        folder = album['folder']
        parts = folder.split(sep)
        artist, album_name = parts[-2], parts[-1]
        images, tracks, warnings = [], [], []
        files = [file_name for file_name in listdir(folder)]

        for my_file in sorted(files):
            ext = my_file[-4:]
            if ext in [".jpg", ".png", ".gif", "jpeg"]:
                images.append(path.join(folder, my_file))
            elif ext in [".mp3", ".ogg"]:
                tracks.append(my_file)
            else:
                warnings.append("Unrecognized file: {0}".format(my_file))

        album.update({'artist': artist,
                      'album': album_name,
                      'tracks': tracks,
                      'images': images,
                      'warnings': warnings})

    def get_row_item(self, index, controller):
        """
        Build and return a formatted DisplayItem for the folder.
        """
        # Initialize
        album = self.albums[index]
        if 'tracks' not in album.keys():
            self._populate_album(album)
        di = DisplayItem()
        add_label = di.ids.labels.add_widget

        # Add header, images, tracks and warnings
        add_label(Label(
            text=u"[b][color=#FFFF00]{0} : {1}[/color][/b]".format(
                 album['artist'], album['album']),
            markup=True))

        [di.ids.images.add_widget(Image(source=image, allow_stretch=True))
         for image in album['images']]
        [add_label(Label(
            text=u"[color=#FF0000]{0}[/color]".format(warn)))
            for warn in album['warnings']]
        [add_label(PlaylistLabel(
            controller=controller,
            text=track,
            album_index=index,
            track_index=k)) for k, track in enumerate(album['tracks'])]

        if len(album['images']) == 0:
            di.ids.images.add_widget(Image(source="images/album.png"))

        return di


class DisplayItem(BoxLayout):
    """ This class represent an individual album found in the search. """


class PlaylistLabel(Label):
    """
    This class is used to represent each playlist item.
    """
    album_index = NumericProperty()
    track_index = NumericProperty()
    playing = BooleanProperty(False)
    controller = ObjectProperty()
    _back_rect = None

    def on_playing(self, widget, value):
        """ Respond to the change in state. """
        if value:
            with self.canvas:
                Color(0.5, 0.5, 1, 0.3)
                self._back_rect = Rectangle(pos=self.pos, size=self.size)
            self.controller.play_track(self.album_index, self.track_index)
        else:
            self.canvas.remove(self._back_rect)

    def on_touch_down(self, touch):
        """ Handle the event. """
        if self.collide_point(*touch.pos):
            touch.grab(self)

    def on_touch_up(self, touch):
        """ Handle the event. """
        if touch.grab_current is self:
            touch.ungrab(self)
            if self.collide_point(*touch.pos):
                self.playing = not self.playing
        else:
            self.playing = False


class AlbumScreen(BoxLayout):
    """"
    The main screen showing a list of albums found.
    """
    album_index = NumericProperty(0)
    track_index = NumericProperty(0)
    music_lib = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(AlbumScreen, self).__init__(**kwargs)
        self.music_lib = MusicLib()
        self.show_album()
        # Clock.schedule_interval(lambda dt: self.show_next(), 10)

    def play_track(self, album_index, track_index):
        """ Play the specified track. """
        self.album_index, self.track_index = album_index, track_index
        print "play track " + self.music_lib.albums[album_index][
            'tracks'][track_index]

    def show_album(self, advance=None):
        """
        Begins the timed display of albums. If *advance* is True, the next item
        is shown. If False, it moves back. If not specified, the current album
        is shown.
        """
        albums = self.music_lib.albums
        album_index = self.album_index
        track_index = self.track_index
        if advance is not None:
            if advance:
                if album_index < len(albums):
                    album_index = (album_index + 1) % len(albums)
                    track_index = 0
            else:
                if 0 < album_index:
                    album_index = (len(albums) + album_index - 1) %\
                                   len(albums)
                    track_index = 0

        container = self.ids.row_container
        container.clear_widgets()
        if len(albums) > album_index:
            container.add_widget(
                self.music_lib.get_row_item(album_index, self))
            self.play_track(album_index, track_index)
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
        return AlbumScreen()

if __name__ == '__main__':
    FolderChecker().run()
