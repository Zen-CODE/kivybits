"""
This module houses the class that defines the row in our RecycleView
"""
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder


Builder.load_string('''
#: import Window kivy.core.window.Window
#: set gap 0.015 * Window.width

<CAMIMenuRow>
    text: ''
    number: 0
    BoxLayout:
        canvas.before:
            Color:
                rgba: 0.7, 0.7, 0.1, 0.5
            RoundedRectangle:
                size: self.size
                pos: self.pos

        padding: gap, 0, 0, 0
        size_hint_x: 1
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

    