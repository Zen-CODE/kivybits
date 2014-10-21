"""
This class houses the PlayList class for ZenPlayer
"""
from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty
from os import sep, path, listdir
from kivy.logger import Logger
from kivy.adapters.dictadapter import DictAdapter
from kivy.uix.listview import SelectableView
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.listview import CompositeListItem
from kivy.properties import StringProperty, ListProperty
from os.path import exists
from kivy.lang import Builder
from kivy.uix.button import ButtonBehavior
from kivy.clock import Clock


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

    def __init__(self, sm, ctrl, playlist, **kwargs):
        Builder.load_file("playlist.kv")
        self.sm = sm
        self.playlist = playlist
        self.ctrl = ctrl
        super(
            PlayListScreen, self).__init__(**kwargs)

    def on_enter(self):
        """ Repopulate the listview """
        info = self.playlist.get_info
        data = {str(i): {'text': item[0],
                         'source': item[1],
                         'album': info(item[0])["album"],
                         'track': info(item[0])["file"],
                         'is_selected': bool(i == self.playlist.current)}
                for i, item in enumerate(self.playlist.queue)}

        def args_converter(row_index, item):
            return {'text': item['text'],
                    'size_hint_y': None,
                    'height': "50dp",
                    'cls_dicts': [{'cls': ZenListImage,
                                   'kwargs': {'source': item['source'],
                                              'size_hint_x': 0.1,
                                              'row_index': row_index}},
                                  {'cls': ZenListButton,
                                   'kwargs': {'text': item['track'],
                                              'is_representing_cls': True,
                                              'size_hint_x': 0.55,
                                              'row_index': row_index}},
                                  {'cls': ZenListButton,
                                   'kwargs': {'text': item['album'],
                                              'size_hint_x': 0.35,
                                              'row_index': row_index}}]}

        dict_adapter = DictAdapter(
            sorted_keys=[str(i) for i in range(len(self.playlist.queue))],
            data=data,
            selection_mode='single',
            args_converter=args_converter,
            propagate_selection_to_data=True,
            cls=ZenListItem)

        self.listview.adapter = dict_adapter
        dict_adapter.bind(on_selection_change=self.selection_changed)

    def selection_changed(self, adapter):
        """ The selection has changed. Start playing the selected track """
        if len(adapter.selection) > 0:
            print "On selection changed {0}".format(adapter.selection[0])
            selection = adapter.selection[0]
            if isinstance(selection, ZenListItem):
                row_index = selection.children[0].row_index
            else:
                row_index = selection.row_index
            if row_index != self.playlist.current:
                self.ctrl.play_index(row_index)

Builder.load_string('''
<ZenSelectableView>:
    padding: 5, 5, 5, 5
    canvas:
        Color:
            rgba: root.background_color
        Rectangle:
            pos: self.pos
            size: self.size
<ZenListImage>:
    Image:
        source: root.source
<ZenListButton>:
    Label:
        id: label
''')


class ZenSelectableView(SelectableView, ButtonBehavior, BoxLayout):
    """
    This defines the base class for the Zen Playlist items elements. It handles
    the background drawing and provide a BoxLayout for subclass to add
    additional elements
    """
    selected_color = [0.5, 0.5, 1, 0.7]
    deselected_color = [0, 0, 0, 1]
    background_color = ListProperty([0, 0, 0, 1])

    def __init__(self, **kwargs):
        self.row_index = kwargs.pop('row_index')
        super(ZenSelectableView, self).__init__(**kwargs)

    def select(self, *args):
        self.background_color = self.selected_color
        if isinstance(self.parent, CompositeListItem):
            self.parent.select_from_child(self, *args)

    def deselect(self, *args):
        self.background_color = self.deselected_color
        if isinstance(self.parent, CompositeListItem):
            self.parent.deselect_from_child(self, *args)

    def select_from_composite(self, *args):
        self.background_color = self.selected_color

    def deselect_from_composite(self, *args):
        self.background_color = self.deselected_color


class ZenListImage(ZenSelectableView):
    """ This item displays the image but functions as a selectable list item
    """
    source = StringProperty()


class ZenListButton(ZenSelectableView):
    """
    The text items displayed in the ZenPlaylist
    """
    text = StringProperty('')

    def on_text(self, widget, value):
        """
        Set the text of the label. This is fired before the objects have
        been fully loaded, so delay the call using the Clock
        """
        def set_text(text):
            self.ids.label.text = text
        Clock.schedule_once(lambda dt: set_text(value))


class ZenListItem(CompositeListItem):
    """
    This item view composes itself out of a image and two ListItem subclasses
    for displaying artist and track information.
    """
    def select(self, selected=True):
        """
        Propagate selection to children
        """
        for child in self.children:
            child.select()

    def deselect(self):
        """
        Propagate deselection to children components
        """
        for child in self.children:
            child.deselect()
