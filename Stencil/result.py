from kivy.uix.modalview import ModalView
from kivy.uix.relativelayout import RelativeLayout
from kivy.properties import OptionProperty, StringProperty, ObjectProperty
from kivy.uix.behaviors import ButtonBehavior
from kivy.lang import Builder
from kivy.uix.gridlayout import GridLayout
from kivy.app import App
from baseclass import CustomButton

class ExampleGL(GridLayout):
    def __init__(self, **kwargs):
        super(ExampleGL, self).__init__(**kwargs)

class ExampleButton(ButtonBehavior, CustomButton):
    state = OptionProperty('normal', options=('normal', 'down'))
    text = StringProperty("Where Did the First Button's text go??")
    
    def __init__(self, **kwargs):
        super(ExampleButton, self).__init__(**kwargs)

class MainView(RelativeLayout):

    def __init__(self, **kwargs):
        self.size_hint = (.5, .3)
        self.pos_hint = {'center_x': .5, 'center_y': .5}
        super(MainView, self).__init__(**kwargs)

        button_container = ExampleGL()
        self.add_widget(button_container)

class TestApp(App):
    
    def build(self):
        root = MainView()
        return root
    
    def delete_button_remove_widget(self, widget):
        self.b_layout2.remove_widget(widget)

Builder.load_string("""

<ExampleGL>:
    cols: 1
    size_hint_y: None
    canvas.before:
        StencilPush
        Rectangle:
            pos: self.pos
            size: self.size
        StencilUse
    canvas.after:
        StencilUnUse
        Rectangle:
            pos: self.pos
            size: self.size
        StencilPop

    ExampleButton:
    ExampleButton:
""")
if __name__ == '__main__':
    TestApp().run()