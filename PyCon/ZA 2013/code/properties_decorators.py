'''
An example of normal Python properties using decorators
'''

class DecProperties(object):
    _text = ''

    @property
    def text(self):
        '''The property "getter"'''
        return self._text

    @text.setter
    def text(self, value):
        '''The property "setter"'''
        self._text = value

if __name__ == '__main__':
    obj = DecProperties()
    obj.text = "Me"
    print obj.text

