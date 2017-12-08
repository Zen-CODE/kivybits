from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.textinput import TextInput
from kivy3dgui.layout3d import Layout3D, Node
from kivy.animation import Animation


class DemoApp(App):
    """
    The App class is a singleton and creates the base of your application.
    """
    @staticmethod
    def get_grid():
        """ Build and return the main grid UI. """
        grid = GridLayout(rows=2, cols=2)
        grid.add_widget(
            Button(text='Click me'))
        grid.add_widget(
            TextInput(text='Click me'))
        grid.add_widget(
            Image(source='audio_icon.png', allow_stretch=True))
        return grid

    def build(self):
        """ This method returns the root widget of your application. """
        grid = self.get_grid()

        layout3d = Layout3D(canvas_size=(800, 600))
        node = Node(
            rotate=(0, 0.3, 1, 0),  # Angle and x, y, z axis of rotation matrix
            scale=(0.4, 0.4, 0.4),  # x, y, z of scaling matrix
            translate=(0, 0.0, -100),  # x, y, z of translation matrix
            effect=True,
            meshes=("./meshes/2dbox.obj",))
        node.add_widget(grid)
        layout3d.add_widget(node)

        ani = self.get_animation()
        ani.start(node)
        return layout3d

    @staticmethod
    def get_animation():
        """ Return an animation object setting the rotation."""
        ani = Animation(rotate=(360, 0.3, 1, 0), duration=3) +\
            Animation(rotate=(0, 0.3, 1, 0), duration=3)
        # ani.repeat = True
        return ani

if __name__ == "__main__":
    DemoApp().run()

