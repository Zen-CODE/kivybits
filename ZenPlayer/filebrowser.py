"""
Displays the file browsing screen for ZenPlayer
"""
from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from kivy.properties import ObjectProperty
#from kivy.uix.popup import Popup
#from kivy.clock import Clock


Builder.load_string('''
<ZenFileBrowser>:
    filechooser: filechooser

    BoxLayout:
        orientation: 'vertical'
        #FileChooserIconView:
        BoxLayout:
            size_hint_y: 0.1
            Button:
                text: "Status"
                on_release: root.print_status()
        FileChooserListView:
            id: filechooser
            size_hint_y: 0.8
            dirselect: True
            multiselect: True
            #TODO: Remove
            path: '/media/Zen320/Zen/Music'
        BoxLayout:
            orientation: 'horizontal'
            padding: 10, 10, 10, 10
            size_hint_y: 0.1
            Button:
                text: 'Back'
                on_release: root.sm.current = "main"
            Button:
                text: "Add and replace"
                on_release: root.add_replace()
            Button:
                text: "Add"
                on_release: root.add_files()
''')


class ZenFileBrowser(Screen):
    """
    Displays a file browsing screen for ZenPlayer
    """
    filechooser = ObjectProperty()


    def __init__(self, sm, playlist, **kwargs):
        self.sm = sm
        self.playlist = playlist
        super(ZenFileBrowser, self).__init__(**kwargs)

    def add_files(self):
        #TODO: Remove
        #print "path=", self.filechooser.path
        for filefolder in self.filechooser.selection:
            print "Adding ", filefolder
            self.playlist.add_files(filefolder)

    def add_replace(self):
        # TODO
        self.playlist.clear_files()
        self.add_files()

