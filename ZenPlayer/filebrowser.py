"""
Displays the file browsing screen for ZenPlayer
"""
from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty
from kivy.storage.jsonstore import JsonStore
from os.path import exists


class ZenFileBrowser(Screen):
    """
    Displays a file browsing screen for ZenPlayer
    """
    filechooser = ObjectProperty()

    def __init__(self, ctrl, playlist, **kwargs):
        self.ctrl = ctrl
        self.playlist = playlist
        self.initialized = False
        super(ZenFileBrowser, self).__init__(**kwargs)

    def add_files(self):
        """ Add any selected files/folders to the playlist"""
        for filefolder in self.filechooser.selection:
            self.playlist.add_files(filefolder)

    def add_replace(self):
        """ Add amy selected files/folders to the playlist removing any that
        already exist """
        state = self.c
        self.playlist.clear_files()
        self.add_files()

    def on_enter(self):
        """ The filebrowser screen is being opened """
        if not self.initialized:
            self.initialized = True
            store = JsonStore("zenplayer.json")
            if store.exists("filebrowser"):
                if "path" in store.get("filebrowser").keys():
                    file_path = store.get("filebrowser")["path"]
                    if exists(file_path):
                        self.filechooser.path = file_path

    def on_leave(self):
        """ The filebrowser screen is being closed """
        if len(self.filechooser.selection) > 0:
            store = JsonStore("zenplayer.json")
            store.put("filebrowser", path=self.filechooser.selection[0])
