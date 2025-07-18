from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QDateEdit,
    QPushButton,
)
from PyQt6.QtGui import QFont, QGuiApplication
from views.setting import SettingForm
from views.income import IncomeView
from views.outcome import OutcomeView
from views.ledger_table import LedgerTableView
from PyQt6 import QtCore


class Home(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        screen = QGuiApplication.primaryScreen()
        
        geometry = screen.availableGeometry()
        desktop_width = geometry.width()
        desktop_height = geometry.height()

        width = int(desktop_width * 0.23)
        height = int(desktop_height * 0.34)

        self.resize(width, height)

        hbox1 = QHBoxLayout()
        hbox1.addStretch()

        vbox1 = QVBoxLayout()
        vbox1.addSpacing(30)

        label = QLabel("Phần mềm thu chi")
        font = QFont('Times', 20)
        label.setFont(font)
        label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        vbox1.addWidget(label)

        self.month_input = QDateEdit()
        self.month_input.setCurrentSection(
            QDateEdit.Section.MonthSection 
        )
        self.month_input.setDateTime(
            QtCore.QDateTime.currentDateTime()
        )
        self.month_input.setDisplayFormat("MM/yyyy")
        vbox1.addWidget(self.month_input)

        hbox2 = QHBoxLayout()

        income_button = QPushButton("Thu")
        income_button.clicked.connect(self.incomeButtonClicked)

        expense_button = QPushButton("Chi")
        expense_button.clicked.connect(self.expenseButtonClicked)

        hbox2.addWidget(income_button)
        hbox2.addWidget(expense_button)
        
        vbox1.addLayout(hbox2)
        
        ledger_table_button = QPushButton("Số quỹ tiền mặt")
        ledger_table_button.clicked.connect(self.ledgerTableButtonClicked)
        vbox1.addWidget(ledger_table_button)
        
        setting_button = QPushButton("Cấu hình")
        setting_button.clicked.connect(self.settingButtonClicked)
        vbox1.addWidget(setting_button)
        
        vbox1.addSpacing(30)

        hbox1.addLayout(vbox1)

        hbox1.addStretch()
        self.setLayout(hbox1)
        self.setWindowTitle("Phần mềm thu chi")
        self.show()


    def incomeButtonClicked(self):
        date = self.month_input.date().toPyDate()
        
        self.screen = IncomeView(date.month, date.year)

        self.close()

    def expenseButtonClicked(self):
        date = self.month_input.date().toPyDate()
        
        self.screen = OutcomeView(date.month, date.year)

        self.close()
        
    def ledgerTableButtonClicked(self):
        date = self.month_input.date().toPyDate()
        
        self.ledger_table = LedgerTableView(date.month, date.year)
        self.ledger_table.show()
        self.close()
        
    def settingButtonClicked(self):
        self.setting_form = SettingForm()
        self.setting_form.show()
        self.close()