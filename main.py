import asyncio
import json
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.core.window import Window

# Force web view window profile
Window.size = (450, 800)

class DashboardScreen(Screen):
    def __init__(self, **kwargs):
        super(DashboardScreen, self).__init__(**kwargs)
        
        # Explicitly build a visible UI hierarchy so the page isn't blank
        layout = BoxLayout(orientation='vertical', padding=20, spacing=15)
        
        title = Label(
            text="Bakery Science App", 
            font_size='24sp', 
            size_hint_y=None, 
            height=50
        )
        layout.add_widget(title)
        
        # Sample interaction components
        self.status_label = Label(text="Welcome! App is ready.", size_hint_y=None, height=40)
        layout.add_widget(self.status_label)
        
        btn_calc = Button(text="Test Calculation", size_hint_y=None, height=50)
        btn_calc.bind(on_press=self.run_test_calculation)
        layout.add_widget(btn_calc)
        
        # Filler area to keep elements formatted nicely at the top
        layout.add_widget(Label()) 
        self.add_widget(layout)

    def run_test_calculation(self, instance):
        # Call structural formulas directly
        app = App.get_running_app()
        result = app.process_water_calculation(ddt=26, rt=22, ft=20, ff=3)
        self.status_label.text = f"Calculated Water Temp: {result}°C"

class BakingApp(App):
    def build(self):
        self._calculating = False
        self.recipes_db = {}
        self.load_recipes_from_disk()
        
        self.sm = ScreenManager()
        self.sm.add_widget(DashboardScreen(name='dashboard'))
        return self.sm

    def load_recipes_from_disk(self):
        # Gracefully fall back if Pygbag isolates the disk path environment
        try:
            with open("recipes_db.json", "r") as f:
                self.recipes_db = json.load(f)
        except Exception:
            self.recipes_db = {}

    def process_water_calculation(self, ddt, rt, ft, ff, spt_input=""):
        try:
            DDT, RT, FT, FF = float(ddt), float(rt), float(ft), float(ff)
            if spt_input.strip():
                return round((4 * DDT) - (RT + FT + float(spt_input) + FF), 2)
            return round((3 * DDT) - (RT + FT - FF), 2)
        except ValueError:
            return "Error"

async def main():
    app = BakingApp()
    await app.async_run(async_loop="asyncio")

if __name__ == '__main__':
    asyncio.run(main())
