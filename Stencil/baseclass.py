from kivy.uix.relativelayout import RelativeLayout
from kivy.properties import OptionProperty, StringProperty
from kivy.lang import Builder

class ButtonLayout(RelativeLayout):
    pass

class CustomButton(ButtonLayout):
    background_normal = StringProperty('atlas://data/images/defaulttheme/button')
    background_down = StringProperty('atlas://data/images/defaulttheme/button_pressed')
    
    state = OptionProperty('normal', options=('normal', 'down'))
    text = StringProperty('My custom button is cooler than yours.')
    #border = ListProperty([16, 16, 16, 16])

    def __init__(self, **kwargs):
        super(CustomButton, self).__init__(**kwargs)        
        
Builder.load_string("""
#:import BoxLayout kivy.uix.boxlayout
#:import Animation kivy.animation.Animation

<-ButtonLayout>:
    state_image: self.background_down if self.state == 'down' else self.background_normal
    canvas.before:
        Color:
            rgb: 1, 1, 1
        Rectangle:
            # self here refers to the widget i.e BoxLayout
            pos: self.pos
            size: self.size
        BorderImage:
            source: self.state_image
            pos: self.pos
            size: self.size
        PushMatrix
        Translate:
            xy: self.center_x, self.center_y
        Rotate:
            angle: 0
            axis: 0, 0, 1
        Translate:
            xy: -self.center_x, -self.center_y
    canvas.after:
        PopMatrix

<CustomButton>:
    layout: layout_id
    label: label_id
    BoxLayout
        id: layout_id
        orientation: 'horizontal'
        pos_hint: {'center_x': .5, 'center_y': .5}
        size_hint: .75, .75
        Label:
            id: label_id
            text: root.text
            shorten: True
            pos_hint: {'center_y': .5} 

""")