from kivy.app import App
from kivy.uix.label import Label
from kivy.lang import Builder
from kivy.clock import Clock


class BoundLabel(Label):
    instances = []  # A list of all instances of the class

    def __init__(self, **kwargs):
        BoundLabel.instances.append(self)
        super(BoundLabel, self).__init__(**kwargs)

    @staticmethod
    def set_shared_text(dt):
        """ Loop through all instances and set to the shared data """
        for instance in BoundLabel.instances:
            instance.text = str(dt)  # use str(dt) as shared for simplicity


class TestApp(App):
    def build(self):
        # Set the clock to alter the all the label captions to the delta time
        Clock.schedule_interval(BoundLabel.set_shared_text, 1)
        return Builder.load_string('''
BoxLayout:
    orientation: "vertical"
    BoundLabel:
    BoundLabel:
    BoundLabel:
''')

TestApp().run()