import sys  # sys нужен для передачи argv в QApplication

from PyQt5 import QtWidgets, QtCore
# from PyQt5.QtGui import QFont, QShowEvent
import PyQt5.QtGui as QtGui

import texts

import skelet  # Это наш конвертированный файл дизайна


class App(QtWidgets.QMainWindow, skelet.Ui_MainWindow):
    def __init__(self):
        '''
        create fields of object 🤯
        не знаю что тут можно написать
        '''
        # Это здесь нужно для доступа к переменным, методам
        # и т.д. в файле design.py
        super().__init__()

        # Fields
        self.output_text = str()
        self.number_of_errors = 0
        self.start_output_length = 0
        self.lang = str()
        self.percent = 0
        self.right_letters = 0

        # Set Title
        self.setupUi(self)  # Это нужно для инициализации нашего дизайна
        self.setWindowTitle("Тренажер для печати")
        # self.setGeometry(1, 1, 2500, 1000)

        # Input - Output
        # self.input_string.setGeometry(0, 0, 500, 300)
        self.input_string.textChanged.connect(self.text_changed)

        # Ready Steady Go Lable
        # self.start_lable_number

        # Progress Bar
        self.progress_bar.setFont(QtGui.QFont("Times New Roman", 10, 10, False))
        self.progress_bar.setValue(self.percent)

        # self.verticalLayout.setGeometry(QRect(200,200,1000,1000))
        self.pause_button.clicked.connect(self.start)

        # Restart Button
        self.restart_button.hide()
        self.restart_button.setText("Перезапустить")
        self.restart_button.clicked.connect(self.restart)

        # Errors lable
        self.errors_lable.setText(f"Количество ошибок = {0}")
        self.errors_lable.hide()

        # Choice language
        self.choice_language.addItem("eng")
        self.choice_language.addItem("rus")
        # self.choice_language.activated.connect(self.start)

        # Button_start
        self.pause_button.setText("Поехали!")

        # Property set checkbox:
        self.is_capital_in_text = False
        self.is_digits_in_text = False
        self.is_other_in_text = False

        self.digits_check.clicked.connect(self.update_digits)
        self.capital_check.clicked.connect(self.update_capital)
        self.other_check.clicked.connect(self.update_other)

        # Timer
        self.timer = QtCore.QTimer()
        self.time = 0
        self.timer.setInterval(500)
        self.timer.timeout.connect(self.update_time)

        # self.timer2 = QtCore.QTimer() TODO this byaka
        # self.timer2.singleShot(5000, self.aboba)
        # Timer to start game

        # Time and Speed Lables

        self.time_lable.setText(f"Время: -")
        self.speed_label.setText(f"Скорость печати: - сим./мин.")

        # Geometry
        # TODO

        # self.setWindowState(Qt.WindowMaximized)

    def text_changed(self):
        '''if text changed, we check if new letter is right.
        If it is, then we delete this letter from the text in both strings.
        If it is not, then we delete this letter only from input string
        Of course, we make some difficult calculations with counting how many right letters we typed with this moment

        '''
        if self.output_string.text() == "":
            return
        if self.input_string.text() == "":
            return
        # print(self.output_string.text(), "aboba", self.input_string.text())
        self.input_string.disconnect()
        if self.output_text[0] == self.input_string.text()[-1]:
            self.output_text = self.output_text[1:]
            self.output_string.setText(self.output_text[:min(len(self.output_text), 25)])
            if self.input_string.text()[-1] == ' ':
                self.input_string.setText("")
            self.percent += 1 / (self.text.number_of_symbols) * 100
            self.right_letters += 1
        else:
            self.input_string.setText(self.input_string.text()[:-1])
            self.number_of_errors += 1

        if self.output_string.text() == "":
            print("The end")
            self.timer.stop()
        self.input_string.textChanged.connect(self.text_changed)
        self.update_progress_bar()
        self.update_errors()

    def start(self):
        '''start game - generate and show new text, start timer'''
        self.timer.start()

        self.text = texts.Text(3, 15,
                               self.is_capital_in_text, self.is_digits_in_text, self.is_other_in_text)
        print(self.text)
        # text = "qwer gkIDk 1234 fkldi Lqwer gkIDk 1234 fkldi L"
        self.output_text = str(self.text)
        # self.start_output_length = self.text.number_of_symbols
        self.output_string.setText(self.output_text[:25])

        self.pause_button.setText("Пауза")
        self.pause_button.disconnect()
        self.pause_button.clicked.connect(self.pause)
        self.restart_button.show()
        self.choice_language.hide()
        self.lang = self.choice_language.currentText()
        # print(self.lang)
        self.start_output_length = len(self.output_string.text())
        self.errors_lable.show()
        # self.input_string.setUpdatesEnabled(True)

    def update_errors(self):
        '''technical method'''
        self.errors_lable.setText(f"Количество ошибок: {self.number_of_errors}")

    def update_time(self):
        '''technical method. He is... update time, and speed on the screen'''
        self.time += 0.5
        # self.time_lable.setText(str(self.time))
        self.time_lable.setText(f"Время: {self.time}")
        # self.speed_label.setText(str(self.right_letters / self.time * 60))
        self.speed_label.setText(f"Скорость печати: {self.right_letters / self.time * 60} сим./мин.")

    def update_progress_bar(self):
        '''technical method. He is ... update progress bar'''
        self.progress_bar.setValue(int(self.percent))

    def pause(self):
        '''pause game - stop time, lock the opportunity to type letters in string'''
        self.pause_button.setText("Продолжить")
        self.pause_button.disconnect()
        self.pause_button.clicked.connect(self.cont)
        self.timer.stop()
        self.input_string.setReadOnly(True)

    def restart(self):
        '''Restart the game - reset all parameters, generate new text'''
        self.input_string.setReadOnly(False)
        self.input_string.setText("")
        self.right_letters = 0
        self.percent = 0
        self.time = 0
        self.timer.start()
        text = texts.Text(3, 15,
                          self.is_capital_in_text, self.is_digits_in_text, self.is_other_in_text)
        self.output_text = str(text)

        self.output_string.setText(self.output_text[:25])

        self.pause_button.setText("Пауза")
        self.pause_button.disconnect()
        self.pause_button.clicked.connect(self.pause)
        self.restart_button.show()
        self.choice_language.hide()
        self.lang = self.choice_language.currentText()
        self.update_progress_bar()

    def cont(self):  # Continue typing
        '''continue game: continue timer, allow to type'''
        self.pause_button.setText("Пауза")
        self.pause_button.disconnect()
        self.pause_button.clicked.connect(self.pause)
        self.timer.start()
        self.input_string.setReadOnly(False)

    def update_digits(self):
        '''technical method. Life is life
        if we want to change some characteristic of our text
        '''
        self.is_digits_in_text = not self.is_digits_in_text

    def update_capital(self):
        '''technical method. Life is life
            if we want to change some characteristic of our text
            '''
        self.is_capital_in_text = not self.is_capital_in_text

    def update_other(self):
        '''technical method. Life is life
            if we want to change some characteristic of our text
            '''
        self.is_other_in_text = not self.is_other_in_text


def main():
    '''the most difficult part of my project is function main()
    In this function I create the app
    create the window
    show the window
    and execute the app
    '''
    app = QtWidgets.QApplication(sys.argv)  # Новый экземпляр QApplication
    window = App()  # Создаём объект класса ExampleApp
    window.show()  # Показываем окно
    sys.exit(app.exec_())  # и запускаем приложение


if __name__ == '__main__':
    main()
