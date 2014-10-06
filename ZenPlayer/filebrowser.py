"""
Displays the file browsing screen for ZenPlayer
"""
from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty
from os.path import exists
from audioplayer import Sound
from kivy.lang import Builder


class ZenFileBrowser(Screen):
    """
    Displays a file browsing screen for ZenPlayer
    """
    filechooser = ObjectProperty()

    def __init__(self, ctrl, playlist, store, **kwargs):
        Builder.load_file('filebrowser.kv')
        self.ctrl = ctrl
        self.playlist = playlist
        super(ZenFileBrowser, self).__init__(**kwargs)
        self._init(store)

    def _init(self, store):
        """
        The filebrowser screen is being opened for the first time.
        Initialize the paths to the one stored.
        """
        if store.exists("filebrowser"):
            if "path" in store.get("filebrowser").keys():
                file_path = store.get("filebrowser")["path"]
                if exists(file_path):
                    self.filechooser.path = file_path

    def add_files(self):
        """ Add any selected files/folders to the playlist"""
        for filefolder in self.filechooser.selection:
            self.playlist.add_files(filefolder)

    def add_replace(self):
        """ Add any selected files/folders to the playlist removing any that
        already exist """
        state = Sound.state
        if state == "playing":
            self.ctrl.stop()
        self.playlist.clear_files()
        self.add_files()
        self.ctrl.play_pause()

    def folder_up(self):
        """ Move a single folder up """
        # TODO: Check this for windows
        print "folderUp fired" + str(self.filechooser.path)
        path = self.filechooser.path
        if path.rfind('/') > 1:
            self.filechooser.path = path[:path.rfind('/')]


    def save(self, store):
        """ Save the file browser state """
        if len(self.filechooser.selection) > 0:
            store.put("filebrowser", path=self.filechooser.selection[0])
