def on_touch_down(self, touch):
    if self.collide_point(*touch.pos):
        # if the touch collides with our widget, let's grab it
        touch.grab(self)
        return True  # Indicate we have handled the touch


def on_touch_move(self, touch):
    # This event can also be used to monitor grabbed touch
    pass


def on_touch_up(self, touch):
    # Check if it's a grabbed touch event
    if touch.grab_current is self:
        # ok, the current touch is dispatched for us.
        print('I have been touched!')
        touch.ungrab(self)  # ungrab or you might have side effects
        return True  # indicate we have handled the event
