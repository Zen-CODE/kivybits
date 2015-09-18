#!/usr/bin/env python
from kivy.app import App
from kivy.uix.settings import SettingsWithTabbedPanel
from kivy.uix.button import Button


class MyApp(App):
    def build(self):
        self.settings_cls = MySettingsWithTabbedPanel
        self.button = Button(text='Click me to show settings or press F1')
        self.button.bind(on_release=lambda but: self.open_settings())
        return self.button

    def build_config(self, config):
        config.setdefaults('My Button', {'dark_button': True})

    def build_settings(self, settings):
        settings.add_json_panel('My Button', self.config, 'settings.json')

    def on_config_change(self, config, section, key, value):
        print("App.on_config_change", config, section, key, value)

    def close_settings(self, settings):
        print("App.close_settings", settings)
        super(MyApp, self).close_settings(settings)


class MySettingsWithTabbedPanel(SettingsWithTabbedPanel):
    def _on_close(self):
        print("MySettingsWithTabbedPanel.on_close")

    def on_config_change(self, config, section,key,value):
        print("MySettingsWithTabbedPanel.on_config_change",config, section,
              key, value)

MyApp().run()