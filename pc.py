'''
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
'''

import socket
import subprocess
from pynput.keyboard import Key, Controller

keyboard = Controller()    # Create a virtual keyboard

HOST = ""    # Address 
PORT = 10000    # Port


def app1():
    '''
    Shutdown the PC 
    '''
    #subprocess.Popen("sudo shutdown", shell=True)
    return "unable to shutdown. it require root privileges"    # The shutdown requires root. It's easier delete this function instead find a way to make it without root

def app2():
    '''
    Restart the PC
    '''
    subprocess.Popen("reboot", shell=True)
    return ""
    
def app3():
    '''
    Execute Firefox web Browser
    '''
    subprocess.Popen("firefox", shell=True)
    return ""
    
def app4():
    '''
    Open a terminal window
    '''
    subprocess.Popen("konsole", shell=True)
    return ""

def app5():
    '''
    Lock the current user session
    '''
    subprocess.Popen("loginctl lock-session", shell=True)
    return ""

def app6():
    '''
    Run VSCodium
    '''
    subprocess.Popen("vscodium", shell=True)
    return ""

def short1():
    '''
    Ctrl+Z
    Undo shortcut
    Usable everywhere
    '''
    with keyboard.pressed(Key.ctrl):
        keyboard.press("z")
        keyboard.release("z")

def short2():
    '''
    Ctrl+c
    Copy
    Usable everywhere
    '''
    with keyboard.pressed(Key.ctrl):
        keyboard.press("c")
        keyboard.release("c")

def short3():
    '''
    Ctrl+x
    Cut
    Usable everywhere
    '''
    with keyboard.pressed(Key.ctrl):
        keyboard.press("x")
        keyboard.release("x")

def short4():
    '''
    Ctrl+v
    Paste
    Usable everywhere
    '''
    with keyboard.pressed(Key.ctrl):
        keyboard.press("v")
        keyboard.release("v")


if __name__ == "__main__":

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:    #creating socket object
            sock.bind((HOST, PORT))    #binding socket on {host:port}
            
            sock.listen()    #listening for connection requests

            while True:
                conn, client_address = sock.accept()    #Accepting connection from {address}
                
                while True:
                    data = conn.recv(16).decode("ascii")     # Recive and decode what-to-do index

                    # Execute the index corresponding program or shortcut
                    if data=="a1":
                        app1()
                    elif data=="a2":
                        app2()
                    elif data=="a3":
                        app3()
                    elif data=="a4":
                        app4()
                    elif data=="a5":
                        app5()
                    elif data=="a6":
                        app6()
                    elif data=="s1":
                        short1()
                    elif data=="s2":
                        short2()
                    elif data=="s3":
                        short3()
                    elif data=="s4":
                        short4()
                    esit = "ok"

                    conn.sendall(esit.encode())

    except Exception as e:
        print(e)
        sock.close()