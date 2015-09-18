#!/usr/bin/env python
from kivy.app import App
from kivy.uix.settings import SettingsWithTabbedPanel
from kivy.logger import Logger
from kivy.lang import Builder

kv = """
BoxLayout:
    orientation: 'vertical'
    Button:
        text: 'Click me to show settings or press F1'
        on_release: app.open_settings()
    Label:
        id: label
        text: 'Hello'
"""


class MyApp(App):
    def build(self):
        return Builder.load_string(kv)

    def build_config(self, config):
        config.setdefaults('My Label', {'text': 'Hello', 'font_size': 12})

    def build_settings(self, settings):
        settings.add_json_panel('My Label', self.config, 'settings.json')

    def on_config_change(self, config, section, key, value):
        Logger.info("main.py: App.on_config_change: {0}, {1}, {2}, {3}".format(
            config, section, key, value))

        # We respond to changes in the configuration here.
        if section == "My Label":
            if key == "text":
                self.root.ids.label.text = value
            elif key == 'font_size':
                self.root.ids.label.font_size = float(value)

    def close_settings(self, settings):
        Logger.info("main.py: App.close_settings: {0}".format(settings))
        super(MyApp, self).close_settings(settings)


class MySettingsWithTabbedPanel(SettingsWithTabbedPanel):
    def on_close(self):
        print("MySettingsWithTabbedPanel.on_close")

    def on_config_change(self, config, section, key, value):
        Logger.info(
            "main.py: MySettingsWithTabbedPanel.on_config_change: "
            "{0}, {1}, {2}, {3}".format(config, section, key, value))


MyApp().run()