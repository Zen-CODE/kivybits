"""
ZenPlayer
=========

ZenPlayer is a minimal audio/video player that explores the ability of the
Kivy framework.

"""
__author__ = 'ZenCODE'

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty
from os import path

Builder.load_string('''
<PlayingScreen>:
    album_image: album_image
    BoxLayout:
        orientation: "horizontal"
        BoxLayout:
            orientation: "vertical"
            size_hint_x: 0.1
        Image:
            id: album_image
            size_hint_x: 0.8
        BoxLayout:
            orientation: "vertical"
            size_hint_x: 0.1
''')


class PlayingScreen(Screen):
    """
    The main screen that shows whats currently playing
    """
    album_image = ObjectProperty()

    def _set_albumart(self, folder):
        for file in ["cover.jpg", "cover.png", "cover.bmp", "cover.jpeg"]:
            print path.join(folder, file)
            full_name = path.join(folder, file)
            if path.exists(full_name):
                self.album_image.source = full_name
                break

    def play_folder(self, folder):
        self._set_albumart(folder)


class ZenPlayer(App):
    def build(self):
        sm = ScreenManager()
        playing = PlayingScreen()
        #TODO: Remove
        playing.play_folder('/media/Zen320/Zen/Music/MP3/In Flames/Colony')

        sm.switch_to(playing)
        return sm

ZenPlayer().run()


