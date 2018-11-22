"""
This module houses the class that defines the row in our RecycleView
"""
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
from kivy.properties import (ListProperty, BooleanProperty, ObjectProperty,
                             StringProperty)
from kivy.uix.label import Label
from kivy.uix.recycleview import RecycleView
from kivy.clock import Clock

Builder.load_file("camimenu.kv")


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
            self.callback()

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
    """
    A list of dictionaries containing:
        source: a path to the image
        callback: the callback to be fired on clicking
    """

    delayed_overlay = ObjectProperty(None)
    """ A function to call which return a widget to be overlayed on the button.
    """

    overlay = ObjectProperty(None)
    """ A reference to the widget used as a floating overlay on the menu item.
    """

    _callback = None
    """ The pending callback for the 'delayed_load' call. """

    def on_post_icons(self, widget, icon_list):
        """ Respond to the setting of the icon_list property. """
        post0, post1 = len(icon_list) > 0, len(icon_list) > 1
        w_post0, w_post1 = self.ids.mb_post0, self.ids.mb_post1
        w_post0.visible = post0
        w_post1.visible = post1
        w_post0.callback = icon_list[0]['callback'] if post0 else None
        w_post1.callback = icon_list[1]['callback'] if post1 else None

    def _re_pos_overlay(self, widget, y):
        """ Re-position our overlay"""
        self.overlay.y = y

    def on_delayed_overlay(self, widget, value):
        """ A callback to return the widget overlaying state into on the menu
        item. """
        mb_text = self.ids.mb_text
        if self._callback is not None:
            self._callback.cancel()
        if self.overlay is not None:
            mb_text.remove_widget(self.overlay)
            mb_text.unbind(on_y=self._re_pos_overlay)

        def add_overlay(dt):
            #  Do we need to check something? That the user has not closed the
            # screen?
            self.overlay = value()
            self.overlay.pos = (
                mb_text.right - self.overlay.width - 15,
                mb_text.y)
            mb_text.add_widget(self.overlay)
            mb_text.bind(on_y=self._re_pos_overlay)

        self._callback = Clock.schedule_once(add_overlay, 2.0)


class CAMIMenu(RecycleView):
    """ An implementation of the RecycleView, to handle the menu area as a
    scrollview.
    """
