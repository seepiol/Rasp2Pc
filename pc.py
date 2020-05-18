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

import socket
import subprocess
from pynput.keyboard import Key, Controller
import logging
import argparse

HOST = ""  # Address
PORT = 10000  # Port

def sysf1():
    """
    Reboot the system
    """
    logging.info("rebooting system")
    subprocess.Popen(["reboot"], shell=False)
    return "completed"

def sysf2():
    """
    Lock the session
    """
    logging.info("Locking the session")
    subprocess.Popen(["loginctl", "lock-session"], shell=False)
    return "completed"

def sysf3():
    """
    Mute the audio
    """
    logging.info("Turning volume to 0%")
    subprocess.Popen(["amixer", "-D", "pulse", "sset", "Master", "0%"], shell=False)
    return "completed"

def app1():
    """
    Launch Firefox web Browser
    """
    logging.info("Launching firefox")
    subprocess.Popen("firefox", shell=False)
    return "completed"


def app2():
    """
    Open a terminal window
    """
    logging.info("Launching konsole")
    subprocess.Popen("konsole", shell=False)
    return "completed"


def app3():
    """
    Launch VirtualBox
    """
    logging.info("launching virtualbox")
    subprocess.Popen("virtualbox", shell=False)
    return "completed"


def app4():
    """
    Launch the File Manager (dolphin)
    """
    logging.info("launching dolphin")
    subprocess.Popen("dolphin", shell=False)
    return "completed"


def app5():
    """
    Run VSCodium
    """
    logging.info("launching vscodium")
    subprocess.Popen("vscodium", shell=False)
    return "completed"


def app6():
    """
    Launch app store (pamac manager)
    """
    logging.info("launching pamac manager")
    subprocess.Popen("pamac-manager", shell=False)
    return "completed"


def app7():
    """
    Launch Telegram
    """
    logging.info("launching telegram")
    subprocess.Popen("telegram-desktop", shell=False)
    return "completed"


def app8():
    """
    Launch Libreofice launcher
    """
    logging.info("launching libreoffice")
    subprocess.Popen("libreoffice", shell=False)
    return "completed"


def app9():
    """
    Run Thunderbird
    """
    logging.info("launching thunderbird")
    subprocess.Popen("thunderbird", shell=False)
    return "completed"


def app10():
    """
    Record screen with simplescreenrecorder
    """
    logging.info("recording screen")
    subprocess.Popen(["simplescreenrecorder", "--start-recording"], shell=False)
    return "completed"


def short1():
    """
    Ctrl+Z
    Undo shortcut
    Usable everywhere
    """
    logging.info("Ctrl+z")
    with keyboard.pressed(Key.ctrl):
        keyboard.press("z")
        keyboard.release("z")
    return "completed"


def short2():
    """
    Ctrl+c
    Copy
    Usable everywhere
    """
    logging.info("Ctrl+c")
    with keyboard.pressed(Key.ctrl):
        keyboard.press("c")
        keyboard.release("c")
    return "completed"


def short3():
    """
    Ctrl+x
    Cut
    Usable everywhere
    """
    logging.info("Ctrl+x")
    with keyboard.pressed(Key.ctrl):
        keyboard.press("x")
        keyboard.release("x")
    return "completed"


def short4():
    """
    Ctrl+v
    Paste
    Usable everywhere
    """
    logging.info("Ctrl+v")
    with keyboard.pressed(Key.ctrl):
        keyboard.press("v")
        keyboard.release("v")
    return "completed"


def short5():
    """
    Ctrl+D
    Activate/disactivate the microphone
    Usable on Google Meet
    """
    logging.info("Ctrl+d")
    with keyboard.pressed(Key.ctrl):
        keyboard.press("d")
        keyboard.release("d")
    return "completed"


def short6():
    """
    Ctrl+E
    Activate/disactivate the microphone
    Usable on Google Meet
    """
    logging.info("Ctrl+e")
    with keyboard.pressed(Key.ctrl):
        keyboard.press("e")
        keyboard.release("e")
    return "completed"


def short7():
    """
    F11
    Make full screen
    Usable everywhere
    """
    logging.info("F11")
    keyboard.press(Key.f11)
    keyboard.release(Key.f11)
    return "completed"


def short8():
    logging.info("Blank")
    return "completed"


def short9():
    logging.info("Blank")
    return "completed"


def short10():
    logging.info("Blank")
    return "completed"


if __name__ == "__main__":
    # Setting up the logger
    logging.basicConfig(
        filename="pc.log",
        filemode="w",
        format="%(asctime)s - %(levelname)s - %(message)s",
        level=logging.INFO,
    )

    keyboard = Controller()  # Create a virtual keyboard

    parser = argparse.ArgumentParser(description="Rasp2Pc PC Component")

    parser.add_argument("--host", type=str, default="", 
    help="the addess the where socket server will be listening (default=everyone)")

    parser.add_argument("--port", type=int, default=10000,
    help="the port where the server will be listening (default=10000)")

    args = parser.parse_args()
    
    HOST = args.host
    PORT = args.port
    
    if PORT < 1024:
        print("WARNING: You have selected a privileged port. Please choose a port above 1024")
        logging.critical("Selected a privileged port")

    logging.info("PC Component started")
    try:
        logging.info("Creating socket object")
        with socket.socket(
            socket.AF_INET, socket.SOCK_STREAM
        ) as sock:  # creating socket object
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

                msg = conn.recv(1024).decode("ascii")
                if msg != "rasp2pc_rasp_component":  # Verify if the client is a """legit""" rasp component
                    print(f"{client_address} doesn't seems to be a RASP component")
                else:
                    print(f"{client_address} seems to be a RASP component")

                accept_connection = input("Do you want to accept this connection? [Y/n]: ")
                if accept_connection.lower() in ["y", "yes", ""]:
                    print(f"Connection with {client_address} accepted")
                    logging.info(f"Connection with {client_address} accepted")
                    conn.send("ConnectionAccepted".encode())
                    pass
                else:
                    print("Connection Denied")
                    logging.info("Connection Denied")
                    conn.send("ConnectionDenied".encode())
                    conn.close()

                try:

                    while True:
                        data = conn.recv(16).decode(
                            "ascii"
                        )  # Recive and decode what-to-do index
                        logging.info(f"{client_address} has requested {data}")
                        # Execute the index corresponding program or shortcut
                        if data == "a1":
                            app1()
                        elif data == "a2":
                            app2()
                        elif data == "a3":
                            app3()
                        elif data == "a4":
                            app4()
                        elif data == "a5":
                            app5()
                        elif data == "a6":
                            app6()
                        elif data == "a7":
                            app7()
                        elif data == "a8":
                            app8()
                        elif data == "a9":
                            app9()
                        elif data == "a10":
                            app10()

                        elif data == "s1":
                            short1()
                        elif data == "s2":
                            short2()
                        elif data == "s3":
                            short3()
                        elif data == "s4":
                            short4()
                        elif data == "s5":
                            short5()
                        elif data == "s6":
                            short6()
                        elif data == "s7":
                            short7()
                        elif data == "s8":
                            short8()
                        elif data == "s9":
                            short9()
                        elif data == "s10":
                            short10()

                        elif data == "sf1":
                            sysf1()
                        elif data == "sf2":
                            sysf2()
                        elif data == "sf3":
                            sysf3()

                        esit = "ok"

                        conn.send(esit.encode())

                except IOError:
                    conn.send("TOff_PC".encode())
                    conn.close()

    except KeyboardInterrupt:
        logging.info("KeyboardInterrupt: quitting")
        print("Closed by keyboard. Bye")
        try:
            conn.send("TOff_PC".encode())
            conn.close()
        except NameError:
            pass
        sock.close()
        exit()

    except Exception as e:
        print("Something went wrong:", e)
        try:
            conn.send("TOff_PC".encode())
            conn.close()
        except NameError:
            pass
        logging.info(f"Error Happened {e}. closing the socket.")
        sock.close()
        exit()
