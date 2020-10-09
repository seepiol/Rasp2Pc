#!/usr/bin/python3
"""
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
"""

import socket
import argparse
from Crypto.Cipher import AES
import os
import json
# TODO: add logging

system_functions_labels = []
labels = []
keyboard_labels = []


def encrypt_index(index):
    """
    encrypt the index, add whitespace to make the string >= 16 bytes and send the index to PC.

    Args:
        index (string): the index to encrypt

    """
    # AES encrypter / decrypter
    #                 A casual 128bit key                A casual 128bit Initialization vector
    crytool = AES.new(b"ghnmXRHOwJ2j1Qfr", AES.MODE_CBC, b"127jH6VBnm09Lkqw")
    index = index + (16 - len(index)) * " "  # make the index 16 bytes
    cipherindex = crytool.encrypt(index.encode("utf-8"))  # encrypting the index
    raspsocket.send(cipherindex)  # send the index
    return cipherindex


def load_json():
    global labels
    # Loading labels
    try:
        with open("shortcuts.json", "r") as shortcuts_file:
            shortcuts_json = json.load(shortcuts_file)

            for label in shortcuts_json["app"]:
                labels.append(label)

            for label in shortcuts_json["system_functions"]:
                system_functions_labels.append(label)

            for label in shortcuts_json["keyboard"]:
                keyboard_labels.append(label)

    except Exception as E:
        print(f"Error while reading shortcuts.json: {E}.\nQuitting.")
        exit()



if __name__ == "__main__":
    try:
        parser = argparse.ArgumentParser(description="Rasp2Pc RASP Component")

        parser.add_argument(
            "--host",
            type=str,
            required=True,
            help=f"the addess of the PC Component (Required)",
        )

        parser.add_argument(
            "--port",
            type=int,
            default=10000,
            help=f"the port of the PC Component (default=10000)",
        )

        args = parser.parse_args()
        PC_HOST = args.host
        PC_PORT = args.port

        # Loading labels
        load_json()

        with socket.socket(
            socket.AF_INET, socket.SOCK_STREAM
        ) as raspsocket:  # Create socket object
            # ATTENTION: You have to modify the line below with the PC ip address and the port (default:10000)
            raspsocket.connect((PC_HOST, PC_PORT))  # Connect to the PC
            print(f"Connected to {PC_HOST}:{PC_PORT}")

            raspsocket.send(
                "rasp2pc_rasp_component".encode("utf-8")
            )  # Declare to PC that this is a """legit""" rasp component
            print("waiting for PC to accept the connection...")
            connection = raspsocket.recv(1024).decode("utf-8")
            if connection == "ConnectionAccepted":
                print("Connection Accepted")
            else:
                print("Connection Denied")
                raspsocket.close()
                exit()

            while True:
                os.system("clear")
                print(
                    f"""
   __                ____    ___  ___ 
  /__\ __ _ ___ _ __|___ \  / _ \/ __\\
 / \/// _` / __| '_ \ __) |/ /_)/ /   
/ _  \ (_| \__ \ |_) / __// ___/ /___ 
\/ \_/\__,_|___/ .__/_____\/   \____/ 
               |_|                    
RASPCLI COMPONENT
https://gitlab.com/seepiol/rasp2pc

    a1) {labels[0]}
    a2) {labels[1]}
    a3) {labels[2]}
    a4) {labels[3]}
    a5) {labels[4]}
    a6) {labels[5]}
    a7) {labels[6]}
    a8) {labels[7]}
    a9) {labels[8]}
    a10) {labels[9]}

    s1) {keyboard_labels[0]}
    s2) {keyboard_labels[1]}
    s3) {keyboard_labels[2]}
    s4) {keyboard_labels[3]}
    s5) {keyboard_labels[4]}
    s6) {keyboard_labels[5]}
    s7) {keyboard_labels[6]}
    s8) {keyboard_labels[7]}
    s9) {keyboard_labels[8]}
    s10) {keyboard_labels[9]}

    sf1) {system_functions_labels[0].title()}
    sf2) {system_functions_labels[1].title()}
    sf3) {system_functions_labels[2].title()}
                """
                )
                choice = input("What to do? :")
                while choice not in [
                    "a1",
                    "a2",
                    "a3",
                    "a4",
                    "a5",
                    "a6",
                    "a7",
                    "a8",
                    "a9",
                    "a10",
                    "s1",
                    "s2",
                    "s3",
                    "s4",
                    "s5",
                    "s6",
                    "s7",
                    "s8",
                    "s9",
                    "s10",
                    "sf1",
                    "sf2",
                    "sf3",
                ]:  # Input validation
                    choice = input("what to do? :")
                try:
                    print("Sending....")
                    encrypt_index(choice)
                    print(raspsocket.recv(1024).decode("utf-8"))  # Recive the response
                except BrokenPipeError:
                    print("Connection closed or denied by PC.  Quitting.")
                    raspsocket.close()
                    exit()
    except KeyboardInterrupt:
        print("Quitting. Bye")
        try:
            raspsocket.close()
        except NameError:
            pass
        exit()
