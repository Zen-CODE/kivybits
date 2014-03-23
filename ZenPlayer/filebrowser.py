"""
Displays the file browsing screen for ZenPlayer
"""
from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from kivy.properties import ObjectProperty


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
        BoxLayout:
            orientation: 'horizontal'
            padding: 10, 10, 10, 10
            size_hint_y: 0.1
            Button:
                text: 'Back'
                on_release: root.sm.current = "main"
            Button:
                text: "Add and replace"
            Button:
                text: "Add"
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

    def print_status(self):
        #TODO: Remove
        print "path=", self.filechooser.path
        print "selection=", str(self.filechooser.selection)
        print "fired"
