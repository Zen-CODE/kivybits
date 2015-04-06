"""
ZenPlayer
=========

ZenPlayer is a minimal audio/video player that explores the ability of the
Kivy framework.

"""
__author__ = 'ZenCODE'

from kivy.app import App
from controller import Controller


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
