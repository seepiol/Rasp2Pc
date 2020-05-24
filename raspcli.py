'''
    WARNING: THIS ISN'T READY YET
    
    Rasp2PC - RASP CLI Component
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
import argparse
import logging

if __name__ == "__main__":

    logging.basicConfig(
        filename="raspcli.log",
        filemode="w",
        format="%(asctime)s - %(levelname)s - %(message)s",
        level=logging.INFO,
    )

    parser = argparse.ArgumentParser(description="Rasp2Pc RASP Component")

    parser.add_argument(
        "--host",
        type=str,
        required=True,
        help=f"the addess of the PC Component (Required)"
    )

    parser.add_argument(
        "--port",
        type=int,
        default=10000,
        help=f"the port of the PC Component (default=10000)",
    )

    logging.info("Getting cli args")
    args = parser.parse_args()
    PC_HOST = args.host
    PC_PORT = args.port

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as raspsocket:    # Create socket object
        # ATTENTION: You have to modify the line below with the PC ip address and the port (default:10000)
        raspsocket.connect((PC_HOST, PC_PORT))    # Connect to the PC 

        while True:
            print("""
a1)
a2)
a3)
a4)
a5)
a6)
a7)
a8)
a9)
a10)

s1)
s2)
s3)
s4)
s5)
s6)
s7)
s8)
s9)
s10)

sysf1)
sysf2)
sysf3)
            """)
            choice = input("What to do? :")
            while choice not in ["a1","a2","a3","a4","a5","a6","a7","a8","a9","a10", "s1","s2","s3","s4","s5","s6","s7","s8","s9","s10","sysf1","sysf2","sysf3"]:    # Input validation
                choice = input("what to do? :")

            raspsocket.sendall(choice.encode())    # Send the index
            response = raspsocket.recv(1024).decode("ascii")    # Recive the response
            print(response)    # Print the response