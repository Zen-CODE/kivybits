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
    value: ''
    number: 0
    Label:
        text: root.value + " - " + str(root.number)
''')

class CAMIMenuRow(BoxLayout):
    pass

    