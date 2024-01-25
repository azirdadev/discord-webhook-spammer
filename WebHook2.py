from PyQt5.QtWidgets import (
    QApplication, QWidget, QPushButton, QVBoxLayout, QTabWidget,
    QGridLayout, QLineEdit, QLabel, QFrame, QFileDialog, QComboBox, QTextEdit,
    QColorDialog, QCheckBox, QGroupBox
)
from PyQt5.QtGui import QIcon, QColor
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtWidgets import QTabBar, QLineEdit, QPushButton, QVBoxLayout
import configparser
import requests
from PyQt5.QtCore import Qt, QPropertyAnimation, QEasingCurve
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QStackedWidget, QPushButton, QLabel

class AnimatedTabWidget(QStackedWidget):
    def __init__(self):
        super().__init__()

        self.currentChanged.connect(self.slide_in_current_tab)
        self.animation_speed = 500

    def slide_in_current_tab(self, index):
        current_tab_widget = self.widget(index)
        if current_tab_widget:
            self.slide_in_animation(current_tab_widget)

    def slide_in_animation(self, widget):
        current_index = self.currentIndex()
        next_index = self.indexOf(widget)

        direction = -1 if current_index > next_index else 1

        widget.setGeometry(direction * self.width(), 0, self.width(), self.height())

        slide_animation = QPropertyAnimation(widget, b"geometry")
        slide_animation.setStartValue(widget.geometry())
        slide_animation.setEndValue(self.rect())
        slide_animation.setDuration(self.animation_speed)
        slide_animation.setEasingCurve(QEasingCurve.OutCubic)

        slide_animation.start()

class RainbowBorderFrame(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.hue = 0
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_border_color)
        self.timer.start(50)

    def update_border_color(self):
        self.hue = (self.hue + 1) % 360
        color = QColor.fromHsv(self.hue, 255, 255)
        self.setStyleSheet(f"border: 2px solid {color.name()};")

class BrighterTabBar(QTabBar):
    def paintEvent(self, event):
        painter = self.Painter(self)
        option = self.TabBarOption()

        self.initStyleOption(option)
        for index in range(self.count()):
            self.drawTab(index, painter)

class BrighterPushButton(QPushButton):
    def __init__(self, text, parent=None):
        super(BrighterPushButton, self).__init__(text, parent)
        self.setStyleSheet("""
            QPushButton {
                background-color: #3498db; /* Brighter blue color */
                color: #ffffff; /* White text */
                border: 1px solid #2980b9; /* Darker blue border */
                border-radius: 4px;
                padding: 5px 10px;
            }

            QPushButton:hover {
                background-color: #2980b9; /* Darker blue on hover */
            }
        """)

class BrighterLineEdit(QLineEdit):
    def __init__(self, parent=None):
        super(BrighterLineEdit, self).__init__(parent)
        self.setStyleSheet("""
            QLineEdit {
                border: 1px solid #3498db; /* Brighter blue border */
                padding: 5px;
            }
        """)

class WebhookApp(QWidget):
    def __init__(self):
        super().__init__()


        self.setWindowTitle("Kona's Discord WebHook Tools :3333")
        self.setWindowIcon(QIcon('icon.png'))
        self.setGeometry(100, 100, 600, 400)
        rainbow_border_frame = RainbowBorderFrame(self)
        rainbow_border_frame.setGeometry(0, 0, self.width(), self.height())
        self.custom_name_entry = QLineEdit(self)
        self.custom_pfp_entry = QLineEdit(self)
        self.webhook_url_entry = QLineEdit(self)
        
        try:
            self.init_ui()
        except AttributeError as e:
            print(f"AttributeError: {e}")
        except TypeError as e:
            print(f"TypeError: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

    def init_ui(self):
        bg_color = "#000000"  
        foreground_color = "#000000"
        button_bg_color = "#000000" 
        button_fg_color = "#000000"

        self.tabs = AnimatedTabWidget()

        self.tabs = QTabWidget()
        self.tab_send_message = QWidget()
        self.tab_spammer = QWidget()
        self.tab_deleter = QWidget()
        self.tab_settings = QWidget()
        self.tab_embed_editor = QWidget()
        self.tab_credits = QWidget()

        self.tabs.addTab(self.tab_send_message, "Send Webhook Message")
        self.tabs.addTab(self.tab_spammer, "WebHook Spammer")
        self.tabs.addTab(self.tab_deleter, "WebHook Deleter")
        self.tabs.addTab(self.tab_embed_editor, "Embed Message")
        self.tabs.addTab(self.tab_settings, "Settings")
        self.tabs.addTab(self.tab_credits, "Credits")

        self.configurations = configparser.ConfigParser()

        self.init_send_message_tab(bg_color, foreground_color, button_bg_color, button_fg_color)
        self.init_spammer_tab()
        self.init_deleter_tab()
        self.init_embed_editor_tab()
        self.init_settings_tab()
        self.init_credits_tab()

        layout = QVBoxLayout()
        layout.setContentsMargins(0, 20, 0, 0)
        layout.addWidget(self.tabs)
        self.setLayout(layout)

        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)

        self.title_bar = QFrame(self)
        self.title_bar.setGeometry(0, 0, self.width(), 30)

        close_button = QPushButton("X", self.title_bar)
        close_button.setGeometry(self.width() - 30, 0, 30, 30)
        close_button.clicked.connect(self.close)

        layout.addWidget(self.tabs)
        self.setLayout(layout)

        self.title_bar.mousePressEvent = self.mousePressEvent
        self.title_bar.mouseMoveEvent = self.mouseMoveEvent
        self.title_bar.mouseReleaseEvent = self.mouseReleaseEvent

        self.set_theme()

        self.theme_combobox.currentIndexChanged.connect(self.set_theme)

    def set_theme(self):
        theme = self.theme_combobox.currentText()

        if theme == "Dark":
            self.setStyleSheet(self.dark_theme_style())
        elif theme == "Waves":
            self.setStyleSheet(self.light_theme_style())

    def dark_theme_style(self):
        return """
            background-color: #000000;
            color: #abb2bf;
            QLineEdit {
                border: 1px solid navy;
            }
        """

    def light_theme_style(self):
        return """
            background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #2c3e50, stop:1 #19232d);
            color: #abb2bf;
            QLineEdit {
                border: 1px solid navy;
            }
        """

    def init_send_message_tab(self, bg_color, foreground_color, button_bg_color, button_fg_color, webhook_url=""):
        # Send Webhook Message Tab
        layout = QGridLayout()

        layout.addWidget(QLabel("Message Content:"), 1, 0)
        self.message_entry = QLineEdit(self)
        layout.addWidget(self.message_entry, 1, 1)

        layout.addWidget(QLabel("Custom Name:"), 2, 0)
        self.custom_name_entry = QLineEdit(self)
        layout.addWidget(self.custom_name_entry, 2, 1)

        layout.addWidget(QLabel("Custom PFP URL:"), 3, 0)
        self.custom_pfp_entry = QLineEdit(self)
        layout.addWidget(self.custom_pfp_entry, 3, 1)

        self.send_button = QPushButton("Send Webhook", self)
        self.send_button.clicked.connect(self.send_webhook)
        layout.addWidget(self.send_button, 4, 0, 1, 2)

        self.save_config_button = QPushButton("Save Config", self)
        self.save_config_button.clicked.connect(self.save_config)
        layout.addWidget(self.save_config_button, 5, 0, 1, 2)
        
        self.tab_send_message.setLayout(layout)

    def init_credits_tab(self):
        layout = QVBoxLayout(self.tab_credits)
        credits_label = QLabel("Kona\nChatGPT\nOsama")
        credits_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(credits_label)

    def init_settings_tab(self):
        # Settings Tab
        layout = QGridLayout()

        layout.addWidget(QLabel("Discord Webhook URL:"), 0, 0)
        self.spammer_webhook_url_entry = QLineEdit(self)
        layout.addWidget(self.webhook_url_entry, 0, 1)
        
        theme_label = QLabel("Select Theme:")
        self.theme_combobox = QComboBox()
        self.theme_combobox.addItems(["Dark", "Waves"])
        self.theme_combobox.setCurrentIndex(0)
        layout.addWidget(theme_label, 1, 0)
        layout.addWidget(self.theme_combobox, 1, 1)

        always_on_top_label = QLabel("Always On Top:")
        self.always_on_top_checkbox = QCheckBox(self)
        self.always_on_top_checkbox.setChecked(True)
        self.always_on_top_checkbox.setStyleSheet(
            "QCheckBox {"
            "   spacing: 2px;"
            "   border: 2px solid transparent;"
            "   border-radius: 8px;"
            "}"
            "QCheckBox::indicator {"
            "   width: 20px;"
            "   height: 20px;"
            "}"
            "QCheckBox::indicator:checked {"
            "   background-color: darkgreen;"
            "   border-color: darkgreen;"
            "}"
            "QCheckBox::indicator:unchecked {"
            "   background-color: darkred;"
            "   border-color: darkred;"
            "}"
        )
        layout.addWidget(always_on_top_label, 2, 0)
        layout.addWidget(self.always_on_top_checkbox, 2, 1)
        self.always_on_top_checkbox.stateChanged.connect(self.toggle_always_on_top)

        self.tab_settings.setLayout(layout)

    def toggle_always_on_top(self, state):
        if state == Qt.Checked:
            self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)
        else:
            self.setWindowFlags(self.windowFlags() & ~Qt.WindowStaysOnTopHint)
        self.show()

    def draw_border(self):
        border_color = QColor(255, 0, 0)
        self.setStyleSheet(f"border: 2px solid {border_color.name()};")
        self.border_animation_timer = QTimer(self)
        self.border_animation_timer.timeout.connect(self.animate_border)
        self.border_animation_timer.start(200)

    def animate_border(self):
        current_color = QColor(self.styleSheet().split(":")[2])
        next_color = current_color.lighter(10)

        self.setStyleSheet(f"border: 2px solid {next_color.name()};")

        if current_color.red() > next_color.red():
            self.border_animation_timer.stop()
            self.setStyleSheet("border: 2px solid transparent;")

    def init_embed_editor_tab(self, webhook_url=""):
        # Embed Tab
        layout = QVBoxLayout()

        embed_fields = ["Title", "Description", "Color", "Field Name 1", "Field Value 1"]

        embed_group = QGroupBox(self)
        grid_layout = QGridLayout(embed_group)

        self.embed_fields = {}

        for row, field_name in enumerate(embed_fields):
            if field_name == "Color":
                color_button = QPushButton("Pick Color", self)
                color_button.clicked.connect(self.pick_color)
                self.embed_fields[field_name] = color_button
                grid_layout.addWidget(QLabel(field_name + ":"), row, 0)
                grid_layout.addWidget(color_button, row, 1)
            else:
                widget = QLineEdit(self)
                widget.setStyleSheet("border: 1px solid navy;")
                self.embed_fields[field_name] = widget
                grid_layout.addWidget(QLabel(field_name + ":"), row, 0)
                grid_layout.addWidget(widget, row, 1)

        send_embed_button = QPushButton("Send Embed", self)
        send_embed_button.clicked.connect(self.send_embed_message)
        layout.addWidget(embed_group)
        layout.addWidget(send_embed_button)

        self.tab_embed_editor.setLayout(layout)
        self.tabs.setTabEnabled(4, True)

        self.setFixedSize(self.width(), self.height())
        
    def send_embed_message(self):
        # Retrieve embed values
        embed_values = {}
        for field_name, widget in self.embed_fields.items():
            embed_values[field_name] = widget.text()

        payload = {
            "embed": {
                "title": embed_values.get("Title", ""),
                "description": embed_values.get("Description", ""),
                "color": int(embed_values.get("Color", "0"), 16),
                "fields": [
                    {
                        "name": embed_values.get("Field Name 1", ""),
                        "value": embed_values.get("Field Value 1", ""),
                        "inline": False,
                    },
                ],
            }
        }

        headers = {"Content-Type": "application/json"}

        webhook_url = self.spammer_webhook_url_entry.text()

        try:
            response = requests.post(webhook_url, json=payload, headers=headers, verify=True)
            response.raise_for_status()
            print("Embed message sent successfully!")
        except requests.exceptions.RequestException as e:
            print(f"Failed to send embed message. Error: {e}")
            
    def message_type_changed(self, index):
        self.tabs.setTabEnabled(4, index == 1)

    def init_spammer_tab(self, webhook_url=""):
        # WebHook Spammer Tab
        layout = QGridLayout()

        layout.addWidget(QLabel("Message Content:"), 0, 0)
        self.spammer_message_entry = QLineEdit(self)
        layout.addWidget(self.spammer_message_entry, 0, 1)

        layout.addWidget(QLabel("Repeat Count:"), 1, 0)
        self.repeat_count_entry_spammer = QLineEdit(self)
        layout.addWidget(self.repeat_count_entry_spammer, 1, 1)

        self.spam_button = QPushButton("Start Spammer", self)
        self.spam_button.clicked.connect(self.start_spammer)
        layout.addWidget(self.spam_button, 2, 0, 1, 2)

        self.save_config_button_spammer = QPushButton("Save Config", self)
        self.save_config_button_spammer.clicked.connect(self.save_config_spammer)
        layout.addWidget(self.save_config_button_spammer, 3, 0, 1, 2)

        self.load_config_button_spammer = QPushButton("Load Config NW", self)
        self.load_config_button_spammer.clicked.connect(self.load_selected_config_spammer)
        layout.addWidget(self.load_config_button_spammer, 4, 0, 1, 2)

        self.tab_spammer.setLayout(layout)

    def init_deleter_tab(self):
        # WebHook Deleter Tab
        layout = QGridLayout()

        layout.addWidget(QLabel("Discord Webhook URL:"), 0, 0)
        self.deleter_webhook_url_entry = QLineEdit(self)
        layout.addWidget(self.deleter_webhook_url_entry, 0, 1)

        self.delete_button = QPushButton("Delete Webhook", self)
        self.delete_button.clicked.connect(self.delete_webhook)
        layout.addWidget(self.delete_button, 1, 0, 1, 2)

        self.tab_deleter.setLayout(layout)
        
    def pick_color(self):
        color = QColorDialog.getColor()
        if color.isValid():
            self.embed_fields["Color"].setText(color.name())

    def send_webhook(self):
        webhook_url = self.webhook_url_entry.text()
        message = self.message_entry.text()
        custom_name = self.custom_name_entry.text()
        custom_pfp = self.custom_pfp_entry.text()

        payload = {
            "content": message,
            "username": custom_name,
            "avatar_url": custom_pfp
        }
        headers = {"Content-Type": "application/json"}

        try:
            response = requests.post(webhook_url, json=payload, headers=headers, verify=True)
            response.raise_for_status()
            print("Webhook message sent successfully!")
        except requests.exceptions.RequestException as e:
            print(f"Failed to send webhook message. Error: {e}")

    def start_spammer(self):
        webhook_url = self.spammer_webhook_url_entry.text()
        message = self.spammer_message_entry.text()
        repeat_count = int(self.repeat_count_entry_spammer.text())
        custom_name = self.custom_name_entry.text()
        custom_pfp = self.custom_pfp_entry.text()

        payload = {
            "content": message,
            "username": custom_name,
            "avatar_url": custom_pfp
        }
        headers = {"Content-Type": "application/json"}

        try:
            for i in range(repeat_count):
                response = requests.post(webhook_url, json=payload, headers=headers, verify=True)
                response.raise_for_status()
                print(f"Webhook message {i + 1} sent successfully!")
        except requests.exceptions.RequestException as e:
            print(f"Failed to send webhook message. Error: {e}")
            
    def delete_webhook(self):
        webhook_url = self.deleter_webhook_url_entry.text()

        try:
            response = requests.delete(webhook_url)
            response.raise_for_status()
            print("Webhook deleted successfully!")
        except requests.exceptions.RequestException as e:
            print(f"Failed to delete webhook. Error: {e}")

    def save_config(self):
        custom_name = self.custom_name_entry.text()
        config_name = f"{custom_name}_config.cfg"

        self.configurations[custom_name] = {
            "webhook_url": self.webhook_url_entry.text(),
            "message": self.message_entry.text(),
            "custom_name": custom_name,
            "custom_pfp": self.custom_pfp_entry.text(),
            "repeat_count": self.repeat_count_entry_spammer.text()
        }

        with open(config_name, "w") as config_file:
            self.configurations.write(config_file)

        self.load_config_dropdown.addItem(custom_name)

    def save_config_spammer(self):
        custom_name = self.custom_name_entry.text()
        config_name = f"{custom_name}_config_spammer.cfg"

        self.configurations[custom_name] = {
            "webhook_url": self.spammer_webhook_url_entry.text(),
            "message": self.spammer_message_entry.text(),
            "custom_name": custom_name,
            "custom_pfp": self.custom_pfp_entry.text(),
            "repeat_count": self.repeat_count_entry_spammer.text()
        }

        with open(config_name, "w") as config_file:
            self.configurations.write(config_file)

        self.load_config_dropdown_spammer.addItem(custom_name)

    def load_selected_config_spammer(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        options |= QFileDialog.HideNameFilterDetails

        config_name, _ = QFileDialog.getOpenFileName(
            self, "Load Config File", "", "Config Files (*.cfg);;All Files (*)", options=options
        )
        if config_name:
            self.load_config_data_spammer(config_name)

    def load_config_data_spammer(self, config_name):
        config_parser = configparser.ConfigParser()
        config_parser.read(config_name)

        if 'WebhookConfig' in config_parser:
            config_data = config_parser['WebhookConfig']

            if hasattr(self, 'spammer_webhook_url_entry'):
                self.spammer_webhook_url_entry.setText(config_data.get("webhook_url", ""))

            if hasattr(self, 'spammer_message_entry'):
                self.spammer_message_entry.setText(config_data.get("message", ""))

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton and event.y() < 30:
            self.draggable = True
            self.offset = event.pos()
            self.setWindowOpacity(0.5)

    def mouseMoveEvent(self, event):
        if self.draggable:
            self.move(self.pos() + event.pos() - self.offset)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.draggable = False
            self.setWindowOpacity(1)

if __name__ == "__main__":
    app = QApplication([])
    app.setStyle("Fusion")

    main_win = WebhookApp()
    main_win.show()

    app.exec_()
