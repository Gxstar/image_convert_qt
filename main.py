import sys
from PySide6.QtWidgets import QApplication
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile, QIODevice

app = QApplication(sys.argv)

ui_file = QFile("main.ui")
ui_file.open(QIODevice.ReadOnly)
window = QUiLoader().load(ui_file)
ui_file.close()

window.show()
sys.exit(app.exec())
