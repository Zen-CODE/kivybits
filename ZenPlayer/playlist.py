"""
This class houses the PlayList class for ZenPlayer
"""
from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty
from os import sep, path, listdir
from kivy.logger import Logger
from kivy.adapters.dictadapter import DictAdapter
from kivy.uix.listview import ListItemButton
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.listview import CompositeListItem
from kivy.properties import StringProperty
from os.path import exists
from kivy.lang import Builder


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
            return "images/zencode.jpg"

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
        elif ".mp3" in filefolder or ".ogg" in filefolder or\
                ".wav" in filefolder:
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
        except:
            return {
                "artist": "-",
                "album": "-",
                "file": "-"}


class PlayListScreen(Screen):
    """
    Displays the playlist along with some simple editing options.
    """
    listview = ObjectProperty()

    def __init__(self, sm, playlist, **kwargs):
        Builder.load_file("playlist.kv")
        self.sm = sm
        self.playlist = playlist
        super(
            PlayListScreen, self).__init__(**kwargs)

    def on_enter(self):
        """ Repopulate the listview """
        info = self.playlist.get_info
        data = {str(i): {'text': item[0],
                         'source': item[1],
                         'album': info(item[0])["album"],
                         'track': info(item[0])["file"]}
                for i, item in enumerate(self.playlist.queue)}

        args_converter = lambda row_index, rec: \
            {'text': rec['text'],
             'size_hint_y': None,
             'height': 50,
             'cls_dicts': [{'cls': ZenListImage,
                            'kwargs': {'source': rec['source'],
                                       'size_hint_x': 0.1,
                                       'row_index': row_index}},
                           {'cls': ZenListButton,
                            'kwargs': {'text': rec['track'],
                                       'is_representing_cls': True,
                                       'size_hint_x': 0.55,
                                       'row_index': row_index}},
                           {'cls': ZenListButton,
                            'kwargs': {'text': rec['album'],
                                       'size_hint_x': 0.35,
                                       'row_index': row_index}}]}

        dict_adapter = DictAdapter(
            sorted_keys=[str(i) for i in range(len(self.playlist.queue))],
            data=data,
            selection_mode='single',
            args_converter=args_converter,
            cls=ZenListItem)

        # args_converter = lambda row_index, rec: \
        #     {'text': rec['text'],
        #      'size_hint_y': None,
        #      'height': 50}
        #
        # dict_adapter = DictAdapter(
        #     sorted_keys=[str(i) for i in range(len(self.playlist.queue))],
        #     data=data,
        #     selection_mode='single',
        #     args_converter=args_converter,
        #     cls=ListItemButton)


        self.listview.adapter = dict_adapter
        dict_adapter.bind(on_selection_change=self.selection_changed)

    def back(self):
        """ Return to the main playing screen """
        self.sm.current = "main"

    def selection_changed(self, adapter):
        print "Selection changed - " + str(adapter.selection)
        if len(adapter.selection) > 0:
            #print "Row index=", str(adapter.selection[0].row_index)
            print "Row index=", str(adapter.selection[0])

Builder.load_string('''
<ZenListImage>:
    padding: 5, 5, 5, 5
    Image:
        source: root.source
''')

# Here we define the colours of the playlist (ZenList*) items
SELECTED_COLOR = [0.5, 0.5, 1, 0.7]
DESELECTED_COLOR = [0, 0, 0, 1]


class ZenListImage(BoxLayout, ListItemButton):
    """ This item displays the image but functions as a selectable list item """
    source = StringProperty()

    def __init__(self, **kwargs):
        self.row_index = kwargs.pop('row_index')
        super(ZenListImage, self).__init__(**kwargs)
        # TODO: Customize background. Could not get this to work properly with
        #       the button drawing
        # self.selected_color = SELECTED_COLOR
        # self.deselected_color = DESELECTED_COLOR
        #self.background_down = ""
        #self.background_normal = ""

    def on_text(self, *args):
        """ Prevent the button from displaying text """
        self.text = ""
        return True


class ZenListButton(ListItemButton):
    def __init__(self, **kwargs):
        self.row_index = kwargs.pop('row_index')
        super(ZenListButton, self).__init__(**kwargs)
        # TODO: Customize background. Could not get this to work properly with
        #       the button drawing
        # self.selected_color = SELECTED_COLOR
        # self.deselected_color = DESELECTED_COLOR
        #self.background_normal = 'images/black.png'
        #self.background_down = 'images/black.png'


class ZenListItem(CompositeListItem):
    pass
