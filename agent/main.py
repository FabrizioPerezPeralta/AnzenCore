import requests
import platform
import os
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput

SUPABASE_URL = "https://hnwradnsykylksjvrmpb.supabase.co"
SUPABASE_KEY = "sb_publishable_Sh4c3OF_PXYUnZcUAF6uTQ_qI3Oga8T"

class AnzenAgent(App):
    def build(self):
        self.view = BoxLayout(orientation='vertical', padding=40, spacing=20)
        self.view.add_widget(Label(text="🛡️ AnzenCore Agent", font_size=30))
        self.uid = TextInput(hint_text="Tu ID de Usuario", multiline=False, size_hint_y=None, height=100)
        self.view.add_widget(self.uid)
        btn = Button(text="ESCANEAR AHORA", size_hint_y=None, height=120, background_color=(0,0.7,1,1))
        btn.bind(on_press=self.scan)
        self.view.add_widget(btn)
        self.log = Label(text="Listo para analizar")
        self.view.add_widget(self.log)
        return self.view

    def scan(self, instance):
        if not self.uid.text:
            self.log.text = "⚠️ Falta ID"; return
        
        self.log.text = "🔍 Analizando..."
        # Simulación de vulnerabilidades reales que el navegador no ve
        res = [
            {"v": "Root Check", "n": "Crítico", "d": "Binarios SU detectados en /system/bin"},
            {"v": "USB Debugging", "n": "Medio", "d": "Modo desarrollador activo"}
        ]
        
        try:
            for item in res:
                payload = {
                    "user_id": self.uid.text,
                    "dispositivo": f"{platform.system()} {platform.machine()}",
                    "vulnerabilidad": item['v'],
                    "nivel": item['n'],
                    "descripcion": item['d']
                }
                requests.post(f"{SUPABASE_URL}/rest/v1/vulnerabilidades", json=payload,
                         headers={"apikey": SUPABASE_KEY, "Authorization": f"Bearer {SUPABASE_KEY}"})
            self.log.text = "✅ Reporte enviado al Dashboard"
        except:
            self.log.text = "❌ Error de conexión"

if __name__ == "__main__":
    AnzenAgent().run()