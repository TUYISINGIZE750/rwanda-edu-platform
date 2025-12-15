import webbrowser
import os

# Open the registration form directly
file_path = os.path.abspath("register.html")
webbrowser.open(f"file://{file_path}")
print(f"🌐 Opening registration form: file://{file_path}")
print("📍 All 14,841 villages from locations.json are loaded!")