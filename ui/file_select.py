import sys
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton, QFileDialog, QLabel, QStackedWidget, QSizePolicy
)
class FileSelectWidget(QWidget):
    def __init__(self, on_file_selected):
        super().__init__()
        layout = QVBoxLayout()
        
        self.label = QLabel("Drag and drop file here!")
        self.label.setAlignment(Qt.AlignCenter)  # Centers text horizontally and vertically
        self.label.setFont(QFont('Segoe UI', 20))
        self.label.setStyleSheet("padding: 20px; font-weight: bold; color: #333;")  # Increase font size (20pt, can adjust)
        self.label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        layout.addWidget(self.label)

        self.btn_browse = QPushButton("Browse and Select a PDF file")
        self.btn_browse.clicked.connect(self.open_file_dialog)
        layout.addWidget(self.btn_browse)
        self.setLayout(layout)
        self.on_file_selected = on_file_selected

        # Enable drag and drop
        self.setAcceptDrops(True)

    def open_file_dialog(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, 'Open PDF File', '', 'PDF Files (*.pdf)'
        )
        if file_path and file_path.lower().endswith('.pdf'):
            self.label.setText(f"Selected: {file_path}")
            self.on_file_selected(file_path)
        elif file_path:
            self.label.setText("❌ Please select a PDF file.")

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            urls = event.mimeData().urls()
            if urls and urls[0].toLocalFile().lower().endswith('.pdf'):
                event.acceptProposedAction()
            else:
                event.ignore()
        else:
            event.ignore()

    def dropEvent(self, event):
        if event.mimeData().hasUrls():
            urls = event.mimeData().urls()
            file_path = urls[0].toLocalFile()
            if file_path.lower().endswith('.pdf'):
                self.label.setText(f"Selected: {file_path}")
                self.on_file_selected(file_path)
            else:
                self.label.setText("❌ Please select a PDF file.")