"""
This module houses the class that defines the row in our RecycleView
"""
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder


Builder.load_string('''
<CAMIMenuRow>
    canvas.before:
        Color:
            rgba: 0.5, 0.5, 0.5, 1
        Rectangle:
            size: self.size
            pos: self.pos
    text: ''
    number: 0
    BoxLayout:
        padding: 5, 5, 5, 5        
        width: 0.7 * root.width
        size_hint_x: None
        Label:
            text: root.text + " - " + str(root.number)
            text_size: self.size
            halign: 'left'
            valign: 'center'

    Button:
        text: "Button"
''')

class CAMIMenuRow(BoxLayout):
    pass

    