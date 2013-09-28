from kivy.gesture import Gesture, GestureDatabase

# Create a gesture
g = Gesture()
g.add_stroke(point_list=[(1, 1), (3, 4), (2, 1)])
g.normalize()
g.name = "triangle"

# Add it to database
gdb = GestureDatabase()
gdb.add_gesture(g)

# And for the next gesture, try to find a match!
g2 = Gesture()
g2.add_stroke(point_list=[(1, 1), (3, 4), (2, 1)])
g2.normalize()
print gdb.find(g2).name  # will print "triangle"

