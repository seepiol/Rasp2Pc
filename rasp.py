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
from PyQt5.QtWidgets import QMessageBox, QApplication
import sys
import logging
import csv
import argparse
from Crypto.Cipher import AES

###POPUPS FOR ERROR###

# BrokenPipeError Exception popup
def connection_interrupted():
    app = QApplication(sys.argv)
    window = QMessageBox()
    window.setIcon(QMessageBox.Critical)
    window.setWindowTitle("Connection Interrupted")
    window.setText(f"Connection has been interrupted")
    window.setStandardButtons(QMessageBox.Ok)
    window.exec()


# Connection denied popup
def connection_denied(socket, host):
    app = QApplication(sys.argv)
    window = QMessageBox()
    window.setIcon(QMessageBox.Critical)
    window.setWindowTitle("Connection Denied")
    window.setText(f"Connection denied by {host}")
    window.setStandardButtons(QMessageBox.Ok)
    window.exec()
    socket.close()
    exit()


def not_reachable(socket, host):
    app = QApplication(sys.argv)
    window = QMessageBox()
    window.setIcon(QMessageBox.Critical)
    window.setWindowTitle("Not reachable")
    window.setText(f"PC {host} is not reachable")
    window.setStandardButtons(QMessageBox.Ok)
    window.exec()
    socket.close()
    exit()


def not_found(socket, host):
    app = QApplication(sys.argv)
    window = QMessageBox()
    window.setIcon(QMessageBox.Critical)
    window.setWindowTitle("Not found")
    window.setText(
        f"PC not found. check the ip address and if the pc component is running."
    )
    window.setStandardButtons(QMessageBox.Ok)
    window.exec()
    socket.close()
    exit()


def pc_turned_off(socket):
    socket.close()
    app = QApplication(sys.argv)
    window = QMessageBox()
    window.setIcon(QMessageBox.Critical)
    window.setWindowTitle("PC Turned off")
    window.setText(
        f"PC is turning off. Closing the socket and application for prevent errors"
    )
    window.setStandardButtons(QMessageBox.Ok)
    window.exec()
    exit()


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(451, 286)

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.RASPcomponent_label = QtWidgets.QLabel(self.centralwidget)
        self.RASPcomponent_label.setGeometry(QtCore.QRect(10, 10, 181, 18))
        self.RASPcomponent_label.setObjectName("RASPcomponent_label")

        self.connected_to_label = QtWidgets.QLabel(self.centralwidget)
        self.connected_to_label.setGeometry(QtCore.QRect(10, 30, 101, 18))
        self.connected_to_label.setObjectName("connected_to_label")

        self.pc_info_label = QtWidgets.QLabel(self.centralwidget)
        self.pc_info_label.setGeometry(QtCore.QRect(110, 30, 181, 18))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(75)
        self.pc_info_label.setFont(font)
        self.pc_info_label.setText("")
        self.pc_info_label.setObjectName("pc_info_label")

        # System Actions
        self.reboot_icon = QtGui.QIcon()
        self.reboot_icon.addPixmap(QtGui.QPixmap("icons/reboot.png"))
        self.reboot_button = QtWidgets.QPushButton(self.centralwidget)
        self.reboot_button.setGeometry(QtCore.QRect(290, 10, 41, 37))
        self.reboot_button.setIcon(self.reboot_icon)
        self.reboot_button.setToolTip("Reboot the PC")
        self.reboot_button.setObjectName("reboot_button")

        self.lock_icon = QtGui.QIcon()
        self.lock_icon.addPixmap(QtGui.QPixmap("icons/lock.png"))
        self.lock_button = QtWidgets.QPushButton(self.centralwidget)
        self.lock_button.setGeometry(QtCore.QRect(340, 10, 41, 37))
        self.lock_button.setIcon(self.lock_icon)
        self.lock_button.setToolTip("Lock the session")
        self.lock_button.setObjectName("lock_button")

        self.mute_icon = QtGui.QIcon()
        self.mute_icon.addPixmap(QtGui.QPixmap("icons/mute.png"))
        self.mute_button = QtWidgets.QPushButton(self.centralwidget)
        self.mute_button.setGeometry(QtCore.QRect(390, 10, 41, 37))
        self.mute_button.setIcon(self.mute_icon)
        self.mute_button.setToolTip("Mute the PC audio")
        self.mute_button.setObjectName("mute_button")

        # Programs
        self.app_frame = QtWidgets.QFrame(self.centralwidget)
        self.app_frame.setGeometry(QtCore.QRect(10, 50, 211, 221))
        self.app_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.app_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.app_frame.setObjectName("app_frame")

        self.app2_button = QtWidgets.QPushButton(self.app_frame)
        self.app2_button.setGeometry(QtCore.QRect(110, 10, 90, 37))
        self.app2_button.setText("")
        self.app2_button.setObjectName("app2_button")

        self.app1_button = QtWidgets.QPushButton(self.app_frame)
        self.app1_button.setGeometry(QtCore.QRect(10, 10, 90, 37))
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
        self.keyboard_frame.setGeometry(QtCore.QRect(230, 50, 211, 221))
        self.keyboard_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.keyboard_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.keyboard_frame.setObjectName("keyboard_frame")

        self.short1_button = QtWidgets.QPushButton(self.keyboard_frame)
        self.short1_button.setGeometry(QtCore.QRect(10, 10, 90, 37))
        self.short1_button.setText("")
        self.short1_button.setShortcut("")
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
        # System Function
        self.reboot_button.clicked.connect(self.sysf1)
        self.lock_button.clicked.connect(self.sysf2)
        self.mute_button.clicked.connect(self.sysf3)
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
        self.RASPcomponent_label.setText(_translate("MainWindow", "RASP Component"))
        self.connected_to_label.setText(_translate("MainWindow", "Connected to:"))
        self.pc_info_label.setText(
            _translate("MainWindow", f"{PC_HOST}:{str(PC_PORT)}")
        )

        # !!!BUTTONS TEXT HERE!!!

        self.app1_button.setText(_translate("MainWindow", "Firefox"))  # app1
        self.app1_button.setToolTip("app1")

        self.app2_button.setText(_translate("MainWindow", "Terminal"))  # app2
        self.app2_button.setToolTip("app2")

        self.app3_button.setText(_translate("MainWindow", "VirtualBox"))  # app3
        self.app3_button.setToolTip("app3")

        self.app4_button.setText(_translate("MainWindow", "Dolphin"))  # app4
        self.app4_button.setToolTip("app4")

        self.app5_button.setText(_translate("MainWindow", "VSCode"))  # app5
        self.app5_button.setToolTip("app5")

        self.app6_button.setText(_translate("MainWindow", "Store"))  # app6
        self.app6_button.setToolTip("app6")

        self.app7_button.setText(_translate("MainWindow", "Telegram"))  # app7
        self.app7_button.setToolTip("app7")

        self.app8_button.setText(_translate("MainWindow", "Libreoffice"))  # app8
        self.app8_button.setToolTip("app8")

        self.app9_button.setText(_translate("MainWindow", "Thunderbird"))  # app9
        self.app9_button.setToolTip("app9")

        self.app10_button.setText(_translate("MainWindow", "Screen REC"))  # app10
        self.app10_button.setToolTip("app10")

        self.short1_button.setText(_translate("MainWindow", "Undo"))  # short1
        self.short1_button.setToolTip("Undo - Ctrl+Z")

        self.short2_button.setText(_translate("MainWindow", "Copy"))  # short2
        self.short2_button.setToolTip("Copy - Ctrl+C")

        self.short3_button.setText(_translate("MainWindow", "Cut"))  # short3
        self.short3_button.setToolTip("Cut - Ctrl+X")

        self.short4_button.setText(_translate("MainWindow", "Paste"))  # short4
        self.short4_button.setToolTip("Paste - Ctrl+V")

        self.short5_button.setText(_translate("MainWindow", "Mic"))  # short5
        self.short5_button.setToolTip("Microphone (googlemeet) - Ctrl+D")

        self.short6_button.setText(_translate("MainWindow", "Webcam"))  # short6
        self.short6_button.setToolTip("Webcam (googlemeet) - Ctrl+E")

        self.short7_button.setText(_translate("MainWindow", "Fullscreen"))  # short7
        self.short7_button.setToolTip("Fullscreen - F11")

        self.short8_button.setText(_translate("MainWindow", "Screenshot"))  # short8
        self.short8_button.setToolTip("Screenshot - PRT-SC")

        self.short9_button.setText(_translate("MainWindow", "Blank"))  # short9

        self.short10_button.setText(_translate("MainWindow", "Blank"))  # short10

    # App launch functions

    # I know that that's not the best way to handle an exception, but it works and it's enough for me

    def app1(self):
        try:
            logging.info("Selected app1")
            encrypt_index("a1")
            response = raspsocket.recv(1024).decode("ascii")  # Recive the response
            print(response)  # Print the response

        except BrokenPipeError:
            print("Connection closed or denied by PC.  Quitting.")
            connection_interrupted()
            raspsocket.close()
            exit()

    def app2(self):
        try:
            logging.info("Selected app2")
            encrypt_index("a2")
            response = raspsocket.recv(1024).decode("ascii")  # Recive the response
            print(response)  # Print the response

        except BrokenPipeError:
            print("Connection closed or denied by PC.  Quitting.")
            connection_interrupted()
            raspsocket.close()
            exit()

    def app3(self):
        try:
            logging.info("Selected app3")
            encrypt_index("a3")
            response = raspsocket.recv(1024).decode("ascii")  # Recive the response
            print(response)  # Print the response

        except BrokenPipeError:
            print("Connection closed or denied by PC.  Quitting.")
            connection_interrupted()
            raspsocket.close()
            exit()

    def app4(self):
        try:
            logging.info("Selected app4")
            encrypt_index("a4")
            response = raspsocket.recv(1024).decode("ascii")  # Recive the response
            print(response)  # Print the response

        except BrokenPipeError:
            print("Connection closed or denied by PC.  Quitting.")
            connection_interrupted()
            raspsocket.close()
            exit()

    def app5(self):
        try:
            logging.info("Selected app5")
            encrypt_index("a5")
            response = raspsocket.recv(1024).decode("ascii")  # Recive the response
            print(response)  # Print the response

        except BrokenPipeError:
            print("Connection closed or denied by PC.  Quitting.")
            connection_interrupted()
            raspsocket.close()
            exit()

    def app6(self):
        try:
            logging.info("Selected app6")
            encrypt_index("a6")
            response = raspsocket.recv(1024).decode("ascii")  # Recive the response
            print(response)  # Print the response

        except BrokenPipeError:
            print("Connection closed or denied by PC.  Quitting.")
            connection_interrupted()
            raspsocket.close()
            exit()

    def app7(self):
        try:
            logging.info("Selected app7")
            encrypt_index("a7")
            response = raspsocket.recv(1024).decode("ascii")  # Recive the response
            print(response)  # Print the response

        except BrokenPipeError:
            print("Connection closed or denied by PC.  Quitting.")
            connection_interrupted()
            raspsocket.close()
            exit()

    def app8(self):
        try:
            logging.info("Selected app8")
            encrypt_index("a8")
            response = raspsocket.recv(1024).decode("ascii")  # Recive the response
            print(response)  # Print the response

        except BrokenPipeError:
            print("Connection closed or denied by PC.  Quitting.")
            connection_interrupted()
            raspsocket.close()
            exit()

    def app9(self):
        try:
            logging.info("Selected app9")
            encrypt_index("a9")
            response = raspsocket.recv(1024).decode("ascii")  # Recive the response
            print(response)  # Print the response

        except BrokenPipeError:
            print("Connection closed or denied by PC.  Quitting.")
            connection_interrupted()
            raspsocket.close()
            exit()

    def app10(self):
        try:
            logging.info("Selected app10")
            encrypt_index("a10")
            response = raspsocket.recv(1024).decode("ascii")  # Recive the response
            print(response)  # Print the response

        except BrokenPipeError:
            print("Connection closed or denied by PC.  Quitting.")
            connection_interrupted()
            raspsocket.close()
            exit()

    # Keyboard shortcuts functions
    def short1(self):
        try:
            logging.info("Selected short1")
            encrypt_index("s1")
            response = raspsocket.recv(1024).decode("ascii")  # Recive the response
            print(response)  # Print the response

        except BrokenPipeError:
            print("Connection closed or denied by PC.  Quitting.")
            connection_interrupted()
            raspsocket.close()
            exit()

    def short2(self):
        try:
            logging.info("Selected short2")
            encrypt_index("s2")
            response = raspsocket.recv(1024).decode("ascii")  # Recive the response
            print(response)  # Print the response

        except BrokenPipeError:
            print("Connection closed or denied by PC.  Quitting.")
            connection_interrupted()
            raspsocket.close()
            exit()

    def short3(self):
        try:
            logging.info("Selected short3")
            encrypt_index("s3")
            response = raspsocket.recv(1024).decode("ascii")  # Recive the response
            print(response)  # Print the response```

        except BrokenPipeError:
            print("Connection closed or denied by PC.  Quitting.")
            connection_interrupted()
            raspsocket.close()
            exit()

    def short4(self):
        try:
            logging.info("Selected short4")
            encrypt_index("s4")
            response = raspsocket.recv(1024).decode("ascii")  # Recive the response
            print(response)  # Print the response

        except BrokenPipeError:
            print("Connection closed or denied by PC.  Quitting.")
            connection_interrupted()
            raspsocket.close()
            exit()

    def short5(self):
        try:
            logging.info("Selected short5")
            encrypt_index("s5")
            response = raspsocket.recv(1024).decode("ascii")  # Recive the response
            print(response)  # Print the response

        except BrokenPipeError:
            print("Connection closed or denied by PC.  Quitting.")
            connection_interrupted()
            raspsocket.close()
            exit()

    def short6(self):
        try:
            logging.info("Selected short6")
            encrypt_index("s6")
            response = raspsocket.recv(1024).decode("ascii")  # Recive the response
            print(response)  # Print the response

        except BrokenPipeError:
            print("Connection closed or denied by PC.  Quitting.")
            connection_interrupted()
            raspsocket.close()
            exit()

    def short7(self):
        try:
            logging.info("Selected short7")
            encrypt_index("s7")
            response = raspsocket.recv(1024).decode("ascii")  # Recive the response
            print(response)  # Print the response

        except BrokenPipeError:
            print("Connection closed or denied by PC.  Quitting.")
            connection_interrupted()
            raspsocket.close()
            exit()

    def short8(self):
        try:
            logging.info("Selected short8")
            encrypt_index("s8")
            response = raspsocket.recv(1024).decode("ascii")  # Recive the response
            print(response)  # Print the response

        except BrokenPipeError:
            print("Connection closed or denied by PC.  Quitting.")
            connection_interrupted()
            raspsocket.close()
            exit()

    def short9(self):
        try:
            logging.info("Selected short9")
            encrypt_index("s9")
            response = raspsocket.recv(1024).decode("ascii")  # Recive the response
            print(response)  # Print the response

        except BrokenPipeError:
            print("Connection closed or denied by PC.  Quitting.")
            connection_interrupted()
            raspsocket.close()
            exit()

    def short10(self):
        try:
            logging.info("Selected short10")
            encrypt_index("s10")
            response = raspsocket.recv(1024).decode("ascii")  # Recive the response
            print(response)  # Print the response

        except BrokenPipeError:
            print("Connection closed or denied by PC.  Quitting.")
            connection_interrupted()
            raspsocket.close()
            exit()

    def sysf1(self):
        try:
            logging.info("Selected system function 1")
            encrypt_index("sf1")
            response = raspsocket.recv(1024).decode("ascii")  # Recive the response
            print(response)  # Print the response

        except BrokenPipeError:
            print("Connection closed or denied by PC.  Quitting.")
            connection_interrupted()
            raspsocket.close()
            exit()

    def sysf2(self):
        try:
            logging.info("Selected system function 2")
            encrypt_index("sf2")
            response = raspsocket.recv(1024).decode("ascii")  # Recive the response
            print(response)  # Print the response

        except BrokenPipeError:
            print("Connection closed or denied by PC.  Quitting.")
            connection_interrupted()
            raspsocket.close()
            exit()

    def sysf3(self):
        try:
            logging.info("Selected system function 3")
            encrypt_index("sf3")
            response = raspsocket.recv(1024).decode("ascii")  # Recive the response
            print(response)  # Print the response

        except BrokenPipeError:
            print("Connection closed or denied by PC.  Quitting.")
            connection_interrupted()
            raspsocket.close()
            exit()


def encrypt_index(index):
    """
    encrypt the index, add whitespace to make the string >= 16 bytes and send the index to PC.

    Args:
        index (string): the index to encrypt

    """
    logging.info(f"Encrypting the index {index}")
    index = index + (16 - len(index)) * " "  # make the index 16 bytes
    cipherindex = crytool.encrypt(index.encode("ascii"))  # encrypting the index
    logging.info("Index encrypted. Sending to PC")
    raspsocket.send(cipherindex)  # send the index
    logging.info("Index sent")


if __name__ == "__main__":
    # Setting up the logger
    logging.basicConfig(
        filename="rasp.log",
        filemode="w",
        format="%(asctime)s - %(levelname)s - %(message)s",
        level=logging.INFO,
    )

    logging.info("Rasp component started")

    logging.info("Creating AES --crypter object")
    # AES encrypter / decrypter
    #                 A casual 128bit key                A casual 128bit Initialization vector
    crytool = AES.new(b"ghnmXRHOwJ2j1Qfr", AES.MODE_CBC, b"127jH6VBnm09Lkqw")

    # Loading configuration file
    try:
        logging.info("Opening rasp.conf")
        with open("rasp.conf", newline="") as conf_file:
            reader = csv.reader(conf_file, delimiter=",")

            for row in reader:
                PC_HOST = row[0]
                PC_PORT = int(row[1])
                break

            logging.info(f"setting pc host to {PC_HOST} and pc port to {PC_PORT}")

    except Exception as e:
        print(f"Error with rasp.conf: {e}. Fix the error and restart.")
        logging.critical(f"Error {e} about rasp.conf. quitting")
        exit()

    # Cli arguments parser
    parser = argparse.ArgumentParser(description="Rasp2Pc RASP Component")

    parser.add_argument(
        "--host",
        type=str,
        default=PC_HOST,
        help=f"the addess of the PC Component (default={PC_HOST})",
    )

    parser.add_argument(
        "--port",
        type=int,
        default=PC_PORT,
        help=f"the port of the PC Component (default={PC_PORT})",
    )

    logging.info("Getting cli args")
    args = parser.parse_args()
    PC_HOST = args.host
    PC_PORT = args.port

    try:
        logging.info("Creating socket...")
        with socket.socket(
            socket.AF_INET, socket.SOCK_STREAM
        ) as raspsocket:  # Create socket object
            # ATTENTION: You have to modify the line 25 with the PC ip address and the port (default:10000)
            logging.info(f"Connecting to {PC_HOST}:{PC_PORT}...")
            raspsocket.connect((PC_HOST, PC_PORT))  # Connect to the PC
            logging.info("sending raspcomponent identifier")
            raspsocket.send(
                "rasp2pc_rasp_component".encode()
            )  # Declare to PC that this is a """legit""" rasp component
            print("Waiting for PC to accept the connection...")
            connection = raspsocket.recv(1024).decode("ascii")
            if connection == "ConnectionAccepted":
                logging.info("Connection accepted")
            else:
                logging.critical(f"connection denied by {PC_HOST}")
                connection_denied(raspsocket, PC_HOST)

            app = QtWidgets.QApplication(sys.argv)
            MainWindow = QtWidgets.QMainWindow()
            ui = Ui_MainWindow()
            ui.setupUi(MainWindow)
            logging.debug("Showing the gui")
            MainWindow.show()

            sys.exit(app.exec_())

    except ConnectionRefusedError as e:
        not_reachable(raspsocket, PC_HOST)
        logging.critical(
            f"Pc ({PC_HOST}:{PC_PORT}) is not reachable. ERROR:{e}. Quitting"
        )
        exit()

    except OSError as e:
        not_found(raspsocket, PC_HOST)
        print(
            "PC not found. check the ip address and if the pc component is running. Quitting"
        )
        logging.critical(f"pc ({PC_HOST}:{PC_PORT}) not found. ERROR:{e}. Quitting")
        exit()
