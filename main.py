import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from desktop_ui import UiMainWindow

class PlayerApp(QMainWindow, UiMainWindow):
    def __init__(self):
        super().__init__()
        self.setup_ui(self)

def main():
    app = QApplication(sys.argv)
    window = PlayerApp()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
