# RASP2PC

A program based on socket protocol that uses a Raspberry Pi with touchscreen to control a computer via shortcuts

![demo](https://user-images.githubusercontent.com/60071372/83892755-62cbcd80-a74f-11ea-87ab-04bca522ce64.gif)

## Index

- [Why?](#why?)
- [How it Works](#how-it-works)
- [Screenshots](#screenshots)
- [Security](#security)
- [Configuration](#configuration)
- [Usage](#usage)
  - [PC Component](#pc-component)
  - [RASP Component](#rasp-component)
  - [RASPBIG Component](#raspbig-component)
  - [RASPCLI Component](#raspcli-component)
- [Default Shortcuts](#default-shortcuts)
  - [System Fuctions](#system-functions)
  - [Programs / Commands](#programs--commands)
  - [Keyboard shortcuts](#keyboard-shortcuts)
- [Technologies](#technologies)
- [Compatibility](#compatibility)
  - [Linux](#linux)
  - [Windows](#windows)
  - [Mac Os](#mac-os)
- [ToDo](#todo)
- [Known Issues](#known-issues)
- [License](#license)

## Why?

Because using the keyboard and mouse, especially while you're doing something else, like video calling, can be really unconfortable. And also, control a computer with a touch screen seems really *c o o l*.

## How it Works

![Rasp2Pc functioning](https://user-images.githubusercontent.com/60071372/81484790-cd6d1480-9248-11ea-8d92-9ec84f5cc686.png)

The project is composed of 3 parts, called "components".

* [**PC Component**](https://github.com/seepiol/Rasp2Pc/blob/master/rasp.py), which runs on the main computer (with linux operating system) and which consists of a socket server
* [**RASP Component**](https://github.com/seepiol/Rasp2Pc/blob/master/rasp.py), which is made to run on a [Raspberry Pi](https://www.raspberrypi.org/) with a touchscreen and it's the client
* [**RASPCLI Component**](https://github.com/seepiol/Rasp2Pc/blob/master/raspcli.py), an alternative to RASP components, for devices that do not have a graphical environment (for example [**Termux**](https://termux.com/) on android)

The RASP (or raspcli) component send an encrypted index to the PC, which corresponds to a certain function. The PC gets the index, run the command and eventually returns the result or the status of the command.

It also exist the [**RASPBIG Component**](https://github.com/seepiol/Rasp2Pc/blob/master/rasp_big.py), which is equal to rasp but the GUI is optimized for high resolution touchscreen monitors (>800x480)

## Screenshots

**[PC Component](https://user-images.githubusercontent.com/60071372/82824947-90408d80-9eaa-11ea-9457-c172377f6858.png)**

**[RASP Component](https://user-images.githubusercontent.com/60071372/82824949-90d92400-9eaa-11ea-8d4e-b58012138afc.png)**

**[RASPCLI Component](https://user-images.githubusercontent.com/60071372/82824929-8880e900-9eaa-11ea-8521-fa99afb0eb06.png)**

**[RASPBIG Component](https://user-images.githubusercontent.com/60071372/86596035-e4568b80-bf99-11ea-9348-0a7fbfae2479.png)**

The user interface may vary depending on the QT settings on your system

## Security

The packets are encrypted before sending with [AES-128](https://en.wikipedia.org/wiki/Advanced_Encryption_Standard)  encryption algorithm. By default is hardcoded a 128 bit key and a 128 bit [initialization vector](https://en.wikipedia.org/wiki/Initialization_vector). Please generate a new key and insert it into the code [on rasp component](https://github.com/seepiol/Rasp2Pc/blob/master/rasp.py#L702), [raspBig component](https://github.com/seepiol/Rasp2Pc/blob/master/rasp_big.py#L702), [raspCli component](https://github.com/seepiol/Rasp2Pc/blob/master/raspcli.py#38) and [on pc component](https://github.com/seepiol/Rasp2Pc/blob/master/pc.py#366)

The library used for the encryption is [PyCryptoDome](https://github.com/Legrandin/pycryptodome)

## Configuration
Make sure that all the dependencies are installed by typing `pip install -r requirements.txt`.
On debian-based distros, install PyQt5 by typing in a terminal window `sudo apt install python3-pyqt5`.

First of all, you need to make sure that the shortcuts file is correct for your pc's system and good for you (more [here](#default-shortcuts))
You have to add the ip address of the PC on the rasp.conf configuration file.
For example, if the ip address of the PC is 192.168.1.20, and the socket is listening to the port 10000 (as default), rasp.conf will be:

```
192.168.1.20, 10000
```

By default is used the port 10000, and the PC accept connection for every IP address. See [usage](#usage) to learn how to bind the server on different address/port.

For security reasons, generate a cryptographic key and insert it into the code (see [security](#security)

## Usage

### PC Component

```
$ cd rasp2pc
$ python3 pc.py
```

Will accept any address on port 10000.
At the moment of the connection you can accept or deny the connection by typing `yes` or `no`

**Yes**

```
('127.0.0.1', 55230) is trying to connect to this pc. 
('127.0.0.1', 55230) seems to be a RASP component
Do you want to accept this connection? <Y es/N o>: y
Connection with ('127.0.0.1', 55230) accepted
```

**No**

```
('127.0.0.1', 55232) is trying to connect to this pc. 
('127.0.0.1', 55232) seems to be a RASP component
Do you want to accept this connection? <Y es/N o>: n
Connection Denied 
```

PC component also support CLI Arguments:

```
$ python pc.py -h
usage: pc.py [-h] [--host HOST] [--port PORT]

Rasp2Pc PC Component

optional arguments:
  -h, --help   show this help message and exit
  --host HOST  the addess the where socket server will be listening (default=everyone)
  --port PORT  the port where the server will be listening (default=10000)
```

If you want to bind the server on a different address or port, you can specify that using

```
$ python3 pc.py --host 192.168.1.20 --port 20222
```

> ⚠️ The ports below 1024 are called "privileged". Theoretically, you can call pc.py with superuser privileges and use there ports, but this is disabled for security reasons.

### RASP Component

Just type

```
$ cd rasp2pc
$ python3 rasp.py
```

in this way, RASP will follow the instructions contained in the [rasp.conf file](#configuration). if you want to change the settings just once, you can do so from the CLI Arguments

```
$ python rasp.py -h
usage: rasp.py [-h] [--host HOST] [--port PORT]

Rasp2Pc RASP Component

optional arguments:
  -h, --help   show this help message and exit
  --host HOST  the addess of the PC Component (default=)
  --port PORT  the port of the PC Component (default=10000)
```

So, if you want to connect the RASP component to a different PC (Ex. `192.168.1.32`) on a different port (Ex. `3042`), you must type

```
$ python rasp.py --host 192.168.1.32 --port 3042
```

ELI5, the cli arguments will temporarily overwrite `rasp.conf` configuration file

### RaspBig Component

The usage is equal to the RASP Component, but the GUI is bigger and T H I C C, made for high resolution monitor (800x420)

### RaspCli Component

This component is the equal to RASP but without GUI.
It's made for non-GUI systems, For example TERMUX on android phones.

type:

```
python raspcli.py --host <pcipaddress> 
```

## Default Shortcuts

By default, the program has 3 system functions shortcuts, 6 shortcuts for launching programs / commands and 6 keyboard shortcuts.

### System Functions

| Function     | Command                          |
| ------------ |:--------------------------------:|
| Reboot PC    | `reboot`                         |
| Lock session | `loginctl lock-session`          |
| Mute audio   | `amixer -D pulse sset Master 0%` |

### Programs / Commands

The labels and the commands are now defined in [shortcuts.csv file](github.com/seepiol/rasp2pc/shortcuts.csv).

For the consistency between rasp(s) component and pc the shortcuts file must be identical.

The file format is `Label,Subprocess Command`. Each shortcut is separated by newline. 

The default programs shortcuts are:

| Program/Action (label)         | Subprocess Command                       |
| ----------------------- |:----------------------------------------:|
| Mozilla Firefox Browser | `firefox`                                |
| Terminal*          | `gnome-terminal`                                |
| Virtualbox              | `virtualbox`                             |
| File Manager*     | `nautilus`                                |
| VS Codium               | `vscodium`                               |
| App Store*               | `pamac-manager`                          |
| Telegram                | `telegram-desktop`                       |
| Libreoffice Launcher    | `libreoffice`                            |
| Mozilla Thunderbird     | `thunderbird`                            |
| Screen Recording        | `simplescreenrecorder --start-recording` |

The actions marked with an asterisk (*) are system specific. 

### Keyboard shortcuts

| Function               | Keys   | Usage       |
|:---------------------- |:------:|:-----------:|
| Undo                   | Ctrl+Z | Everywhere  |
| Copy                   | Ctrl+C | Everywhere  |
| Cut                    | Ctrl+X | Everywhere  |
| Paste                  | Ctrl+V | Everywhere  |
| Mic ON/OFF             | Ctrl+D | Google Meet |
| Webcam ON/OFF          | Ctrl+E | Google Meet |
| Fullscreen             | F11    | Everywhere  |
| Screenshot (spectacle) | PRTSC  | everywhere  |
| Blank                  | -      | -           |
| Blank                  | -      | -           |

If you want to modify the keyboard shortcuts,

1) Modify rasp.py and change the button text, and keep note of the name of the shortcut index (written in the comment next to it)
2) Go on the corresponding function on pc.py and change the keys called by pynput. For example, if you want to add the `Ctrl+F` shortcut, write:

```
with keyboard.pressed(Key.ctrl):
    keyboard.press("f")
    keyboard.release("f")
```

If you want to know more about keyboard shortcuts, view [PyNput documentation](https://pynput.readthedocs.io/en/latest/keyboard.html).


## Technologies

- Python 3
- Socket - communication between pc and raspberry
- Subprocess - execute commands on pc
- [pynput](https://pypi.org/project/pynput) - emulates keyboard shortcuts
- [PyQt5](https://riverbankcomputing.com/software/pyqt/) - GUI for rasp component
- amixer - mute the pc
- [pycrypto](https://pypi.org/project/pycrypto/) - encrypt packets with AES-128 

## Compatibility

I've succesfully tested all the components on these configs:
| Component | OS | Device |
|:----------|:----|:-------|
| PC | Manjaro GNU/Linux (Plasma) | Laptop |
| PC | Manjaro GNU/Linux (Gnome) | Laptop |
| PC | GNU/LINUX antiX-19 | Laptop|
| PC | Microsoft Windows 10* | Laptop |
| PC | WSL Ubuntu (win 10) |Laptop| 
| RASP/RASPBIG | Raspbian GNU/Linux 10 (Buster) | Raspberry Pi 3B+ <br>800x480 5 inch touchscreen monitor|
| RASP/RASPBIG | Manjaro GNU/Linux (Plasma) | Laptop |
| RASP/RASPBIG | Manjaro GNU/Linux (Gnome) | Laptop |
| RASP/RASPBIG | GNU/LINUX antiX-19 | Laptop|
| RASP/RASPBIG | Microsoft Windows 10* | Laptop|
| RASPCLI | Android 10 (Termux) | Google Pixel 3a |

Feel free to test it on your machine and open an issue to let me know if it works.

\* : see [Windows](#windows) for windows configuration

### Linux
I made this on linux, and I've tested on it all of the time. It should work on every distro without problems.

### Windows
To make the PC component compatible with windows, it's enough to customize the shortcuts.csv.
The command should be `start <executable filename>`. If the executable is in the path, is enough to insert `start <name>`.  
For example:<br>
```Firefox, start firefox```.

At the moment, the only way to make the system actions work on windows is to change the code.

RASP and RASPBIG components are compatible by default.

### Mac Os
It teorically works (because it uses the bash shell), both pc and rasp, but I haven't tested yet.


## ToDo

- [x] Basic "PC" component (server)
- [x] Basic "RASP" component (client)
- [x] Add reqirements.txt
- [x] GUI for RASP component (PyQt5)
- [x] Add logging on rasp
- [x] Add more shortcuts
- [x] Add logging on pc
- [x] Implement a better way to choose the pc address on rasp (using rasp.conf file)
- [x] Add CLI arguments on PC component (host and port)
- [x] Add possibility to deny connection on PC and verify that is a RASP component
- [x] Avoid execution by unauthorized devices
- [x] Add tooltips on RASP
- [x] Add popups on rasp component instead of cli messages
- [x] Improve communication security using AES
- [x] Comment the code
- [ ] Improve error handling
- [x] ~~Resolution-responsive UI on rasp component~~ Make a bigger UI
- [x] Add better way to change shortcuts, functions and button text on RASP component from pc
- [x] Android component (RaspCli)
- [X] Windows support
  - [X] Test if is enough to put into shortcuts.CSV the path of the executable file
- [ ] Mac Os support (but i haven't a mac so idk)
- [ ] System Tray Icon and actions (exit, )

## Known Issues

* If the PC component is turned off (Ctrl+C) with a RASP component still connected, PC will give you `Something went wrong: [Errno 98] Address already in use`. This is a system issue. Close the RASP component and wait 1 minute more or less, and restart the PC component

## License

GNU General Public License v3.

See [LICENSE](https://github.com/seepiol/Rasp2Pc/blob/master/LICENSE) for more details .

###### Made with 🖤 during COVID-19 Quarantine
