"""
This module houses the class that defines the row in our RecycleView
"""
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
from kivy.properties import ListProperty
from kivy.core.window import Window

Builder.load_string('''
#: import Window kivy.core.window.Window
#: set gap 0.015 * Window.width

<CAMIMenuRow>
    text: ''
    callback: None
    number: 0
    spacing: 5
    Label:
        canvas:
            Color:
                rgba: 0.5, 1, 0.5, 0.5
            RoundedRectangle:
                size: self.size
                pos: self.pos

        # Houses the number image before the label
        text: str(root.number)
        size_hint_x: None
        width: self.height
        on_touch_down: self.collide_point(*args[1].pos) and root.callback()

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

class CAMIMenuRow(BoxLayout):
    """
    The display class for CAMI Menu rows, optimized for the RecycleView.
    """
    post_icons = ListProperty(None)
    """ A list of dictionaries containing:
        icon: a path to the image
        callback: the callback to be fired on clicking
    """

    def on_post_icons(self, widget, icon_list):
        print("camimenurow.py: on_post_icons fired with {0}".format(icon_list))

