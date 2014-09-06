"""
ZenPlayer
=========

ZenPlayer is a minimal audio/video player that explores the ability of the
Kivy framework.

"""
__author__ = 'ZenCODE'

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import ObjectProperty, StringProperty
from controller import Controller


Builder.load_file('style.kv')


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


class ZenPlayer(App):
    """
    The App initialisation class
    """
    ctrl = None  # Reference to the controller (for saving)

    def on_pause(self):
        """ Enable support for pause """
        return True

    def on_resume(self):
        """ Enable support for resume """
        pass

    def build(self):
        """ Build the app and return the screen manager """
        self.ctrl = Controller()
        return self.ctrl.sm

    def on_stop(self):
        """The app is closing. Save the state."""
        self.ctrl.save()

ZenPlayer().run()
