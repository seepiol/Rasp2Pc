import socket


if __name__ == "__main__":

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as raspsocket:
        raspsocket.connect(("localhost", 10000))   

        while True:
            print("""
a1) Shutdown system
a2) Reboot system
a3) Open firefox
a4) Open terminal
a5) Lock the system
a6) Open vscodium 
s1) Ctrl-Z
s2) Copy
s3) Cut
s4) Paste
            """)
            choice = input("What to do? :")
            while choice not in ["a1","a2","a3","a4","a5","a6", "s1","s2","s3","s4"]:
                choice = input("what to do? :")

            raspsocket.sendall(choice.encode())
            response = raspsocket.recv(1024).decode("ascii")
            print(response)

