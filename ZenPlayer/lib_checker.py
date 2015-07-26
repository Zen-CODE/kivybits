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
from kivy.event import EventDispatcher
from audioplayer import SoundLoader
from kivy.uix.screenmanager import Screen
from kivy.clock import Clock


class MusicLib(EventDispatcher):
    """
    This class houses metadata about our music collection.
    """
    source = u'/media/ZenOne/Zen/Music/CD'  # PC. Linux
    # source = u'/media/richard/ZenUno/Zen/Music/MP3'  Laptop, linux
    # source = r"d:\Zen\Music\MP3"  # PC, Windows

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
    max_albums = 100

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

        # Add header
        add_label(Label(
            text=u"[b][color=#FFFF00]{0} : {1}[/color][/b]".format(
                 album['artist'], album['album']),
            markup=True))

        # Add images + warnings
        if len(album['images']) == 0:
            di.ids.images.add_widget(Image(source="images/album.png"))
        else:
            for source in album['images']:
                image = Image(source=source, allow_stretch=True)
                image.bind(on_touch_down=lambda w, t:
                           w.collide_point(*t.pos) and controller.stop())
                di.ids.images.add_widget(image)

        [add_label(Label(
            text=u"[color=#FF0000]{0}[/color]".format(warn)))
            for warn in album['warnings']]

        # Add tracks
        for k, track in enumerate(album['tracks']):
            playing = bool(
                controller.playing_album == controller.album_index and
                controller.playing_track == k)
            pl_label = PlaylistLabel(
                controller=controller,
                text=track,
                album_index=index,
                track_index=k)
            add_label(pl_label)
            if playing:
                controller.set_selected(pl_label)

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

    back_colour = ListProperty([0, 0, 0, 0])

    def on_playing(self, widget, value):
        """ Respond to the change in state. """
        self.back_colour = [0.5, 0.5, 1, 0.3] if value else [0, 0, 0, 0]

    def on_touch_down(self, touch):
        """ Handle the event. """
        if self.collide_point(*touch.pos):
            touch.grab(self)

    def on_touch_up(self, touch):
        """ Handle the event. """
        if touch.grab_current is self:
            touch.ungrab(self)
            if self.collide_point(*touch.pos):
                if self.controller.sound is None:
                    self.controller.play_track(self)
                else:
                    self.controller.stop()


class Controller(EventDispatcher):
    """
    This class houses the logic and management of the current album and
    track index as well as the management of the audio.
    """
    album_index = NumericProperty(0)  # Currently displayed
    track_index = NumericProperty(0)  # Currently displayed
    playing_album = NumericProperty(0)  # Currently playing
    playing_track = NumericProperty(-1)  # Currently playing

    music_lib = ObjectProperty(None)
    album_screen = ObjectProperty(None)
    current_pl_label = None

    sound = None
    volume = NumericProperty(1.0)
    manual_stop = False
    '''
    Prevent the manual stopping of audio from moving to the next track, as
    if it's finished playing.
    '''

    def _sound_state(self, *args):
        if not self.manual_stop:
            if args[1] == "stop":
                if self._set_next_track():
                    self.play_track(None, self.playing_album,
                                    self.playing_track)
                    self.album_screen.show_album()

    def _set_next_track(self):
        """ Set the album and track index of the next legal track. """
        albums = self.music_lib.albums
        if len(albums[self.playing_album]['tracks']) > self.playing_track + 1:
            self.playing_track += 1
        elif len(albums) > self.playing_album + 1:
            self.playing_album += 1
            self.playing_track = 0
        else:
            return False
        return True

    def stop(self):
        """ Stop any currently playing track."""
        if self.sound is not None:
            self.manual_stop = True  # Prevent triggering track endings
            self.sound.stop()
            self.manual_stop = False
            self.sound = None

    def play_track(self, pl_label=None, album_index=0, track_index=0):
        """
        Play the track linked to be the PlaylistLabel, or the one specified
        by the indices.
        """
        if pl_label is None:
            self.playing_album = album_index
            self.playing_track = track_index
        else:
            self.playing_album = pl_label.album_index
            self.playing_track = pl_label.track_index
            self.set_selected(pl_label)

        if self.sound is not None:
            self.stop()

        album = self.music_lib.albums[self.playing_album]
        full_path = path.join(album['folder'], album['tracks'][
            self.playing_track])
        self.sound = SoundLoader.load(full_path)
        self.sound.play()
        self.sound.volume = self.volume
        self.sound.bind(state=self._sound_state)

    def move_next(self, advance):
        """
        Play the next track if advance in true, the previous track if False.
        If advance is None, the track info is not changed.
        """
        if advance is None:
            return

        album_index, track_index = self.album_index, self.track_index
        albums = self.music_lib.albums
        if advance:
            if album_index < len(albums):
                album_index = (album_index + 1) % len(albums)
                track_index = 0
        else:
            if 0 < album_index:
                album_index = (len(albums) + album_index - 1) % len(albums)
                track_index = 0
        self.album_index, self.track_index = album_index, track_index

    def get_currrent_album(self):
        """ Build and return a DisplayItem for the current album. """
        return self.music_lib.get_row_item(self.album_index, self)

    def on_volume(self, widget, value):
        """ Set the volume of the current tracks. """
        if self.sound is not None:
            self.sound.volume = value

    def set_selected(self, pl_label):
        """
        Set the PlaylistLabel as the one linked to the currently playing
        track.
        """
        if self.current_pl_label is not None:
            self.current_pl_label.playing = False

        self.current_pl_label = pl_label
        pl_label.playing = True


class AlbumScreen(Screen):
    """"
    The main screen showing a list of albums found.
    """
    music_lib = ObjectProperty(None)
    controller = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(AlbumScreen, self).__init__(**kwargs)
        self.music_lib = MusicLib()
        self.controller = Controller(music_lib=self.music_lib,
                                     album_screen=self)
        Clock.schedule_once(lambda dt: self.show_album())

    def show_album(self, advance=None):
        """
        Begins the timed display of albums. If *advance* is True, the next item
        is shown. If False, it moves back. If not specified, the current album
        is shown.
        """
        self.controller.move_next(advance)
        container = self.ids.row_container
        container.clear_widgets()
        if len(self.music_lib.albums) > self.controller.album_index:
            self.ids.header_label.text = "Music Library ({0} / {1})".format(
                self.controller.album_index + 1, len(self.music_lib.albums))

            container.add_widget(self.controller.get_currrent_album())
        else:
            container.add_widget(Label(text="No albums found"))

    def show_next(self):
        """ Show the next album. """
        self.show_album(True)

    def show_previous(self):
        """ Show the next album. """
        self.show_album(False)


class OptionScreen(Screen):
    pass


class FolderChecker(App):
    def build(self):
        return Builder.load_file('lib_checker.kv')

if __name__ == '__main__':
    FolderChecker().run()
