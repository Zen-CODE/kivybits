#!/usr/bin/env python
# -*- coding: utf-8 -*-

from kivy.base import runTouchApp
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.boxlayout import BoxLayout

#widget = Label(text='/media/Zen320/Zen/Music/MP3/Bob Sinclar/Champs ElyséEs/cover.jpg')
box = BoxLayout()
box.add_widget(
    Image(source='/media/Zen320/Zen/Music/MP3/Bob Sinclar/Champs ElyséEs/cover.jpg'))
box.add_widget(
    Image(source='/media/Zen320/Zen/Music/MP3/Bob Sinclar/Champs ElyséEs/cover.jpg'))

runTouchApp(box)
