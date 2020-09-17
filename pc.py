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
system_functions = []
keyboard_shortcuts = []

windows = None

# System functions methods
# TODO: take the system functions from shortcuts.csv

def sysf1():
    """
    Reboot the system
    """
    logging.info(f"executing system function: {' '.join(system_functions[0])}")  # Logging
    try:
        subprocess.Popen(system_functions[0], shell=False)  # Run the command
    except FileNotFoundError:
        print("No such file or directory")
    return "sysf1"  # action name


def sysf2():
    """
    Lock the session
    """
    logging.info(f"executing system function: {' '.join(system_functions[1])}")  # Logging
    try:
        subprocess.Popen(system_functions[1], shell=False)  # Run the command
    except FileNotFoundError:
        print("No such file or directory")
    return "sysf2"


def sysf3():
    """
    Mute the audio
    """
    logging.info(f"executing system function: {' '.join(system_functions[2])}")  # Logging
    try:
        subprocess.Popen(system_functions[2], shell=False)  # Run the command
    except FileNotFoundError:
        print("No such file or directory")
    return "sysf3"


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

            for key in shortcuts_json["system_functions"]:
                system_functions.append(parse_command(shortcuts_json["system_functions"].get(key)))

            for key in shortcuts_json["keyboard"]:
                keyboard_shortcuts.append(shortcuts_json["keyboard"].get(key))
                            
    except Exception as E:
        print(f"Error while reading shortcuts.json: {E}.\nQuitting.")
        logging.critical("Error while reading shortcuts.json")
        exit()


def keyboard_shortcut(keyboard, index):
    # https://pynput.readthedocs.io/en/latest/keyboard.html#pynput.keyboard.Key
    keys = {
        "alt":Key.alt,
        "alt_gr":Key.alt_gr,
        "alt_r":Key.alt_r,
        "alt_l":Key.alt_l,
        "backspace":Key.backspace,
        "caps_lock":Key.caps_lock,
        "cmd":Key.cmd,
        "cmd_l":Key.cmd_l,
        "cmd_r":Key.cmd_r,
        "ctrl":Key.ctrl,
        "ctrl_l":Key.ctrl_l,
        "ctrl_r":Key.ctrl_r,
        "delete":Key.delete,
        "down":Key.down,
        "end":Key.end,
        "enter":Key.enter,
        "esc":Key.esc,
        "f1":Key.f1,
        "f2":Key.f2,
        "f3":Key.f3,
        "f4":Key.f4,
        "f5":Key.f5,
        "f6":Key.f6,
        "f7":Key.f7,
        "f8":Key.f8,
        "f9":Key.f9,
        "f10":Key.f10,
        "f11":Key.f11,
        "f12":Key.f12,
        "f13":Key.f13,
        "f14":Key.f14,
        "f15":Key.f15,
        "f16":Key.f16,
        "f17":Key.f17,
        "f18":Key.f18,
        "f19":Key.f19,
        "f10":Key.f20,
        "home":Key.home,
        "insert":Key.insert,
        "left":Key.left,
        "media_next":Key.media_next,
        "media_play_pause":Key.media_play_pause,
        "media_previous":Key.media_previous,
        "media_volume_down":Key.media_volume_down,
        "media_volume_mute":Key.media_volume_mute,
        "media_volume_up":Key.media_volume_up,
        "menu":Key.menu,
        "num_lock":Key.num_lock,
        "page_down":Key.page_down,
        "page_up":Key.page_up,
        "pause":Key.pause,
        "print_screen":Key.print_screen,
        "right":Key.right,
        "scroll_lock":Key.scroll_lock,
        "shift":Key.shift,
        "shift_l":Key.shift_l,
        "shift_r":Key.shift_r,
        "space":Key.space,
        "tab":Key.tab,
        "up":Key.up,
    }

    index = int(index[1:]) - 1

    press = keyboard_shortcuts[index]

    press = press.split("+")

    if "" in press:
        pass
    else:
        if len(press) == 1:
            if press[0] in keys:
                keyboard.press(keys.get(press[0]))
                keyboard.release(keys.get(press[0]))
            else:
                keyboard.press(press[0])
                keyboard.release(press[0])

        elif len(press) == 2:
            if press[0] in keys:
                first = keys.get(press[0])
            else:
                first = press[0]

            if press[1] in keys:
                second = keys.get(press[1])
            else:
                second = press[1]

            with keyboard.pressed(first):
                keyboard.press(second)
                keyboard.release(second)
            


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

                            elif(
                                data[0] == "s"
                            ):
                                keyboard_shortcut(keyboard, data)

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



    index = int(index[1:]) - 1
    index = int(index[1:]) - 1
