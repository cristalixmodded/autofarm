from PyQt6.QtWidgets import QApplication, QMainWindow, QMessageBox
from PyQt6.QtGui import QIntValidator, QIcon
from PyQt6.QtCore import QTimer
from PyQt6.QtTest import QTest
from PyQt6 import uic
import configparser
import pyautogui

def farm(warp, slot, time_range, time_sleep):
    fpr i in range(2):
        pyautogui.press('t')
        pyautogui.write("/warp " + warp, interval=0.25)
        pyautogui.press('enter')
    QTest.qWait(4000)
   
    pyautogui.press(slot)
    for _ in range(time_range):
        pyautogui.leftClick()
        QTest.qWait(time_sleep)

class Ui(QMainWindow):
    def __init__(self):
        super(Ui, self).__init__()
        uic.loadUi('mainwindow.ui', self)
        self.show()
        
        self.setWindowIcon(QIcon('img\cattocry.png'))
        
        self.oresSlot.setValidator(QIntValidator(self))
        self.mobsSlot.setValidator(QIntValidator(self))
        self.delay.setValidator(QIntValidator(self))

        self.startButton.clicked.connect(self.start_button)

        config = configparser.ConfigParser()
        config.read_file(open(r'config.ini'))
        ores_warp = config.get('Config', 'ores_warp')
        ores_slot = config.get('Config', 'ores_slot')
        mobs_warp = config.get('Config', 'mobs_warp')
        mobs_slot = config.get('Config', 'mobs_slot')
        delay = config.get('Config', 'delay')
            
        self.oresWarp.setText(ores_warp)
        self.oresSlot.setText(ores_slot)
        self.mobsWarp.setText(mobs_warp)
        self.mobsSlot.setText(mobs_slot)
        self.delay.setText(delay)
        
    def start_button(self):      
        self.startButton.setEnabled(False)
        QTest.qWait(10000)
        while True:  
            farm(self.oresWarp.text(), self.oresSlot.text(), 5, 3000)
            farm(self.mobsWarp.text(), self.mobsSlot.text(), 10, 20000) 

            delay = self.delay.text()
            delay = int(delay) * 60 * 1000 / 100
            delay = round(delay)
            
            self.timer = QTimer()
            self.timer.timeout.connect(self.progress_bar)
            self.timer.start(delay)   
            
            delat = self.delay.text()
            delay = int(delay) * 60 * 1000
            QTest.qWait(delay)

    def progress_bar(self):
        value = self.progressBar.value()
        if value < 100:
            value = value + 1
            self.progressBar.setValue(value)
        else:
            self.timer.stop()
            self.progressBar.setValue(0)
            
    def closeEvent(self, event):
        close = QMessageBox()
        close.setWindowIcon(QIcon('img\cattocry.png'))
        close.setText('Есть несохраненные изменения.')
        close.setWindowTitle('Сохранить результаты работы?')
        close.setStandardButtons(QMessageBox.StandardButton.Save | QMessageBox.StandardButton.Cancel | QMessageBox.StandardButton.Close)
        close = close.exec()
        
        if close == QMessageBox.StandardButton.Save:
            config = configparser.ConfigParser()
            config.add_section('Config')
            config.set('Config', 'ores_warp', self.oresWarp.text())
            config.set('Config', 'ores_slot', self.oresSlot.text())
            config.set('Config', 'mobs_warp', self.mobsWarp.text())
            config.set('Config', 'mobs_slot', self.mobsSlot.text())
            config.set('Config', 'delay', self.delay.text())
    
            with open('config.ini', 'w') as config_file:
                config.write(config_file)
        elif close == QMessageBox.StandardButton.Cancel:
            event.ignore() 
        elif close == QMessageBox.StandardButton.Close:
            event.accept()  

app = QApplication([])
UIWindow = Ui()
app.exec()
