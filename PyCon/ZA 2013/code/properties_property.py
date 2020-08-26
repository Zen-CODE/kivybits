'''
An example of normal Python properties using decorators
'''
from kivy.properties import StringProperty

class PropProperties(object):
    _text = ''

    def _get_text(self):
        '''The "getter"'''
        return self._text

    def _set_text(self, value):
        '''The "setter"'''
        self._text = value

    text = property(_get_text, _set_text)

if __name__ == '__main__':
    obj = PropProperties()
    obj.text = "Me"
    print obj.text

