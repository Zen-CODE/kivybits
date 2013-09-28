'''
An example of normal Python properties using decorators
'''
from kivy.properties import StringProperty
from kivy.event import EventDispatcher

class KivyProperties(EventDispatcher):
    text = StringProperty()

if __name__ == '__main__':
    obj = KivyProperties()
    obj.text = "Me"
    print obj.text

