"""
This class houses the PlayList class for ZenPlayer
"""
from kivy.uix.screenmanager import Screen
from kivy.properties import (ObjectProperty, NumericProperty, BooleanProperty,
                             ListProperty)
from os import sep, path, listdir
from kivy.logger import Logger
from os.path import exists
from kivy.lang import Builder
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.event import EventDispatcher


class PlayList(object):
    """
    Holds the current playlist class.
    """
    current = 0  # The index of the currently playing track in the queue
    queue = []  # contains a list of (filename, albumart) pairs
    art_names = ["cover.jpg", "cover.png", "cover.bmp", "cover.jpeg"]

    def __init__(self, store):

        super(PlayList, self).__init__()
        self._load(store)

    def _load(self, store):
        """ Initialize and load previous state """
        # See if there is an existing playlist to restore
        if store.exists("playlist"):
            if "items" in store.get("playlist"):
                items = store.get("playlist")["items"]
                k = 1
                while "item" + str(k) in items.keys():
                    if exists(items["item" + str(k)]):
                        self.add_files(items["item" + str(k)])
                    k += 1
            self.current = store.get("playlist")["current"]
            if self.current >= len(self.queue) - 1:
                self.current = 0

    def get_current_file(self):
        """Returns the filename of the current audio file."""
        if len(self.queue) > self.current:
            return self.queue[self.current][0]
        else:
            return ""

    def get_current_art(self):
        """Return the filename for the artwork associated with the currently
        playing file."""
        if len(self.queue) > self.current:
            return self.queue[self.current][1]
        else:
            return u"images/zencode.jpg"

    def get_current_info(self):
        """ Return a dictionary of information on the current track"""
        if len(self.queue) > self.current:
            return self.get_info(self.queue[self.current][0])
        else:
            return {}

    def add_files(self, filefolder):
        """ Add the specified folder to the queue """
        # To convert to pure asc as the logger does not handle unicode
        Logger.info("playlist.py: processing {0}".format(
            filefolder.encode('ascii', 'replace')))
        if path.isdir(filefolder):
            for f in sorted(listdir(filefolder)):
                self.add_files(path.join(filefolder, f))
        elif filefolder[-3:] in ["mp3", "ogg", "wav", "m4a"]:
            self.queue.append((filefolder, self._get_albumart(filefolder)))

    def clear_files(self):
        """ Clear the existing playlist"""
        self.queue = []
        self.current = 0

    def move_next(self):
        """ Move the selected track to the next"""
        if len(self.queue) > self.current:
            self.current += 1
        elif len(self.queue) > 0:
            self.current = 1
        else:
            self.current = 0

    def move_previous(self):
        """ Move the selected track to the previous entry"""
        if 0 < self.current:
            self.current += -1

    def save(self, store):
        """ The playlist screen is being closed """
        all_items = {}
        for k, item in enumerate(self.queue):
            all_items.update({"item" + str(k + 1): item[0]})
        store.put("playlist",
                  current=self.current,
                  items=all_items)

    def set_index(self, index):
        """ Set the currently selected track to the one specified by the index
        """
        if index < len(self.queue):
            self.current = index

    @staticmethod
    def _get_albumart(audiofile):
        """
        Return the full image filename from the folder
        """
        folder = audiofile[0: audiofile.rfind(sep)]
        for art in PlayList.art_names:
            full_name = path.join(folder, art)
            if path.exists(full_name):
                return full_name
        return "images/zencode.jpg"

    @staticmethod
    def get_info(filename):
        """
        Return a dictionary containing the metadata on the track """
        try:
            parts = filename.split(sep)
            return {
                "artist": parts[-3],
                "album": parts[-2],
                "file": parts[-1]}
        except IndexError:
            return {
                "artist": "-",
                "album": "-",
                "file": "-"}


class PlayListScreen(Screen):
    """
    Displays the playlist along with some simple editing options.
    """
    listview = ObjectProperty()

    def __init__(self, sm, ctrl, playlist, **kwargs):
        Builder.load_file("playlist.kv")
        self.sm = sm
        self.playlist = playlist
        self.ctrl = ctrl
        super(PlayListScreen, self).__init__(**kwargs)

        self.items_per_page = 10
        self.num_pages = len(self.playlist.queue) // self.items_per_page + 1
        self.current_page = 1

    def on_enter(self):
        """ Repopulate the view area and setup the display. """
        self.ids.page_count.text = str(self.current_page)
        self.ids.page_count_suffix.text = "of {0}".format(self.num_pages)
        self.show_page(self.current_page)

    def show_page(self, page_no):
        """ Show the playlist items on the current page. """

        def init_page(_page_no):
            """ Initialise the display and controls. """
            self.current_page = _page_no
            self.ids.album_col.clear_widgets()
            self.ids.file_col.clear_widgets()
            self.ids.page_count.text = str(page_no)

        def display_page(start, end, queue):
            """
            Add the items from the start to end index to the display
            """
            info, cover = self.playlist.get_info, ""
            for i in range(start, end):
                new_cover = queue[i][1]
                if new_cover != cover:
                    cover = new_cover
                    self.ids.album_col.add_widget(
                        PlaylistImage(source=cover,
                                      ctrl=self.ctrl,
                                      playlist_index=i))

                self.ids.file_col.add_widget(
                    PlaylistLabel(
                        text=info(queue[i][0])['file'],
                        ctrl=self.ctrl,
                        playlist_index=i,
                        selected=bool(i==self.playlist.current)))

        queue = self.playlist.queue
        start = (page_no - 1) * self.items_per_page
        end = start + self.items_per_page
        if end > len(queue):
            end = len(queue)

        init_page(page_no)
        display_page(start, end, queue)

    def show_next_page(self, next_page=True):
        """ Show the next/previous page. """
        page = self.current_page + 1 if next_page else self.current_page - 1
        if 0 < page <= self.num_pages:
            self.show_page(page)


class PlaylistItem(EventDispatcher):
    """
    A mixin class for adding playlist click/play behaviour.
    """

    playlist_index = NumericProperty()
    ctrl = ObjectProperty()
    selected = BooleanProperty(False)

    def on_touch_down(self, touch):
        """ Add support for clicking to play. """
        self.selected = self.collide_point(*touch.pos)
        if self.selected:
            self.ctrl.play_index(self.playlist_index)


class PlaylistImage(PlaylistItem, Image):
    pass


class PlaylistLabel(PlaylistItem, Label):
    """
    The label shown in the playlist giving the details of the track.
    """
    back_color = ListProperty([0, 0, 0, 0])

    def on_selected(self, widget, value):
        """ The label has been selected. Change the visuals accordingly. """
        self.back_color = [0.5, 0.5, 1, 0.5] if value else [0, 0, 0, 0]
