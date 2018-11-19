"""
This module houses the class that defines the row in our RecycleView
"""
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
from kivy.properties import (ListProperty, BooleanProperty, ObjectProperty,
                             StringProperty)
from kivy.core.window import Window
from kivy.uix.label import Label

Builder.load_string('''
#: import Window kivy.core.window.Window
#: set gap 0.015 * Window.width
<CAMIMenuBlock>:
    canvas:

        Color:
            rgba: [0, 0, 0, 0] if not self.pressed else [0, 0.5, 0.5, 0.25]
        RoundedRectangle:
            size: self.size
            pos: self.pos
    size_hint_x: None
    width: self.height
    

<CAMIMenuRow>
    text: ''
    callback: None
    number: 0
    spacing: 5
    CAMIMenuBlock:
        canvas:
            Color:
                rgba: 0.5, 1, 0.5, 0.5
            RoundedRectangle:
                size: self.size
                pos: self.pos

        # Houses the number image before the label
        text: str(root.number)
        callback: root.callback() if root.callback else None

    BoxLayout:
        canvas.before:
            Color:
                rgba: 0.75, 0.75, 0.1, 0.5
            RoundedRectangle:
                size: self.size
                pos: self.pos

        padding: gap, 0, 0, 0
        Label:
            text: root.text + " - " + str(root.number)
            text_size: self.size
            halign: 'left'
            valign: 'center'
    Widget:
        # Handles the placement of extra items in the row e.g. trophy/send
        size_hint_x: None
        width: 0
''')

class CAMIMenuBlock(Label):
    """
    An item appearing in a CAMIMenuRow. It adds press highlights, callback
    functionality and 
    """
    callback = ObjectProperty(None)
    """ The callback to fire or press """

    pressed = BooleanProperty(False)
    """ Indicates whether the block has been tapped or not. """

    source = StringProperty('graphics/blank.png')
    """ The graphics to be drawn for the block """


class CAMIMenuRow(BoxLayout):
    """
    The display class for CAMI Menu rows, optimized for the RecycleView.
    """
    post_icons = ListProperty(None)
    """ A list of dictionaries containing:
        source: a path to the image
        callback: the callback to be fired on clicking
    """

    def on_post_icons(self, widget, icon_list):
        print("camimenurow.py: on_post_icons fired with {0}".format(icon_list))

