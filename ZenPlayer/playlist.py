"""
This class houses the PlayList class for ZenPlayer
"""
from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from kivy.properties import ObjectProperty
from os import sep, path, listdir
from kivy.logger import Logger
from kivy.adapters.dictadapter import DictAdapter
from kivy.storage.jsonstore import JsonStore


class PlayList(object):
    """
    Holds the current playlist class.
    """
    current = 0  # The index of the currently playing track in the queue
    queue = []  # contains a list of (filename, albumart) pairs
    art_names = ["cover.jpg", "cover.png", "cover.bmp", "cover.jpeg"]
    store = JsonStore("zenplayer.json")

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
            return "images/zencode.jpg"

    def get_current_info(self):
        """ Return a dictionary of information on the current track"""
        if len(self.queue) > self.current:
            return self._get_info(self.queue[self.current][0])
        else:
            return {}

    def add_files(self, filefolder):
        """ Add the specified folder to the queue """
        Logger.info("playlist.py: processing {0}".format(filefolder))
        if path.isdir(filefolder):
            for f in sorted(listdir(filefolder)):
                self.add_files(path.join(filefolder, f))
        elif ".mp3" in filefolder or ".ogg" in filefolder or\
                ".wav" in filefolder:
            self.queue.append((filefolder, self._get_albumart(filefolder)))

    def clear_files(self):
        """ Clear the existing playlist"""
        self.queue = []

    def move_next(self):
        """ Move the selected track to the next"""
        if len(self.queue) > self.current:
            self.current += 1
        else:
            self.current = -1

    def move_previous(self):
        """ Move the selected track to the previous entry"""
        if 0 < self.current:
            self.current += -1

    def save(self):
        """ The playlist screen is being closed """
        if len(self.queue) > -1:
            all_items = {}
            for k, item in enumerate(self.queue):
                all_items.update({"item" + str(k + 1): item[0]})
            self.store.put("playlist", current=self.current,
                      items=all_items)

    def load(self):
        """ Initialize and load previous state """
        # See if there is an existing playlist to restore
        if self.store.exists("playlist"):
            if "items" in self.store.get("playlist"):
                items = self.store.get("playlist")["items"]
                k = 1
                while "item" + str(k) in items.keys():
                    self.add_files(items["item" + str(k)])
                    k += 1
            self.current = self.store.get("playlist")["current"]
            if self.current > len(self.queue):
                self.current = -1


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
    def _get_info(filename):
        """
        Return a dictionary containing the metadata on the track """
        try:
            parts = filename.split(sep)
            return {
                "artist": parts[-3],
                "album": parts[-2],
                "file": parts[-1]}
        except:
            return {
                "artist": "-",
                "album": "-",
                "file": "-"}


Builder.load_string('''
[ZenListItem@SelectableView+BoxLayout]:
    orientation: 'horizontal'
    size_hint_y: ctx.size_hint_y
    height: "25sp"
    Image:
        size_hint_x: 0.1
        source: ctx.source
    Label:
        size_hint_x: 0.4
        text: ctx.album
    Label
        size_hint_x: 0.5
        text: ctx.file

<PlayListScreen>:
    listview: listview

    BoxLayout:
        orientation: 'vertical'
        ListView:
            id: listview
            size_hint_y: 0.9
        BoxLayout:
            size_hint_y: 0.1
            orientation: 'horizontal'
            padding: 10, 10, 10, 10
            Button:
                text: 'Back'
                on_release: root.back()
''')


class PlayListScreen(Screen):
    """
    Displays the playlist along with some simple editing options.
    """
    listview = ObjectProperty()

    def __init__(self, sm, playlist, **kwargs):
        self.sm = sm
        self.playlist = playlist
        super(PlayListScreen, self).__init__(**kwargs)

    def on_enter(self):
        """ Repopulate the listview """
        info = self.playlist._get_info
        data = {str(i - 1): {'text': item[0],
                             'source': item[1],
                             'album': info(item[0])["album"],
                             'file': info(item[0])["file"]}
                for i, item in enumerate(self.playlist.queue)}
        list_item_args_converter = lambda row_index, rec: {'text': rec['text'],
                                'source': rec['source'],
                                'album': rec['album'],
                                'file': rec['file'],
                                'size_hint_y': None,
                                'height': "25sp"}
        dict_adapter = DictAdapter(
            sorted_keys=[str(i - 1) for i in range(len(self.playlist.queue))],
            data=data,
            args_converter=list_item_args_converter,
            template='ZenListItem')
        self.listview.adapter = dict_adapter

    def back(self):
        """ Return to the main playing screen """
        self.sm.current = "main"
