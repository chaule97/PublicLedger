from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QTableWidget,
    QTableWidgetItem,
    QHeaderView,
    QHBoxLayout,
    QPushButton,
    QStyle,
)
from PyQt6.QtCore import Qt


class LedgerTableView(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
    
    def initUI(self):
        self.setWindowTitle("Sổ Thu Chi")
        
        layout = QVBoxLayout()
        
        hbox1 = QHBoxLayout()
        back_button = QPushButton()
        back_button.setIcon(
            self.style().standardIcon(QStyle.StandardPixmap.SP_ArrowBack)
        )
        back_button.clicked.connect(self.backButtonClicked)

        hbox1.addWidget(back_button)

        hbox1.addStretch()
        
        layout.addLayout(hbox1)
        
        self.table = self.createTableView()
        
        layout.addWidget(self.table)
        
        self.setLayout(layout)
        
        self.showMaximized()
        
    def createTableView(self):
        table = QTableWidget(12, 7)  # 2 header rows + 10 data rows, 9 columns
        
        table.setSpan(0, 0, 2, 1)
        table.setSpan(0, 1, 1, 2) # "Số phiếu" spans
        table.setSpan(0, 3, 2, 1) # "DIỄN GIẢI" spans
        table.setSpan(0, 4, 1, 3) # "SỐ TIỀN" spans

        # Fill header rows manually
        headers_row1 = ["Ngày tháng", "Số phiếu", "", "DIỄN GIẢI", "SỐ TIỀN", "", ""]
        headers_row2 = ["", "Thu", "Chi", "NỘI DUNG CHI", "THU", "CHI", "TỒN",]
        
        for col, text in enumerate(headers_row1):
            item = QTableWidgetItem(text)
            item.setFlags(Qt.ItemFlag.ItemIsEnabled)
            table.setItem(0, col, item)

        for col, text in enumerate(headers_row2):
            item = QTableWidgetItem(text)
            item.setFlags(Qt.ItemFlag.ItemIsEnabled)
            table.setItem(1, col, item)

        # Optional: center-align header cells
        for row in [0, 1]:
            for col in range(9):
                item = table.item(row, col)
                if item:
                    item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)

        # # Freeze header rows (make them uneditable)
        for col in range(7):
            table.item(0, col).setFlags(Qt.ItemFlag.ItemIsEnabled)
            table.item(1, col).setFlags(Qt.ItemFlag.ItemIsEnabled)
        
        table.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeMode.Stretch)
        # Make the table editable from row 2 onward (row 0, 1 are headers)
        table.setVerticalHeaderLabels([""]*12)  # hide row numbers
        table.horizontalHeader().hide()
        
        return table
    
    def backButtonClicked(self):
        from .home import Home
        self.screen = Home()
        self.close()