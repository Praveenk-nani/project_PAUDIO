from FrontPage import Ui_FrontPageWindow
from AboutPage import Ui_AboutPageWindow
from ListenPage import Ui_ListenPageWindow
from DetailsPage import Ui_DetailsPageWindow
import sys
import os
import PyPDF2 as pdf
from PyQt5.QtWidgets import QApplication, QMainWindow, QStackedWidget, QFileDialog,QMessageBox
from PyQt5.QtCore import QThread, pyqtSignal
import pyttsx3 as ptt
import pygame,tempfile
from gtts import gTTS


class thread_class(QThread):
    any_sig = pyqtSignal(str)

    def __init__(self,getfile,from_page,to_page,listenpage):
        super(thread_class, self).__init__()
        self.is_run = True
        self.get_pdf_file=getfile
        self.from_page=from_page
        self.to_page=to_page
        self.listening=listenpage

    def run(self):
        try:
            for i in range(self.from_page,self.to_page):
                if not self.is_run:
                    break
                get_reauired_page=self.get_pdf_file.pages[i]
                text=get_reauired_page.extract_text()
                # self.listening.plainTextEdit.setPlainText(text)
                # self.any_sig.emit(text)
                print(text)

                # Create a temporary file
                with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as f:
                    temp_filename = f.name

                # Create a gTTS object and save to the temporary file
                tts = gTTS(text=text, lang='en')
                tts.save(temp_filename)

                pygame.mixer.init()
                pygame.mixer.music.load(temp_filename)


                self.any_sig.emit(text)
                pygame.mixer.music.play()
                while pygame.mixer.music.get_busy():
                    pygame.time.Clock().tick(1)

                pygame.mixer.quit()

                # Delete the temporary file after usage

                os.remove(temp_filename)
                # os.remove(temp.mp3)

            # self.any_sig.emit()
        except Exception as e:
            print(f"something has happened sorry this is happened {e}")

    def stop(self):
        self.is_run = False
        print("here the thread is stopping")
        pygame.mixer.music.stop()
        self.terminate()
        self.wait()


class front_page1(QMainWindow, Ui_FrontPageWindow):
    def __init__(self):
        super(front_page1, self).__init__()
        self.setupUi(self)


class about_page1(QMainWindow, Ui_AboutPageWindow):
    def __init__(self):
        super(about_page1, self).__init__()
        self.setupUi(self)


class listen_page1(QMainWindow, Ui_ListenPageWindow):
    def __init__(self):
        super(listen_page1, self).__init__()
        self.setupUi(self)


class details_page1(QMainWindow, Ui_DetailsPageWindow):
    def __init__(self):
        super(details_page1, self).__init__()
        self.setupUi(self)


class mainwindow(QMainWindow):
    def __init__(self):
        super(mainwindow, self).__init__()
        self.stacked_wid = QStackedWidget(self)
        self.thread1 = None

        self.front_page = front_page1()
        self.about_page = about_page1()
        self.details_page = details_page1()
        self.listen_page = listen_page1()

        self.stacked_wid.addWidget(self.front_page)  # 0
        self.stacked_wid.addWidget(self.about_page)  # 1
        self.stacked_wid.addWidget(self.details_page)  # 2
        self.stacked_wid.addWidget(self.listen_page)  # 3

        self.setCentralWidget(self.stacked_wid)

        # for front page
        self.front_page.start_btn.clicked.connect(self.selectfile)
        self.front_page.close_btn.clicked.connect(self.are_you_want_to_exit)
        self.front_page.about_btn.clicked.connect(self.open_about_page)

        # for about page
        self.about_page.back_btn.clicked.connect(self.open_front_page)

        # for details page
        self.details_page.back_btn.clicked.connect(self.open_front_page)
        self.details_page.Start_btn.clicked.connect(self.open_listen_page)


        # for listen page
        self.listen_page.back_btn.clicked.connect(self.open_details_page)
        self.listen_page.stop_btn.clicked.connect(self.stoplisten)
        self.listen_page.listen_btn.clicked.connect(self.startlisten)
        self.stop_signal_flag = False
        # self.thread1.any_sig.connect(self.update_text)
    
    def update_text(self,text):
        self.listen_page.plainTextEdit.setPlainText(text)

    def open_front_page(self):
        self.stacked_wid.setCurrentIndex(0)

    def open_about_page(self):
        self.stacked_wid.setCurrentIndex(1)

    def open_listen_page(self):
        dialog=QMessageBox(self)
        dialog.setWindowTitle("Information")
        dialog.setText("Sorry for the inconvience!!!")
        dialog.setIcon(QMessageBox.Critical)
        dialog.setInformativeText("See the details below")
        dialog.setDetailedText("again sorry but the speach has some seconds delay sorry for the incovience but it depends upon your internet speed again sorry")
        dialog.setStandardButtons(QMessageBox.Ok)
        dialog.exec_()
        # dialog.buttonClicked.connect(self.message_box_buttons_page)
        self.stacked_wid.setCurrentIndex(3)

        # getting pages range
        try:
            global from_page, to_page
            from_page = int(self.details_page.From_pages.text())
            to_page = int(self.details_page.To_pages.text())
            if from_page < 0 or to_page > numberofpages or from_page > numberofpages or to_page < 0 or to_page < from_page:
                raise ValueError("no this page number we cannot accept")
        except ValueError as e:
            tex = str(e)
            self.open_message_dialog(tex)
            # print(e)
    def open_message_dialog(self,e):
        dialog=QMessageBox(self)
        dialog.setWindowTitle("Warning")
        dialog.setText(e)
        dialog.setIcon(QMessageBox.Warning)
        dialog.setStandardButtons(QMessageBox.Ok)
        dialog.buttonClicked.connect(self.message_box_buttons_page)

        dialog.exec_()
    def message_box_buttons_page(self,message_buttons):
        self.open_details_page()

    def are_you_want_to_exit(self):

        dialog=QMessageBox(self)
        dialog.setWindowTitle("CRITICAL")
        dialog.setText("Are You Sure want to exit")
        dialog.setIcon(QMessageBox.Critical)
        dialog.setStandardButtons(QMessageBox.Cancel | QMessageBox.Ok)
        dialog.buttonClicked.connect(self.message_box_buttons)

        dialog.exec_()
    
    def message_box_buttons(self,message_buttons):
        if message_buttons.text() == "OK":
            self.close()


    def open_details_page(self):
        self.stacked_wid.setCurrentIndex(2)



    def selectfile(self):
        try:
            self.option_files = QFileDialog.Options()
            self.option_files |= QFileDialog.DontUseNativeDialog

            self.file_open_dialog = QFileDialog()
            self.path_of_file, _ = QFileDialog.getOpenFileName(self, "Open PDF File", "",
                                                            "PDF Files (*.pdf);;All Files (*)", options=self.option_files)

            # opening file
            self.pdf_file = open(self.path_of_file, 'rb')
            self.get_pdf_file = pdf.PdfReader(self.pdf_file)

            # getting number of pages info
            global numberofpages
            numberofpages = len(self.get_pdf_file.pages)
            self.details_page.availablePages_lb.setText(str(numberofpages))
            self.details_page.To_pages.setText(str(numberofpages))
            self.details_page.From_pages.setText("1")

            # getting name of the file
            filename = os.path.basename(self.path_of_file)
            self.details_page.File_name_lb.setText(filename)

            self.open_details_page()

        except Exception as e:
            print(f"no file is selected sorry {e}")

    def stoplisten(self):
        try:
            self.listen_page.listen_btn.setEnabled(True)
            if self.thread1 and self.thread1.isRunning():
                self.thread1.stop()
                # self.playbtn.setEnabled(True)
        except Exception as e:
            print(e)

    def startlisten(self):
        try:
            if self.thread1 is None or not self.thread1.isRunning():
                self.thread1 = thread_class(self.get_pdf_file,from_page,to_page,self.listen_page)
                self.thread1.start()
                self.listen_page.listen_btn.setEnabled(False)
                self.thread1.any_sig.connect(self.update_text)
        except Exception as e:
            print(f"something has happened sorry {e}")



if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = mainwindow()
    window.show()
    sys.exit(app.exec_())
