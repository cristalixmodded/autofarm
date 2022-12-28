from PyQt6.QtWidgets import QApplication, QMainWindow, QStyle, QSystemTrayIcon, QMenu
from PyQt6.QtGui import QIntValidator, QIcon, QAction
from PyQt6.QtCore import QTimer
from PyQt6 import uic
import configparser
import threading
from farm import start_farm

class Ui(QMainWindow):
    def __init__(self):
        super(Ui, self).__init__()
        uic.loadUi('mainwindow.ui', self)
        self.show()
        
        self.load_config()
        self.tray()
        
        self.setWindowIcon(QIcon('img\cattocry.png'))
        
        self.oresSlot.setValidator(QIntValidator(self))
        self.mobsSlot.setValidator(QIntValidator(self))
        self.delay.setValidator(QIntValidator(self))

        self.startButton.clicked.connect(self.start_button)
        
    def start_button(self):    
        self.save_config()  
        self.startButton.setEnabled(False)
        self.startButton.setText('working...')
        
        farm_thread = threading.Thread(target=start_farm, name='send_thread')
        if not farm_thread.is_alive():
            farm_thread.start()
            
        delay = int(self.delay.text())
        delay = delay * 60 * 1000 / 100
        delay = round(delay)
            
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.progress_bar)
        self.timer.start(delay)
        
    def load_config(self):
        config = configparser.ConfigParser()
        config.read_file(open(r'config.ini'))
        ores_warp = config.get('Config', 'ores_warp')
        ores_slot = config.get('Config', 'ores_slot')
        mobs_warp = config.get('Config', 'mobs_warp')
        mobs_slot = config.get('Config', 'mobs_slot')
        delay = config.get('Config', 'delay')
            
        tray = eval(config.get('Config', 'tray'))
            
        self.oresWarp.setText(ores_warp)
        self.oresSlot.setText(ores_slot)
        self.mobsWarp.setText(mobs_warp)
        self.mobsSlot.setText(mobs_slot)
        self.delay.setText(delay)
        
        self.trayCheckBox.setChecked(tray) 
         
    def save_config(self):
        config = configparser.ConfigParser()
        config.add_section('Config')
        config.set('Config', 'ores_warp', self.oresWarp.text())
        config.set('Config', 'ores_slot', self.oresSlot.text())
        config.set('Config', 'mobs_warp', self.mobsWarp.text())
        config.set('Config', 'mobs_slot', self.mobsSlot.text())
        config.set('Config', 'delay', self.delay.text())

        config.set('Config', 'tray', str(self.trayCheckBox.isChecked()))
        
        with open('config.ini', 'w') as config_file:
            config.write(config_file)

    def tray(self):
        self.tray = QSystemTrayIcon(self)
        icon = self.style().standardIcon(QStyle.StandardPixmap.SP_ComputerIcon)
        self.tray.setIcon(icon)
        
        show_action = QAction("Открыть", self)
        quit_action = QAction("Закрыть", self)
        
        show_action.triggered.connect(self.show)
        quit_action.triggered.connect(QApplication.quit)
        
        tray_menu = QMenu()
        tray_menu.addAction(show_action)
        tray_menu.addAction(quit_action)
        
        self.tray.setContextMenu(tray_menu)
        self.tray.show()   
 
    def progress_bar(self):
        value = self.progressBar.value()
        if value < 100:
            value = value + 1
            self.progressBar.setValue(value)
        else:
            self.progressBar.setValue(0)
            
    def closeEvent(self, event):
        self.save_config()
        if self.trayCheckBox.isChecked():
            event.ignore()
            self.hide()
            self.tray.showMessage
            (
                "Auto Farm",
                "Программа свернута.",
                QSystemTrayIcon.MessageIcon.Information,
                2000
            )        
            
app = QApplication([])
UIWindow = Ui()
app.exec()