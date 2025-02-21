from kivy.lang import Builder
from kivy.clock import Clock
from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.pickers import MDModalDatePicker, MDModalInputDatePicker
from kivy.properties import StringProperty, ObjectProperty

KV = '''
MDScreenManager:
    MainScreen:
        name: "main_screen"
<MainScreen>
    md_bg_color: self.theme_cls.backgroundColor
    MDLabel:
        text: 'Ingrese compra'
        halign: "center"
        role: "large"
        theme_text_color: "Primary"
        pos_hint: {"center_x": 0.5, "center_y": 0.9}
    MDLabel:
        text: root.selected_date_text
        halign: "center"
        role: "large"
        theme_text_color: "Primary"
        pos_hint: {"center_x": 0.2, "center_y": 0.7}
    MDFabButton:
        icon: "calendar"
        style: "small"
        pos_hint: {"center_x": .4, "center_y": .7}
        on_release: app.show_date_picker()
'''
from datetime import datetime
class MainScreen(MDScreen):
    selected_date_text = StringProperty(f'Fecha de la compra: {datetime.now().strftime("%m/%d/%Y")}')

class Example(MDApp):
    def build(self):
        self.theme_cls.primary_palette = "Olive"
        self.today_date=datetime.now().strftime("%m/%d/%Y")
        return Builder.load_string(KV)
    def new_row(self):
        self.new_row = [self.today_date]
        return self.new_row
    def show_date_picker(self):
        date_dialog = MDModalDatePicker()
        date_dialog.open()
        date_dialog.bind(on_cancel=self.on_cancel)
        date_dialog.bind(on_ok=self.on_ok)
        date_dialog.bind(on_edit=self.on_edit)
    def on_cancel(self, instance_date_picker):
        instance_date_picker.dismiss()
    def on_edit(self, instance_date_picker):
        instance_date_picker.dismiss()
        Clock.schedule_once(self.show_modal_input_date_picker, 0.2)
    def on_ok(self, instance_date_picker):
        self.today_date=instance_date_picker.set_text_full_date()
        print(self.new_row)
        screen = self.root.get_screen('main_screen')
        screen.selected_date_text = f"Fecha de la compra: {self.today_date}"
        instance_date_picker.dismiss()
        return self.today_date
    def show_modal_input_date_picker(self, *args):
        def on_edit(*args):
            date_dialog.dismiss()
            Clock.schedule_once(self.show_date_picker, 0.2)
        def on_cancel(self, instance_date_picker):
            instance_date_picker.dismiss()
        def on_ok(self, instance_date_picker):
            self.today_date=instance_date_picker.set_text_full_date()
            print(self.new_row)
            instance_date_picker.dismiss()
            screen = self.root.get_screen('main_screen')
            screen.selected_date_text = f"Fecha de la compra: {self.today_date}"
            return self.today_date
        date_dialog = MDModalInputDatePicker(text_button_ok='Agregar evento',text_button_cancel='Cancelar')
        date_dialog.bind(on_cancel=self.on_cancel)
        date_dialog.bind(on_edit=on_edit)
        date_dialog.bind(on_ok=self.on_ok)
        date_dialog.open()

Example().run()
