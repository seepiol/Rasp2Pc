#!/usr/bin/python3
"""
    Rasp2PC - RASP T H I C C Component
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
import json
import argparse
from Crypto.Cipher import AES

system_functions_icons = []
labels = []
keyboard_labels = []


# POPUPS FOR ERROR

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
        MainWindow.resize(800, 480)

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.RASPcomponent_label = QtWidgets.QLabel(self.centralwidget)
        self.RASPcomponent_label.setGeometry(QtCore.QRect(540, 10, 181, 18))
        self.RASPcomponent_label.setObjectName("RASPcomponent_label")

        self.connected_to_label = QtWidgets.QLabel(self.centralwidget)
        self.connected_to_label.setGeometry(QtCore.QRect(540, 30, 101, 18))
        self.connected_to_label.setObjectName("connected_to_label")

        self.pc_info_label = QtWidgets.QLabel(self.centralwidget)
        self.pc_info_label.setGeometry(QtCore.QRect(640, 30, 181, 18))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(75)
        self.pc_info_label.setFont(font)
        self.pc_info_label.setText("")
        self.pc_info_label.setObjectName("pc_info_label")

        # System Functions
        self.sysf1_icon = QtGui.QIcon()
        self.sysf1_icon.addPixmap(QtGui.QPixmap(f"icons/{system_functions_icons[0]}.png"))
        self.sysf1_button = QtWidgets.QPushButton(self.centralwidget)
        self.sysf1_button.setGeometry(QtCore.QRect(540, 60, 221, 55))
        self.sysf1_button.setIcon(self.sysf1_icon)
        self.sysf1_button.setToolTip("System Function 1")
        self.sysf1_button.setObjectName("sysf1_button")

        self.sysf2_icon = QtGui.QIcon()
        self.sysf2_icon.addPixmap(QtGui.QPixmap(f"icons/{system_functions_icons[1]}.png"))
        self.sysf2_button = QtWidgets.QPushButton(self.centralwidget)
        self.sysf2_button.setGeometry(QtCore.QRect(540, 140, 221, 55))
        self.sysf2_button.setIcon(self.sysf2_icon)
        self.sysf2_button.setToolTip("System Function 2")
        self.sysf2_button.setObjectName("sysf2_button")

        self.sysf3_icon = QtGui.QIcon()
        self.sysf3_icon.addPixmap(QtGui.QPixmap(f"icons/{system_functions_icons[2]}.png"))
        self.sysf3_button = QtWidgets.QPushButton(self.centralwidget)
        self.sysf3_button.setGeometry(QtCore.QRect(540, 220, 221, 55))
        self.sysf3_button.setIcon(self.sysf3_icon)
        self.sysf3_button.setToolTip("System Function 3")
        self.sysf3_button.setObjectName("sysf3_button")

        # Programs
        self.app_frame = QtWidgets.QFrame(self.centralwidget)
        self.app_frame.setGeometry(QtCore.QRect(10, 10, 231, 401))
        self.app_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.app_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.app_frame.setObjectName("app_frame")

        self.app2_button = QtWidgets.QPushButton(self.app_frame)
        self.app2_button.setGeometry(QtCore.QRect(130, 10, 90, 60))
        self.app2_button.setText("")
        self.app2_button.setObjectName("app2_button")

        self.app1_button = QtWidgets.QPushButton(self.app_frame)
        self.app1_button.setGeometry(QtCore.QRect(10, 10, 90, 60))
        self.app1_button.setObjectName("app1_button")

        self.app3_button = QtWidgets.QPushButton(self.app_frame)
        self.app3_button.setGeometry(QtCore.QRect(10, 90, 90, 60))
        self.app3_button.setText("")
        self.app3_button.setObjectName("app3_button")

        self.app4_button = QtWidgets.QPushButton(self.app_frame)
        self.app4_button.setGeometry(QtCore.QRect(130, 90, 90, 60))
        self.app4_button.setText("")
        self.app4_button.setObjectName("app4_button")

        self.app5_button = QtWidgets.QPushButton(self.app_frame)
        self.app5_button.setGeometry(QtCore.QRect(10, 170, 90, 60))
        self.app5_button.setText("")
        self.app5_button.setObjectName("app5_button")

        self.app6_button = QtWidgets.QPushButton(self.app_frame)
        self.app6_button.setGeometry(QtCore.QRect(130, 170, 90, 60))
        self.app6_button.setText("")
        self.app6_button.setObjectName("app6_button")

        self.app7_button = QtWidgets.QPushButton(self.app_frame)
        self.app7_button.setGeometry(QtCore.QRect(10, 250, 90, 60))
        self.app7_button.setText("")
        self.app7_button.setObjectName("app7_button")

        self.app8_button = QtWidgets.QPushButton(self.app_frame)
        self.app8_button.setGeometry(QtCore.QRect(130, 250, 90, 60))
        self.app8_button.setText("")
        self.app8_button.setObjectName("app8_button")

        self.app9_button = QtWidgets.QPushButton(self.app_frame)
        self.app9_button.setGeometry(QtCore.QRect(10, 330, 90, 60))
        self.app9_button.setText("")
        self.app9_button.setObjectName("app9_button")

        self.app10_button = QtWidgets.QPushButton(self.app_frame)
        self.app10_button.setGeometry(QtCore.QRect(130, 330, 90, 60))
        self.app10_button.setText("")
        self.app10_button.setObjectName("app10_button")

        # Keyboard

        self.keyboard_frame = QtWidgets.QFrame(self.centralwidget)
        self.keyboard_frame.setGeometry(QtCore.QRect(280, 10, 231, 401))
        self.keyboard_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.keyboard_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.keyboard_frame.setObjectName("keyboard_frame")

        self.short1_button = QtWidgets.QPushButton(self.keyboard_frame)
        self.short1_button.setGeometry(QtCore.QRect(10, 10, 90, 60))
        self.short1_button.setText("")
        self.short1_button.setShortcut("")
        self.short1_button.setObjectName("short1_button")

        self.short2_button = QtWidgets.QPushButton(self.keyboard_frame)
        self.short2_button.setGeometry(QtCore.QRect(130, 10, 90, 60))
        self.short2_button.setText("")
        self.short2_button.setObjectName("short2_button")

        self.short3_button = QtWidgets.QPushButton(self.keyboard_frame)
        self.short3_button.setGeometry(QtCore.QRect(10, 90, 90, 60))
        self.short3_button.setText("")
        self.short3_button.setObjectName("short3_button")

        self.short4_button = QtWidgets.QPushButton(self.keyboard_frame)
        self.short4_button.setGeometry(QtCore.QRect(130, 90, 90, 60))
        self.short4_button.setText("")
        self.short4_button.setObjectName("short4_button")

        self.short5_button = QtWidgets.QPushButton(self.keyboard_frame)
        self.short5_button.setGeometry(QtCore.QRect(10, 170, 90, 60))
        self.short5_button.setText("")
        self.short5_button.setObjectName("short5_button")

        self.short6_button = QtWidgets.QPushButton(self.keyboard_frame)
        self.short6_button.setGeometry(QtCore.QRect(130, 170, 90, 60))
        self.short6_button.setText("")
        self.short6_button.setObjectName("short6_button")

        self.short7_button = QtWidgets.QPushButton(self.keyboard_frame)
        self.short7_button.setGeometry(QtCore.QRect(10, 250, 90, 60))
        self.short7_button.setText("")
        self.short7_button.setObjectName("short7_button")

        self.short8_button = QtWidgets.QPushButton(self.keyboard_frame)
        self.short8_button.setGeometry(QtCore.QRect(130, 250, 90, 60))
        self.short8_button.setText("")
        self.short8_button.setObjectName("short8_button")

        self.short9_button = QtWidgets.QPushButton(self.keyboard_frame)
        self.short9_button.setGeometry(QtCore.QRect(10, 330, 90, 60))
        self.short9_button.setText("")
        self.short9_button.setObjectName("short9_button")

        self.short10_button = QtWidgets.QPushButton(self.keyboard_frame)
        self.short10_button.setGeometry(QtCore.QRect(130, 330, 90, 60))
        self.short10_button.setText("")
        self.short10_button.setObjectName("short10_button")

        # Function Connections
        # System Function
        self.sysf1_button.clicked.connect(lambda: self.send("sf1"))
        self.sysf2_button.clicked.connect(lambda: self.send("sf2"))
        self.sysf3_button.clicked.connect(lambda: self.send("sf3"))
        # Apps
        self.app1_button.clicked.connect(lambda: self.send("a1"))
        self.app2_button.clicked.connect(lambda: self.send("a2"))
        self.app3_button.clicked.connect(lambda: self.send("a3"))
        self.app4_button.clicked.connect(lambda: self.send("a4"))
        self.app5_button.clicked.connect(lambda: self.send("a5"))
        self.app6_button.clicked.connect(lambda: self.send("a6"))
        self.app7_button.clicked.connect(lambda: self.send("a7"))
        self.app8_button.clicked.connect(lambda: self.send("a8"))
        self.app9_button.clicked.connect(lambda: self.send("a9"))
        self.app10_button.clicked.connect(lambda: self.send("a10"))
        # Keyboard
        self.short1_button.clicked.connect(lambda: self.send("s1"))
        self.short2_button.clicked.connect(lambda: self.send("s2"))
        self.short3_button.clicked.connect(lambda: self.send("s3"))
        self.short4_button.clicked.connect(lambda: self.send("s4"))
        self.short5_button.clicked.connect(lambda: self.send("s5"))
        self.short6_button.clicked.connect(lambda: self.send("s6"))
        self.short7_button.clicked.connect(lambda: self.send("s7"))
        self.short8_button.clicked.connect(lambda: self.send("s8"))
        self.short9_button.clicked.connect(lambda: self.send("s9"))
        self.short10_button.clicked.connect(lambda: self.send("s10"))

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

        self.app1_button.setText(_translate("MainWindow", labels[0]))  # app1
        self.app1_button.setToolTip("Application 1")

        self.app2_button.setText(_translate("MainWindow", labels[1]))  # app2
        self.app2_button.setToolTip("Application 2")

        self.app3_button.setText(_translate("MainWindow", labels[2]))  # app3
        self.app3_button.setToolTip("Application 3")

        self.app4_button.setText(_translate("MainWindow", labels[3]))  # app4
        self.app4_button.setToolTip("Application 4")

        self.app5_button.setText(_translate("MainWindow", labels[4]))  # app5
        self.app5_button.setToolTip("Application 5")

        self.app6_button.setText(_translate("MainWindow", labels[5]))  # app6
        self.app6_button.setToolTip("Application 6")

        self.app7_button.setText(_translate("MainWindow", labels[6]))  # app7
        self.app7_button.setToolTip("Application 7")

        self.app8_button.setText(_translate("MainWindow", labels[7]))  # app8
        self.app8_button.setToolTip("Application 8")

        self.app9_button.setText(_translate("MainWindow", labels[8]))  # app9
        self.app9_button.setToolTip("Application 9")

        self.app10_button.setText(_translate("MainWindow", labels[9]))  # app10
        self.app10_button.setToolTip("Application 10")

        self.short1_button.setText(_translate("MainWindow", keyboard_labels[0]))  # short1
        self.short1_button.setToolTip("Keyboard Shortcut 1")

        self.short2_button.setText(_translate("MainWindow", keyboard_labels[1]))  # short2
        self.short2_button.setToolTip("Keyboard Shortcut 2")

        self.short3_button.setText(_translate("MainWindow", keyboard_labels[2]))  # short3
        self.short3_button.setToolTip("Keyboard Shortcut 3")

        self.short4_button.setText(_translate("MainWindow", keyboard_labels[3]))  # short4
        self.short4_button.setToolTip("Keyboard Shortcut 4")

        self.short5_button.setText(_translate("MainWindow", keyboard_labels[4]))  # short5
        self.short5_button.setToolTip("Keyboard Shortcut 5")

        self.short6_button.setText(_translate("MainWindow", keyboard_labels[5]))  # short6
        self.short6_button.setToolTip("Keyboard Shortcut 6")

        self.short7_button.setText(_translate("MainWindow", keyboard_labels[6]))  # short7
        self.short7_button.setToolTip("Keyboard Shortcut 7")

        self.short8_button.setText(_translate("MainWindow", keyboard_labels[7]))  # short8
        self.short8_button.setToolTip("Keyboard Shortcut 8")

        self.short9_button.setText(_translate("MainWindow", keyboard_labels[8]))  # short9
        self.short9_button.setToolTip("Keyboard Shortcut 9")

        self.short10_button.setText(_translate("MainWindow", keyboard_labels[9]))  # short10
        self.short9_button.setToolTip("Keyboard Shortcut 10")

    # App/keyboard shortcuts/system functions launch functions

    # I know that that's not the best way to handle an exception, but it works and it's enough for me

    def send(self, index):
        try:
            logging.info(f"Selected {index}")
            encrypt_index(f"{index}")
            response = raspsocket.recv(1024).decode("utf-8")  # Recive the response
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
    # AES encrypter / decrypter
    #                 A casual 128bit key                A casual 128bit Initialization vector
    crytool = AES.new(b"ghnmXRHOwJ2j1Qfr", AES.MODE_CBC, b"127jH6VBnm09Lkqw")
    logging.info(f"Encrypting the index {index}")
    index = index + (16 - len(index)) * " "  # make the index 16 bytes
    cipherindex = crytool.encrypt(index.encode("utf-8"))  # encrypting the index
    logging.info("Index encrypted. Sending to PC")
    raspsocket.send(cipherindex)  # send the index
    logging.info("Index sent")


def load_json():
    global labels
    # Loading labels
    try:
        with open("shortcuts.json", "r") as shortcuts_file:
            shortcuts_json = json.load(shortcuts_file)

            for label in shortcuts_json["app"]:
                labels.append(label)

            for icon in shortcuts_json["system_functions"]:
                system_functions_icons.append(icon)

            for label in shortcuts_json["keyboard"]:
                keyboard_labels.append(label)

    except Exception as E:
        print(f"Error while reading shortcuts.json: {E}.\nQuitting.")
        logging.critical("Error while reading shortcuts.json")
        exit()



if __name__ == "__main__":
    # Setting up the logger
    logging.basicConfig(
        filename="rasp.log",
        filemode="w",
        format="%(asctime)s - %(levelname)s - %(message)s",
        level=logging.INFO,
    )

    logging.info("Rasp component started")

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

    load_json()

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
                "rasp2pc_rasp_component".encode("utf-8")
            )  # Declare to PC that this is a """legit""" rasp component
            print("Waiting for PC to accept the connection...")
            connection = raspsocket.recv(1024).decode("utf-8")
            if connection == "ConnectionAccepted":
                logging.info("Connection accepted")
            else:
                logging.critical(f"connection denied by {PC_HOST}")
                connection_denied(raspsocket, PC_HOST)

            app = QtWidgets.QApplication(sys.argv)
            ex = Ui_MainWindow()
            w = QtWidgets.QMainWindow()
            w.setWindowIcon(QtGui.QIcon("icons/icon.png"))
            ex.setupUi(w)
            w.show()

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
