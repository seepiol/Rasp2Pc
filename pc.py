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

import time
import socket
import subprocess
from pynput.keyboard import Key, Controller
import logging
import argparse
from Crypto.Cipher import AES
import notify2

HOST = ""  # Address
PORT = 10000  # Port


def sysf1():
    """
    Reboot the system
    """
    logging.info("rebooting system")    # Logging
    subprocess.Popen(["reboot"], shell=False)   # Run the command
    return "Reboot"  # action name


def sysf2():
    """
    Lock the session
    """
    logging.info("Locking the session")
    subprocess.Popen(["loginctl", "lock-session"], shell=False)
    return "lock"


def sysf3():
    """
    Mute the audio
    """
    logging.info("Turning volume to 0%")
    subprocess.Popen(["amixer", "-D", "pulse", "sset", "Master", "0%"], shell=False)
    return "mute"


def app1():
    """
    Launch Firefox web Browser
    """
    logging.info("Launching firefox")
    subprocess.Popen("firefox", shell=False)
    return "firefox"


def app2():
    """
    Open a terminal window
    """
    logging.info("Launching konsole")
    subprocess.Popen("konsole", shell=False)
    return "terminal"


def app3():
    """
    Launch VirtualBox
    """
    logging.info("launching virtualbox")
    subprocess.Popen("virtualbox", shell=False)
    return "virtualbox"


def app4():
    """
    Launch the File Manager (dolphin)
    """
    logging.info("launching dolphin")
    subprocess.Popen("dolphin", shell=False)
    return "dolphin"


def app5():
    """
    Run VSCodium
    """
    logging.info("launching vscodium")
    subprocess.Popen("vscodium", shell=False)
    return "VSCodium"


def app6():
    """
    Launch app store (pamac manager)
    """
    logging.info("launching pamac manager")
    subprocess.Popen("pamac-manager", shell=False)
    return "Store"


def app7():
    """
    Launch Telegram
    """
    logging.info("launching telegram")
    subprocess.Popen("telegram-desktop", shell=False)
    return "telegram"


def app8():
    """
    Launch Libreofice launcher
    """
    logging.info("launching libreoffice")
    subprocess.Popen("libreoffice", shell=False)
    return "libreoffice"


def app9():
    """
    Run Thunderbird
    """
    logging.info("launching thunderbird")
    subprocess.Popen("thunderbird", shell=False)
    return "thunderbird"


def app10():
    """
    Record screen with simplescreenrecorder
    """
    logging.info("recording screen")
    subprocess.Popen(["simplescreenrecorder", "--start-recording"], shell=False)
    return "screen recording"


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
    return "undo"


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
    return "copy"


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
    return "cut"


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
    return "paste"


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
    return "webcam"


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
    return "microphone"


def short7():
    """
    F11
    Make full screen
    Usable everywhere
    """
    logging.info("F11")
    keyboard.press(Key.f11)
    keyboard.release(Key.f11)
    return "fullscreen"


def short8():
    """
    PRT-SC
    Print Screen (Screenshot)
    Usable everywhere
    """
    logging.info("PRT SC")
    keyboard.press(Key.print_screen)
    keyboard.release(Key.print_screen)
    return "screenshot"


def short9():
    logging.info("Blank")
    return 


def short10():
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
    logging.info("Decrypting the index")
    index = crytool.decrypt(crypted_index).decode("ascii")  # Decrypting
    index = index.replace(" ", "")  # Replacing whitespaces with blankstring
    return index

def send_notification(title, message):
    # Avoid a weird bug with fstrings
    #title=title
    #message=message
    #n = notify2.Notification(title,
    #                        message
    #                        )
    #time.sleep(1)
    #try:
    #    n.show()
    #except: 
    #    pass
    pass

if __name__ == "__main__":
    # AES encrypter / decrypter
    #                 A casual 128bit key                A casual 128bit Initialization vector
    crytool = AES.new(b"ghnmXRHOwJ2j1Qfr", AES.MODE_CBC, b"127jH6VBnm09Lkqw")

    # Setting up the logger
    logging.basicConfig(
        filename="pc.log",
        filemode="w",
        format="%(asctime)s - %(levelname)s - %(message)s",
        level=logging.INFO,
    )

    keyboard = Controller()  # Create a virtual keyboard

    # Notifications settings
    notify2.init("RASP2PC")
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


    logging.info("PC Component started")
    try:
        logging.info("Creating socket object")
        with socket.socket(
            socket.AF_INET, socket.SOCK_STREAM
        ) as sock:  # creating socket object
            sock.bind((HOST, PORT))  # binding socket on {host:port}

            # Start notification
            send_notification("Start","Pc component is running.")

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

                # connection notification
                send_notification("Connection", f"{client_address[0]}:{str(client_address[1])} Is trying to connect to this pc")

                # Connection Control
                print(f"{client_address} is trying to connect to this pc. ")

                msg = conn.recv(1024).decode("ascii")
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
                    conn.send("ConnectionAccepted".encode())
                    pass
                else:
                    print("Connection Denied")
                    logging.info("Connection Denied")
                    conn.send("ConnectionDenied".encode())
                    conn.close()

                try:
                    
                    action_title=None
                    while True:
                        logging.info("Reciving the index")
                        # Reciving the encrypted index directly as an argument for decrypt_index()
                        data = decrypt_index(conn.recv(1024))
                        logging.info(f"{client_address} has requested {data}")

                        # Execute the index corresponding program or shortcut
                        if data == "a1":
                            action_title = app1()
                        elif data == "a2":
                            action_title = app2()
                        elif data == "a3":
                            action_title = app3()
                        elif data == "a4":
                            action_title = app4()
                        elif data == "a5":
                            action_title = app5()
                        elif data == "a6":
                            action_title = app6()
                        elif data == "a7":
                            action_title = app7()
                        elif data == "a8":
                            action_title = app8()
                        elif data == "a9":
                            action_title = app9()
                        elif data == "a10":
                            action_title = app10()

                        elif data == "s1":
                            action_title = short1()
                        elif data == "s2":
                            action_title = short2()
                        elif data == "s3":
                            action_title = short3()
                        elif data == "s4":
                            action_title = short4()
                        elif data == "s5":
                            action_title = short5()
                        elif data == "s6":
                            action_title = short6()
                        elif data == "s7":
                            action_title = short7()
                        elif data == "s8":
                            action_title = short8()
                        elif data == "s9":
                            action_title = short9()
                        elif data == "s10":
                            action_title = short10()

                        elif data == "sf1":
                            action_title = sysf1()
                        elif data == "sf2":
                            action_title = sysf2()
                        elif data == "sf3":
                            action_title = sysf3()
                        
                        if action_title != None:
                            # Notification
                            send_notification("Rasp2Pc Action", f"Action {action_title}")

                        esit = "ok"

                        conn.send(esit.encode())  # sending a "fake" confirm message

                except IOError:
                    logging.info("RASP Disconnected")

    except KeyboardInterrupt:
        logging.info("KeyboardInterrupt: quitting")
        print("Closed by keyboard. Bye")
        sock.close()
        exit()

    except IOError as E:
        logging.info("RASP disconnected")
        print(E)
        pass

    except Exception as e:
        print("Something went wrong:", e)
        logging.info(f"Error Happened {e}. closing the socket.")
        sock.close()
        exit()
