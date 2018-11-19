"""
This module houses the class that defines the row in our RecycleView
"""
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder


Builder.load_string('''
#: import Window kivy.core.window.Window
#: set gap 0.015 * Window.width
#: set height 0.1 * Window.height

<CAMIMenuRow>
    text: ''
    callback: None
    number: 0
    row_height: height
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

    Button:
        text: "Button"
        width: self.height
        size_hint_x: None
''')

class CAMIMenuRow(BoxLayout):
    pass

    