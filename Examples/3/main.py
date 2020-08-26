# File name: mycharts.py
import random

import kivy
kivy.require('1.7.0')
from kivy.app import App
from kivy.uix.anchorlayout import AnchorLayout
from kivy.clock import Clock
from kivy.properties import StringProperty
from kivy.graphics import Color, Ellipse
from kivy.uix.image import Image

#from widgetshot import widgetshot

# This is Mathieu Virbel's answer to a question on kivy-users forum
# about how to save a widget's canvas contents as a .png file
import pygame 
from kivy.graphics.fbo import Fbo 
from kivy.core.gl import glReadPixels, GL_RGBA, GL_UNSIGNED_BYTE 
from kivy.graphics.texture import Texture 

def widgetshot(widget, filename='output.png'): 
# detach the widget from the parent 
    parent = widget.parent
    if parent:
        parent.remove_widget(widget)

    # put the widget canvas on a Fbo
    texture = Texture.create(size=widget.size, colorfmt='rgb')
    fbo = Fbo(size=widget.size, texture=texture)
    fbo.add(widget.canvas)

    # clear the fbo background
    fbo.bind()
    fbo.clear_buffer()
    fbo.release()

    # draw!
    fbo.draw()

    # get the fbo data
    fbo.bind()
    data = glReadPixels(0, 0, widget.size[0], widget.size[1], GL_RGBA, GL_UNSIGNED_BYTE)
    fbo.release()

    # save to a file
    surf = pygame.image.fromstring(data, widget.size, 'RGBA', True)
    pygame.image.save(surf, filename)

    # reattach to the parent
    if parent:
        parent.add_widget(widget)

    return True


from juts_utils import *

#juts_deb()

Builder.load_string('''
<MyCharts>:
#timer_label: time_label.text
    BoxLayout:
        id: box1
        #rows: 1
        #cols: 2
        orientation: 'horizontal'
        XAnchorLayout:
            width: 100
            size_hint: None,1
            anchor_x: 'left'
            anchor_y: 'top'
        GridLayout:
            id: gr2
            rows: 3
            cols: 1
            #padding: (self.width - self.cols*draw.width)/2, (self.height - self.rows*draw.height)/2
        Button:
            id: draw
            text: 'Draw'
            size_hint: None,None
            on_press: root.draw()
        Button:
            text: 'Save'
            size_hint: None,None
            on_press: root.save()
        Button:
            text: 'Load'
            size_hint: None,None
            on_press: root.load()
        Label:
            #width: int(0.9*root.width)
            #size_hint: 0.9,None
            id: chart
''')

class MyCharts(AnchorLayout):
    def draw(self):
        with self.canvas:
            d = random.randrange(1., 100.)
            #Color(random.randrange(0,2), random.randrange(0,2), random.randrange(0,2))
            Color(0,1,0)
            Ellipse(pos=(random.randrange(0,self.width), random.randrange(0,self.height)), size=(d, d))
        def save(self):
            widgetshot(self, filename = juts_gsd() + 'mycharts.png')
            #self.ids.score_all.text = '%d/%d' % (self.succ_count,self.try_count)

        def load(self):
            with self.canvas:
                Image(source='mycharts.png')


class MyChartsApp(App):
    def build(self):
        return MyCharts()

if __name__=="__main__":
    MyChartsApp().run()