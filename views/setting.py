from PyQt6.QtWidgets import (
    QWidget, QLineEdit, QPushButton,
    QVBoxLayout, QHBoxLayout, QFormLayout, QMessageBox, QStyle
)
from PyQt6.QtCore import Qt
from models.setting import Setting

class SettingForm(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Cài đặt thông tin")
        self.resize(400, 300)
        self.initUI()

    def initUI(self):
        main_layout = QVBoxLayout()
        
        top_bar = QHBoxLayout()
        self.back_button = QPushButton()
        self.back_button.setIcon(
            self.style().standardIcon(QStyle.StandardPixmap.SP_ArrowBack)
        )
        self.back_button.clicked.connect(self.go_back)
        top_bar.addWidget(self.back_button, alignment=Qt.AlignmentFlag.AlignLeft)

        main_layout.addLayout(top_bar)
        
        form_layout = QFormLayout()

        self.department_input = QLineEdit()
        self.agency_input = QLineEdit()
        self.address_input = QLineEdit()
        
        self.chief_label_input = QLineEdit()
        self.chief_input = QLineEdit()
        
        self.chief_accountant_label_input = QLineEdit()
        self.chief_accountant_input = QLineEdit()
        
        self.treasurer_label_input = QLineEdit()
        self.treasurer_input = QLineEdit()

        form_layout.addRow("Phòng ban:", self.department_input)
        form_layout.addRow("Cơ quan:", self.agency_input)
        form_layout.addRow("Địa chỉ:", self.address_input)
        form_layout.addRow(self.chief_label_input, self.chief_input)
        form_layout.addRow(self.chief_accountant_label_input, self.chief_accountant_input)
        form_layout.addRow(self.treasurer_label_input, self.treasurer_input)
        
        main_layout.addLayout(form_layout)

        self.save_button = QPushButton("Lưu")
        self.save_button.clicked.connect(self.save_settings)
        main_layout.addWidget(self.save_button, alignment=Qt.AlignmentFlag.AlignCenter)

        self.setLayout(main_layout)
        self.load_existing_settings()

    def save_settings(self):
        Setting.set_value("department", self.department_input.text())
        Setting.set_value("agency", self.agency_input.text())
        Setting.set_value("address", self.address_input.text())
        Setting.set_value("chief_label", self.chief_label_input.text())
        Setting.set_value("chief", self.chief_input.text())
        Setting.set_value("chief_accountant_label", self.chief_accountant_label_input.text())
        Setting.set_value("chief_accountant", self.chief_accountant_input.text())
        Setting.set_value("treasurer_label", self.treasurer_label_input.text())
        Setting.set_value("treasurer", self.treasurer_input.text())

        QMessageBox.information(self, "Thành công", "Đã lưu thông tin cài đặt.")
        
    def go_back(self):
        from views.home import Home
        self.view = Home()
        self.close()

    def load_existing_settings(self):
        self.department_input.setText(Setting.get_value("department", ""))
        self.agency_input.setText(Setting.get_value("agency", ""))
        self.address_input.setText(Setting.get_value("address", ""))
        self.chief_label_input.setText(Setting.get_value("chief_label", "Thủ trưởng"))
        self.chief_input.setText(Setting.get_value("chief", ""))
        self.chief_accountant_label_input.setText(Setting.get_value("chief_accountant_label", "Kế toán trưởng"))
        self.chief_accountant_input.setText(Setting.get_value("chief_accountant", ""))
        self.treasurer_label_input.setText(Setting.get_value("treasurer_label", "Thủ quỹ"))
        self.treasurer_input.setText(Setting.get_value("treasurer", ""))
