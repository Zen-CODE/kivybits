"""
Displays the file browsing screen for ZenPlayer
"""
from kivy.uix.screenmanager import Screen
from kivy.lang import Builder


Builder.load_string('''
<ZenFileBrowser>:
    BoxLayout:
        orientation: 'vertical'
        Label:
            size_hint_y: 0.9
            text: "Place holder"
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
    def __init__(self, sm, playlist, **kwargs):
        self.sm = sm
        self.playlist = playlist
        super(ZenFileBrowser, self).__init__(**kwargs)
