'''
A demo of Kivy Properties and why they rule
'''
from kivy.app import App
from kivy.properties import ObjectProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
from kivy.animation import Animation, AnimationTransition

Builder.load_string('''
<ButtonBox>:
    b1: b1
    b2: b2
    b3: b3
    orientation: 'horizontal'
    spacing: '10sp'
    padding: 10, 0, 10, 0
    Button:
        id: b1
        text: "one"
    Button:
        id: b2
        text: "two"
    Button:
        id: b3
        text: "three"
''')


class ButtonBox(BoxLayout):
    '''
    Illustrate animation
    '''
    b1 = ObjectProperty()
    b2 = ObjectProperty()
    b3 = ObjectProperty()

    def start(self):
        '''
        Create and start the animations
        Note. In production code, you would probably want a different
        'on_complete' callback for each animation. We use the same on
        here for simplicity sake.
        '''
        anim = Animation(size_hint_y=0 if self.b1.size_hint_y > 0.5 else 1,
                         duration=1)
        anim.bind(on_complete=lambda x, y: self.start())
        anim.start(self.b1)

        anim2 = Animation(size_hint_y=0 if self.b2.size_hint_y > 0.5 else 1,
                         duration=1,
                         transition=AnimationTransition.in_bounce)
        anim2.start(self.b2)

        anim3 = Animation(size_hint_y=0 if self.b3.size_hint_y > 0.5 else 1,
                         duration=1,
                         transition=AnimationTransition.in_circ)
        anim3.start(self.b3)


class AnimDemo(App):

    def build(self):
        bb = ButtonBox()
        bb.start()
        return bb

if __name__ == '__main__':
    AnimDemo().run()
