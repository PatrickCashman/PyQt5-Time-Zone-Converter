import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QComboBox, QHBoxLayout
from PyQt5.QtCore import QTimer, Qt
from datetime import datetime
import pytz
from tzlocal import get_localzone

class DigitalClock(QWidget):
    def __init__(self):
        super().__init__()
        self.time_label = QLabel(self)
        self.timezone_label = QLabel(self)  
        self.timer = QTimer(self)
        self.timezone_combo = QComboBox(self)
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Timezone Converter")

        window_width = 400
        window_height = 200

        # Center the window on the screen
        screen_geometry = QApplication.desktop().screenGeometry()
        x = (screen_geometry.width() - window_width) // 2
        y = (screen_geometry.height() - window_height) // 2
        self.setGeometry(x, y, window_width, window_height)

        vbox = QVBoxLayout()
        hbox = QHBoxLayout()  # Horizontal layout for combo box and timezone label

        vbox.addWidget(self.time_label)
        hbox.addWidget(self.timezone_combo)
        hbox.addWidget(self.timezone_label)
        vbox.addLayout(hbox)
        self.setLayout(vbox)

        self.time_label.setAlignment(Qt.AlignCenter)
        self.timezone_label.setAlignment(Qt.AlignCenter)
        self.time_label.setStyleSheet("font-size: 50px;")
        self.timezone_label.setStyleSheet("font-size: 30px;")

        # Populate the combo box with timezones
        self.populate_timezones()

        self.timer.timeout.connect(self.update_time)
        self.timer.start(1000)
        self.update_time()

        # Connect the combo box selection change signal to update the time
        self.timezone_combo.currentIndexChanged.connect(self.update_time)

    def populate_timezones(self):
        timezones = pytz.all_timezones
        self.timezone_combo.addItems(timezones)

        # Set the default timezone to the local timezone
        local_timezone = get_localzone() 
        local_timezone_name = local_timezone.key
        index = self.timezone_combo.findText(local_timezone_name)
        if index >= 0:
            self.timezone_combo.setCurrentIndex(index)

    def update_time(self):
        selected_timezone = self.timezone_combo.currentText()
        timezone = pytz.timezone(selected_timezone)
        current_time = datetime.now(timezone).strftime("%I:%M:%S %p")
        timezone_name = timezone.zone

        self.time_label.setText(current_time)
        self.timezone_label.setText(timezone_name)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    clock = DigitalClock()
    clock.show()
    sys.exit(app.exec_())
