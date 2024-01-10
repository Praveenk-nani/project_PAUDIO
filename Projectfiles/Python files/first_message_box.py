from PyQt5.QtWidgets import QApplication,QLabel,QMainWindow,QMessageBox
from PyQt5 import QtWidgets
import sys

class main_win(QMainWindow):
    def __init__(self):
        super(main_win,self).__init__()
        self.setGeometry(100,100,400,600)
        self.setupgui()
        self.show()
    def setupgui(self):
        self.lb1 = QLabel(self)
        self.lb1.setGeometry(20,20,300,100)
        self.lb1.setText("hello this is just a label")
        self.lb1.setStyleSheet("QLabel""{""border:2px solid black""}")
        self.btn1=QtWidgets.QPushButton('hello',self)
        self.btn1.setGeometry(150,200,50,30)
        self.btn1.clicked.connect(self.click)
    def click(self):
        # print("clicked button")
        dialo = QMessageBox(self)
        dialo.setWindowTitle("warning")
        dialo.setText('hello this is just a dialog box')
        # dialo.setIcon(QMessageBox.Critical)#here the latters are capital
        # dialo.setIcon(QMessageBox.Warning)
        # dialo.setIcon(QMessageBox.Information)
        dialo.setIcon(QMessageBox.Question)

        dialo.setInformativeText('they are just information')
        dialo.setDetailedText('You can put any text here')
        dialo.setStandardButtons(QMessageBox.Cancel | QMessageBox.Ok | QMessageBox.Retry)

         #we have to add just only one call for the btn_pressed method
        dialo.buttonClicked.connect(self.btn_pressed)
        # dialo.buttonClicked.connect(self.btn_pressed)


        
        #below are some standrard buttons to add
            # QMessageBox.Ok
            # QMessageBox.Open
            # QMessageBox.Save
            # QMessageBox.Cancel
            # QMessageBox.Close
            # QMessageBox.Yes
            # QMessageBox.No
            # QMessageBox.Abort
            # QMessageBox.Retry
            # QMessageBox.Ignore

        dialo.exec_()

    def btn_pressed(self,btn):
        if btn.text() == "Ok":
            print("ok is pressed")
        elif btn.text() == "Cancel":
            print("cancel is pressed")
        elif btn.text()== "Retry":
            # print("retry is pressed")
            self.retry_method()

    def retry_method(self):
        self.btn1.setText("retry")




def meth():
    app = QApplication(sys.argv)
    wind = main_win()
    sys.exit(app.exec())

if __name__ == '__main__':
    meth()