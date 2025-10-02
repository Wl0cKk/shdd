from kivy.app import App
from kivy.properties import StringProperty
from kivy.core.window import Window
from kivy.clock import Clock

class ShddApp(App):
    status_text = StringProperty('')
    
    def on_start(self):
        Window.size = (400, 600)
        Window.minimum_width = 400
        Window.minimum_height = 600
        Window.maximum_width = 400
        Window.maximum_height = 600
    
    def download_short(self):
        url = self.root.ids.url_input.text
        if not url.strip():
            self.status_text = "Please enter a URL first!"
            return
            
        self.status_text = "Downloading..."
        Clock.schedule_once(self.finish_download, 2)
    
    def finish_download(self, dt):
        self.status_text = "Download completed!"
        self.root.ids.url_input.text = ""

if __name__ == '__main__':
    ShddApp().run()