from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.popup import Popup

from kivy.app import App
from kivy.lang import Builder
from kivy.properties import StringProperty, ObjectProperty

Builder.load_string("""
<_InfoDialogContent>:
    orientation: 'vertical'
    textlabel: textlabel
    padding: 10
    spacing: 10

    Label:
        id: textlabel
        size_hint: 1, None
        text: root.text
        bold: True
        font_size: '25sp'
        #shorten: True
        text_size: 450, None
    Widget:
        heigth: 5
    BoxLayout:
        spacing: 10

        Button:
            id: close_button
            text: 'Close'
            bold: True
            font_size: '30sp'
            size_hint: (1, 1.5)
            on_press: root.on_close_button_clicked()
""")

class _InfoDialogContent(BoxLayout):
    """Object build by kv."""
    text = StringProperty('')
    textlabel = ObjectProperty()

    #TODO: Explain to prefer **kwargs as you're subclassing a Kivy widget which might use these
    def __init__(self, text, parent):
        BoxLayout.__init__(self)
        self.text = text
        self.myparent = parent

    def on_close_button_clicked(self):
        self.myparent.dismiss()

class InfoDialog(Popup):
    def __init__(self, title, text):
        """Extends the kivy popup dialog with a custom content object.
        """
        Popup.__init__(self, title=title, size_hint=(0.6, 0.5), size=(800, 400))
        self.content = _InfoDialogContent(text, self)

class MyApp(App):
    def build(self):
        fl = FloatLayout()
        dlg = InfoDialog('popup title', 'Why is this text outside the popup ?\nIt should be inside or am I missing something ?')
        dlg.open()
        return fl

MyApp().run()