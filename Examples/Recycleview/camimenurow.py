"""
This module houses the class that defines the row in our RecycleView
"""
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
from kivy.properties import (ListProperty, BooleanProperty, ObjectProperty,
                             StringProperty)
from kivy.core.window import Window
from kivy.uix.label import Label

Builder.load_file("camimenurow.kv")


class CAMIMenuBlock(Label):
    """
    An item appearing in a CAMIMenuRow. It adds press highlights, callback
    functionality and 
    """
    callback = ObjectProperty(None)
    """ The callback to fire or press """

    source = StringProperty('graphics/blank.png')
    """ The graphics to be drawn for the block """

    pressed = BooleanProperty(False)
    """ Indicates whether the block has been tapped or not. """

    visible = BooleanProperty(False)
    """ Indicates whether the widget is displayed or not (has a width)"""

    def on_touch_down(self, touch):
        """ Respond to the touch down event """
        if self.collide_point(*touch.pos) and self.visible:
            self.pressed = True

        return super(CAMIMenuBlock, self).on_touch_down(touch)

    def on_touch_up(self, touch):
        """ Respond to the touch up event """
        if self.pressed:
            self.pressed = False
        return super(CAMIMenuBlock, self).on_touch_up(touch)


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
        # print("camimenurow.py: on_post_icons fired with {0}".format(icon_list))
        post0, post1 = len(icon_list) > 0, len(icon_list) > 1
        w_post0, w_post1 = self.ids.mb_post0, self.ids.mb_post1
        w_post0.visible = post0
        w_post1.visible = post1
        w_post0.callback = icon_list[0]['callback'] if w_post0 else None
        w_post1.callback = icon_list[1]['callback'] if w_post0 else None

