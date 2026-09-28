ESTILO_GLOBAL = """
QWidget {
    background-color: #F5F6FA;
    font-family: 'Segoe UI', sans-serif;
    font-size: 13px;
    color: #333333;
}

QLineEdit, QDateEdit {
    background-color: white;
    border: 1px solid #DDDDDD;
    border-radius: 10px;
    padding: 8px 12px;
    font-size: 13px;
}

QLineEdit:focus, QDateEdit:focus {
    border: 1px solid #2E7DE1;
}

QDateEdit::drop-down {
    border: none;
    width: 26px;
    background: transparent;
}

QDateEdit::down-arrow {
    width: 12px;
    height: 12px;
}

QPushButton {
    background-color: #2E7DE1;
    color: white;
    border: none;
    border-radius: 16px;
    padding: 10px 22px;
    font-size: 13px;
    font-weight: bold;
}

QPushButton:hover {
    background-color: #245FB0;
}

QPushButton:pressed {
    background-color: #1E2761;
}

QLabel#titulo {
    font-size: 22px;
    font-weight: bold;
    color: #1E2761;
}

QTableWidget, QListWidget {
    background-color: white;
    border: 1px solid #DDDDDD;
    border-radius: 10px;
    gridline-color: #EEEEEE;
}

QHeaderView::section {
    background-color: #F0F2F8;
    color: #1E2761;
    padding: 6px;
    border: none;
    font-weight: bold;
}

QCheckBox {
    font-size: 13px;
}
"""