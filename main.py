from kivy.app import App
from kivy.properties import StringProperty
from kivy.graphics import RoundedRectangle, Line
from kivy.clock import Clock

class ShddApp(App):
    status_text = StringProperty("Paste YouTube URL")
    
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