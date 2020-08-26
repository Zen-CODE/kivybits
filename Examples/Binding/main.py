from kivy.uix.boxlayout import BoxLayout
from kivy.app import App
from kivy.uix.button import Button
from functools import partial


class DemoBox(BoxLayout):
    """
    This class demonstrates various techniques that can be used for binding to
    events. Although parts could me made more optimal, advanced Python concepts
    are avoided for the sake of readability and clarity.
    """
    def __init__(self, **kwargs):
        super(DemoBox, self).__init__(**kwargs)
        self.orientation = "vertical"

        # We start with standard binding to a standard event. The only argument
        # passed to the callback is the object on which the event has occurred.
        btn = Button(text="Normal binding to event")
        btn.bind(on_press=self.on_event)

        # Next, we bind to a standard property change event. These typically
        # pass 2 arguments: the object and the value
        btn2 = Button(text="Normal binding to a property change")
        btn2.bind(state=self.on_property)

        # Here we use anonymous functions (a.k.a lambda's) to perform binding.
        # Their advantage is that you can avoid declaring new functions i.e.
        # they offer a concise way to "redirect" callbacks.
        btn3 = Button(text="Using anonymous functions.")
        btn3.bind(on_press=lambda x: self.on_event(None))

        # You can also declare a function that accepts a variable number of
        # positional and keyword arguments and use introspection to determine
        # what is being passed in. This is very handy for debugging as well
        # as function re-use. Here, we use standard event binding to a function
        # that accepts optional positional and keyword arguments.
        btn4 = Button(text="Use a flexible function")
        btn4.bind(on_press=self.on_anything)

        # Lastly, we show how to use partial functions. They are sometimes
        # difficult to grasp, but provide a very flexible and powerful way to
        # re-use functions.
        btn5 = Button(text="Using partial functions. For hardcore's.")
        btn5.bind(on_press=partial(self.on_anything, "1", "2", monthy="python"))

        for but in [btn, btn2, btn3, btn4, btn5]:
            self.add_widget(but)

    def on_event(self, obj):
        print("Typical event from", obj)

    def on_property(self, obj, value):
        print("Typical property change from", obj, "to", value)

    def on_anything(self, *args, **kwargs):
        print('The flexible function has *args of', str(args),
              "and **kwargs of", str(kwargs))


class DemoApp(App):
    def build(self):
        return DemoBox()

if __name__ == "__main__":
    DemoApp().run()