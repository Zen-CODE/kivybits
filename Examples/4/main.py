from kivy.app import App
from kivy.uix.label import Label
from kivy.clock import Clock
from kivy.config import Config

Config.set("graphics", "fullscreen", 'auto')

class TestApp(App):
    counter = 0
    label = None
    
    def build(self):        
        self.label = Label(text="Hello")
        Clock.schedule_interval(self.increment, 1)
        return self.label

    def increment(self, dt):
        print "fired", Config.get("graphics", "fullscreen"), "type=", type(Config.get("graphics", "fullscreen"))
        #print "Desktop=", Config.get("kivy", "Desktop"), "type=", type(Config.get("kivy", "Desktop"))
        self.counter += 1
        if self.counter > 5:
            return False


if __name__ == "__main__":
    TestApp().run()
