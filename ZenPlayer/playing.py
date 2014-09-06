from kivy.properties import ObjectProperty
from kivy.clock import Clock
from kivy.uix.screenmanager import Screen
from controller import Controller


class PlayingScreen(Screen):
    """
    The main screen that shows whats currently playing
    """
    #TODO : Document properties once stable
    album_image = ObjectProperty()
    but_playpause = ObjectProperty()
    info_label = ObjectProperty()
    volume_slider = ObjectProperty()
    progress_slider = ObjectProperty()
    time_label = ObjectProperty()
    ctrl = None  #Controller()

    def __init__(self, sm, **kwargs):
        self.ctrl = Controller(sm)
        super(PlayingScreen, self).__init__(**kwargs)
        Clock.schedule_interval(self._update_progress, 1/25)
        self.volume_slider.value = self.ctrl.volume

    def init_display(self):
        """ Initialize the display """
        self.album_image.source = self.ctrl.get_current_art()
        info = self.ctrl.get_current_info()
        if info:
            self.info_label1.text = info["artist"]
            self.info_label2.text = info["album"]
            self.info_label3.text = info["file"]

    def save(self):
        """ Save the current playlist state """
        self.ctrl.save()

    def _update_progress(self, dt):
        """ Update the progressbar  """
        #if Sound.state == "playing":
        if self.ctrl.state == "playing":
            pos, length = Sound.get_pos_length()
            if length > 0:
                self.progress_slider.value = pos / length

                self.time_label.text = "{0}m {1:02d}s / {2}m {3:02d}s".format(
                    int(pos / 60),
                    int(pos % 60),
                    int(length / 60),
                    int(length % 60))
