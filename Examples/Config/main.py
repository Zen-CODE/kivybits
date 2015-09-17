#!/usr/bin/env python
from kivy.app import App
from kivy.uix.settings import SettingsWithTabbedPanel
from kivy.uix.screenmanager import ScreenManager


class MyApp(App):
    def build(self):
        self.settings_cls=MySettingsWithTabbedPanel
        return ScreenManager()

    def build_config(self,config):

        config.setdefaults('Panel Name', {'setting1': True})

    def build_settings(self, settings):

        settings.add_json_panel('Panel Name',
                             self.config, 'settings.json')

    def on_config_change(self, config, section,key,value):
        print config, section, key, value

class MySettingsWithTabbedPanel(SettingsWithTabbedPanel):

    def on_close(self):
        print('closed')

    def on_config_change(self, config, section,key,value):
        print("Changed!")
        print config, section, key, value

MyApp().run()