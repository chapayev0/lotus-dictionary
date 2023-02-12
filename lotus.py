from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import sqlite3
import sys, time
import importlib
import pyautogui
import platform
from win32com.client import Dispatch
import winreg

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s
try:
    _encoding = QtGui.QApplication.UnicodeUTF8

    def _translate(contex, text, disambing):
        return QtGui.QApplication.translate(contex, text, disambing, _encoding)
except AttributeError:
    def _translate(contex, text, disambing):
        return QtGui.QApplication.translate(contex, text, disambing)


dock_expand = False
about_d_show = False
option_d_show = False
key_d_show = False
ocr_d_show = False
index_d_show = False
CBListner = False
baloon_w_show = False
real_time_dic = False
timer_cnt = 0
lang_change = False
tray_icon_visiable = False
auto_search = False
mini_mod_tab_visiable = False
mini_mod_window_show = False
mini_mod_x_pos = 1024 # define mini txt browser X position/ Static
mini_mod_y_pos = 104  # define mini txt browser Y position/ Dayanamic
mini_mod_x_pos_title = 1024
mini_mod_y_pos_title = 59
mini_mod_colaps_y_pos = 59 # tab caolaps error fix
dragable_btn_mouse_release = False
mini_mod_title_timer_cnt = 0
mini_mod_timer_cnt = 0
mini_mod_switch = False
sujest_type = 1
key_press = False
css_pack = "theme/dark_theme/dark.qss"
keybord_shift_press = False
splash_i = 0
splash_stop = 0
max_i = 38
alwaysonthetop = False
mini_mod_title_timer_timeout = 8000
widget_auto_hide =  False
open_at_startup = False



def updateSplashScreen():
    global splash_i, splash_stop

    if splash_i == 35:
        splash_i = 0
        splash_stop = 1
    else:
        if splash_i < max_i:
            splash_i = splash_i + 1
    pixmap = QPixmap("meta/splash/splash_" + str(splash_i) + ".png")
    splashScreen.setPixmap(pixmap)


class SplashThread(QThread):
    mysignal = pyqtSignal(int)

    def __init__(self, parent=None):
        QThread.__init__(self, parent)

    def run(self):
        global splash_i, splash_stop, max_i

        start_time = time.time()
        t = round(time.time() - start_time)
        if t < 3:
            max_i = 35

        while splash_stop == 0:
            app.processEvents()
        if splash_stop == 1:
            self.mysignal.emit(1)


def stopTimer(signal):
    if signal == 1:
        timer.stop()
        main.show()
        splashScreen.finish(main)

    else:
        pass


class Grep_button(QtWidgets.QPushButton):
    def __init__(self):
        QtWidgets.QPushButton.__init__(self)

        self.setMaximumHeight(50)
        self.setMaximumWidth(27)
        self.setObjectName("Grep_button")

        self.setEnabled(True)

    def enterEvent(self, event):
        global mini_mod_title_timer_cnt

        main.mini_mod_title_timer.stop()
        main.mini_mod_title.setWindowOpacity(1)
        mini_mod_title_timer_cnt = 0

    def leaveEvent(self, event):
        global mini_mod_title_timer_timeout

        main.mini_mod_title_timer.start(mini_mod_title_timer_timeout)


    def mousePressEvent(self, event):

        main.mini_mod_title.__mousePressPos = None
        main.mini_mod_title.__mouseMovePos = None

        if event.button() == Qt.LeftButton:
            main.mini_mod_title.__mousePressPos = event.globalPos()
            print(main.mini_mod_title.__mousePressPos)
            main.mini_mod_title.__mouseMovePos = event.globalPos()


    def mouseMoveEvent(self, event):
        print("mouse move event line 133")
        global mini_mod_x_pos
        global mini_mod_y_pos
        global mini_mod_colaps_y_pos

        main.mini_mod.hide()


        if event.buttons() == Qt.LeftButton:
            currPos = main.mini_mod_title.mapToGlobal(main.mini_mod_title.pos())

            globalPos = event.globalPos()

            diff = globalPos - main.mini_mod_title.__mouseMovePos
            newPos = main.mini_mod_title.mapFromGlobal(currPos + diff)

            main.mini_mod_title.move(newPos)
            print(newPos)

            main.mini_mod_title.__mouseMovePos = globalPos

        mini_mod_x_pos = newPos.x()
        mini_mod_y_pos = newPos.y() + 45
        mini_mod_colaps_y_pos = newPos.y()

    def mouseReleaseEvent(self, event):

        global mini_mod_x_pos
        global mini_mod_y_pos
        global mini_mod_tab_visiable
        global dragable_btn_mouse_release

        dragable_btn_mouse_release = True



        if main.mini_mod_title.__mousePressPos is not None:
            moved = event.globalPos() - main.mini_mod_title.__mousePressPos
            if moved:

                event.ignore()

                if main.mini_mod_title.txt_input.text() == "" or mini_mod_tab_visiable == True:
                    main.mini_mod.move(mini_mod_x_pos, mini_mod_y_pos)

                else:

                    main.mini_mod.move(mini_mod_x_pos, mini_mod_y_pos)
                    main.mini_mod.show()


class Dragable_button(QtWidgets.QPushButton):
    def __init__(self):
        QtWidgets.QPushButton.__init__(self)

        self.setMaximumHeight(50)
        self.setMaximumWidth(35)
        self.setObjectName("Dragable_button")

    def enterEvent(self, event):

        global mini_mod_title_timer_cnt, mini_mod_tab_visiable


        main.mini_mod_title_timer.stop()
        main.mini_mod_title.setWindowOpacity(1)
        mini_mod_title_timer_cnt = 0

    def leaveEvent(self, event):
        global mini_mod_tab_visiable, mini_mod_title_timer_timeout



        main.mini_mod_title_timer.start(mini_mod_title_timer_timeout)

    def mousePressEvent(self, event):


        main.mini_mod_title.__mousePressPos = None
        main.mini_mod_title.__mouseMovePos = None

        if event.button() == Qt.LeftButton:
            main.mini_mod_title.__mousePressPos = event.globalPos()
            print(main.mini_mod_title.__mousePressPos)
            main.mini_mod_title.__mouseMovePos = event.globalPos()



    def mouseMoveEvent(self, event):

        global mini_mod_x_pos
        global mini_mod_y_pos
        global mini_mod_colaps_y_pos

        main.mini_mod.hide()


        if event.buttons() == Qt.LeftButton:

            currPos = main.mini_mod_title.mapToGlobal(main.mini_mod_title.pos())

            globalPos = event.globalPos()

            diff = globalPos - main.mini_mod_title.__mouseMovePos
            newPos = main.mini_mod_title.mapFromGlobal(currPos + diff)

            main.mini_mod_title.move(newPos)
            print(newPos)

            main.mini_mod_title.__mouseMovePos = globalPos

        mini_mod_x_pos = newPos.x()
        mini_mod_y_pos = newPos.y() + 45
        mini_mod_colaps_y_pos = newPos.y()


    def mouseReleaseEvent(self, event):

        global mini_mod_x_pos
        global mini_mod_y_pos
        global mini_mod_tab_visiable
        global dragable_btn_mouse_release

        dragable_btn_mouse_release = True



        if main.mini_mod_title.__mousePressPos is not None:
            moved = event.globalPos() - main.mini_mod_title.__mousePressPos
            if moved:

                event.ignore()

                if main.mini_mod_title.txt_input.text() == "" or mini_mod_tab_visiable == True:


                    main.mini_mod.move(mini_mod_x_pos, mini_mod_y_pos)

                else:

                    main.mini_mod.move(mini_mod_x_pos, mini_mod_y_pos)
                    main.mini_mod.show()


    def mouseDoubleClickEvent(self, event):
        global mini_mod_title_timer_timeout

        global mini_mod_y_pos
        global mini_mod_x_pos
        global mini_mod_colaps_y_pos
        global mini_mod_tab_visiable

        if mini_mod_tab_visiable == False:
            mini_mod_tab_visiable = True

        else:
            mini_mod_tab_visiable = False

        print("miniModTabVisiable  = " + str(mini_mod_tab_visiable))

        x_pos = event.globalPos().x()

        print("x =" + str(x_pos))
        y_pos = event.globalPos().y()

        print("y =" + str(y_pos))

        if mini_mod_tab_visiable == True:
            main.mini_mod_title.grep_btn.hide()
            main.mini_mod_title.oder_btn.hide()
            main.mini_mod_title.mini_mod_lang_change.hide()
            main.mini_mod_title.speaker_btn.hide()
            main.mini_mod_title.txt_input.hide()
            main.mini_mod_title.serch_btn.hide()
            main.mini_mod_title.span_lbl.hide()
            main.mini_mod_title.setFixedSize(50, 45)
            main.mini_mod_title.horizontalLayoutWidget.setGeometry(QtCore.QRect(0, 0, 50, 45))

            x_pos = x_pos - 20
            main.mini_mod_title.move(x_pos, mini_mod_colaps_y_pos)
            main.mini_mod.hide()
        else:
            main.mini_mod_title_timer.start(mini_mod_title_timer_timeout)

            main.mini_mod_title.setFixedSize(330,45)
            main.mini_mod_title.horizontalLayoutWidget.setGeometry(QtCore.QRect(0, 0, 330, 45))

            main.mini_mod_title.grep_btn.show()
            main.mini_mod_title.oder_btn.show()
            main.mini_mod_title.mini_mod_lang_change.show()
            main.mini_mod_title.speaker_btn.show()
            main.mini_mod_title.txt_input.show()
            main.mini_mod_title.txt_input.setMinimumWidth(150)
            main.mini_mod_title.serch_btn.show()
            main.mini_mod_title.span_lbl.show()
            x_pos = x_pos - 303
            main.mini_mod_title.move(x_pos, mini_mod_colaps_y_pos)
            main.mini_mod_title.setMaximumWidth(344)
            main.mini_mod_title.setWindowOpacity(1)


        print("mini mod tab = " + str(mini_mod_tab_visiable))
        mini_mod_x_pos = x_pos



class Mini_Mod_TitleBar(QtWidgets.QDialog):
    def __init__(self):
        QtWidgets.QDialog.__init__(self)


        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.dragable_btn = Dragable_button()
        self.grep_btn = Grep_button()
        self.move(1024, 59)
        self.setMaximumHeight(50)
        self.setMaximumWidth(400)
        self.mini_mod_timer = QTimer()
        self.setObjectName("Mini_Mod_TitleBar")
        self.setStyleSheet(open(css_pack, "r").read())

        self.moving = False

        self.setAutoFillBackground(True)
        self.setBackgroundRole(QtGui.QPalette.Highlight)

        self.maxmize_btn = QtWidgets.QToolButton(self)
        self.maxmize_btn.setObjectName("mini_mod_maxmize_btn")

        self.close_btn = QtWidgets.QToolButton(self)
        self.close_btn.setObjectName("mini_mod_close_btn")

        self.tray_btn = QtWidgets.QToolButton(self)
        self.tray_btn.setObjectName("mini_mod_tray_btn")

        self.tray_btn.setMaximumWidth(21)
        self.tray_btn.setMaximumHeight(15)
        self.maxmize_btn.setMaximumWidth(20)
        self.maxmize_btn.setMaximumHeight(15)
        self.close_btn.setMaximumWidth(20)
        self.close_btn.setMaximumHeight(15)

        self.txt_input = QtWidgets.QLineEdit(self)
        self.txt_input.setMaximumSize(150, 32)
        self.txt_input.setObjectName("mini_mod_txt_input")

        mini_font = QtGui.QFont()
        mini_font.setPixelSize(16)
        self.txt_input.setFont(mini_font)

        self.speaker_btn = QtWidgets.QPushButton(self)
        self.speaker_btn.setObjectName("mini_mod_serch_btn")
        self.speaker_btn.setMaximumSize(38, 30)

        self.span_lbl = QtWidgets.QLabel(self)
        self.span_lbl.setMaximumSize(5, 50)

        self.serch_btn = QtWidgets.QPushButton(self)
        self.serch_btn.setMaximumSize(35, 28)
        self.serch_btn.setObjectName("mini_mod_speaker_btn")

        self.oder_btn = QtWidgets.QPushButton(self)
        self.oder_btn.setMaximumWidth(24)
        self.oder_btn.setMaximumHeight(22)
        self.oder_btn.setObjectName("mini_mod_oder_btn")
        self.oder_btn.setText("O")
        # self.oder_btn.setContentsMargins(0, 0, 0, 0)

        self.mini_mod_lang_change = QtWidgets.QPushButton(self)
        self.mini_mod_lang_change.setMaximumWidth(24)
        self.mini_mod_lang_change.setMaximumHeight(22)
        self.mini_mod_lang_change.setObjectName("mini_mod_lang_change")
        self.mini_mod_lang_change.setText("EN")

        self.hiden_txt_box = QtWidgets.QTextEdit(self)
        self.hiden_txt_box.hide()

        self.vbox1 = QtWidgets.QVBoxLayout()
        self.vbox1.addWidget(self.mini_mod_lang_change)
        self.vbox1.addWidget(self.oder_btn)
        self.vbox1.setContentsMargins(0, 0, 0, 0)
        self.vbox1.setSpacing(0)

        self.vbox = QtWidgets.QVBoxLayout()
        self.vbox.addWidget(self.tray_btn)
        self.vbox.addWidget(self.maxmize_btn)
        self.vbox.addWidget(self.close_btn)
        self.vbox.setSpacing(0)

        self.horizontalLayoutWidget = QtWidgets.QWidget(self)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(0, 0,  330, 45))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.horizontalLayout.addWidget(self.grep_btn)
        self.horizontalLayout.addLayout(self.vbox1)
        self.horizontalLayout.addWidget(self.serch_btn) # speaker button unknown error
        self.horizontalLayout.addWidget(self.txt_input)
        self.horizontalLayout.addWidget(self.speaker_btn)  # search button Unknown error
        self.horizontalLayout.addWidget(self.span_lbl)
        self.horizontalLayout.addWidget(self.dragable_btn)
        self.horizontalLayout.addLayout(self.vbox)
        self.horizontalLayout.setSpacing(0)

        self.maxNormal = False
        self.setWindowOpacity(1)

        self.mini_mod_timer.timeout.connect(self.mini_mod_timer_cnt)
        self.txt_input.textChanged.connect(self.onTextChanged)
        self.serch_btn.clicked.connect(self.mini_mod_voice)
        self.oder_btn.clicked.connect(self.oder_change)



    def oder_change(self):
        global sujest_type
        global lang_change

        if sujest_type == 1:
            sujest_type = 2

        elif sujest_type == 2:
            sujest_type = 3

        elif sujest_type == 3:
            sujest_type = 4

        elif sujest_type == 4:
            sujest_type = 1

        print("sujest_type = " + str(sujest_type))

        if sujest_type == 1:
            self.oder_btn.setObjectName("mini_mod_lang_change")
            self.oder_btn.setText("O")

            main.mini_mod.mini_mod_list.clear()

        elif sujest_type == 2:

            self.oder_btn.setObjectName("mini_mod_lang_change")
            self.oder_btn.setText("*O")

            main.mini_mod.mini_mod_list.clear()
            word = str(self.txt_input.text()).encode("utf-8").decode("utf-8")
            if word != "":
                data_base = sqlite3.connect("Database/Shashika.ire")
                data_base.text_factory()
                word = word.lower()
                sql_word = "%" + word
                sql_cmd_1 = data_base.execute("""SELECT * FROM Distinct_words WHERE d_english LIKE '%s' """ % sql_word)

                for raw in sql_cmd_1:
                    mean = "|".join(map(str, raw)).split("|")[1].encode("utf-8").decode("utf-8")
                    main.mini_mod.mini_mod_list.addItem(mean)

        elif sujest_type == 3:

            self.oder_btn.setObjectName("mini_mod_lang_change")
            self.oder_btn.setText("O*")

            main.mini_mod.mini_mod_list.clear()
            word = str(self.txt_input.text()).encode("utf-8").decode("utf-8")
            if word != "":

                data_base = sqlite3.connect("Database/Shashika.ire")
                data_base.text_factory()
                word = word.lower()
                sql_word = word + "%"
                sql_cmd_1 = data_base.execute("""SELECT * FROM Distinct_words WHERE d_english LIKE '%s' """ % sql_word)

                for raw in sql_cmd_1:
                    mean = "|".join(map(str, raw)).split("|")[1].encode("utf-8").decode("utf-8")
                    main.mini_mod.mini_mod_list.addItem(mean)

        elif sujest_type == 4:

            self.oder_btn.setObjectName("mini_mod_lang_change")
            self.oder_btn.setText("*O*")

            main.mini_mod.mini_mod_list.clear()
            word = str(self.txt_input.text()).encode("utf-8").decode("utf-8")
            if word != "":

                data_base = sqlite3.connect("Database/Shashika.ire")
                data_base.text_factory()
                word = word.lower()
                sql_word = "%" + word + "%"
                sql_cmd_1 = data_base.execute("""SELECT * FROM Distinct_words WHERE d_english LIKE '%s' """ % sql_word)

                for raw in sql_cmd_1:
                    mean = "|".join(map(str, raw)).split("|")[1].encode("utf-8").decode("utf-8")
                    main.mini_mod.mini_mod_list.addItem(mean)

        if sujest_type == 2 and lang_change == True:

            self.oder_btn.setObjectName("mini_mod_lang_change")
            self.oder_btn.setText("*O")

            main.mini_mod.mini_mod_list.clear()
            word = str(self.txt_input.text()).encode("utf-8").decode("utf-8")
            if word != "":
                data_base = sqlite3.connect("Database/Shashika.ire")
                data_base.text_factory()
                word = word.lower()
                sql_word = "%" + word
                sql_cmd_1 = data_base.execute("""SELECT * FROM Word_list WHERE sinhala LIKE '%s' """ % sql_word)

                for raw in sql_cmd_1:
                    mean = "|".join(map(str, raw)).split("|")[-1].encode("utf-8").decode("utf-8")
                    main.mini_mod.mini_mod_list.addItem(mean)

        elif sujest_type == 3 and lang_change == True:

            self.oder_btn.setObjectName("mini_mod_lang_change")
            self.oder_btn.setText("O*")

            main.mini_mod.mini_mod_list.clear()
            word = str(self.txt_input.text()).encode("utf-8").decode("utf-8")
            if word != "":

                data_base = sqlite3.connect("Database/Shashika.ire")
                data_base.text_factory()
                word = word.lower()
                sql_word = word + "%"
                sql_cmd_1 = data_base.execute("""SELECT * FROM Word_list WHERE sinhala LIKE '%s' """ % sql_word)

                for raw in sql_cmd_1:
                    mean = "|".join(map(str, raw)).split("|")[-1].encode("utf-8").decode("utf-8")
                    main.mini_mod.mini_mod_list.addItem(mean)

        elif sujest_type == 4 and lang_change == True:

            self.oder_btn.setObjectName("mini_mod_lang_change")
            self.oder_btn.setText("*O*")

            main.mini_mod.mini_mod_list.clear()
            word = str(self.txt_input.text()).encode("utf-8").decode("utf-8")
            if word != "":

                data_base = sqlite3.connect("Database/Shashika.ire")
                data_base.text_factory()
                word = word.lower()
                sql_word = "%" + word + "%"
                sql_cmd_1 = data_base.execute("""SELECT * FROM Word_list WHERE sinhala LIKE '%s' """ % sql_word)

                for raw in sql_cmd_1:
                    mean = "|".join(map(str, raw)).split("|")[-1].encode("utf-8").decode("utf-8")
                    main.mini_mod.mini_mod_list.addItem(mean)

        self.setStyleSheet(open(css_pack, "r").read())


    def mini_mod_timer_cnt(self):

        global mini_mod_timer_cnt, mini_mod_tab_visiable
        mini_mod_timer_cnt += 1

        print("mini_mod_timer_cnt = " + str(mini_mod_timer_cnt))

        if mini_mod_timer_cnt == 0 or 1:
            main.mini_mod.setWindowOpacity(0.8)

        if mini_mod_timer_cnt == 2:

            main.mini_mod.hide()

    def enterEvent(self, event):
        global mini_mod_title_timer_cnt


        main.mini_mod_title_timer.stop()
        self.setWindowOpacity(1)
        mini_mod_title_timer_cnt = 0

    def leaveEvent(self, event):
        global mini_mod_title_timer_timeout

        main.mini_mod_title_timer.start(mini_mod_title_timer_timeout)



    def showEvent(self, event):
        global mini_mod_title_timer_timeout

        main.mini_mod_title_timer.start(mini_mod_title_timer_timeout)


    def keyReleaseEvent(self, event):
        key = event.key()
        removing_list = []

        if self.hiden_txt_box.toPlainText() != "":

            if key == QtCore.Qt.Key_Backspace:


                text = self.hiden_txt_box.toPlainText()

                for letter in text:
                    print(letter)
                    removing_list.append(letter)

                removing_list.pop(-1)

                self.hiden_txt_box.clear()

                for item in removing_list:
                    self.hiden_txt_box.insertPlainText(item)


        if key == QtCore.Qt.Key_Space:


            self.hiden_txt_box.insertPlainText(" ")

    def mini_mod_voice(self):
        v_word = str(self.txt_input.text())
        voice_engine = Dispatch("SAPI.SpVoice")
        voice_engine.Speak(v_word)

    def onTextChanged(self):
        global lang_change

        if lang_change == True:



            lst = []

            lst2 = ["q", "w", "e", "r", "t", "y", "u", "i", "o", "p", "[", "]", "\\",
                    "a", "s", "d", "f", "g", "h", "j", "k", "l", ";", "'"
                    "z", "x", "c", "v", "b", "n", "m", ",", ".", "/",
                    "Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P", "{", "}", "|",
                    "A", "S", "D", "F", "G", "H", "J", "K", "L", ";", '"',
                    "Z", "X", "C", "V", "B", "N", "M", "<", ">", "?", " "]
            input_word = ""
            word = self.txt_input.text()
            hiden_text = self.hiden_txt_box.toPlainText()
            if word == "":
                self.hiden_txt_box.clear()

            for item in str(word):

                if item in lst2:
                    print(item)
                    input_word = item
                else:
                    lst.append(item)

            unicode_dic = {"q": 3540, "w": 3461, "e": 3536, "r": 3515, "t": 3509, "y": 3524, "u": 3512, "i": 3523, "o": 3507, "p": 3488,
                           "a": 3530, "s": 3538, "d": 3535, "f": 3545, "g": 3495, "h": 3514, "j": 3520, "k": 3505, "l": 3482, ";": 3501,
                           "x": 3458, "c": 3490, "v": 3497, "b": 3465, "n": 3510, "m": 3508, ",": 3517, ".": 3484,
                           "Q": 3542, "W": 3467, "E": 3537, "R": 3469, "T": 3476, "Y": 3521, "U": 3513, "I": 3522, "O": 3504, "P": 3489,
                           "A": 3530, "S": 3539, "D": 3544, "G": 3496, "K": 3499, "L": 3483, ":": 3502, "F": 3551,
                           "V": 3498, "B": 3466, "N": 3487, "M": 3509, "<": 3525, ">": 3485,
                           "[": 3463, "{": 3464, "]": 3459, "\\": 3491, "|": 3493, "/": 3492," `": 3502,}


            if input_word == "H":

                sinhala = chr(3530)+ chr (8205) + chr(3514)
                self.hiden_txt_box.insertPlainText(sinhala)
                self.txt_input.setText(self.hiden_txt_box.toPlainText())

            elif input_word == "`":

                sinhala = chr(3530) + chr(8205) + chr(3515)
                self.hiden_txt_box.insertPlainText(sinhala)
                self.txt_input.setText(self.hiden_txt_box.toPlainText())

            word_code = unicode_dic.get(input_word)

            if word_code == None:
                pass

            else:

                sinhala_word = chr(int(word_code))


                self.hiden_txt_box.insertPlainText(sinhala_word)

                self.txt_input.setText(self.hiden_txt_box.toPlainText())


class Mini_Mod_List(QtWidgets.QListWidget):

    def __init__(self):
        QtWidgets.QListWidget.__init__(self)

        self.resize(315, 75)
        self.move(10, 10)
        self.setObjectName("mini_mod_list")
        txt_font = QtGui.QFont()
        #l_font.setFamily(_fromUtf8("UN-Abhaya"))
        txt_font.setPixelSize(16)
        self.setFont(txt_font)

class Mini_Mod(QtWidgets.QFrame):
    def __init__(self):
        QtWidgets.QFrame.__init__(self)

        global mini_mod_x_pos
        global mini_mod_y_pos

        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)

        #self.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.setFixedSize(330, 105)
        self.setObjectName("Mini_Mod")
        self.setWindowOpacity(1)
        self.setMouseTracking(True)
        self.setContentsMargins(0, 0, 0, 0)
        self.setStyleSheet(open(css_pack, "r").read())

        self.moving = False

        self.mini_mod_list = Mini_Mod_List()

        self.minimod_stat_lbl = QtWidgets.QLabel(self)
        self.minimod_stat_lbl.resize(300, 20)
        self.minimod_stat_lbl.move(mini_mod_x_pos, mini_mod_y_pos)
        self.minimod_stat_lbl.setObjectName("minimod_stat_lbl")

        self.mini_mod_box = QtWidgets.QVBoxLayout(self)
        self.mini_mod_box.setSpacing(0)
        self.mini_mod_box.setContentsMargins(0, 0, 0, 0)
        self.mini_mod_box.addWidget(self.mini_mod_list)
        self.mini_mod_box.addWidget(self.minimod_stat_lbl)

    def enterEvent(self, event):

        global mini_mod_timer_cnt

        main.mini_mod_title.mini_mod_timer.stop()
        mini_mod_timer_cnt = 0
        main.mini_mod.setWindowOpacity(1)

    def leaveEvent(self, event):


        main.mini_mod_title.mini_mod_timer.start(6000)


    def showEvent(self, event):

        global mini_mod_window_show
        mini_mod_window_show = True

        main.mini_mod_title.mini_mod_timer.start(6000)
        main.mini_mod_title_timer.stop()

    def hideEvent(self, event):

        global mini_mod_window_show
        mini_mod_window_show = True


        global mini_mod_timer_cnt


        main.mini_mod_title.mini_mod_timer.stop()
        mini_mod_timer_cnt = 0
        main.mini_mod.setWindowOpacity(1)
        main.mini_mod_title_timer.start(mini_mod_title_timer_timeout)

    def mousePressEvent(self, event):


        if event.button() == Qt.LeftButton:
            self.moving = True
            self.offset = event.pos()

    def mouseMoveEvent(self, event):


        if self.moving:
            self.move(event.globalPos() - self.offset)

    def mouseReleaseEvent(self, event):

        self.moving = False


class baloon_title_bar(QtWidgets.QDialog):
    def __init__(self):
        QtWidgets.QDialog.__init__(self)

        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setMaximumHeight(22)
        self.setMouseTracking(True)
        self.setObjectName("baloon_title_bar")

        self.setAutoFillBackground(True)
        self.setBackgroundRole(QtGui.QPalette.Highlight)

        self.baloon_lbl = QtWidgets.QLabel(self)
        self.baloon_lbl.setText("")
        self.baloon_lbl.setAlignment(QtCore.Qt.AlignRight)
        self.baloon_lbl.setObjectName("baloon_lbl")

        self.hbox = QtWidgets.QHBoxLayout(self)
        self.hbox.setContentsMargins(0, 3, 0, 3)
        self.hbox.addWidget(self.baloon_lbl)
        self.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)

    def mousePressEvent(self, event):

        if event.button() == Qt.LeftButton:
            main.baloon_window.moving = True
            main.baloon_window.offset = event.pos()

    def mouseMoveEvent(self, event):

        if main.baloon_window.moving:
            main.baloon_window.move(event.globalPos() - main.baloon_window.offset)

    def mouseReleaseEvent(self, event):
        main.baloon_window.moving = False

    def mouseDoubleClickEvent(self, event):
        global timer_cnt
        global tray_icon_visiable
        if tray_icon_visiable == True:
            main.baloon_window.hide()
        else:
            main.baloon_window.close()
        timer_cnt = 0



class BaloonWindow(QtWidgets.QFrame):
    def __init__(self):
        QtWidgets.QFrame.__init__(self)

        self.setMouseTracking(True)
        self.setFrameShape(QtWidgets.QFrame.StyledPanel)

        self.setFixedSize(210, 115)
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)
        self.setObjectName("BaloonWindow")

        self.moving = False

        self.setStyleSheet(open(css_pack, "r").read())
        self.title_bar = baloon_title_bar()
        self.content = QtWidgets.QWidget(self)
        self.vbox = QtWidgets.QVBoxLayout(self)
        self.vbox.addWidget(self.title_bar)
        self.txt_area = QtWidgets.QPlainTextEdit(self)
        self.txt_area.setObjectName("baloon_txt_area")
        self.txt_area.setMaximumSize(210, 100)
        self.txt_area.setReadOnly(True)
        self.txt_area.move(25, 25)
        txt_font = QtGui.QFont()
        #l_font.setFamily(_fromUtf8("UN-Abhaya"))
        txt_font.setPixelSize(16)
        self.txt_area.setFont(txt_font)

        self.vbox.addWidget(self.txt_area)
        self.vbox.setSpacing(0)
        self.vbox.setContentsMargins(0,0,0,0)
        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.addWidget(self.content)
        #self.layout.setMargin(0)
        self.layout.setSpacing(0)
        self.vbox.addLayout(self.layout)

    def enterEvent(self, event):
        global timer_cnt

        main.baloon_w_timer.stop()
        self.setWindowOpacity(1)
        timer_cnt = 0

    def leaveEvent(self, QEvent):

        main.baloon_w_timer.start(6000)

    def showEvent(self, event):

        main.baloon_w_timer.start(6000)

    def closeEvent(self, event):
        global timer_cnt
        main.baloon_w_timer.stop()
        timer_cnt = 0
        self.setWindowOpacity(1)


    def mousePressEvent(self, event):

        if event.button() == Qt.LeftButton:
            self.moving = True
            self.offset = event.pos()

    def mouseMoveEvent(self, event):

        if self.moving:
            self.move(event.globalPos() - self.offset)
        self.setWindowOpacity(1)

    def mouseReleaseEvent(self, event):
        self.moving = False

    def mouseDoubleClickEvent(self, event):
        global tray_icon_visiable
        if tray_icon_visiable == True:
            self.hide()
        else:
            self.close()

    def hideEvent(self, event):
        global timer_cnt
        main.baloon_w_timer.stop()
        timer_cnt = 0
        self.setWindowOpacity(1)


class default_title_bar(QtWidgets.QDialog):
    def __init__(self):
        QtWidgets.QDialog.__init__(self)

        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setObjectName("default_title_bar")
        self.setMaximumHeight(50)
        self.setMinimumHeight(50)
        self.setMouseTracking(True)


        self.setAutoFillBackground(True)
        self.setBackgroundRole(QtGui.QPalette.Highlight)

        self.icon_button = QtWidgets.QPushButton(self)
        self.icon_button.setMaximumSize(50, 150)
        self.icon_button.setEnabled(False)

        self.line = QtWidgets.QFrame(self)
        self.line.setMaximumSize(2, 35)
        self.line.setFrameShape(QtWidgets.QFrame.VLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("default_title_line")

        self.title_lbl = QtWidgets.QLabel(self)
        self.title_lbl.setMaximumWidth(70)
        self.title_lbl.setObjectName("title_lbl")

        self.index_search = QtWidgets.QLineEdit(self)
        self.index_search.setObjectName("index_search")
        self.index_search.setMaximumWidth(100)
        self.index_search.setMaximumHeight(25)
        self.index_search.setPlaceholderText("search")
        index_font = QtGui.QFont()
        index_font.setFamily(_fromUtf8(""))
        index_font.setPixelSize(14)
        self.index_search.setFont(index_font)


        self.index_search.setVisible(False)


        self.index_line = QtWidgets.QFrame(self)
        self.index_line.setMaximumSize(2, 25)
        self.index_line.setFrameShape(QtWidgets.QFrame.VLine)
        self.index_line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.index_line.setObjectName("default_title_line")
        self.index_line.setVisible(False)

        self.space_lbl2 = QtWidgets.QLabel(self)
        self.space_lbl2.setMaximumWidth(600)

        self.close_btn = QtWidgets.QToolButton(self)
        self.close_btn.setObjectName("default_close_btn")
        self.close_btn.setMaximumSize(20, 20)

        self.hbox = QtWidgets.QHBoxLayout(self)
        self.hbox.setContentsMargins(0, 0, 0, 0)
        self.hbox.addWidget(self.icon_button)
        self.hbox.addWidget(self.line)
        self.hbox.addWidget(self.title_lbl)
        self.hbox.addWidget(self.index_line)
        self.hbox.addWidget(self.index_search)

        self.hbox.addWidget(self.space_lbl2)
        self.hbox.addWidget(self.close_btn)
        self.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)

    #   ******Button Commands ****
        self.close_btn.clicked.connect(self.default_close)
        self.index_search.textChanged.connect(self.index_list_search)


    def index_list_search(self):
        main.index_dialog.index_list.clear()

        word = str(self.index_search.text()).encode("utf-8").decode("utf-8")

        db = sqlite3.connect("Database/Shashika.ire")
        db.text_factory

        word_row = db.execute("""SELECT * FROM Abbreviations""")

        for line in word_row:

            if word in line:
                abb = "|".join(map(str, line)).split("|")[1].encode("utf-8").decode("utf-8")
                abb_mean = "|".join(map(str, line)).split("|")[1 + 1].encode("utf-8").decode("utf-8")

                result = abb + "          " + "          " + abb_mean



                main.index_dialog.index_list.addItem(result)

    def default_minimize(self):
        global about_d_show
        global option_d_show
        global key_d_show
        global ocr_d_show

        if about_d_show == True:
            main.about_dialog.showMinimized()
        elif option_d_show == True:
            main.opt_dialog.showMinimized()
        elif key_d_show == True:
            main.key_dialog.showMinimized()
        else:
            main.ocr_dialog.showMinimized()

    def default_close(self):
        global about_d_show
        global option_d_show
        global key_d_show
        global ocr_d_show
        global index_d_show

        if about_d_show == True:
            main.about_dialog.close()
            main.setWindowOpacity(1)
            about_d_show = False

        elif option_d_show == True:
            main.opt_dialog.close()
            option_d_show = False
            main.setWindowOpacity(1)

        elif key_d_show == True:
            main.key_dialog.close()
            key_d_show = False
            main.setWindowOpacity(1)
        elif ocr_d_show == True:
            main.ocr_dialog.close()
            ocr_d_show = False
            main.setWindowOpacity(1)
        else:
            main.index_dialog.close()
            index_d_show_d_show = False
            main.setWindowOpacity(1)

    def mousePressEvent(self, event):
        global about_d_show
        global option_d_show
        global key_d_show
        global ocr_d_show
        global index_d_show

        if event.button() == Qt.LeftButton:
            if option_d_show == True:
                main.opt_dialog.moving = True
                main.opt_dialog.offset = event.pos()

            elif about_d_show == True:
                main.about_dialog.moving = True
                main.about_dialog.offset = event.pos()

            elif key_d_show == True:
                main.key_dialog.moving = True
                main.key_dialog.offset = event.pos()

            elif ocr_d_show == True:
                main.ocr_dialog.moving = True
                main.ocr_dialog.offset = event.pos()
            else:
                main.index_dialog.moving = True
                main.index_dialog.offset = event.pos()

    def mouseMoveEvent(self, event):
        global about_d_show
        global option_d_show
        global key_d_show
        global ocr_d_show
        global index_d_show

        if option_d_show == True:
            if main.opt_dialog.moving:
                main.opt_dialog.move(event.globalPos() - main.opt_dialog.offset)
        elif about_d_show == True:
            if main.about_dialog.moving:
                main.about_dialog.move(event.globalPos() - main.about_dialog.offset)
        elif key_d_show == True:
            if main.key_dialog.moving:
                main.key_dialog.move(event.globalPos() - main.key_dialog.offset)
        elif ocr_d_show == True:
            if main.ocr_dialog.moving:
                main.ocr_dialog.move(event.globalPos() - main.ocr_dialog.offset)
        else:
            if main.index_dialog.moving:
                main.index_dialog.move(event.globalPos() - main.index_dialog.offset)

    def mouseReleaseEvent(self, event):
        global about_d_show
        global option_d_show
        global key_d_show
        global ocr_d_show
        global index_d_show

        if about_d_show == True:
            main.about_dialog.moving = False
        elif option_d_show == True:
            main.opt_dialog.moving = False
        elif key_d_show == True:
            main.key_dialog.moving = False
        elif ocr_d_show == True:
            main.ocr_dialog.moving = False
        else:
            main.index_dialog.moving = False


class About_Dialog(QtWidgets.QDialog):

    def __init__(self):

        QtWidgets.QDialog.__init__(self)

        self.setMouseTracking(True)
        self.setObjectName("commen")
        self.setStyleSheet(open(css_pack, "r").read())

        self.move(200, 50)
        self.setFixedSize(600, 400)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.moving = False

        self.logo_btn = QtWidgets.QPushButton(self)
        self.logo_btn.setObjectName("logo_btn")
        self.logo_btn.setMinimumHeight(100)
        self.logo_btn.setMinimumWidth(100)
        self.logo_btn.setMaximumHeight(100)
        self.logo_btn.setMaximumWidth(100)

        self.profile_btn = QtWidgets.QPushButton(self)
        self.profile_btn.setObjectName("profile_btn")
        self.profile_btn.setMinimumHeight(100)
        self.profile_btn.setMinimumWidth(100)
        self.profile_btn.setMaximumHeight(100)
        self.profile_btn.setMaximumWidth(100)

        self.detail_lbl = QtWidgets.QPlainTextEdit(self)
        self.detail_lbl.setObjectName("detail_lbl")
        info = """
Lotus Dictionary
Version: 2.0
2019

    Lotus Dictionary is the updated version of “Sinhala Dictionary” and it was released on 2018. But it is  not good much as i accepted, it was a really buggy software. In this version of software I improved proformance and re created User interface and also fixed known bugs previously find out. Now The Lotus Dictionary support both Windows and Linux operating systems. 

    Previously released version had a database with 120, 000 words, In this version it improved up to 250, 000 words. I think this is the largest database among the all sinhala dictionary software in Linux, Windows and Android. I believe this software will be helpful for linux users and also Windows users too.

Following new features are added to Lotus Dictionary V.2.0

* Updated Database
* New Dictionary Mod [Widget Mod]
* New GUI
* Windows OS Support
* Easy Sinhala Typing Keyboard [UTF-8]

  """

        info2 = """
M.M.S.Dilhara
Email: sdilhara@protonmail.ch
Website: www.linuxworldz.wordpress.com
Facebook Page: Lotus Dictionary

    There is a my close friend`s picture in the side panel, P.Rangika Prasad Who died by an accident last month, while he came back to home after A/L exam. I tribute this software for my friend. May Rest in peace!

    I`m M.M.Shashika Dilhara Currently studying at Technical Collage Embilipitiya. I’m an experienced Linux user for long time. I want to make Linux familiar to general users in Sri Lanka. There for I made this dictionary software for Linux operating systems.

Special Thanks:

* Technical Collage of Embilipitiya, Staff and Students
* NCPE batch 2019, Class Teacher
* And All the supportive

If you found any bug or error please report me. And always welcome your suggestions and any kind of discussions. Contact me

Thank you for Download Lotus Dictionary V.2.0

        """

        self.detail_lbl.setPlainText(info)
        self.detail_lbl.setReadOnly(True)
        detail_lbl_font = QtGui.QFont()
        detail_lbl_font.setPixelSize(15)
        self.detail_lbl.setFont(detail_lbl_font)


        self.detail_lbl.setMaximumHeight(400)
        self.detail_lbl.setMinimumWidth(480)

        self.space_lbl = QtWidgets.QLabel(self)
        self.space_lbl.setMinimumHeight(25)

        self.space_lbl1 = QtWidgets.QLabel(self)
        self.space_lbl1.setMinimumHeight(100)

        self.space_lbl2 = QtWidgets.QLabel(self)
        self.space_lbl2.setMinimumHeight(50)



        self.btn_vbox = QtWidgets.QVBoxLayout()
        self.btn_vbox.addWidget(self.space_lbl2)
        self.btn_vbox.addWidget(self.logo_btn)
        self.btn_vbox.addWidget(self.space_lbl)
        self.btn_vbox.addWidget(self.profile_btn)
        self.btn_vbox.addWidget(self.space_lbl1)
        self.btn_vbox.setContentsMargins(0, 0, 0, 0)

        self.hbox = QtWidgets.QHBoxLayout()
        self.hbox.addLayout(self.btn_vbox)
        self.hbox.addWidget(self.detail_lbl)
        self.hbox.setContentsMargins(10, 10, 10, 10)

        self.title_bar = default_title_bar()
        self.content = QtWidgets.QWidget(self)
        self.vbox = QtWidgets.QVBoxLayout(self)
        self.vbox.addWidget(self.title_bar)
        self.vbox.addLayout(self.hbox)

        self.vbox.setSpacing(0)

        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.addWidget(self.content)

        self.layout.setSpacing(0)
        self.vbox.addLayout(self.layout)
        self.vbox.setContentsMargins(0, 0, 0, 0)

        self.setContentsMargins(0, 0, 0, 0)

        self.logo_btn.clicked.connect(self.ver_info)
        self.profile_btn.clicked.connect(self.prog_info)

    def ver_info(self):

        info = """
Lotus Dictionary
Version: 2.0
2019

    Lotus Dictionary is the updated version of “Sinhala Dictionary” and it was released on 2018. But it is  not good much as i accepted, it was a really buggy software. In this version of software I improved performance and re created User interface and also fixed known bugs previously find out. Now The Lotus Dictionary support both Windows and Linux operating systems. 

    Previously released version had a database with 120, 000 words, In this version it improved up to 250, 000 words. I think this is the largest database among the all Sinhala dictionary software in Linux, Windows and Android. I believe this software will be helpful for Linux users and also Windows users too.

Following new features are added to Lotus Dictionary V.2.0

* Updated Database
* New Dictionary Mod [Widget Mod]
* New GUI
* Windows OS Support
* Easy Sinhala Typing Keyboard [UTF-8]

                        """
        self.detail_lbl.setPlainText(info)
        self.logo_btn.setObjectName("logo_btn_active")
        self.profile_btn.setObjectName("profile_btn")
        self.setStyleSheet(open(css_pack, "r").read())

    def prog_info(self):

        info2 = """
M.M.S.Dilhara
Email: sdilhara@protonmail.ch
Website: www.linuxworldz.wordpress.com
Facebook Page: Lotus Dictionary

    There is a my close friend`s picture in the side panel, P.Rangika Prasad Who died by an accident last month, while he came back to home after A/L exam. I tribute this software for my friend. May Rest in peace!

    I`m M.M.Shashika Dilhara Currently studying at Technical Collage Embilipitiya. I’m an experienced Linux user for long time. I want to make Linux familiar to general users in Sri Lanka. There for I made this dictionary software for Linux operating systems.

Special Thanks:

* Technical Collage of Embilipitiya, Staff and Students
* NCPE batch 2019, Class Teacher
* And All the supportive

If you found any bug or error please report me. And always welcome your suggestions and any kind of discussions. Contact me

Thank you for Download Lotus Dictionary V.2.0

        """

        self.detail_lbl.setPlainText(info2)
        self.logo_btn.setObjectName("logo_btn_inactive")
        self.profile_btn.setObjectName("profile_btn_active")
        self.setStyleSheet(open(css_pack, "r").read())

    def mousePressEvent(self, event):

        if event.button() == Qt.LeftButton:
            self.moving = True
            self.offset = event.pos()

    def mouseMoveEvent(self, event):

        if self.moving:
            self.move(event.globalPos() - self.offset)

    def mouseReleaseEvent(self, event):
        self.moving = False


class Option_Dialog(QtWidgets.QDialog):

    def __init__(self):
        QtWidgets.QDialog.__init__(self)

        self.setMouseTracking(True)
        self.setStyleSheet(open(css_pack, "r").read())
        self.setObjectName("commen")

        self.move(200, 50)
        self.setFixedSize(600, 400)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setContentsMargins(0, 0, 0, 0)
        self.moving = False

        self.title_bar = default_title_bar()
        self.content = QtWidgets.QWidget(self)
        self.vbox = QtWidgets.QVBoxLayout(self)
        self.vbox.addWidget(self.title_bar)

        self.lbl1 = QtWidgets.QLabel(self)
        self.lbl1.setObjectName("opt_lbl")
        self.lbl1.setText("Real Time Dictionary")

        self.lbl1.setMaximumSize(200, 20)
        self.spacing_lbl = QtWidgets.QLabel(self)
        self.spacing_lbl.setMaximumWidth(320)
        self.btn1 = QtWidgets.QPushButton()
        self.btn1.setObjectName("btn1")

        self.btn1.setMaximumSize(50, 20)
        self.hbox = QtWidgets.QHBoxLayout()
        self.hbox.setContentsMargins(10,10,10,10)
        self.line1 = QtWidgets.QFrame(self)
        self.line1.setFrameShape(QtWidgets.QFrame.VLine)
        self.line1.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line1.setMaximumSize(2, 50)
        self.line1.setObjectName("line1")

        self.hbox.addWidget(self.line1)
        self.hbox.addWidget(self.lbl1)
        self.hbox.addWidget(self.spacing_lbl)
        self.hbox.addWidget(self.btn1)
        self.vbox.addLayout(self.hbox)

        self.lbl2 = QtWidgets.QLabel(self)
        self.lbl2.setText("Always On The Top")

        self.lbl2.setObjectName("opt_lbl")
        self.lbl2.setMaximumSize(200, 20)
        self.spacing_lbl = QtWidgets.QLabel(self)
        self.spacing_lbl.setMaximumWidth(320)
        self.btn2 = QtWidgets.QPushButton()
        self.btn2.setObjectName("btn2")
        self.btn2.setMaximumSize(50, 20)

        self.hbox2 = QtWidgets.QHBoxLayout()
        self.hbox2.setContentsMargins(10, 10, 10, 10)
        self.line2 = QtWidgets.QFrame(self)
        self.line2.setFrameShape(QtWidgets.QFrame.VLine)
        self.line2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line2.setMaximumSize(2, 50)
        self.line2.setObjectName("line2")

        self.hbox2.addWidget(self.line2)
        self.hbox2.addWidget(self.lbl2)
        self.hbox2.addWidget(self.spacing_lbl)
        self.hbox2.addWidget(self.btn2)
        self.vbox.addLayout(self.hbox2)

        self.lbl3 = QtWidgets.QLabel(self)
        self.lbl3.setObjectName("opt_lbl")
        self.lbl3.setText("Open At StartUp")
        self.lbl3.setMaximumSize(200, 20)

        self.spacing_lbl = QtWidgets.QLabel(self)
        self.spacing_lbl.setMaximumWidth(320)
        self.btn3 = QtWidgets.QPushButton()
        self.btn3.setObjectName("btn3")
        self.btn3.setMaximumSize(50, 20)

        self.hbox3 = QtWidgets.QHBoxLayout()
        self.hbox3.setContentsMargins(10, 10, 10, 10)
        self.line3 = QtWidgets.QFrame(self)
        self.line3.setFrameShape(QtWidgets.QFrame.VLine)
        self.line3.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line3.setMaximumSize(2, 50)
        self.line3.setObjectName("line3")

        self.hbox3.addWidget(self.line3)
        self.hbox3.addWidget(self.lbl3)
        self.hbox3.addWidget(self.spacing_lbl)
        self.hbox3.addWidget(self.btn3)
        self.vbox.addLayout(self.hbox3)

        self.lbl4 = QtWidgets.QLabel(self)
        self.lbl4.setObjectName("opt_lbl")
        self.lbl4.setText("Widget Auto Hide")

        self.lbl4.setMaximumSize(120, 20)
        self.spacing_lbl = QtWidgets.QLabel(self)
        self.spacing_lbl.setMaximumWidth(400)
        self.btn4 = QtWidgets.QPushButton()
        self.btn4.setObjectName("btn4")
        self.btn4.setMaximumSize(50, 20)

        self.hbox4 = QtWidgets.QHBoxLayout()
        self.hbox4.setContentsMargins(10, 10, 10, 10)
        self.line4 = QtWidgets.QFrame(self)
        self.line4.setFrameShape(QtWidgets.QFrame.VLine)
        self.line4.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line4.setMaximumSize(2, 50)
        self.line4.setObjectName("line4")

        self.hbox4.addWidget(self.line4)
        self.hbox4.addWidget(self.lbl4)
        self.hbox4.addWidget(self.spacing_lbl)
        self.hbox4.addWidget(self.btn4)
        self.vbox.addLayout(self.hbox4)

        self.hbox6 = QtWidgets.QHBoxLayout()
        self.spacing_lbl = QtWidgets.QLabel(self)
        self.spacing_lbl.resize(200, 20)
        self.hbox6.addWidget(self.spacing_lbl)
        self.vbox.addLayout(self.hbox6)

        self.hbox8 = QtWidgets.QHBoxLayout()
        self.spacing_lbl = QtWidgets.QLabel(self)
        self.spacing_lbl.setMaximumWidth(500)
        self.ok_btn = QtWidgets.QPushButton()
        self.ok_btn.setMaximumSize(70, 30)
        self.ok_btn.setText("| OK")
        self.ok_btn.setObjectName("ok_btn")

        self.hbox8.addWidget(self.spacing_lbl)
        self.hbox8.addWidget(self.ok_btn)
        self.vbox.addLayout(self.hbox8)

        self.vbox.setSpacing(0)

        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.addWidget(self.content)

        self.layout.setSpacing(0)
        self.vbox.addLayout(self.layout)
        self.vbox.setContentsMargins(0, 0, 0, 0)

    #  ********Button Commands***************

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.moving = True
            self.offset = event.pos()

    def mouseMoveEvent(self, event):
        if self.moving:
            self.move(event.globalPos() - self.offset)

    def mouseReleaseEvent(self, event):
        self.moving = False

    def mouseDoubleClickEvent(self, event):
        self.moving = False


class Key_Dialog(QtWidgets.QDialog):
    def __init__(self):
        QtWidgets.QDialog.__init__(self)

        self.setMouseTracking(True)
        self.setStyleSheet(open(css_pack, "r").read())

        self.move(200, 50)
        self.setFixedSize(800, 330)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setContentsMargins(0, 0, 0, 0)
        self.moving = False

        self.keybord_lbl = QtWidgets.QLabel()
        self.keybord_lbl.setFixedSize(800, 220)

        self.keybord_lbl.setObjectName("keybord_lbl")

        self.shift_btn = QtWidgets.QPushButton(self)
        self.shift_btn.setText("SHIFT")
        self.shift_btn.setMinimumHeight(50)
        self.shift_btn.setObjectName("shift_btn")

        self.shift_btn1 = QtWidgets.QPushButton(self)
        self.shift_btn1.setText("SHIFT")
        self.shift_btn1.setMinimumHeight(50)
        self.shift_btn1.setObjectName("shift_btn1")

        self.spacing_lbl = QtWidgets.QLabel()
        self.spacing_lbl.setMinimumWidth(100)

        self.hbox1 = QtWidgets.QHBoxLayout()
        self.hbox1.addWidget(self.shift_btn)
        self.hbox1.addWidget(self.spacing_lbl)
        self.hbox1.addWidget(self.shift_btn1)

        self.hbox = QtWidgets.QHBoxLayout()
        self.hbox.addWidget(self.keybord_lbl)

        self.title_bar = default_title_bar()
        self.content = QtWidgets.QWidget(self)
        self.vbox = QtWidgets.QVBoxLayout(self)
        self.vbox.addWidget(self.title_bar)
        self.vbox.addLayout(self.hbox)
        self.vbox.addLayout(self.hbox1)
        self.vbox.setSpacing(0)
        # self.vbox.setMargin(0)
        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.addWidget(self.content)
        # self.layout.setMargin(0)
        self.layout.setSpacing(0)
        self.vbox.addLayout(self.layout)
        self.vbox.setContentsMargins(0, 0, 0, 0)

        # ************Button_Commands************

        self.shift_btn.clicked.connect(self.shift_press)
        self.shift_btn1.clicked.connect(self.shift_press)

    def keyReleaseEvent(self, event):

        key = event.key()

        if key == Qt.Key_Shift:
            self.shift_press()

    def shift_press(self):
        global keybord_shift_press

        if keybord_shift_press == False:
            keybord_shift_press = True

        else:
            keybord_shift_press = False

        if keybord_shift_press == True:

            self.shift_btn.setObjectName("shift_btn_active")
            self.shift_btn1.setObjectName("shift_btn1_active")
            self.keybord_lbl.setObjectName("keybord_lbl_shift")
            self.setStyleSheet(open(css_pack, "r").read())


        else:

            self.shift_btn.setObjectName("shift_btn")
            self.shift_btn1.setObjectName("shift_btn1")
            self.keybord_lbl.setObjectName("keybord_lbl")
            self.setStyleSheet(open(css_pack, "r").read())

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.moving = True
            self.offset = event.pos()

    def mouseMoveEvent(self, event):
        if self.moving:
            self.move(event.globalPos() - self.offset)

    def mouseReleaseEvent(self, event):
        self.moving = False


class OCR_Dialog(QtWidgets.QDialog):
    def __init__(self):
        QtWidgets.QDialog.__init__(self)

        self.setMouseTracking(True)
        self.setStyleSheet(open(css_pack, "r").read())

        self.move(200, 50)
        self.setFixedSize(600, 400)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.moving = False

        self.title_bar = default_title_bar()
        self.content = QtWidgets.QWidget(self)
        self.vbox = QtWidgets.QVBoxLayout(self)
        self.vbox.addWidget(self.title_bar)

        self.vbox.setSpacing(0)

        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.addWidget(self.content)

        self.layout.setSpacing(0)
        self.vbox.addLayout(self.layout)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.moving = True
            self.offset = event.pos()

    def mouseMoveEvent(self, event):
        if self.moving:
            self.move(event.globalPos() - self.offset)

    def mouseReleaseEvent(self, event):
        self.moving = False


class Index_Dialog(QtWidgets.QDialog):
    def __init__(self):
        QtWidgets.QDialog.__init__(self)

        self.setMouseTracking(True)
        self.setStyleSheet(open(css_pack, "r").read())

        self.move(200, 50)
        self.setFixedSize(600, 400)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.moving = False

        self.index_list = QtWidgets.QListWidget()

        self.index_list.setFixedSize(550, 360)
        self.index_list.setObjectName("index_list")
        self.index_list.setAlternatingRowColors(False)
        self.index_list.setSpacing(4)
        index_font = QtGui.QFont()
        index_font.setFamily(_fromUtf8("LKLUG"))
        index_font.setPixelSize(15)
        self.index_list.setFont(index_font)

        self.spacing_lbl = QtWidgets.QLabel()
        self.spacing_lbl.setMinimumWidth(100)

        self.hbox = QtWidgets.QHBoxLayout()
        self.hbox.setGeometry(QtCore.QRect(0, 0, 550, 360))

        self.hbox.addWidget(self.index_list)

        self.title_bar = default_title_bar()


        self.verticalLayoutWidget = QtWidgets.QWidget(self)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(0, 0, 600, 360))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")

        self.verticalLayout.addWidget(self.title_bar)
        self.verticalLayout.addWidget(self.spacing_lbl)
        self.verticalLayout.addLayout(self.hbox)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.moving = True
            self.offset = event.pos()

    def mouseMoveEvent(self, event):
        if self.moving:
            self.move(event.globalPos() - self.offset)

    def mouseReleaseEvent(self, event):
        self.moving = False

    def showEvent(self, event):
        spacing = ""
        db = sqlite3.connect("Database/Shashika.ire")
        db.text_factory

        word_row = db.execute("""SELECT * FROM Abbreviations""")

        for line in word_row:
            abb = "|".join(map(str, line)).split("|")[1].encode("utf-8").decode("utf-8")
            abb_mean = "|".join(map(str, line)).split("|")[1 + 1].encode("utf-8").decode("utf-8")

            result = abb + "          " + "          " + abb_mean

            self.index_list.addItem(result)


class TitleBar(QtWidgets.QDialog):

    def __init__(self):
        QtWidgets.QDialog.__init__(self)

        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setObjectName("TitleBar")
        self.setStyleSheet(open(css_pack, "r").read())
        self.move(200, 50)
        self.setMaximumHeight(50)


        self.setAutoFillBackground(True)
        self.setBackgroundRole(QtGui.QPalette.Highlight)
        self.minimize_btn = QtWidgets.QToolButton(self)
        self.minimize_btn.setObjectName("minimize_btn")

        self.maxmize_btn = QtWidgets.QToolButton(self)
        self.maxmize_btn.setObjectName("maxmize_btn")

        self.close_btn = QtWidgets.QToolButton(self)
        self.close_btn.setObjectName("close_btn")

        self.tray_btn = QtWidgets.QToolButton(self)
        self.tray_btn.setObjectName("tray_btn")


        self.minimize_btn.setMaximumSize(20, 20)
        self.tray_btn.setMaximumSize(20, 20)
        self.maxmize_btn.setMaximumSize(20, 20)
        self.close_btn.setMaximumSize(20, 20)

        self.txt_input = QtWidgets.QLineEdit(self)
        self.txt_input.setObjectName("txt_input")
        signal_txt = self.txt_input.text()
        self.txt_input.setMaximumSize(180, 32)
        txt_font = QtGui.QFont()

        txt_font.setPixelSize(16)
        self.txt_input.setFont(txt_font)

        self.speaker_btn = QtWidgets.QPushButton(self)
        self.speaker_btn.setObjectName("speaker_btn")

        self.speaker_btn.setMaximumSize(40, 30)
        self.span_lbl = QtWidgets.QLabel(self)
        self.span_lbl.setObjectName("span_lbl")
        self.span_lbl.setMaximumSize(5, 50)
        self.span_lbl.setMinimumHeight(100)

        self.serch_btn = QtWidgets.QPushButton(self)
        self.serch_btn.setMaximumSize(40, 30)
        self.serch_btn.setObjectName("serch_btn")

        self.hiden_txt_box = QtWidgets.QTextEdit(self)

        self.hiden_txt_box.hide()

        self.hbox = QtWidgets.QHBoxLayout(self)
        self.hbox.setContentsMargins(5,5,5,5)
        self.hbox.addWidget(self.speaker_btn)
        self.hbox.addWidget(self.txt_input)
        self.hbox.addWidget(self.serch_btn)
        self.hbox.addWidget(self.span_lbl)
        self.hbox.addWidget(self.minimize_btn)
        self.hbox.addWidget(self.tray_btn)
        self.hbox.addWidget(self.maxmize_btn)
        self.hbox.addWidget(self.close_btn)
        self.hbox.setSpacing(0)
        self.setSizePolicy(QtWidgets.QSizePolicy.Expanding,QtWidgets.QSizePolicy.Fixed)
        self.maxNormal = False

        self.close_btn.clicked.connect(self.close)
        self.minimize_btn.clicked.connect(self.minimize)
        self.txt_input.textChanged.connect(self.onTextChanged)



    def keyReleaseEvent(self, event):
        key = event.key()
        removing_list = []

        if self.hiden_txt_box.toPlainText() != "":

            if key == QtCore.Qt.Key_Backspace:

                print(" back space pressed")

                text = self.hiden_txt_box.toPlainText()

                for letter in text:
                    print(letter)
                    removing_list.append(letter)

                removing_list.pop(-1)

                self.hiden_txt_box.clear()

                for item in removing_list:
                    self.hiden_txt_box.insertPlainText(item)


        if key == QtCore.Qt.Key_Space:

            print("space key pressed")

            self.hiden_txt_box.insertPlainText(" ")



    def onTextChanged(self):
        global lang_change

        if lang_change == True:



            lst = []

            lst2 = ["q", "w", "e", "r", "t", "y", "u", "i", "o", "p", "[", "]", "\\",
                    "a", "s", "d", "f", "g", "h", "j", "k", "l", ";", "'"
                    "z", "x", "c", "v", "b", "n", "m", ",", ".", "/",
                    "Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P", "{", "}", "|",
                    "A", "S", "D", "F", "G", "H", "J", "K", "L", ";", '"',
                    "Z", "X", "C", "V", "B", "N", "M", "<", ">", "?", "`", ":"]
            input_word = ""
            word = self.txt_input.text()

            if word == "":
                self.hiden_txt_box.clear()

            for item in str(word):

                if item in lst2:
                    print(item)
                    input_word = item
                else:
                    lst.append(item)

            unicode_dic = {"q": 3540, "w": 3461, "e": 3536, "r": 3515, "t": 3509, "y": 3524, "u": 3512, "i": 3523, "o": 3507, "p": 3488,
                           "a": 3530, "s": 3538, "d": 3535, "f": 3545, "g": 3495, "h": 3514, "j": 3520, "k": 3505, "l": 3482, ";": 3501,
                           "x": 3458, "c": 3490, "v": 3497, "b": 3465, "n": 3510, "m": 3508, ",": 3517, ".": 3484,
                           "Q": 3542, "W": 3467, "E": 3537, "R": 3469, "T": 3476, "Y": 3521, "U": 3513, "I": 3522, "O": 3504, "P": 3489,
                           "A": 3530, "S": 3539, "D": 3544, "G": 3496, "K": 3499, "L": 3483, ":": 3502, "F": 3551,
                           "V": 3498, "B": 3466, "N": 3487, "M": 3509, "<": 3525, ">": 3485,
                           "[": 3463, "{": 3464, "]": 3459, "\\": 3491, "|": 3493, "/": 3492, ":": 3502}


            if input_word == "H":

                sinhala = chr(3530)+ chr (8205) + chr(3514)
                self.hiden_txt_box.insertPlainText(sinhala)
                self.txt_input.setText(self.hiden_txt_box.toPlainText())

            elif input_word == "`":

                sinhala = chr(3530)+ chr (8205) + chr(3515)
                self.hiden_txt_box.insertPlainText(sinhala)
                self.txt_input.setText(self.hiden_txt_box.toPlainText())

            print(unicode_dic.get(input_word, None))
            word_code = unicode_dic.get(input_word)

            if word_code == None:
                pass

            else:

                sinhala_word = chr(int(word_code))
                print("printing word" + sinhala_word)

                self.hiden_txt_box.insertPlainText(sinhala_word)

                print(self.hiden_txt_box.toPlainText())
                self.txt_input.setText(self.hiden_txt_box.toPlainText())


    def minimize(self):
        main.showMinimized()

    def close(self):

        main.close()
        main.about_dialog.close()
        main.index_dialog.close()
        main.opt_dialog.close()
        main.key_dialog.close()
        main.baloon_window.close()
        main.mini_mod_title.close()


    def mousePressEvent(self, event):

        if event.button() == Qt.LeftButton:

            main.moving = True
            main.offset = event.pos()

    def mouseMoveEvent(self, event):
        if main.moving: main.move(event.globalPos()-main.offset)

class History_box(QtWidgets.QListWidget):
    def __init__(self):
        QtWidgets.QListWidget.__init__(self)

        self.move(398, 87)
        self.resize(330, 31)
        self.setObjectName("hstry_box")

    def enterEvent(self, event):

        main.history_frame.resize(325, 100)
        main.history_box.resize(330, 100)
        main.sujest_list.resize(325, 230)
        main.sujest_list.move(400, 189)

    def leaveEvent(self, event):

        main.history_frame.resize(325, 31)
        main.history_box.resize(330, 31)
        main.sujest_list.move(400, 120)
        main.sujest_list.resize(325, 299)



class Ui_Main(QtWidgets.QFrame):

    def __init__(self):
        QtWidgets.QFrame.__init__(self)
        self.setupUi()

    def setupUi(self):

        self.setObjectName("Main")
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(sizePolicy)
        self.setFixedSize(344, 463)
        self.setWindowOpacity(1)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setStyleSheet(open(css_pack, "r").read())

        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("theme/dark_theme/asset/Lotus3.png"))

        self.setWindowIcon(icon)
        self.tray_icon = QtWidgets.QSystemTrayIcon()
        self.tray_icon.setIcon(icon)


        self.moving = False
        self.title_bar = TitleBar()
        self.about_dialog = About_Dialog()
        self.opt_dialog = Option_Dialog()
        self.key_dialog = Key_Dialog()
        self.ocr_dialog = OCR_Dialog()
        self.index_dialog = Index_Dialog()
        self.baloon_window = BaloonWindow()
        self.default_title_bar = default_title_bar()
        self.baloon_title = baloon_title_bar()
        self.mini_mod = Mini_Mod()
        self.mini_mod_title = Mini_Mod_TitleBar()
        self.history_box = History_box()



        self.verticalLayoutWidget = QtWidgets.QWidget(self)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(0, 0, 344, 50))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")

        self.verticalLayout.addWidget(self.title_bar)

        self.lst_w = QtWidgets.QListWidget(self)

        self.lst_w.setObjectName("main_wrd_lst")
        self.lst_w.move(22, 88)
        self.lst_w.resize(301, 315)
        self.lst_w.setAcceptDrops(False)
        self.lst_w.setAlternatingRowColors(False)
        self.lst_w.setSpacing(7)
        self.lst_w.setModelColumn(0)
        self.lst_w.setUniformItemSizes(False)
        l_font = QtGui.QFont()
        l_font.setFamily(_fromUtf8("UN-Abhaya"))
        l_font.setPixelSize(21)
        self.lst_w.setFont(l_font)



        self.sujest_expand_btn = QtWidgets.QPushButton(self)
        self.sujest_expand_btn.setObjectName("sujest_expand_btn")
        self.sujest_expand_btn.move(325, 190)
        self.sujest_expand_btn.resize(21, 81)

        self.sujest_list = QtWidgets.QListWidget(self)
        self.sujest_list.setObjectName("sujest_list")
        self.sujest_list.move(400, 120)
        self.sujest_list.resize(325, 299)
        self.sujest_list.setSpacing(3)
        sujest_font = QtGui.QFont()
        sujest_font.setFamily(_fromUtf8("LKLUG"))
        sujest_font.setPixelSize(15)
        self.sujest_list.setFont(sujest_font)

        self.sujest_colaps_btn = QtWidgets.QPushButton(self)
        self.sujest_colaps_btn.setObjectName("sujest_colaps_btn")
        self.sujest_colaps_btn.move(730, 190)
        self.sujest_colaps_btn.resize(21, 81)

        self.boder_line = QtWidgets.QFrame(self)
        self.boder_line.setObjectName("boder_line")
        self.boder_line.move(360, 50)
        self.boder_line.resize(2, 450)
        self.boder_line.setFrameShape(QtWidgets.QFrame.VLine)
        self.boder_line.setFrameShadow(QtWidgets.QFrame.Sunken)

        self.stats_lbl = QtWidgets.QLabel(self)
        self.stats_lbl.setObjectName("stats_lbl")
        self.stats_lbl.resize(301, 30)
        self.stats_lbl.move(22, 407)

        self.switch_lbl_eng = QtWidgets.QLabel(self)
        self.switch_lbl_eng.setObjectName("switch_lbl_eng_active")
        self.switch_lbl_eng.resize(50, 20)
        self.switch_lbl_eng.move(122, 60)
        self.switch_lbl_eng.setText("EN")

        self.switch_lbl_si = QtWidgets.QLabel(self)
        self.switch_lbl_si.setObjectName("switch_lbl_si")
        self.switch_lbl_si.resize(50, 20)
        self.switch_lbl_si.move(202, 60)
        self.switch_lbl_si.setText("SI")

        self.switch_line = QtWidgets.QFrame(self)
        self.switch_line.setObjectName("switch_line")
        self.switch_line.setFrameShape(QtWidgets.QFrame.VLine)

        self.switch_line.move(112, 60)
        self.switch_line.setMaximumSize(1, 20)

        self.switch_line1 = QtWidgets.QFrame(self)
        self.switch_line1.setObjectName("switch_line1")
        self.switch_line1.setFrameShape(QtWidgets.QFrame.VLine)

        self.switch_line1.move(222, 60)
        self.switch_line1.setMaximumSize(1, 20)

        self.option_btn = QtWidgets.QPushButton(self)
        self.option_btn.setObjectName("option_btn")
        self.option_btn.setText("A")
        self.option_btn.resize(30, 30)
        self.option_btn.move(77, 55)
        self.option_btn.setVisible(True)

        self.option_btn1 = QtWidgets.QPushButton(self)
        self.option_btn1.setObjectName("option_btn1")
        self.option_btn1.setText("O")
        self.option_btn1.resize(30, 30)
        self.option_btn1.move(227, 55)
        self.option_btn1.setVisible(True)

        self.radio_btn2 = QtWidgets.QPushButton(self)
        self.radio_btn2.setObjectName("radio_btn2")
        self.radio_btn2.resize(50, 20)
        self.radio_btn2.move(147, 60)

        self.dock_expand_btn = QtWidgets.QPushButton(self)
        self.dock_expand_btn.setObjectName("dock_expand_btn")
        self.dock_expand_btn.resize(65, 20)
        self.dock_expand_btn.move(330, 50)
        self.dock_expand_btn.setVisible(False)

        self.dock_frame = QtWidgets.QFrame(self)
        self.dock_frame.setObjectName("dock_frame")
        self.dock_frame.resize(65, 395)
        self.dock_frame.move(330, 70)
        self.dock_frame.setVisible(False)

        self.dock_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)

        self.about_btn = QtWidgets.QPushButton(self)
        self.about_btn.setObjectName("about_btn")
        self.about_btn.setMaximumSize(65, 50)
        self.about_btn.move(330, 445)
        self.about_btn.setVisible(True)


        self.key_btn = QtWidgets.QPushButton(self)
        self.key_btn.setObjectName("key_btn")
        self.key_btn.setMaximumSize(65, 50)
        self.key_btn.move(330, 445)
        self.key_btn.setVisible(True)


        self.setting_btn = QtWidgets.QPushButton(self)
        self.setting_btn.setObjectName("setting_btn")
        self.setting_btn.setMaximumSize(65, 50)
        self.setting_btn.move(330, 445)
        self.setting_btn.setVisible(True)

        self.index_btn = QtWidgets.QPushButton(self)
        self.index_btn.setObjectName("index_btn")
        self.index_btn.setMaximumSize(65, 50)
        self.index_btn.move(330, 445)
        self.index_btn.setVisible(True)


        self.dock_box = QtWidgets.QVBoxLayout(self.dock_frame)

        self.dock_box.setSpacing(0)
        self.dock_box.setContentsMargins(0, 0, 0, 0)
        self.dock_box.addWidget(self.about_btn)
        self.dock_box.addWidget(self.key_btn)
        self.dock_box.addWidget(self.setting_btn)

        self.dock_box.addWidget(self.index_btn)

        self.history_frame = QtWidgets.QFrame(self)
        self.history_frame.setObjectName("history_frame")
        self.history_frame.resize(325, 31)
        self.history_frame.move(400, 87)
        self.history_frame.setVisible(True)

        self.history_box_frame = QtWidgets.QHBoxLayout(self.history_frame)
        self.history_box_frame.addWidget(self.history_box)
        self.history_box_frame.setContentsMargins(0, 0, 0, 0)
        self.history_box_frame.setSpacing(0)


        self.load_settings()     # Load previously settings
        self.title_bar.txt_input.setFocus()         # focus on start
        self.mini_mod_title.txt_input.setFocus()    # focus on start

        self.baloon_w_timer = QTimer()
        self.mini_mod_title_timer = QTimer()
        self.about_dialog.setObjectName("About_Dialog")


    #   *************** Button Commands ****************************
        self.sujest_expand_btn.clicked.connect(self.sujest_expand)
        self.sujest_colaps_btn.clicked.connect(self.sujest_colaps)
        self.title_bar.txt_input.returnPressed.connect(self.search_switch)
        self.title_bar.serch_btn.clicked.connect(self.search_switch)
        self.lst_w.itemClicked.connect(self.lst_item_click)
        self.dock_expand_btn.clicked.connect(self.dock_expand)
        self.about_btn.clicked.connect(self.about_d)
        self.setting_btn.clicked.connect(self.opt_d)
        self.key_btn.clicked.connect(self.key_d)

        self.index_btn.clicked.connect(self.index_d)
        self.title_bar.speaker_btn.clicked.connect(self.voice)
        self.radio_btn2.clicked.connect(self.lang_change)
        self.opt_dialog.btn1.clicked.connect(self.real_time_dic)
        self.opt_dialog.btn2.clicked.connect(self.always_onthe_top)
        self.opt_dialog.btn3.clicked.connect(self.open_at_start)
        self.opt_dialog.btn4.clicked.connect(self.widget_hide)
        self.opt_dialog.ok_btn.clicked.connect(self.save_data)
        self.baloon_w_timer.timeout.connect(self.baloon_timer_cnt)
        self.title_bar.tray_btn.clicked.connect(self.tray_event)
        self.tray_icon.activated.connect(self.tray_restore)
        self.option_btn.clicked.connect(self.auto_search)
        self.title_bar.maxmize_btn.clicked.connect(self.mini_mod_switch)
        self.mini_mod_title.txt_input.returnPressed.connect(self.minimod_search_switch)
        self.mini_mod_title.speaker_btn.clicked.connect(self.minimod_search_switch)
        self.mini_mod.mini_mod_list.itemClicked.connect(self.lst_click)
        self.mini_mod_title.mini_mod_lang_change.clicked.connect(self.mini_mod_ln_change)

        self.mini_mod_title_timer.timeout.connect(self.mini_mod_titleTimer_cnt)
        self.mini_mod_title.tray_btn.clicked.connect(self.minimize)
        self.mini_mod_title.maxmize_btn.clicked.connect(self.mod_switch)
        self.mini_mod_title.close_btn.clicked.connect(self.close_w)
        self.option_btn1.clicked.connect(self.sujest_type_switch)

        self.sujest_list.itemClicked.connect(self.sujjest_item_click)
        self.history_box.itemDoubleClicked.connect(self.history_box_item_click)
        self.center()

    def mini_mod_ln_change(self):
        global lang_change


        if lang_change == False:
            lang_change = True
            main.mini_mod_title.txt_input.clear()
            main.mini_mod.mini_mod_list.clear()
        else:
            lang_change = False
            main.mini_mod_title.txt_input.clear()
            main.mini_mod.mini_mod_list.clear()


        if lang_change == True:

            main.mini_mod_title.mini_mod_lang_change.setText("SI")


        else:

            main.mini_mod_title.mini_mod_lang_change.setText("EN")

    def lst_click(self):

        global lang_change

        if main.mini_mod.mini_mod_list.item:


            lst_word = str(main.mini_mod.mini_mod_list.currentItem().text()).encode("utf-8").decode("utf-8")

            try:
                split_lst_word = lst_word.split(". ")[1]

                self.mini_mod_ln_change()
                main.mini_mod_title.txt_input.setText(split_lst_word)


            except IndexError:

                self.mini_mod_ln_change()
                main.mini_mod_title.txt_input.setText(lst_word)

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())




    def history_box_item_click(self):
        global lang_change

        english_list = ["a","b","c","d","e","f","g","h","i","j","k","l","m",
                        "n","o","p","q","r","s","t","u","v","w","x","y","z",
                        "A","B","C","D","E","F","G","H","I","J","K","L","M",
                        "N","O","P","Q","R","S","T","U","V","W","X","Y","Z"]
        if self.history_box.item:

            history_item = str(self.history_box.currentItem().text()).encode("utf-8").decode("utf-8")

            for letters in history_item:

                if letters in english_list:

                    lang_change = False
                    self.lang_change_apearance()
                    self.title_bar.txt_input.setText(history_item)


                else:


                    lang_change = True
                    self.lang_change_apearance()
                    self.title_bar.txt_input.setText(history_item)




    def sujest_type_switch(self):
        global sujest_type
        global lang_change

        if sujest_type == 1:
            sujest_type = 2

        elif sujest_type == 2:
            sujest_type = 3

        elif sujest_type == 3:
            sujest_type = 4

        elif sujest_type == 4:
            sujest_type = 1


        if sujest_type == 1:
            self.option_btn1.setObjectName("option_btn1")
            self.option_btn1.setText("O")

            self.sujest_list.clear()

        elif sujest_type == 2:

            self.option_btn1.setObjectName("option_btn1_active")
            self.option_btn1.setText("*O")

            self.sujest_list.clear()
            word = str(self.title_bar.txt_input.text()).encode("utf-8").decode("utf-8")
            if word != "":
                data_base = sqlite3.connect("Database/Shashika.ire")
                data_base.text_factory()
                word = word.lower()
                sql_word = "%" + word
                sql_cmd_1 = data_base.execute("""SELECT * FROM Distinct_words WHERE d_english LIKE '%s' """ % sql_word)

                for raw in sql_cmd_1:
                    mean = "|".join(map(str, raw)).split("|")[1].encode("utf-8").decode("utf-8")
                    self.sujest_list.addItem(mean)

        elif sujest_type == 3:

            self.option_btn1.setObjectName("option_btn1_active")
            self.option_btn1.setText("O*")

            self.sujest_list.clear()
            word = str(self.title_bar.txt_input.text()).encode("utf-8").decode("utf-8")
            if word != "":

                data_base = sqlite3.connect("Database/Shashika.ire")
                data_base.text_factory()
                word = word.lower()
                sql_word = word + "%"
                sql_cmd_1 = data_base.execute("""SELECT * FROM Distinct_words WHERE d_english LIKE '%s' """ % sql_word)

                for raw in sql_cmd_1:
                    mean = "|".join(map(str, raw)).split("|")[1].encode("utf-8").decode("utf-8")
                    self.sujest_list.addItem(mean)

        elif sujest_type == 4:

            self.option_btn1.setObjectName("option_btn1_active")
            self.option_btn1.setText("*O*")

            self.sujest_list.clear()
            word = str(self.title_bar.txt_input.text()).encode("utf-8").decode("utf-8")
            if word != "":

                data_base = sqlite3.connect("Database/Shashika.ire")
                data_base.text_factory()
                word = word.lower()
                sql_word = "%" + word + "%"
                sql_cmd_1 = data_base.execute("""SELECT * FROM Distinct_words WHERE d_english LIKE '%s' """ % sql_word)

                for raw in sql_cmd_1:
                    mean = "|".join(map(str, raw)).split("|")[1].encode("utf-8").decode("utf-8")
                    self.sujest_list.addItem(mean)


        if sujest_type == 2 and lang_change == True:

            self.option_btn1.setObjectName("option_btn1_active")
            self.option_btn1.setText("*O")

            self.sujest_list.clear()
            word = str(self.title_bar.txt_input.text()).encode("utf-8").decode("utf-8")
            if word != "":
                data_base = sqlite3.connect("Database/Shashika.ire")
                data_base.text_factory()
                word = word.lower()
                sql_word = "%" + word
                sql_cmd_1 = data_base.execute("""SELECT * FROM Word_list WHERE sinhala LIKE '%s' """ % sql_word)

                for raw in sql_cmd_1:
                    mean = "|".join(map(str, raw)).split("|")[-1].encode("utf-8").decode("utf-8")
                    self.sujest_list.addItem(mean)

        elif sujest_type == 3 and lang_change == True:

            self.option_btn1.setObjectName("option_btn1_active")
            self.option_btn1.setText("O*")

            self.sujest_list.clear()
            word = str(self.title_bar.txt_input.text()).encode("utf-8").decode("utf-8")
            if word != "":

                data_base = sqlite3.connect("Database/Shashika.ire")
                data_base.text_factory()
                word = word.lower()
                sql_word = word + "%"
                sql_cmd_1 = data_base.execute("""SELECT * FROM Word_list WHERE sinhala LIKE '%s' """ % sql_word)

                for raw in sql_cmd_1:
                    mean = "|".join(map(str, raw)).split("|")[-1].encode("utf-8").decode("utf-8")
                    self.sujest_list.addItem(mean)

        elif sujest_type == 4 and lang_change == True:

            self.option_btn1.setObjectName("option_btn1_active")
            self.option_btn1.setText("*O*")

            self.sujest_list.clear()
            word = str(self.title_bar.txt_input.text()).encode("utf-8").decode("utf-8")
            if word != "":

                data_base = sqlite3.connect("Database/Shashika.ire")
                data_base.text_factory()
                word = word.lower()
                sql_word = "%" + word + "%"
                sql_cmd_1 = data_base.execute("""SELECT * FROM Word_list WHERE sinhala LIKE '%s' """ % sql_word)

                for raw in sql_cmd_1:
                    mean = "|".join(map(str, raw)).split("|")[-1].encode("utf-8").decode("utf-8")
                    self.sujest_list.addItem(mean)

        self.setStyleSheet(open(css_pack, "r").read())

    def minimize(self):
        self.mini_mod_title.showMinimized()

    def mod_switch(self):
        global mini_mod_switch
        mini_mod_switch = False

        self.show()
        self.mini_mod_title.close()

    def close_w(self):

        self.mini_mod_title.close()
        main.close()
        main.about_dialog.close()
        main.index_dialog.close()
        main.opt_dialog.close()
        main.key_dialog.close()
        main.baloon_window.close()
        main.mini_mod.close()

    def mini_mod_title_colaps(self):
        global mini_mod_x_pos_title
        global mini_mod_y_pos_title
        global mini_mod_tab_visiable
        global mini_mod_title_timer_cnt
        mini_mod_tab_visiable = True



        main.mini_mod_title.grep_btn.hide()
        main.mini_mod_title.oder_btn.hide()
        main.mini_mod_title.mini_mod_lang_change.hide()
        main.mini_mod_title.speaker_btn.hide()
        main.mini_mod_title.txt_input.hide()
        main.mini_mod_title.serch_btn.hide()
        main.mini_mod_title.span_lbl.hide()
        main.mini_mod_title.setFixedSize(50, 45)
        main.mini_mod_title.horizontalLayoutWidget.setGeometry(QtCore.QRect(0, 0, 50, 45))

        x_pos = mini_mod_x_pos  + 293
        y_pos = mini_mod_y_pos - 25

        main.mini_mod_title.move(x_pos, y_pos)


        main.mini_mod.hide()

        mini_mod_title_timer_cnt = 0
        self.mini_mod_title_timer.stop()
        self.mini_mod_title.setWindowOpacity(1)

    def mini_mod_titleTimer_cnt(self):

        global mini_mod_title_timer_cnt, mini_mod_tab_visiable
        mini_mod_title_timer_cnt += 1

        if mini_mod_tab_visiable == True:
            self.mini_mod_title_timer.stop()
        else:


            if mini_mod_title_timer_cnt == 0 or 1:
                main.mini_mod_title.setWindowOpacity(0.8)

            if mini_mod_title_timer_cnt == 2:

                self.mini_mod_title_colaps()

    def minimod_search_switch(self):
        global lang_change

        if lang_change == False:

            self.minimod_e_search()

        else:
            self.minimod_s_search()

    def minimod_s_search(self):
        global mini_mod_x_pos
        global mini_mod_y_pos

        self.mini_mod.mini_mod_list.clear()
        db = sqlite3.connect("Database/Shashika.ire")
        db.text_factory()
        wrd = str(self.mini_mod_title.txt_input.text()).encode("utf-8").decode("utf-8")
        wrd = wrd.lower()
        word_count = 0

        sec = db
        line_x = sec.execute("""SELECT * FROM Word_list """)



        if wrd == "":
            pass

        else:
            for raw in line_x:
                if wrd in raw:
                    word_count += 1

                    w_type = "|".join(map(str, raw)).split("|")[1].encode("utf-8").decode("utf-8")
                    mean = "|".join(map(str, raw)).split("|")[1 + 1].encode("utf-8").decode("utf-8")

                    output = w_type + " " + mean


                    self.mini_mod.mini_mod_list.addItem(output)



            self.mini_mod.move(mini_mod_x_pos, mini_mod_y_pos)
            self.mini_mod.show()

    def minimod_e_search(self):
        global mini_mod_x_pos
        global mini_mod_y_pos

        self.mini_mod.mini_mod_list.clear()
        db = sqlite3.connect("Database/Shashika.ire")
        db.text_factory()
        wrd = str(self.mini_mod_title.txt_input.text()).encode("utf-8").decode("utf-8")
        wrd = wrd.lower()
        word_count = 0

        sec = db
        line_x = sec.execute("""SELECT * FROM Word_list """)


        if wrd == "":
            pass

        else:
            for raw in line_x:
                if wrd in raw:
                    word_count += 1

                    w_type = "|".join(map(str, raw)).split("|")[1].encode("utf-8").decode("utf-8")
                    mean = "|".join(map(str, raw)).split("|")[-1].encode("utf-8").decode("utf-8")

                    output = w_type + " " + mean


                    self.mini_mod.mini_mod_list.addItem(output)


            self.mini_mod.move(mini_mod_x_pos, mini_mod_y_pos)
            self.mini_mod.show()



    def mini_mod_switch(self):
        global mini_mod_switch
        global lang_change

        lang_change = False
        mini_mod_switch = True

        self.mini_mod_title.show()
        self.close()
        self.index_dialog.close()
        self.key_dialog.close()
        self.opt_dialog.close()
        self.about_dialog.close()

    def auto_search(self):
        global CBListner
        global real_time_dic
        global auto_search

        if auto_search == False:
            auto_search = True
            CBListner = True
        elif auto_search == True and real_time_dic == True:
            auto_search = False
        elif auto_search == True and real_time_dic == False:
            auto_search =False
            CBListner = False


        if auto_search == False:
            self.option_btn.setObjectName("option_btn")

        else:
            self.option_btn.setObjectName("option_btn_active")

        self.setStyleSheet(open(css_pack, "r").read())

    def tray_restore(self):
        global tray_icon_visiable

        if QtWidgets.QSystemTrayIcon.DoubleClick:
            tray_icon_visiable = False

            self.tray_icon.hide()
            self.show()
            self.showNormal()

    def tray_event(self):
        global tray_icon_visiable
        tray_icon_visiable = True
        self.showMinimized()

        self.hide()
        self.tray_icon.show()

    def lang_change(self):
        global lang_change
        self.title_bar.txt_input.clear()
        self.lst_w.clear()
        self.sujest_list.clear()

        if lang_change == False:
            lang_change = True

        else:
            lang_change = False

        self.lang_change_apearance()

    def lang_change_apearance(self):
        global lang_change


        if lang_change == True:

            self.radio_btn2.setObjectName("radio_btn2_clicked")
            self.switch_lbl_si.setObjectName("switch_lbl_si_active")
            self.switch_lbl_eng.setObjectName("switch_lbl_eng")
            self.setStyleSheet(open(css_pack, "r").read())


        else:

            self.radio_btn2.setObjectName("radio_btn2")
            self.switch_lbl_eng.setObjectName("switch_lbl_eng_active")
            self.switch_lbl_si.setObjectName("switch_lbl_si")
            self.setStyleSheet(open(css_pack, "r").read())


    def baloon_timer_cnt(self):
        global timer_cnt
        global tray_icon_visiable
        timer_cnt += 1

        if timer_cnt == 1 or 0:
            self.baloon_window.setWindowOpacity(0.8)

        elif timer_cnt == 2 and tray_icon_visiable == False:
            self.baloon_window.close()

        elif timer_cnt == 2 and tray_icon_visiable == True:
            self.baloon_window.hide()

    def save_data(self):
        global option_d_show, open_at_startup
        global CBListner, main_window_flag
        global real_time_dic, widget_auto_hide

        setting_file = open("meta/settings.ire", "w+")
        setting_file.write("CBListner" + "|" + str(CBListner) + "\n")
        setting_file.write("real_time_dic" + "|" + str(real_time_dic) + "\n")
        setting_file.write("alwaysonthetop" + "|" + str(alwaysonthetop) + "\n")
        setting_file.write("widget_auto_hide" + "|" + str(widget_auto_hide) + "\n")
        setting_file.write("widget_auto_hide" + "|" + str(widget_auto_hide) + "\n")
        setting_file.write("open_at_startup" + "|" + str(open_at_startup) + "\n")
        setting_file.close()

        self.opt_dialog.close()
        option_d_show = False
        self.setWindowOpacity(1)

    def load_settings(self):
        global CBListner, main_window_flag
        global real_time_dic, alwaysonthetop
        global widget_auto_hide, mini_mod_title_timer_timeout
        global open_at_startup

        dic = {}
        setting_file = open("meta/settings.ire", "r")

        for lines in setting_file:

            ver = lines.split("|")[0]
            val = lines.split("|")[1]
            #hex_val = val.encode("hex")
            #bool_val = hex_val.replace("0a", "")
            #val = bool_val.decode("hex")
            if val == "False\n":

                val = bool(0)
            elif val == "True\n":

                val = bool(1)

            dic[ver] = val


        CBListner = dic["CBListner"]
        real_time_dic = dic["real_time_dic"]
        alwaysonthetop = dic["alwaysonthetop"]
        widget_auto_hide = dic["widget_auto_hide"]
        open_at_startup = dic["open_at_startup"]
        self.real_time_dic_apearnce()

        if alwaysonthetop == True:
            self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        else:
            self.setWindowFlags(Qt.FramelessWindowHint)

    def open_at_start(self):
        global open_at_startup

        if open_at_startup == False:
            open_at_startup = True
        else:
            open_at_startup = False

        self.real_time_dic_apearnce()

        try:

            if open_at_startup == True:
                key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Run", 0,
                                     winreg.KEY_SET_VALUE)

                winreg.SetValueEx(key, "lotus", 0, winreg.REG_SZ,
                                  r"C:\Program Files\Lotus Dictionary\lotus.exe")

                key.Close()

            else:
                try:
                    key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Run", 0,
                                         winreg.KEY_SET_VALUE)

                    winreg.DeleteValue(key, "lotus")

                    key.Close()

                except:

                    pass

        except:

            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Error")
            msg.setInformativeText("You don`n have access to Registry")
            msg.setWindowTitle("Error")
            msg.exec_()


    def widget_hide(self):
        global widget_auto_hide
        global mini_mod_title_timer_timeout

        if widget_auto_hide == False:
            widget_auto_hide = True
        else:
            widget_auto_hide = False

        self.real_time_dic_apearnce()

        if widget_auto_hide == False:
            mini_mod_title_timer_timeout = 8000
        else:
            mini_mod_title_timer_timeout = 800000

    def always_onthe_top(self):
        global alwaysonthetop, main_window_flag

        if alwaysonthetop == False:
            alwaysonthetop = True
        else:
            alwaysonthetop = False

        self.real_time_dic_apearnce()

        if alwaysonthetop == True:
            self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
            self.show()
        else:
            self.setWindowFlags(Qt.FramelessWindowHint)
            self.show()


    def real_time_dic(self):
        global real_time_dic
        global CBListner
        global auto_search

        if real_time_dic == False:
            real_time_dic = True
            CBListner = True
        elif real_time_dic == True and auto_search == True:
            real_time_dic = False
            #CBListner = False
        elif real_time_dic == True and auto_search == False:
            real_time_dic = False
            CBListner = False

        self.real_time_dic_apearnce()

    def real_time_dic_apearnce(self):
        global real_time_dic
        global CBListner
        global alwaysonthetop, open_at_startup

        if real_time_dic == False:
            self.opt_dialog.btn1.setObjectName("btn1")
            self.opt_dialog.line1.setObjectName("line1")

        else:
            self.opt_dialog.btn1.setObjectName("btn1_active")
            self.opt_dialog.line1.setObjectName("line1_active")


        if alwaysonthetop == False:
            self.opt_dialog.btn2.setObjectName("btn2")
            self.opt_dialog.line2.setObjectName("line2")
        else:
            self.opt_dialog.btn2.setObjectName("btn2_active")
            self.opt_dialog.line2.setObjectName("line2_active")

        if widget_auto_hide == False:
            self.opt_dialog.btn4.setObjectName("btn2")
            self.opt_dialog.line4.setObjectName("line2")
        else:
            self.opt_dialog.btn4.setObjectName("btn2_active")
            self.opt_dialog.line4.setObjectName("line2_active")

        if open_at_startup == False:
            self.opt_dialog.btn3.setObjectName("btn3")
            self.opt_dialog.line3.setObjectName("line3")
        else:
            self.opt_dialog.btn3.setObjectName("btn3_active")
            self.opt_dialog.line3.setObjectName("line3_active")

        self.opt_dialog.setStyleSheet(open(css_pack, "r").read())


    def baloon_w_active(self):
        global baloon_w_show

        if baloon_w_show == False:

            baloon_w_show = True
        else:
            baloon_w_show = False

        if baloon_w_show == True:

            self.baloon_window.show()
        else:
            self.baloon_window.close()

    def clp_board_active(self):
        global CBListner


        if CBListner == False:
            CBListner = True
        else:
            CBListner = False


    def mousePressEvent(self, event):

        if event.button() == Qt.LeftButton:
            main.moving = True
            main.offset = event.pos()


    def mouseMoveEvent(self, event):

        if main.moving:
            main.move(event.globalPos() - main.offset)

    def mouseReleaseEvent(self, event):


     main.moving = False


    def voice(self):
        global mini_mod_switch

        voice_txt = self.title_bar.txt_input.text()

        if voice_txt == "":
            self.stats_lbl.setText("Insert a word first!")
        else:
            voice_engine = Dispatch("SAPI.SpVoice")
            voice_engine.Speak(voice_txt)

    def key_d(self):
        global key_d_show
        global ocr_d_show
        global option_d_show
        global about_d_show
        global index_d_show

        if key_d_show == False:
            key_d_show = True
        else:
            key_d_show = False


        if key_d_show == True:
            self.key_dialog.title_bar.title_lbl.setText("Keyboard")
            self.key_dialog.title_bar.icon_button.setObjectName("keyboard_w_active")
            self.key_dialog.title_bar.icon_button.setStyleSheet(open("theme/dark_theme/dark.qss", "r").read())

            self.key_dialog.show()
            ocr_d_show = False
            self.ocr_dialog.close()
            option_d_show = False
            self.opt_dialog.close()
            about_d_show = False
            self.about_dialog.close()
            self.setWindowOpacity(0.9)
            self.index_dialog.close()
            index_d_show = False
        else:
            self.key_dialog.close()
            self.setWindowOpacity(1)

    def ocr_d(self):
        global ocr_d_show
        global key_d_show
        global option_d_show
        global about_d_show
        global index_d_show

        if ocr_d_show == False:
            ocr_d_show = True
        else:
            ocr_d_show = False


        if ocr_d_show == True:
            self.ocr_dialog.title_bar.title_lbl.setText("OCR")
            self.ocr_dialog.title_bar.icon_button.setObjectName("ocr_w_active")
            self.ocr_dialog.title_bar.icon_button.setStyleSheet(open(css_pack, "r").read())

            self.ocr_dialog.show()
            self.setWindowOpacity(0.9)
            key_d_show = False
            self.key_dialog.close()
            option_d_show = False
            self.opt_dialog.close()
            about_d_show = False
            self.about_dialog.close()
            self.index_dialog.close()
            index_d_show = False
        else:
            self.ocr_dialog.close()
            self.setWindowOpacity(1)

    def opt_d(self):
        global option_d_show
        global ocr_d_show
        global key_d_show
        global about_d_show
        global index_d_show

        if option_d_show == False:
            option_d_show = True
        else:
            option_d_show = False


        if option_d_show == True:
            self.opt_dialog.title_bar.title_lbl.setText("Settings")
            self.opt_dialog.title_bar.icon_button.setObjectName("settings_w_active")
            self.opt_dialog.title_bar.icon_button.setStyleSheet(open(css_pack, "r").read())

            self.opt_dialog.show()
            key_d_show = False
            self.key_dialog.close()
            about_d_show = False
            self.about_dialog.close()
            ocr_d_show = False
            self.ocr_dialog.close()
            self.index_dialog.close()
            index_d_show = False
            self.setWindowOpacity(0.9)
        else:
            self.opt_dialog.close()
            self.setWindowOpacity(1)

    def about_d(self):
        global about_d_show
        global option_d_show
        global ocr_d_show
        global key_d_show
        global index_d_show

        if about_d_show == False:
            about_d_show = True

        else:
            about_d_show = False


        if about_d_show == True:
            self.about_dialog.title_bar.title_lbl.setText("About")
            self.about_dialog.title_bar.icon_button.setObjectName("about_w_active")
            self.about_dialog.title_bar.icon_button.setStyleSheet(open(css_pack, "r").read())

            self.about_dialog.show()
            self.setWindowOpacity(0.9)
            key_d_show = False
            self.key_dialog.close()
            ocr_d_show = False
            self.ocr_dialog.close()
            option_d_show = False
            self.opt_dialog.close()
            self.index_dialog.close()
            index_d_show = False
        else:
            self.about_dialog.close()
            self.setWindowOpacity(1)

    def index_d(self):

        global ocr_d_show
        global key_d_show
        global option_d_show
        global about_d_show
        global index_d_show

        if index_d_show == False:
            index_d_show = True
        else:
            index_d_show = False

        if index_d_show == True:
            self.index_dialog.title_bar.title_lbl.setText("Index")
            self.index_dialog.title_bar.icon_button.setObjectName("index_w_active")
            self.index_dialog.title_bar.icon_button.setStyleSheet(open(css_pack, "r").read())

            self.index_dialog.title_bar.index_search.setVisible(True)
            self.index_dialog.title_bar.index_line.setVisible(True)


            self.index_dialog.show()
            self.setWindowOpacity(0.9)
            key_d_show = False
            self.key_dialog.close()
            option_d_show = False
            self.opt_dialog.close()
            about_d_show = False
            ocr_d_show = False
            self.about_dialog.close()
            self.ocr_dialog.close()
        else:
            self.index_dialog.close()
            self.setWindowOpacity(1)


    def dock_expand(self):

        global dock_expand

        if dock_expand == False:

            self.dock_expand_btn.setObjectName("dock_expand_btn_active")
            self.dock_expand_btn.setStyleSheet(open(css_pack, "r").read())

            dock_expand = True

        else:
            self.dock_expand_btn.setObjectName("dock_expand_btn")
            self.dock_expand_btn.setStyleSheet(open(css_pack, "r").read())
            dock_expand = False


        if dock_expand == True:
            self.dock_frame.setVisible(True)

        else:

            self.dock_frame.setVisible(False)

    def sujest_expand(self):

        self.setFixedSize(751, 463)
        self.title_bar.txt_input.setMaximumWidth(215)
        self.title_bar.span_lbl.setMaximumWidth(550)
        self.sujest_expand_btn.hide()
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(0, 0, 751, 50))
        self.dock_expand_btn.setVisible(True)

    def sujest_colaps(self):

        self.setFixedSize(344, 463)
        self.title_bar.span_lbl.setMaximumWidth(5)
        self.title_bar.txt_input.setMaximumWidth(180)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(0, 0, 344, 50))
        self.sujest_expand_btn.show()
        self.dock_expand_btn.setVisible(False)
        self.dock_frame.setVisible(False)

    def sinhala_search(self):
        global sujest_type

        self.lst_w.clear()
        data_base = sqlite3.connect("Database/Shashika.ire")
        data_base.text_factory()
        word = str(self.title_bar.txt_input.text()).encode("utf-8").decode("utf-8")
        word = word.lower()
        word_count = 0

        sql_cmd = data_base.execute("""SELECT * FROM Word_list """)


        if word == "":
            self.stats_lbl.setText("Insert a word frist!")
        else:
            for raw in sql_cmd:
                if word in raw:
                    word_count += 1

                    w_type = "|".join(map(str, raw)).split("|")[1].encode("utf-8").decode("utf-8")
                    mean = "|".join(map(str, raw)).split("|")[1+1].encode("utf-8").decode("utf-8")

                    output = w_type + " " + mean

                    self.lst_w.addItem(output)

            self.stats_lbl.setText("Words found: " + str(word_count))

        if sujest_type == 2:

            self.sujest_list.clear()
            sql_word = "%" + word
            sql_cmd_1 = data_base.execute("""SELECT * FROM Word_list WHERE sinhala LIKE '%s' """ % sql_word)

            for raw in sql_cmd_1:
                mean = "|".join(map(str, raw)).split("|")[-1].encode("utf-8").decode("utf-8")
                self.sujest_list.addItem(mean)

        elif sujest_type == 3:

            self.sujest_list.clear()
            sql_word = word + "%"
            sql_cmd_1 = data_base.execute("""SELECT * FROM Word_list WHERE sinhala LIKE '%s' """ % sql_word)

            for raw in sql_cmd_1:
                mean = "|".join(map(str, raw)).split("|")[-1].encode("utf-8").decode("utf-8")
                self.sujest_list.addItem(mean)

        elif sujest_type == 4:

            self.sujest_list.clear()
            sql_word = "%" + word + "%"
            sql_cmd_1 = data_base.execute("""SELECT * FROM Word_list WHERE sinhala LIKE '%s' """ % sql_word)

            for raw in sql_cmd_1:
                mean = "|".join(map(str, raw)).split("|")[-1].encode("utf-8").decode("utf-8")
                self.sujest_list.addItem(mean)

    def english_search(self):
        global sujest_type

        self.lst_w.clear()
        data_base = sqlite3.connect("Database/Shashika.ire")
        data_base.text_factory()
        word = str(self.title_bar.txt_input.text()).encode("utf-8").decode("utf-8")
        word = word.lower()
        word_count = 0

        sql_cmd = data_base.execute("""SELECT * FROM Word_list """)

        if word == "":
            self.stats_lbl.setText("Insert a word frist!")
        else:
            for raw in sql_cmd:
                if word in raw:
                    word_count += 1

                    w_type = "|".join(map(str, raw)).split("|")[1].encode("utf-8").decode("utf-8")
                    mean = "|".join(map(str, raw)).split("|")[-1].encode("utf-8").decode("utf-8")

                    output = w_type + " " + mean

                    self.lst_w.addItem(output)

            self.stats_lbl.setText("Words found: " + str(word_count))

        if sujest_type == 2:

            self.sujest_list.clear()
            sql_word = "%" + word
            sql_cmd_1 = data_base.execute("""SELECT * FROM Distinct_words WHERE d_english LIKE '%s' """ % sql_word)

            for raw in sql_cmd_1:
                mean = "|".join(map(str, raw)).split("|")[1].encode("utf-8").decode("utf-8")
                self.sujest_list.addItem(mean)

        elif sujest_type == 3:

            self.sujest_list.clear()
            sql_word = word + "%"
            sql_cmd_1 = data_base.execute("""SELECT * FROM Distinct_words WHERE d_english LIKE '%s' """ % sql_word)

            for raw in sql_cmd_1:
                mean = "|".join(map(str, raw)).split("|")[1].encode("utf-8").decode("utf-8")
                self.sujest_list.addItem(mean)

        elif sujest_type == 4:

            self.sujest_list.clear()
            sql_word = "%" + word + "%"
            sql_cmd_1 = data_base.execute("""SELECT * FROM Distinct_words WHERE d_english LIKE '%s' """ % sql_word)

            for raw in sql_cmd_1:
                mean = "|".join(map(str, raw)).split("|")[1].encode("utf-8").decode("utf-8")
                self.sujest_list.addItem(mean)

    def real_time_english_search(self):
        global mouse_pos_x
        global mouse_pos_y


        self.baloon_window.txt_area.clear()
        self.baloon_window.hide()
        db = sqlite3.connect("Database/Shashika.ire")
        db.text_factory()
        wrd = str(self.baloon_title.baloon_lbl.text()).encode("utf-8").decode("utf-8")
        self.baloon_window.title_bar.baloon_lbl.setText(wrd)
        wrd = wrd.lower()
        word_count = 0

        sec = db
        line_x =sec.execute("""SELECT * FROM Word_list """)


        if wrd == "":
            self.baloon_window.txt_area.setPlainText("No word selected !")
        else:
            for raw in line_x:
                if wrd in raw:
                    word_count += 1

                    w_type = "|".join(map(str, raw)).split("|")[1].encode("utf-8").decode("utf-8")
                    mean = "|".join(map(str, raw)).split("|")[-1].encode("utf-8").decode("utf-8")

                    output = w_type + " " + mean
                    print(output)

                    self.baloon_window.txt_area.appendPlainText(output)

            if word_count == 0:
                self.baloon_window.txt_area.setPlainText("No words Found in DB !")

    def real_time_sinhala_search(self):
        global mouse_pos_x
        global mouse_pos_y



        self.baloon_window.txt_area.clear()
        self.baloon_window.hide()
        db = sqlite3.connect("Database/Shashika.ire")
        db.text_factory()
        wrd = str(self.baloon_title.baloon_lbl.text()).encode("utf-8").decode("utf-8")
        self.baloon_window.title_bar.baloon_lbl.setText(wrd)

        word_count = 0

        sec = db
        line_x =sec.execute("""SELECT * FROM Word_list """)



        if wrd == "":
            self.baloon_window.txt_area.setPlainText("No word selected !")
        else:
            for raw in line_x:
                if wrd in raw:
                    word_count += 1

                    w_type = "|".join(map(str, raw)).split("|")[1].encode("utf-8").decode("utf-8")
                    mean = "|".join(map(str, raw)).split("|")[1 + 1].encode("utf-8").decode("utf-8")

                    output = w_type + " " + mean

                    self.baloon_window.txt_area.appendPlainText(output)

            if word_count == 0:
                self.baloon_window.txt_area.setPlainText("No words Found in DB !")

    def doul_sinhala_search(self):

        self.lst_w.clear()
        self.baloon_window.txt_area.clear()
        db = sqlite3.connect("Database/Shashika.ire")
        db.text_factory()
        wrd = str(self.title_bar.txt_input.text()).encode("utf-8").decode("utf-8")
        self.baloon_window.title_bar.baloon_lbl.setText(wrd)
        wrd = wrd.lower()
        word_count = 0

        sec = db
        line_x = sec.execute("""SELECT * FROM Word_list """)

        if wrd == "":
            self.stats_lbl.setText("Insert a word frist!")
        else:
            for raw in line_x:
                if wrd in raw:
                    word_count += 1

                    w_type = "|".join(map(str, raw)).split("|")[1].encode("utf-8").decode("utf-8")
                    mean = "|".join(map(str, raw)).split("|")[1 + 1].encode("utf-8").decode("utf-8")

                    output = w_type + " " + mean


                    self.lst_w.addItem(output)
                    self.baloon_window.txt_area.appendPlainText(output)

            self.stats_lbl.setText("Words found: " + str(word_count))
            if word_count == 0:
                self.baloon_window.txt_area.setPlainText("No words Found in DB !")



    def doul_search(self):

        self.lst_w.clear()
        self.baloon_window.txt_area.clear()
        db = sqlite3.connect("Database/Shashika.ire")
        db.text_factory()
        wrd = str(self.title_bar.txt_input.text()).encode("utf-8").decode("utf-8")
        self.baloon_window.title_bar.baloon_lbl.setText(wrd)
        wrd = wrd.lower()
        word_count = 0

        sec = db
        line_x = sec.execute("""SELECT * FROM Word_list """)


        if wrd == "":
            self.stats_lbl.setText("Insert a word frist!")
        else:
            for raw in line_x:
                if wrd in raw:
                    word_count += 1

                    w_type = "|".join(map(str, raw)).split("|")[1].encode("utf-8").decode("utf-8")
                    mean = "|".join(map(str, raw)).split("|")[-1].encode("utf-8").decode("utf-8")

                    output = w_type + " " + mean


                    self.lst_w.addItem(output)
                    self.baloon_window.txt_area.appendPlainText(output)

            self.stats_lbl.setText("Words found: " + str(word_count))
            if word_count == 0:
                self.baloon_window.txt_area.setPlainText("No words Found in DB !")



    def search_switch(self):
        global lang_change

        if lang_change == True:

            main.sinhala_search()

        else:
            main.english_search()

    def lst_item_click(self):
        global lang_change



        if self.lst_w.item:



            self.history_box.addItem(str(self.title_bar.txt_input.text()).encode("utf-8").decode("utf-8"))

            lst_word = str(self.lst_w.currentItem().text()).encode("utf-8").decode("utf-8")

            try:
                split_lst_word = lst_word.split(". ")[1]

                self.lang_change()
                self.title_bar.txt_input.setText(split_lst_word)
                self.search_switch()

            except IndexError:

                self.lang_change()
                self.title_bar.txt_input.setText(lst_word)
                self.search_switch()





    def sujjest_item_click(self):

        global lang_change

        if self.sujest_list.item:


            lst_word = str(self.sujest_list.currentItem().text()).encode("utf-8").decode("utf-8")


            self.title_bar.txt_input.setText(lst_word)
            self.search_switch()



    def dataReciver(self, clipdata):
        global real_time_dic
        global auto_search
        global lang_change

        english_list = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m",
                        "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z",
                        "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M",
                        "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]

        for letters in clipdata:

            if letters in english_list:
                lang_change = False
                self.lang_change_apearance()

            else:
                lang_change = True
                self.lang_change_apearance()


        if real_time_dic == True and auto_search == False and lang_change == False:

            self.baloon_title.baloon_lbl.setText(clipdata)
            #self.title_bar.txt_input.setText(clipdata)
            #self.search()
            self.real_time_english_search()
            mouse_pos = pyautogui.position()


            mouse_pos_x = mouse_pos.x + 10
            mouse_pos_y = mouse_pos.y + 10

            self.baloon_window.move(mouse_pos_x, mouse_pos_y)
            self.baloon_window.show()

        elif real_time_dic and auto_search == True and lang_change == False:

            self.baloon_title.baloon_lbl.setText(clipdata)
            #self.real_time_search()
            self.title_bar.txt_input.setText(clipdata)
            self.doul_search()
            mouse_pos = pyautogui.position()

            mouse_pos_x = mouse_pos.x + 10
            mouse_pos_y = mouse_pos.y + 10

            self.baloon_window.move(mouse_pos_x, mouse_pos_y)
            self.baloon_window.show()

        elif real_time_dic and auto_search == True and lang_change == True:

            self.baloon_title.baloon_lbl.setText(clipdata)
            #self.real_time_search()
            self.title_bar.txt_input.setText(clipdata)
            self.doul_sinhala_search()
            mouse_pos = pyautogui.position()


            mouse_pos_x = mouse_pos.x + 10
            mouse_pos_y = mouse_pos.y + 10

            self.baloon_window.move(mouse_pos_x, mouse_pos_y)
            self.baloon_window.show()

        if real_time_dic == True and auto_search == False and lang_change == True:


            self.baloon_title.baloon_lbl.setText(clipdata)
            self.real_time_sinhala_search()
            mouse_pos = pyautogui.position()


            mouse_pos_x = mouse_pos.x + 10
            mouse_pos_y = mouse_pos.y + 10

            self.baloon_window.move(mouse_pos_x, mouse_pos_y)
            self.baloon_window.show()

        elif auto_search == True and real_time_dic == False and lang_change == False:

            self.baloon_title.baloon_lbl.setText(clipdata)

            self.title_bar.txt_input.setText(clipdata)
            self.doul_search()
            mouse_pos = pyautogui.position()


            mouse_pos_x = mouse_pos.x + 10
            mouse_pos_y = mouse_pos.y + 10

            self.baloon_window.move(mouse_pos_x, mouse_pos_y)
            self.baloon_window.show()

        elif auto_search == True and real_time_dic == False and lang_change == True:


            self.baloon_title.baloon_lbl.setText(clipdata)
            #self.real_time_search()
            self.title_bar.txt_input.setText(clipdata)
            self.doul_sinhala_search()
            mouse_pos = pyautogui.position()


            mouse_pos_x = mouse_pos.x + 10
            mouse_pos_y = mouse_pos.y + 10

            self.baloon_window.move(mouse_pos_x, mouse_pos_y)
            self.baloon_window.show()

class ClipBoardListner(QObject):
    def __init__(self, target):
        QObject.__init__(self)
        self.target = target

    @pyqtSlot()
    def changedSlot(self):
        global CBListner
        if CBListner:
            clipdata = QApplication.clipboard().text()
            self.target.dataReciver(clipdata)


if __name__ == "__main__":

    app = QtWidgets.QApplication(sys.argv)

    SplashThread = SplashThread()

    splashScreen = QSplashScreen()
    splashPixmap = QPixmap("meta/splash/splash_0.png")
    splashScreen.setPixmap(splashPixmap)
    splashScreen.show()


    main = Ui_Main()

    dataListner = ClipBoardListner(main)
    QApplication.clipboard().dataChanged.connect(dataListner.changedSlot)
    #main.show()


    timer = QTimer()
    timer.setInterval(60)
    timer.setSingleShot(False)
    timer.timeout.connect(updateSplashScreen)
    timer.start()

    SplashThread.mysignal.connect(stopTimer)

    SplashThread.start()

    sys.exit(app.exec_())


