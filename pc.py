import socket
import subprocess
from pynput.keyboard import Key, Controller

keyboard = Controller()

HOST = ""
PORT = 10000


def app1():
    #subprocess.Popen("sudo shutdown", shell=True)
    return "unable to shutdown. it require root privileges"

def app2():
    subprocess.Popen("reboot", shell=True)
    return ""
    
def app3():
    subprocess.Popen("firefox", shell=True)
    return ""
    
def app4():
    subprocess.Popen("konsole", shell=True)
    return ""

def app5():
    subprocess.Popen("loginctl lock-session", shell=True)
    return ""

def app6():
    subprocess.Popen("vscodium", shell=True)
    return ""

def short1():
    with keyboard.pressed(Key.ctrl):
        keyboard.press("z")
        keyboard.release("z")

def short2():
    with keyboard.pressed(Key.ctrl):
        keyboard.press("c")
        keyboard.release("c")

def short3():
    with keyboard.pressed(Key.ctrl):
        keyboard.press("x")
        keyboard.release("x")

def short4():
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
                    data = conn.recv(16).decode("ascii")
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

    except e:
        sock.close()