
def simplegesture(name, point_list):
    '''A simple helper function to create and return a gesture'''
    g = Gesture()
    g.add_stroke(point_list)
    g.normalize()
    g.name = name
    return g

class GestureBoard(FloatLayout):
    def on_touch_down(self, touch):
        '''Collect points in touch.ud'''
        with self.canvas:
            touch.ud['line'] = Line(points=(touch.x, touch.y))
        return True

    def on_touch_move(self, touch):
        '''store points of the touch movement'''
        try:
            touch.ud['line'].points += [touch.x, touch.y]
            return True
        except (KeyError) as e:
            pass

    def on_touch_up(self, touch):
        '''The touch is over. Create a gesture and store it'''
        g = simplegesture('cross',
            list(zip(touch.ud['line'].points[::2], touch.ud['line'].points[1::2])))
        gdb = GestureDatabase()
        gdb.add_gesture(g)
