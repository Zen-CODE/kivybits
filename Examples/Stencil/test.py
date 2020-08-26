from kivy.lang import Builder
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.floatlayout import FloatLayout


Builder.load_string("""
<CustomLabel>:
    canvas.before:
        # We push a stencil and define a clipping area in the bottom right
        StencilPush
        Rectangle:
            pos: 0, 0
            size: 200, 200
        StencilUse
    # Uncommenting the #canvas.after below breaks things because
    # it's in a different set of drawing instructions
    #canvas.after:
        Color:
            rgba: 0, 0, 1, 0.5
        Rectangle:
            pos: self.pos
            size: self.size
        StencilUnUse
        StencilPop
        Color:
            rgba: 0, 1, 0, 0.5
        Rectangle:
            pos: self.pos
            size: self.size
""")


class CustomLabel(Label):
    pass


class TestApp(App):
    def build(self):
        root = FloatLayout()
        lbl = CustomLabel(text="Test")
        root.add_widget(lbl)
        return root

if __name__ == "__main__":
    TestApp().run()
