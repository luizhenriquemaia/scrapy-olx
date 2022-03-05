import sys

from scrapy.cmdline import execute
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow


def init_property_spider(region: str, apartment: bool,  filename: str):
    execute([
        'scrapy', 'crawl', 'property', '-a', f'region={region}', 
        '-a', f'apartment={apartment}', '-o', f'{filename}', '-t', 'csv'])

class Windown(QMainWindow):

    def __init__(self) -> None:
        super().__init__()
        self.setGeometry(600, 200, 450, 500)
        self.setWindowTitle("Olx imóveis crawler")
        self.initUI()

    def initUI(self):
        self.label_property_type = QtWidgets.QLabel(self)
        self.label_property_type.setText("Tipo de imóvel")
        self.label_property_type.move(50, 60)
        self.label_property_type.adjustSize()

        self.combo_property_choices = QtWidgets.QComboBox(self)
        self.combo_property_choices.setGeometry(QtCore.QRect(200,50,200,40))
        self.combo_property_choices.addItem("Apartamento")
        self.combo_property_choices.addItem("Casa")

        self.label_region = QtWidgets.QLabel(self)
        self.label_region.setText("Região")
        self.label_region.move(50, 110)
        self.label_region.adjustSize()

        self.input_region = QtWidgets.QLineEdit(self)
        self.input_region.setGeometry(QtCore.QRect(200,100,200,40))

        self.label_file_name = QtWidgets.QLabel(self)
        self.label_file_name.setText("Nome do arquivo")
        self.label_file_name.move(50, 160)
        self.label_file_name.adjustSize()

        self.input_file_name = QtWidgets.QLineEdit(self)
        self.input_file_name.setGeometry(QtCore.QRect(200,150,200,40))

        self.button_start = QtWidgets.QPushButton(self)
        self.button_start.setText("Ok")
        self.button_start.clicked.connect(self.start_spider)
        self.button_start.move(150, 300)

    def start_spider(self):
        dialog = QtWidgets.QFileDialog(self, '', "", "All Files (*)")
        dialog.setFileMode(QtWidgets.QFileDialog.DirectoryOnly)
        if dialog.exec_() == QtWidgets.QDialog.Accepted:
            self.folder_path = dialog.selectedFiles()[0]
        property_type = self.combo_property_choices.currentText().lower()
        apartment = True if property_type == 'apartamento' else False
        region = self.input_region.text().lower().replace(" ", "-").replace("ã", "a")
        file_name = self.input_file_name.text().lower().replace(" ", "-").replace("ã", "a") + ".csv"
        file_name_with_path = "file:///" + self.folder_path + "/" + file_name
        init_property_spider(region, apartment, file_name_with_path)


def window():
    app = QApplication(sys.argv)
    win = Windown()
    win.show()
    sys.exit(app.exec_())

window()
