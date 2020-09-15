#!/usr/bin/python3
"""
    Rasp2PC - PC component
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
import json
import socket
import subprocess
from pynput.keyboard import Key, Controller
import logging
import argparse
from Crypto.Cipher import AES
import time
import platform

HOST = ""  # Address
PORT = 10000  # Port

commands = []
windows = None

# System functions methods
# TODO: take the system functions from shortcuts.csv

def sysf1():
    """
    Reboot the system
    """
    logging.info("rebooting system")  # Logging
    try:
        subprocess.Popen(["reboot"], shell=False)  # Run the command
    except FileNotFoundError:
        print("No such file or directory")
    return "Reboot"  # action name


def sysf2():
    """
    Lock the session
    """
    logging.info("Locking the session")
    try:
        subprocess.Popen(["loginctl", "lock-session"], shell=False)
    except FileNotFoundError:
        print("No such file or directory")
    return "lock"


def sysf3():
    """
    Mute the audio
    """
    logging.info("Turning volume to 0%")
    try:
        subprocess.Popen(["amixer", "-D", "pulse", "sset", "Master", "0%"], shell=False)
    except FileNotFoundError:
        print("No such file or directory")
    return "mute"


# App launch methods
# It's kinda ok, but 
# TODO: return the esit (if the execution is gone ok)
# TODO: mantain the command running even if I close pc component

def app(index):
    # Parsing the index: transform the app index sent from rasp ("a2") to the command list index (1)
    index = int(index[1:]) - 1

    logging.info(f"Executing {commands[index]}")
    try:
        # Platform Check
        if (
            windows
        ):  # With windows subprocess needs to run in a shell. More here: https://stackoverflow.com/questions/3172470/actual-meaning-of-shell-true-in-subprocess#3172488
            subprocess.Popen(commands[index], shell=True)
        else:  # If not windows, better with shell=False
            subprocess.Popen(commands[index], shell=False)
    except FileNotFoundError:  # The command isn't recognized
        print("No such file or directory")
    return commands[index]


# Keyboard shortcuts execution methods
# TODO: avoid to hardcode. maybe parse from shortcuts.csv in some way? 

def short1(keyboard):
    """
    Ctrl+Z
    Undo shortcut
    Usable everywhere
    """
    logging.info("Ctrl+z")
    with keyboard.pressed(Key.ctrl):
        keyboard.press("z")
        keyboard.release("z")
    return "undo"


def short2(keyboard):
    """
    Ctrl+c
    Copy
    Usable everywhere
    """
    logging.info("Ctrl+c")
    with keyboard.pressed(Key.ctrl):
        keyboard.press("c")
        keyboard.release("c")
    return "copy"


def short3(keyboard):
    """
    Ctrl+x
    Cut
    Usable everywhere
    """
    logging.info("Ctrl+x")
    with keyboard.pressed(Key.ctrl):
        keyboard.press("x")
        keyboard.release("x")
    return "cut"


def short4(keyboard):
    """
    Ctrl+v
    Paste
    Usable everywhere
    """
    logging.info("Ctrl+v")
    with keyboard.pressed(Key.ctrl):
        keyboard.press("v")
        keyboard.release("v")
    return "paste"


def short5(keyboard):
    """
    Ctrl+D
    Activate/disactivate the microphone
    Usable on Google Meet
    """
    logging.info("Ctrl+d")
    with keyboard.pressed(Key.ctrl):
        keyboard.press("d")
        keyboard.release("d")
    return "webcam"


def short6(keyboard):
    """
    Ctrl+E
    Activate/disactivate the microphone
    Usable on Google Meet
    """
    logging.info("Ctrl+e")
    with keyboard.pressed(Key.ctrl):
        keyboard.press("e")
        keyboard.release("e")
    return "microphone"


def short7(keyboard):
    """
    F11
    Make full screen
    Usable everywhere
    """
    logging.info("F11")
    keyboard.press(Key.f11)
    keyboard.release(Key.f11)
    return "fullscreen"


def short8(keyboard):
    """
    PRT-SC
    Print Screen (Screenshot)
    Usable everywhere
    """
    logging.info("PRT SC")
    keyboard.press(Key.print_screen)
    keyboard.release(Key.print_screen)
    return "screenshot"


def short9(keyboard):
    """
    ALT-F4
    Close window
    Usable everywhere
    """
    logging.info("Alt+F4")
    with keyboard.pressed(Key.alt):
        keyboard.press(Key.f4)
        keyboard.release(Key.f4)
    return "close window"


def short10(keyboard):
    logging.info("Blank")
    return


def decrypt_index(crypted_index):
    """
    Decrypt the index recived from rasp

    Args:
        crypted index {bytes}: the aes128 encryptrd byte string

    Returns:
        index {string}: the decrypted index

    """
    # AES encrypter / decrypter
    #                 A casual 128bit key                A casual 128bit Initialization vector
    crytool = AES.new(b"ghnmXRHOwJ2j1Qfr", AES.MODE_CBC, b"127jH6VBnm09Lkqw")

    logging.info("Decrypting the index")
    index = crytool.decrypt(crypted_index)  # Decrypting
    try:  # When rasp disconnect and another rasp connect, the pc component recive a strange and non-decodable "string"
        index = index.decode("utf-8")
    except UnicodeDecodeError:
        index = "0"
    index = index.replace(" ", "")  # Replacing whitespaces with blankstring
    return index


def parse_command(command):
    return command.split()


def load_json():
    global commands
    # Loading commands
    try:
        with open("shortcuts.json", "r") as shortcuts_file:
            shortcuts_json = json.load(shortcuts_file)
            for key in shortcuts_json["app"]:
                commands.append(parse_command(shortcuts_json["app"].get(key)))
            print(commands)
    except Exception as E:
        print(f"Error while reading shortcuts.json: {E}.\nQuitting.")
        logging.critical("Error while reading shortcuts.json")
        exit()


def initialize():
    global windows
    if platform.system() == "Windows":
        windows = True
    else:
        windows = False

    # Setting up the logger
    logging.basicConfig(
        filename="pc.log",
        filemode="w",
        format="%(asctime)s - %(levelname)s - %(message)s",
        level=logging.INFO,
    )

    keyboard = Controller()  # Create a virtual keyboard

    # Cli arguments parser
    parser = argparse.ArgumentParser(description="Rasp2Pc PC Component")

    parser.add_argument(
        "--host",
        type=str,
        default="",
        help="the addess the where socket server will be listening (default=everyone)",
    )

    parser.add_argument(
        "--port",
        type=int,
        default=10000,
        help="the port where the server will be listening (default=10000)",
    )

    args = parser.parse_args()

    HOST = args.host
    PORT = args.port

    # If a privileged port is selected
    if PORT < 1024:
        print(
            "WARNING: You have selected a privileged port. Please choose a port above 1024"
        )
        logging.critical("Selected a privileged port")

    load_json()

    logging.info("PC Component started")
    try:
        logging.info("Creating socket object")
        while True:
            with socket.socket(
                socket.AF_INET, socket.SOCK_STREAM
            ) as sock:  # creating socket object
                sock.setsockopt(
                    socket.SOL_SOCKET, socket.SO_REUSEADDR, 1
                )  # Permit the reutilization of the socket when in TIME_WAIT
                sock.bind((HOST, PORT))  # binding socket on {host:port}

                print(f"Socket binded on {HOST}:{PORT}")
                logging.info(f"binding socket on {HOST}:{PORT}")

                sock.listen()  # listening for connection requests
                print("Socket in listening...")
                logging.info(f"Socket listening on {HOST}:{PORT}")
                while True:
                    (
                        conn,
                        client_address,
                    ) = sock.accept()  # Accepting connection from {address}

                    # Connection Control
                    print(f"{client_address} is trying to connect to this pc. ")

                    msg = conn.recv(1024).decode("utf-8")
                    if (
                        msg != "rasp2pc_rasp_component"
                    ):  # Verify if the client is a """legit""" rasp component
                        print(f"{client_address} doesn't seems to be a RASP component")
                    else:
                        print(f"{client_address} seems to be a RASP component")

                    # Accept or deny the connection
                    accept_connection = input(
                        "Do you want to accept this connection? [Y/n]: "
                    )
                    if accept_connection.lower() in ["y", "yes", ""]:
                        print(f"Connection with {client_address} accepted")
                        logging.info(f"Connection with {client_address} accepted")
                        conn.send("ConnectionAccepted".encode("utf-8"))
                    else:
                        print("Connection Denied")
                        logging.info("Connection Denied")
                        conn.send("ConnectionDenied".encode("utf-8"))
                        conn.close()

                    try:

                        action_title = None
                        while True:
                            logging.info("Reciving the index")
                            # Reciving the encrypted index directly as an argument for decrypt_index()
                            data = decrypt_index(conn.recv(1024))
                            if data == "":  # FIXME: is that useless?
                                raise IOError
                            elif data == "0":  # see decrypt_index try comment
                                pass
                            logging.info(f"{client_address} has requested {data}")

                            # Execute the index corresponding program or shortcut

                            if (
                                data[0] == "a"
                            ):  # If the first char of the data is "a" (an application), use the unified function
                                app(data)
                            elif data == "s1":
                                action_title = short1(keyboard) # FIXME; does really make sense to pass the keyboard as argument? 
                            elif data == "s2":
                                action_title = short2(keyboard)
                            elif data == "s3":
                                action_title = short3(keyboard)
                            elif data == "s4":
                                action_title = short4(keyboard)
                            elif data == "s5":
                                action_title = short5(keyboard)
                            elif data == "s6":
                                action_title = short6(keyboard)
                            elif data == "s7":
                                action_title = short7(keyboard)
                            elif data == "s8":
                                action_title = short8(keyboard)
                            elif data == "s9":
                                action_title = short9(keyboard)
                            elif data == "s10":
                                action_title = short10(keyboard)

                            elif data == "sf1":
                                action_title = sysf1()
                            elif data == "sf2":
                                action_title = sysf2()
                            elif data == "sf3":
                                action_title = sysf3()

                            esit = "ok" # FIXME: this useless return code

                            conn.send(
                                esit.encode("utf-8")
                            )  # sending a "fake" confirm message

                    except IOError as e:
                        logging.info("RASP Disconnected")
                        print("RASP Disconnected")
                        sock.close()
                        break

    except KeyboardInterrupt:
        logging.info("KeyboardInterrupt: quitting")
        print("Closed by keyboard. Bye")
        sock.close()
        exit()

    except IOError as E:
        logging.info(E)
        print(E)
        pass

    except Exception as e:
        print("Something went wrong:", e)
        logging.info(f"Error Happened {e}. closing the socket.")
        sock.close()
        exit()


if __name__ == "__main__":
    initialize()
