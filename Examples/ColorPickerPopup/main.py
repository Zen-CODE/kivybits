'''
Demo Popup with a ColorPicker
'''
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.colorpicker import ColorPicker
from kivy.uix.popup import Popup
from kivy.uix.label import Label


class ColorPopup(App):
    '''
    This class represent you application. There should be only one per app.
    '''
    def build(self):
        '''
        This method is called automatically and should return your "root"
        widget.
        '''
        self.label = Label(text="Colour not selected.")

        layout = BoxLayout(
            orientation="vertical",
            padding=[50, 50, 50, 50])
        layout.add_widget(self.label)
        layout.add_widget(
            Button(
                text="Select colour",
                on_release=self.select_color))
        layout.add_widget(
            Button(
                text="OK and Cancel",
                on_release=lambda inst: self.select_color(inst, False)))
        return layout

    def select_color(self, instance, no_buts=True):
        '''
        The button click has fired the event, so show the popup.
        no_buts is  boolean and specifies whether to include buttons
        in the popup or not.
        '''
        popup = Popup(
            title="Select your colour",
            size_hint=(0.75, 0.75))

        # NOTE: the below properties can also be passed in to the Popup
        # constructor but we do them separately for clarity.
        if no_buts:
            colorPicker = ColorPicker()
            popup.bind(
                on_dismiss=lambda popup: \
                    self.popup_dismissed(popup, colorPicker.hex_color))
            popup.content = colorPicker
        else:
            # We prevent the default dismiss behaviour and roll our own in
            # the content.
            popup.auto_dismiss = False
            popup.content = self.get_ok_cancel_content(popup)
        popup.open()

    def popup_dismissed(self, popup, color):
        ''' The popup has been dismissed'''
        self.label.text = "Colour in hex = " + color

    def get_ok_cancel_content(self, popup):
        '''Return content with OK and cancel buttons for validating'''
        colorPicker = ColorPicker()
        buttonLayout = BoxLayout(orientation="horizontal",
            padding="5sp",
            size_hint_y=0.2)
        okButton = Button(
            text="Okay",
            on_release=lambda but: \
                popup.dismiss() and \
                self.popup_dismissed(popup, colorPicker.hex_color))
        cancelButton = Button(
            text="Cancel",
            on_release=lambda but: popup.dismiss())
        buttonLayout.add_widget(okButton)
        buttonLayout.add_widget(cancelButton)

        mainLayout = BoxLayout(orientation="vertical")
        mainLayout.add_widget(colorPicker)
        mainLayout.add_widget(buttonLayout)
        return mainLayout


if __name__ == '__main__':
    ColorPopup().run()
