"""
    Rasp2PC - RASP Component
    A program based on socket protocol that uses a Raspberry Pi with touchscreen to control a computer via shortcuts

    Copyright (C) 2020 seepiol

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

import socket
from PyQt5 import QtCore, QtGui, QtWidgets
import sys
import logging
import csv


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(451, 338)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.RASP2PC_label = QtWidgets.QLabel(self.centralwidget)
        self.RASP2PC_label.setGeometry(QtCore.QRect(10, 10, 111, 21))
        font = QtGui.QFont()
        font.setPointSize(18)
        font.setBold(True)
        font.setWeight(75)
        self.RASP2PC_label.setFont(font)
        self.RASP2PC_label.setObjectName("RASP2PC_label")

        self.RASPcomponent_label = QtWidgets.QLabel(self.centralwidget)
        self.RASPcomponent_label.setGeometry(QtCore.QRect(10, 40, 181, 18))
        self.RASPcomponent_label.setObjectName("RASPcomponent_label")

        self.connected_to_label = QtWidgets.QLabel(self.centralwidget)
        self.connected_to_label.setGeometry(QtCore.QRect(10, 70, 101, 18))
        self.connected_to_label.setObjectName("connected_to_label")

        self.pc_info_label = QtWidgets.QLabel(self.centralwidget)
        self.pc_info_label.setGeometry(QtCore.QRect(110, 70, 181, 18))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(75)
        self.pc_info_label.setFont(font)
        self.pc_info_label.setObjectName("pc_info_label")

        # Programs
        self.app_frame = QtWidgets.QFrame(self.centralwidget)
        self.app_frame.setGeometry(QtCore.QRect(10, 100, 211, 221))
        self.app_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.app_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.app_frame.setObjectName("app_frame")

        self.app2_button = QtWidgets.QPushButton(self.app_frame)
        self.app2_button.setGeometry(QtCore.QRect(110, 10, 90, 37))
        self.app2_button.setText("")
        self.app2_button.setObjectName("app2_button")

        self.app1_button = QtWidgets.QPushButton(self.app_frame)
        self.app1_button.setGeometry(QtCore.QRect(10, 10, 90, 37))
        self.app1_button.setText("")
        self.app1_button.setObjectName("app1_button")

        self.app3_button = QtWidgets.QPushButton(self.app_frame)
        self.app3_button.setGeometry(QtCore.QRect(10, 50, 90, 37))
        self.app3_button.setText("")
        self.app3_button.setObjectName("app3_button")

        self.app4_button = QtWidgets.QPushButton(self.app_frame)
        self.app4_button.setGeometry(QtCore.QRect(110, 50, 90, 37))
        self.app4_button.setText("")
        self.app4_button.setObjectName("app4_button")

        self.app5_button = QtWidgets.QPushButton(self.app_frame)
        self.app5_button.setGeometry(QtCore.QRect(10, 90, 90, 37))
        self.app5_button.setText("")
        self.app5_button.setObjectName("app5_button")

        self.app6_button = QtWidgets.QPushButton(self.app_frame)
        self.app6_button.setGeometry(QtCore.QRect(110, 90, 90, 37))
        self.app6_button.setText("")
        self.app6_button.setObjectName("app6_button")

        self.app7_button = QtWidgets.QPushButton(self.app_frame)
        self.app7_button.setGeometry(QtCore.QRect(10, 130, 90, 37))
        self.app7_button.setText("")
        self.app7_button.setObjectName("app7_button")

        self.app8_button = QtWidgets.QPushButton(self.app_frame)
        self.app8_button.setGeometry(QtCore.QRect(110, 130, 90, 37))
        self.app8_button.setText("")
        self.app8_button.setObjectName("app8_button")

        self.app9_button = QtWidgets.QPushButton(self.app_frame)
        self.app9_button.setGeometry(QtCore.QRect(10, 170, 90, 37))
        self.app9_button.setText("")
        self.app9_button.setObjectName("app9_button")

        self.app10_button = QtWidgets.QPushButton(self.app_frame)
        self.app10_button.setGeometry(QtCore.QRect(110, 170, 90, 37))
        self.app10_button.setText("")
        self.app10_button.setObjectName("app10_button")

        # Keyboard
        self.keyboard_frame = QtWidgets.QFrame(self.centralwidget)
        self.keyboard_frame.setGeometry(QtCore.QRect(230, 100, 211, 221))
        self.keyboard_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.keyboard_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.keyboard_frame.setObjectName("keyboard_frame")

        self.short1_button = QtWidgets.QPushButton(self.keyboard_frame)
        self.short1_button.setGeometry(QtCore.QRect(10, 10, 90, 37))
        self.short1_button.setText("")
        self.short1_button.setObjectName("short1_button")

        self.short2_button = QtWidgets.QPushButton(self.keyboard_frame)
        self.short2_button.setGeometry(QtCore.QRect(110, 10, 90, 37))
        self.short2_button.setText("")
        self.short2_button.setObjectName("short2_button")

        self.short3_button = QtWidgets.QPushButton(self.keyboard_frame)
        self.short3_button.setGeometry(QtCore.QRect(10, 50, 90, 37))
        self.short3_button.setText("")
        self.short3_button.setObjectName("short3_button")

        self.short4_button = QtWidgets.QPushButton(self.keyboard_frame)
        self.short4_button.setGeometry(QtCore.QRect(110, 50, 90, 37))
        self.short4_button.setText("")
        self.short4_button.setObjectName("short4_button")

        self.short5_button = QtWidgets.QPushButton(self.keyboard_frame)
        self.short5_button.setGeometry(QtCore.QRect(10, 90, 90, 37))
        self.short5_button.setText("")
        self.short5_button.setObjectName("short5_button")

        self.short6_button = QtWidgets.QPushButton(self.keyboard_frame)
        self.short6_button.setGeometry(QtCore.QRect(110, 90, 90, 37))
        self.short6_button.setText("")
        self.short6_button.setObjectName("short6_button")

        self.short7_button = QtWidgets.QPushButton(self.keyboard_frame)
        self.short7_button.setGeometry(QtCore.QRect(10, 130, 90, 37))
        self.short7_button.setText("")
        self.short7_button.setObjectName("short7_button")

        self.short8_button = QtWidgets.QPushButton(self.keyboard_frame)
        self.short8_button.setGeometry(QtCore.QRect(110, 130, 90, 37))
        self.short8_button.setText("")
        self.short8_button.setObjectName("short8_button")

        self.short9_button = QtWidgets.QPushButton(self.keyboard_frame)
        self.short9_button.setGeometry(QtCore.QRect(10, 170, 90, 37))
        self.short9_button.setText("")
        self.short9_button.setObjectName("short9_button")

        self.short10_button = QtWidgets.QPushButton(self.keyboard_frame)
        self.short10_button.setGeometry(QtCore.QRect(110, 170, 90, 37))
        self.short10_button.setText("")
        self.short10_button.setObjectName("short10_button")

        # Function Connections
        # Apps
        self.app1_button.clicked.connect(self.app1)
        self.app2_button.clicked.connect(self.app2)
        self.app3_button.clicked.connect(self.app3)
        self.app4_button.clicked.connect(self.app4)
        self.app5_button.clicked.connect(self.app5)
        self.app6_button.clicked.connect(self.app6)
        self.app7_button.clicked.connect(self.app7)
        self.app8_button.clicked.connect(self.app8)
        self.app9_button.clicked.connect(self.app9)
        self.app10_button.clicked.connect(self.app10)
        # Keyboard
        self.short1_button.clicked.connect(self.short1)
        self.short2_button.clicked.connect(self.short2)
        self.short3_button.clicked.connect(self.short3)
        self.short4_button.clicked.connect(self.short4)
        self.short5_button.clicked.connect(self.short5)
        self.short6_button.clicked.connect(self.short6)
        self.short7_button.clicked.connect(self.short7)
        self.short8_button.clicked.connect(self.short8)
        self.short9_button.clicked.connect(self.short9)
        self.short10_button.clicked.connect(self.short10)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Rasp2Pc "))
        self.RASP2PC_label.setText(_translate("MainWindow", "RASP2PC"))
        self.RASPcomponent_label.setText(_translate("MainWindow", "RASP Component"))
        self.connected_to_label.setText(_translate("MainWindow", "Connected to:"))
        self.pc_info_label.setText(
            _translate("MainWindow", f"{PC_HOST}:{str(PC_PORT)}")
        )

        # !!!BUTTONS TEXT HERE!!!

        self.app1_button.setText(_translate("MainWindow", "Firefox"))  # app1
        self.app2_button.setText(_translate("MainWindow", "Terminal"))  # app2
        self.app3_button.setText(_translate("MainWindow", "VirtualBox"))  # app3
        self.app4_button.setText(_translate("MainWindow", "Dolphin"))  # app4
        self.app5_button.setText(_translate("MainWindow", "VSCode"))  # app5
        self.app6_button.setText(_translate("MainWindow", "Lock Sys"))  # app6
        self.app7_button.setText(_translate("MainWindow", "Telegram"))  # app7
        self.app8_button.setText(_translate("MainWindow", "Libreoffice"))  # app8
        self.app9_button.setText(_translate("MainWindow", "Thunderbird"))  # app9
        self.app10_button.setText(_translate("MainWindow", "Reboot"))  # app10

        self.short1_button.setText(_translate("MainWindow", "Undo"))  # short1
        self.short2_button.setText(_translate("MainWindow", "Copy"))  # short2
        self.short3_button.setText(_translate("MainWindow", "Cut"))  # short3
        self.short4_button.setText(_translate("MainWindow", "Paste"))  # short4
        self.short5_button.setText(_translate("MainWindow", "Mic"))  # short5
        self.short6_button.setText(_translate("MainWindow", "Webcam"))  # short6
        self.short7_button.setText(_translate("MainWindow", "Fullscreen"))  # short7
        self.short8_button.setText(_translate("MainWindow", "Blank"))  # short8
        self.short9_button.setText(_translate("MainWindow", "Blank"))  # short9
        self.short10_button.setText(_translate("MainWindow", "Blank"))  # short10

    # App launch functions

    # I know that that's not the best way to handle an exception, but it works and it's enough for me

    def app1(self):
        try:
            logging.info("Sending a1 index")
            raspsocket.send("a1".encode())
            response = raspsocket.recv(1024).decode("ascii")  # Recive the response
            print(response)  # Print the response

        except BrokenPipeError:
            print("Connection closed by PC. exiting")
            logging.critical("Connection closed by PC. quitting")
            raspsocket.close()
            exit()

    def app2(self):
        try:
            logging.info("Sending a2 index")
            raspsocket.send("a2".encode())
            response = raspsocket.recv(1024).decode("ascii")  # Recive the response
            print(response)  # Print the response

        except BrokenPipeError:
            print("Connection closed by PC. exiting")
            logging.critical("Connection closed by PC. quitting")
            raspsocket.close()
            exit()

    def app3(self):
        try:
            logging.info("Sending a3 index")
            raspsocket.send("a3".encode())
            response = raspsocket.recv(1024).decode("ascii")  # Recive the response
            print(response)  # Print the response

        except BrokenPipeError:
            print("Connection closed by PC. exiting")
            logging.critical("Connection closed by PC. quitting")
            raspsocket.close()
            exit()

    def app4(self):
        try:
            logging.info("Sending a4 index")
            raspsocket.send("a4".encode())
            response = raspsocket.recv(1024).decode("ascii")  # Recive the response
            print(response)  # Print the response

        except BrokenPipeError:
            print("Connection closed by PC. exiting")
            logging.critical("Connection closed by PC. quitting")
            raspsocket.close()
            exit()

    def app5(self):
        try:
            logging.info("Sending a5 index")
            raspsocket.send("a5".encode())
            response = raspsocket.recv(1024).decode("ascii")  # Recive the response
            print(response)  # Print the response

        except BrokenPipeError:
            print("Connection closed by PC. exiting")
            logging.critical("Connection closed by PC. quitting")
            raspsocket.close()
            exit()

    def app6(self):
        try:
            logging.info("Sending a6 index")
            raspsocket.send("a6".encode())
            response = raspsocket.recv(1024).decode("ascii")  # Recive the response
            print(response)  # Print the response

        except BrokenPipeError:
            print("Connection closed by PC. exiting")
            logging.critical("Connection closed by PC. quitting")
            raspsocket.close()
            exit()

    def app7(self):
        try:
            logging.info("Sending a7 index")
            raspsocket.send("a7".encode())
            response = raspsocket.recv(1024).decode("ascii")  # Recive the response
            print(response)  # Print the response

        except BrokenPipeError:
            print("Connection closed by PC. exiting")
            logging.critical("Connection closed by PC. quitting")
            raspsocket.close()
            exit()

    def app8(self):
        try:
            logging.info("Sending a8 index")
            raspsocket.send("a8".encode())
            response = raspsocket.recv(1024).decode("ascii")  # Recive the response
            print(response)  # Print the response

        except BrokenPipeError:
            print("Connection closed by PC. exiting")
            logging.critical("Connection closed by PC. quitting")
            raspsocket.close()
            exit()

    def app9(self):
        try:
            logging.info("Sending a9 index")
            raspsocket.send("a9".encode())
            response = raspsocket.recv(1024).decode("ascii")  # Recive the response
            print(response)  # Print the response

        except BrokenPipeError:
            print("Connection closed by PC. exiting")
            logging.critical("Connection closed by PC. quitting")
            raspsocket.close()
            exit()

    def app10(self):
        try:
            logging.info("Sending a10 index")
            raspsocket.send("a10".encode())
            response = raspsocket.recv(1024).decode("ascii")  # Recive the response
            print(response)  # Print the response

        except BrokenPipeError:
            print("Connection closed by PC. exiting")
            logging.critical("Connection closed by PC. quitting")
            raspsocket.close()
            exit()

    # Keyboard shortcuts functions
    def short1(self):
        try:
            logging.info("Sending s1 index")
            raspsocket.send("s1".encode())
            response = raspsocket.recv(1024).decode("ascii")  # Recive the response
            print(response)  # Print the response

        except BrokenPipeError:
            print("Connection closed by PC. exiting")
            logging.critical("Connection closed by PC. quitting")
            raspsocket.close()
            exit()

    def short2(self):
        try:
            logging.info("Sending s2 index")
            raspsocket.send("s2".encode())
            response = raspsocket.recv(1024).decode("ascii")  # Recive the response
            print(response)  # Print the response

        except BrokenPipeError:
            print("Connection closed by PC. exiting")
            logging.critical("Connection closed by PC. quitting")
            raspsocket.close()
            exit()

    def short3(self):
        try:
            logging.info("Sending s3 index")
            raspsocket.send("s3".encode())
            response = raspsocket.recv(1024).decode("ascii")  # Recive the response
            print(response)  # Print the response

        except BrokenPipeError:
            print("Connection closed by PC. exiting")
            logging.critical("Connection closed by PC. quitting")
            raspsocket.close()
            exit()

    def short4(self):
        try:
            logging.info("Sending s4 index")
            raspsocket.send("s4".encode())
            response = raspsocket.recv(1024).decode("ascii")  # Recive the response
            print(response)  # Print the response

        except BrokenPipeError:
            print("Connection closed by PC. exiting")
            logging.critical("Connection closed by PC. quitting")
            raspsocket.close()
            exit()

    def short5(self):
        try:
            logging.info("Sending s5 index")
            raspsocket.send("s5".encode())
            response = raspsocket.recv(1024).decode("ascii")  # Recive the response
            print(response)  # Print the response

        except BrokenPipeError:
            print("Connection closed by PC. exiting")
            logging.critical("Connection closed by PC. quitting")
            raspsocket.close()
            exit()

    def short6(self):
        try:
            logging.info("Sending s6 index")
            raspsocket.send("s6".encode())
            response = raspsocket.recv(1024).decode("ascii")  # Recive the response
            print(response)  # Print the response

        except BrokenPipeError:
            print("Connection closed by PC. exiting")
            logging.critical("Connection closed by PC. quitting")
            raspsocket.close()
            exit()

    def short7(self):
        try:
            logging.info("Sending s7 index")
            raspsocket.send("s7".encode())
            response = raspsocket.recv(1024).decode("ascii")  # Recive the response
            print(response)  # Print the response

        except BrokenPipeError:
            print("Connection closed by PC. exiting")
            logging.critical("Connection closed by PC. quitting")
            raspsocket.close()
            exit()

    def short8(self):
        try:
            logging.info("Sending s8 index")
            raspsocket.send("s8".encode())
            response = raspsocket.recv(1024).decode("ascii")  # Recive the response
            print(response)  # Print the response

        except BrokenPipeError:
            print("Connection closed by PC. exiting")
            logging.critical("Connection closed by PC. quitting")
            raspsocket.close()
            exit()

    def short9(self):
        try:
            logging.info("Sending s9 index")
            raspsocket.send("s9".encode())
            response = raspsocket.recv(1024).decode("ascii")  # Recive the response
            print(response)  # Print the response

        except BrokenPipeError:
            print("Connection closed by PC. exiting")
            logging.critical("Connection closed by PC. quitting")
            raspsocket.close()
            exit()

    def short10(self):
        try:
            logging.info("Sending s10 index")
            raspsocket.send("s10".encode())
            response = raspsocket.recv(1024).decode("ascii")  # Recive the response
            print(response)  # Print the response

        except BrokenPipeError:
            print("Connection closed by PC. exiting")
            logging.critical("Connection closed by PC. quitting")
            raspsocket.close()
            exit()


if __name__ == "__main__":

    # Loading configuration file
    with open("rasp.conf", newline="") as conf_file:
        reader = csv.reader(conf_file, delimiter=",")
        for row in reader:
            PC_HOST = row[0]
            PC_PORT = int(row[1])
            break

    # Setting up the logger
    logging.basicConfig(
        filename="rasp.log",
        filemode="w",
        format="%(asctime)s - %(levelname)s - %(message)s",
        level=logging.INFO,
    )

    logging.info("Rasp component started")

    try:
        logging.info("Creating socket...")
        with socket.socket(
            socket.AF_INET, socket.SOCK_STREAM
        ) as raspsocket:  # Create socket object
            # ATTENTION: You have to modify the line 25 with the PC ip address and the port (default:10000)
            logging.info(f"Connecting to {PC_HOST}:{PC_PORT}...")
            raspsocket.connect((PC_HOST, PC_PORT))  # Connect to the PC
            app = QtWidgets.QApplication(sys.argv)
            MainWindow = QtWidgets.QMainWindow()
            ui = Ui_MainWindow()
            ui.setupUi(MainWindow)
            logging.debug("Showing the gui")
            MainWindow.show()

            sys.exit(app.exec_())

    except ConnectionRefusedError as e:
        print("Pc is not reachable. exiting")
        logging.critical(
            f"Pc ({PC_HOST}:{PC_PORT}) is not reachable. ERROR:{e}. Quitting"
        )
        exit()

    except OSError as e:
        print(
            "PC not found. check the ip address and if the pc component is running. Quitting"
        )
        logging.critical(f"pc ({PC_HOST}:{PC_PORT}) not found. ERROR:{e}. Quitting")
        exit()
