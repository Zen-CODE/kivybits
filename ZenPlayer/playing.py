from kivy.properties import ObjectProperty, StringProperty
from kivy.clock import Clock
from kivy.uix.screenmanager import Screen
from audioplayer import Sound
from kivy.lang import Builder
from kivy.uix.floatlayout import FloatLayout
from kivy3dgui.layout3d import Layout3D


class MediaButton(FloatLayout):
    """
    A pretty, shiny button showing the player controls
    """
    source = StringProperty('')
    image = ObjectProperty()

    def __init__(self, **kwargs):
        """ Override the constructor so we can register an event """
        super(MediaButton, self).__init__(**kwargs)
        self.register_event_type("on_click")

    def on_source(self, widget, value):
        """ The 'source' property for the image has changed. Change it. """
        self.image.source = value

    def on_click(self):
        """ The button has been clicked. """
        pass


class PlayingScreen(Screen):
    """
    The main screen that shows whats currently playing
    """
    album_image = ObjectProperty()
    but_playpause = ObjectProperty()
    info_label = ObjectProperty()
    volume_slider = ObjectProperty()
    progress_slider = ObjectProperty()
    time_label = ObjectProperty()
    ctrl = None  # The Controller

    def __init__(self, ctrl, **kwargs):
        Builder.load_file("playing.kv")
        self.ctrl = ctrl
        super(PlayingScreen, self).__init__(**kwargs)
        Clock.schedule_interval(self._update_progress, 1/25)
        self.volume_slider.value = self.ctrl.volume
        self.init_display()

    def init_display(self):
        """ Initialize the display """
        self.album_image.source = self.ctrl.get_current_art()
        info = self.ctrl.get_current_info()
        if info:
            self.info_label1.text = info["artist"]
            self.info_label2.text = info["album"]
            self.info_label3.text = info["file"]

        from kivy.animation import Animation
        anims = Animation(rotate=(360.0, 1, 0, 0), duration=5, t='in_quad') + \
            Animation(rotate=(0.0, 1, 0, 0), duration=5, t='in_quad') + \
            Animation(rotate=(360.0, 0, 1, 0), duration=5, t='in_quad') + \
            Animation(rotate=(0.0, 0, 1, 0), duration=5, t='in_quad')
        anims.repeat = True
        anims.start(self.ids.node)

    def on_sound_state(self, state):
        """ React to the change of state of the sound """
        if state == "playing":
            self.but_playpause.source = "images/pause.png"
            self.init_display()
        else:
            self.but_playpause.source = "images/play.png"

    def _update_progress(self, dt):
        """ Update the progressbar  """
        if Sound.state == "playing":
            pos, length = Sound.get_pos_length()
            if length > 0:
                self.progress_slider.value = pos / length

                self.time_label.text = "{0}m {1:02d}s / {2}m {3:02d}s".format(
                    int(pos / 60),
                    int(pos % 60),
                    int(length / 60),
                    int(length % 60))
