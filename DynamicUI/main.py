"""
Small app demonstrating a dynamic UI

Author: ZenCODE
Date: 22/10/2013
"""

from kivy.lang import Builder
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.factory import Factory


class DataSource(object):
    """
    This class would be an abstraction of your data source:
    the MySQLdb in this case.
    """
    def get_data(self):
        """Return the data. We use a list of dicts representing a list of rows
        """
        return [{"image": "kivy1.png",
                 "row_id": 1,
                 "header": "Question 1",
                 "type": "Label",
                 "value_name": "text",
                 "value": "My Text"},
                {"image": "kivy2.png",
                 "row_id": 2,
                 "header": "Question 2",
                 "type": "Button",
                 "value_name": "text",
                 "value": "Button"},
                {"image": "kivy1.png",
                 "row_id": 3,
                 "header": "Question 3",
                 "type": "CheckBox",
                 "value_name": "active",
                 "value": "True"}]


Builder.load_string('''
<QuestionWidget>:
    ques_image: ques_image  # These do your mapping to the ObjectProperty
    header_label: header_label
    box_container: box_container

    orientation: "vertical"
    Image:
        id: ques_image
    Label:
        id: header_label
    BoxLayout:
        id: box_container
''')


class QuestionWidget(BoxLayout):
    """
    This widget would represent each Question
    """
    def build(self, data_dict):
        """Build the widget based on the dictionary from the data source"""
        # The widgets are part of every instance
        self.ques_image.source = data_dict["image"]
        self.header_label.text = data_dict["header"]
        # But this content is generated dynamically
        self.box_container.add_widget(self.get_content(data_dict))

    @staticmethod
    def get_content(data_dict):
        """Returns the instance specific widgets for the box_layout"""
        # We get class based on it's name as registered in the factory and instantiate
        content = Factory.get(data_dict["type"])()
        # We noe set any of it's properties and return it
        setattr(content, data_dict["value_name"], data_dict["value"])
        return content


class TestApp(App):
    def __init__(self, **kwargs):
        """
        On initialization, register the classes we want to create dynamically
        via the Factory object
        """
        super(TestApp, self).__init__(**kwargs)
        Factory.register('Label', module='kivy.uix.label')
        Factory.register('Button', module='kivy.uix.button')
        Factory.register('CheckBox', module='kivy.uix.checkbox')

    def build(self):
        container = BoxLayout()  # or screen, carousel etc.
        for item in DataSource().get_data():
            ques_widget = QuestionWidget()
            ques_widget.build(item)
            container.add_widget(ques_widget)
        return container

if __name__ == "__main__":
    TestApp().run()

