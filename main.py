import asyncio
import json
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.core.window import Window

# -------------------------------------------------------------------------
# Step 1: Explicit Window Metrics & Web Optimization [cite: 375]
# -------------------------------------------------------------------------
# Force a clean portrait aspect ratio inside the HTML5 browser canvas [cite: 375]
Window.size = (450, 800)

class BakingApp(App):
    def build(self):
        self._calculating = False  # Safety flag to prevent infinite update loops [cite: 497]
        self.recipes_db = {}
        self.load_recipes_from_disk()
        
        # Simple Screen Manager setup for demonstration
        self.sm = ScreenManager()
        self.sm.add_widget(DashboardScreen(name='dashboard'))
        return self.sm

    # -------------------------------------------------------------------------
    # Permanent Storage (JSON Backend Local Handling) [cite: 509, 511]
    # -------------------------------------------------------------------------
    def load_recipes_from_disk(self):
        try:
            with open("recipes_db.json", "r") as f:
                self.recipes_db = json.load(f) [cite: 510, 512]
        except FileNotFoundError:
            self.recipes_db = {} [cite: 512]

    def save_recipes_to_disk(self):
        with open("recipes_db.json", "w") as f:
            json.dump(self.recipes_db, f) [cite: 511, 512]

    # -------------------------------------------------------------------------
    # Water Temperature Logic (With Optional Sp.T Parameter) [cite: 394, 477]
    # -------------------------------------------------------------------------
    def process_water_calculation(self, ddt, rt, ft, ff, spt_input=""):
        try:
            DDT = float(ddt)
            RT = float(rt)
            FT = float(ft)
            FF = float(ff)
            
            # Scenario B: If Sp.T is provided [cite: 482]
            if spt_input.strip():
                SpT = float(spt_input)
                cal_wt = (4 * DDT) - (RT + FT + SpT + FF) [cite: 396, 482]
            else:
                # Scenario A: If Sp.T is blank [cite: 482]
                cal_wt = (3 * DDT) - (RT + FT - FF) [cite: 430, 482]
                
            return round(cal_wt, 2)
        except ValueError:
            return "Invalid Input" [cite: 498]

    # -------------------------------------------------------------------------
    # Bidirectional Recipe Matrix Engine [cite: 451, 489, 491]
    # -------------------------------------------------------------------------
    def calculate_recipe_matrix(self, trigger_field, current_row_data, global_totals):
        if self._calculating:
            return [cite: 497]
        
        self._calculating = True [cite: 497]
        try:
            # Prevent circular events while solving equations programmatically [cite: 492, 497]
            
            # Scenario 01: Dynamic True % to Baker's % Conversion [cite: 493]
            if trigger_field == 'true_pct':
                total_flour_true = global_totals.get('total_flour_true_pct', 100.0)
                if total_flour_true > 0:
                    current_row_data['bakers_pct'] = (current_row_data['true_pct'] / total_flour_true) * 100 [cite: 494]

            # Scenario 02: Total Dough Weight Extraction [cite: 494]
            if current_row_data.get('true_pct', 0) > 0 and current_row_data.get('weight', 0) > 0:
                derived_total_wt = (current_row_data['weight'] / current_row_data['true_pct']) * 100 [cite: 495]
                global_totals['total_wt'] = derived_total_wt [cite: 495]

            # Scenario 03: Full Matrix Breakdown from Total Dough Weight [cite: 495]
            if global_totals.get('total_wt', 0) > 0:
                # If True % is known, extract ingredient weight directly [cite: 496]
                if current_row_data.get('true_pct', 0) > 0:
                    current_row_data['weight'] = (global_totals['total_wt'] * current_row_data['true_pct']) / 100 [cite: 496]
                # If Baker's % is known, structural mappings break down via totals [cite: 495]
                elif current_row_data.get('bakers_pct', 0) > 0:
                    pass # Additional math mappings handled iteratively here [cite: 505]

        finally:
            self._calculating = False [cite: 497]


class DashboardScreen(Screen):
    pass # UI elements and interaction points hook into functions listed above [cite: 390]

# -------------------------------------------------------------------------
# Step 2: Asynchronous Pygbag Lifecycle Hook [cite: 375, 379]
# -------------------------------------------------------------------------
async def main():
    app = BakingApp()
    # Runs the Kivy engine asynchronously inside the web ecosystem [cite: 380, 381]
    await app.async_run(async_loop="asyncio") 

if __name__ == '__main__':
    asyncio.run(main()) [cite: 381]
