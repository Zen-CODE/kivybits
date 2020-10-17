from kivy.app import App
from kivy.lang import Builder
from textwrap import dedent

kv = dedent('''
BoxLayout:
    orientation: "vertical"
    padding: 20
    BoxLayout:
        orientation: "horizontal"
        spacing: 20
        Label:
            text: "Input Type for TextInput:"
        Spinner:
            id: spinner
            text: "text"
            values: ["text", "number", "url", "mail", "datetime", "tel", "address"]
    TextInput:
        id: ti
        input_type: spinner.text if spinner.text else "text"
    Label:
        text: "Input type : " + ti.input_type
''')

class TestApp(App):
    def build(self):
        return Builder.load_string(kv)


TestApp().run()
