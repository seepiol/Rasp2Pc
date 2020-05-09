'''
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
'''

import socket

if __name__ == "__main__":

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as raspsocket:    # Create socket object
        # ATTENTION: You have to modify the line below with the PC ip address and the port (default:10000)
        raspsocket.connect(("<insert pc address here>", 10000))    # Connect to the PC 

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
            while choice not in ["a1","a2","a3","a4","a5","a6", "s1","s2","s3","s4"]:    # Input validation
                choice = input("what to do? :")

            raspsocket.sendall(choice.encode())    # Send the index
            response = raspsocket.recv(1024).decode("ascii")    # Recive the response
            print(response)    # Print the response

