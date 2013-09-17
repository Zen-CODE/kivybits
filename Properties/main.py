'''
A demo of Kivy Properties and why they rule
'''
from kivy.app import App
from kivy.uix.button import Button
from kivy.properties import StringProperty
from kivy.event import EventDispatcher
from kivy.logger import Logger


class DecoratedProp(object):
    '''
    Normal Python properties using decorators
    '''
    _wobble = ''

    @property
    def wobble(self):
        Logger.info("main.py: you got wobbled " + self._wobble)
        return self._wobble

    @wobble.setter
    def wobble(self, value):
        self._wobble = value
        Logger.info("main.py: you returned a wobble.")

    # 1. @wobble.setter? Pretty un-intuitive syntax
    # 2. Hidden variable along with 2 methods and 2 decorators
    # 3. Property value need to me manually fetched from object
    #    i.e. self._wobble


class PyProp(object):
    '''
    Normal Python properties using property()
    '''
    _wobble = ""

    def _get_wobble(self):
        Logger.info("main.py: get your wobble")
        return self._wobble

    def _set_wobble(self, value):
        self._wobble = value
        Logger.info("main.py: you returned a wobbled" + self._wobble)

    wobble = property(_get_wobble, _set_wobble)

    # 1. Gosh, now it's 4 things.
    # 2. Property value need to me manually fetched from object
    #    i.e. self._wobble


class KivyProp(EventDispatcher):
    '''
    Kivy Properties
    '''
    wobble = StringProperty("")

    # That's it. Were done, all plumbing in place. Anyone can now
    # request to get the event

    # In order to catch the property change, simple add an 'on<propname>'
    def on_wobble(self, instance, value):
        Logger.info("main.py: you wobbled " + value)

    # To manually add observers,
    def __init__(self, **kwargs):
        super(KivyProp, self).__init__(**kwargs)
        self.bind(wobble=lambda x, y: Logger.info("main.py: You wobbled " + y))

    # 1. A single line of code.
    # 2. Fired events get passed the widget + the new value - no lookup
    # 3. Any number if observers can can bind to the same property
    # 4. Better Memory Management The same instance of a property is
    #    shared across multiple widget instances
    # 5. Just plain more Pythonic ;-)

# Other interesting features
#    prop = self.property("wobble")  # Get the property object
#    prop.dispatch(self)  # Dispatch the event to listeners
#
#    prop = self.property("wobble")
#    prop.get_property_observers()  # Returns list of listeners
#    .. version:: New in 1.8.0.


class PropDemo(App):

    def build(self):
        KivyProp().wobble = "sideways"
        DecoratedProp().wobble = "upwards"
        PyProp().wobble = "down"
        return Button(text="Hi")

if __name__ == '__main__':
    PropDemo().run()
