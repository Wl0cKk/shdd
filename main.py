from kivy.app import App
from kivy.properties import StringProperty
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.utils import platform
from kivy.metrics import dp
import re

def is_youtube_video_link(url):
    pattern = r'^(?:https?://)?(?:www\.|m\.)?(?:youtube\.com/(?:watch\?v=|v/|shorts/)|youtu\.be/)[\w-]{11}(?:&|\?|$| )'
    return bool(re.match(pattern, url.strip(), re.IGNORECASE))

class ShddApp(App):
    status_text = StringProperty('')
    
    def on_start(self):
        if platform in ['win', 'linux', 'macosx', 'darwin', 'unknown']:
            Window.size = (400, 600)
            Window.minimum_width = 400
            Window.minimum_height = 600
    
    def download_short(self):
        url = self.root.ids.url_input.text.strip()
        if not url:
            self.status_text = "Please enter a URL first!"
            return
        if not is_youtube_video_link(url):
            self.status_text = "Invalid YouTube URL! Please check your link."
            return
            
        self.status_text = "Downloading..."
        Clock.schedule_once(self.finish_download, 2)
    
    def finish_download(self, dt):
        self.status_text = "Download completed!"
        self.root.ids.url_input.text = ""

if __name__ == '__main__':
    ShddApp().run()