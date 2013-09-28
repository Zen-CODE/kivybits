'''
An example of normal Python properties using decorators
'''
from kivy.properties import StringProperty
from kivy.event import EventDispatcher

class KivyProperties(EventDispatcher):
    text = StringProperty()

    # To listen for changes
    def on_text(self, instance, value):
        print "Changing to ", value

if __name__ == '__main__':
    obj = KivyProperties()
    obj.text = "Me"
    print obj.text

