# -*- coding: utf-8 -*-
"""
Test

"""


import kivy
kivy.require('1.0.7')

from kivy.app import App
from kivy.clock import Clock
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import AsyncImage


from kivy.uix.widget import Widget
from kivy.uix.scatter import ScatterPlane
from kivy.uix.stencilview import StencilView


from kivy.config import Config
Config.set('graphics', 'width', '1024')
Config.set('graphics', 'height', '768')



class MyScatter(ScatterPlane):
    def load_images(self, *args):
        with self.canvas:
            for x in range(0, 2):
                for y in range(0, 2):
                    source="http://b.tile.openstreetmap.org/1/%s/%s.png" % (x, y)
                    r = 256 / self.scale
                    AsyncImage(source=source, mipmap=False, allow_stretch=True, pos=(x*256 , (1-y)*256), size=(r, r))


class MyStencil(StencilView):
    def __init__(self, **kwargs):
        super(MyStencil, self).__init__(**kwargs)
        self.map = MyScatter(**kwargs)
        self.add_widget(self.map)



class MyApp(App):


    def build(self):
        layout = FloatLayout()
        self.mv = MyStencil()
        layout.add_widget(self.mv)
        return layout

    def appInit(self, dt):
        self.mv.map.load_images()

    def on_start(self):
        Clock.schedule_once(self.appInit)


if __name__ in ('__android__','__main__'):
    MyApp().run()
