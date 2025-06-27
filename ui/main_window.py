import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton, QFileDialog, QLabel, QStackedWidget, QSizePolicy
)
from PyQt5.QtGui import QFont
from file_select import FileSelectWidget
class PDFTableExtractorMainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('PDF Table Extractor')
        self.setGeometry(100, 100, 1200, 900)  # Large enough for PDF page
        self.layout = QVBoxLayout(self)
        self.stacked = QStackedWidget()
        self.layout.addWidget(self.stacked)
        self.setLayout(self.layout)

        self.file_select_widget = FileSelectWidget(self.file_selected)
        self.stacked.addWidget(self.file_select_widget)

        # Placeholder widgets for next steps
        self.watermark_widget = QLabel("Watermark Cleaner UI goes here")
        self.box_maker_widget = QLabel("Box Maker UI goes here")

        self.stacked.addWidget(self.watermark_widget)
        self.stacked.addWidget(self.box_maker_widget)

    def file_selected(self, file_path):
        self.selected_file = file_path
        # Example: go to watermark cleaner or box maker
        # self.stacked.setCurrentWidget(self.watermark_widget)
        self.stacked.setCurrentWidget(self.box_maker_widget)  # or whichever step you want

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setFont(QFont("Segoe UI", 13))
    window = PDFTableExtractorMainWindow()
    window.show()
    sys.exit(app.exec_())