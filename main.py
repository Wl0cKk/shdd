from kivy.app import App
from kivy.properties import StringProperty
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.utils import platform
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
import os
import re
import yt_dlp
import threading

def is_youtube_video_link(url):
    pattern = r'^(?:https?://)?(?:www\.|m\.)?(?:youtube\.com/(?:watch\?v=|v/|shorts/|embed/)|youtu\.be/)[\w-]{11}(?:&|\?|$| )'
    return bool(re.match(pattern, url.strip(), re.IGNORECASE))

class ShddApp(App):
    status_text = StringProperty('')
    
    def on_start(self):
        if platform in ['win', 'linux', 'macosx', 'darwin', 'unknown']:
            Window.size = (400, 600)
            Window.minimum_width = 400
            Window.minimum_height = 600
    
    def get_download_path(self):
        if platform == 'android':
            try:
                from android.storage import primary_external_storage_path
                primary_storage = primary_external_storage_path()
                download_path = os.path.join(primary_storage, 'Download')
                test_file = os.path.join(download_path, 'test_write.tmp')
                with open(test_file, 'w') as f:
                    f.write('test')
                os.remove(test_file)
                
            except (OSError, PermissionError):
                from jnius import autoclass
                Context = autoclass('android.content.Context')
                PythonActivity = autoclass('org.kivy.android.PythonActivity')
                context = PythonActivity.mActivity
                files_dir = context.getExternalFilesDir(None)
                download_path = files_dir.getAbsolutePath()
        
        elif platform == 'ios':
            download_path = os.path.expanduser('~/Documents')
        else:
            download_path = os.path.expanduser('~/Downloads')
        
        os.makedirs(download_path, exist_ok=True)
        return download_path
    
    def safe_button_disable(self, disabled):
        try:
            if hasattr(self, 'root') and self.root and hasattr(self.root, 'ids'):
                self.root.ids.download_btn.disabled = disabled
        except (KeyError, AttributeError):
            pass
    
    def download_short(self):
        url = self.root.ids.url_input.text.strip()
        if not url:
            self.status_text = "Please enter a URL first!"
            return
        if not is_youtube_video_link(url):
            self.status_text = "Please check your link."
            return
            
        self.status_text = "Downloading..."
        self.safe_button_disable(True)
        threading.Thread(target=self.start_download, args=(url,), daemon=True).start()
    
    def start_download(self, url):
        try:
            download_path = self.get_download_path()
            
            ydl_opts = {
                'outtmpl': os.path.join(download_path, '%(title).100s.%(ext)s'),
                'format': 'best[height<=720]',
                'quiet': True,
                'no_warnings': True,
            }
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            
            Clock.schedule_once(lambda dt: self.download_complete(download_path))
            
        except Exception as e:
            Clock.schedule_once(lambda dt: self.download_error(str(e)))
    
    def download_complete(self, download_path):
        self.status_text = f"Download completed, see your Download folder!\n"
        self.root.ids.url_input.text = ""
        self.safe_button_disable(False)
    
    def download_error(self, error_msg):
        self.status_text = f"Download failed: {error_msg}"
        self.safe_button_disable(False)
        self.show_popup("Error", f"Download failed:\n{error_msg}")
    
    def show_popup(self, title, message):
        content = BoxLayout(orientation='vertical', padding=10, spacing=10)
        content.add_widget(Label(text=message, text_size=(None, None)))
        
        close_btn = Button(text='Close', size_hint_y=None, height=50)
        popup = Popup(
            title=title,
            content=content,
            size_hint=(0.8, 0.4)
        )
        close_btn.bind(on_press=popup.dismiss)
        content.add_widget(close_btn)
        
        popup.open()

if __name__ == '__main__':
    ShddApp().run()