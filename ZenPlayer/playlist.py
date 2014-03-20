"""
This class houses the PlayList class for ZenPlayer
"""
from os import path, listdir


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
