"""
This class houses the PlayList class for ZenPlayer
"""
from os import path, listdir
from kivy.uix.screenmanager import Screen
from kvy.lang import Builder


class PlayList(object):
    """
    Holds the current playlist class.
    """
    current = 0  # The index of the currently playing track in the queue
    queue = []  # contains a list of (filename, albumart) pairs

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
            return ""

    def get_current_info(self):
        """ Return a dictionary of information on the current track"""
        if len(self.queue) > self.current:
            return self._get_current_info()
        else:
            return {}

    def add_folder(self, folder):
        """ Add the specified folder to the queue """
        artwork = self._get_albumart(folder)
        for f in listdir(folder):
            if ".mp3" in f or ".ogg" in f or ".wav" in f:
                self.queue.append((path.join(folder, f), artwork))

    def move_next(self):
        """ Move the selected track to the next"""
        if len(self.queue) > self.current:
            self.current += 1
        else:
            self.current = -1

    @staticmethod
    def _get_albumart(folder):
        """
        Return the full image filename from the folder
        """
        for f in ["cover.jpg", "cover.png", "cover.bmp", "cover.jpeg"]:
            full_name = path.join(folder, f)
            if path.exists(full_name):
                return full_name
        return ""

    def _get_current_info(self):
        """
        Return a dictionary containing the metadata on the track """
        try:
            parts = self.queue[self.current][0].split("/")
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
<PlayListScreen>:
    BoxLayout:
        orientation: 'vertical'
        ListView:
            size_hint_y: 0.95
        BoxLayout:
            size_hint_y: 0.05
            orientation: 'horizontal'
            Padding: 10, 10, 10, 10
            Button:
                text: 'Back'
                on_release: root.back()
            Button
                text: 'Add and replace'
            Button
                text: 'Add'
''')


class PlayListScreen(Screen):
    """
    Displays the playlist along with some simple editing options.
    """
    def __init__(self, sm, **kwargs):
        self.sm = sm
        super(PlayListScreen, self).__init(**kwargs)

    def back(self):
        """ Return to the main playing screen """
        self.sm.current = "main"