# RASP2PC
A program based on socket protocol that uses a Raspberry Pi with touchscreen to control a computer via shortcuts

![demo](https://user-images.githubusercontent.com/60071372/83892755-62cbcd80-a74f-11ea-87ab-04bca522ce64.gif)

## Index
  - [How it Works](#how-it-works)
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
  - [ToDo](#todo)
  - [Known Issues](#known-issues)
  - [License](#license)
         


## How it Works

![Rasp2Pc functioning](https://user-images.githubusercontent.com/60071372/81484790-cd6d1480-9248-11ea-8d92-9ec84f5cc686.png)

The project is composed of 3 parts, called "components".

* **PC Component**, which runs on the main computer (with linux operating system) and which consists of a socket server
* **RASP Component**, which is made to run on a [Raspberry Pi](https://www.raspberrypi.org/) with a touchscreen and it's the client
* **RASPCLI Component**, an alternative to RASP components, for devices that do not have a graphical environment (for example **[Termux](https://termux.com/) on android**)

The RASP (or raspcli) component send an encrypted index to the PC, which corresponds to a certain function. The PC gets the index, run the command and eventually returns the result or the status of the command.

## Screenshots
**[PC Component](https://user-images.githubusercontent.com/60071372/82824947-90408d80-9eaa-11ea-9457-c172377f6858.png)**

**[RASP Component](https://user-images.githubusercontent.com/60071372/82824949-90d92400-9eaa-11ea-8d4e-b58012138afc.png)**

**[RASPCLI Component](https://user-images.githubusercontent.com/60071372/82824929-8880e900-9eaa-11ea-8521-fa99afb0eb06.png)**

## Security
The packets are encrypted before sending with [AES-128](https://en.wikipedia.org/wiki/Advanced_Encryption_Standard)  encryption algorithm. By default is hardcoded a 128 bit key and a 128 bit [initialization vector](https://en.wikipedia.org/wiki/Initialization_vector). Please generate a new key and insert it into the code [on rasp component](https://github.com/seepiol/Rasp2Pc/blob/master/rasp.py#L700), [raspCli component](https://github.com/seepiol/Rasp2Pc/blob/master/raspcli.py#40) and [on pc component](https://github.com/seepiol/Rasp2Pc/blob/master/pc.py#L291)

The library used for the encryption is [PyCryptoDome](https://github.com/Legrandin/pycryptodome)

## Configuration
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
This is equal to the RASP Component, but the GUI is bigger and T H I C C, made for high resolution monitor (800x420)

### RaspCli Component
This component is the equal to RASP but without GUI.
It's made for non-GUI systems, For example TERMUX on android phones.

type:
```
python raspcli.py --host <pcipaddress> 
```
## Default Shortcuts

![Rasp Ui](https://user-images.githubusercontent.com/60071372/82150926-18df7e00-985a-11ea-9746-9316ddae0272.png)

By default, the program has 3 system functions shortcuts, 6 shortcuts for launching programs / commands and 6 keyboard shortcuts.

### System Functions
| Function | Command |
|----------|:--------:|
| Reboot PC | `reboot` |
| Lock session | `loginctl lock-session` |
| Mute audio | `amixer -D pulse sset Master 0%` |

### Programs / Commands

| Program/Action | Subprocess Command |
|----------------|:------------------:|
| Mozilla Firefox Browser | `firefox` |
| Terminal (KDE) | `konsole` |
| Virtualbox | `virtualbox` |
| File Manager (KDE) | `dolphin` |
| VS Codium | `vscodium` |
| App Store | `pamac-manager` |
| Telegram | `telegram-desktop` |
| Libreoffice Launcher | `libreoffice` |
| Mozilla Thunderbird | `thunderbird` | 
| Screen Recording | `simplescreenrecorder --start-recording` |



### Keyboard shortcuts

| Function | Keys | Usage |
|:----------|:----:|:-------:|
| Undo | Ctrl+Z | Everywhere |
| Copy | Ctrl+C | Everywhere |
| Cut | Ctrl+X | Everywhere |
| Paste | Ctrl+V | Everywhere |
| Mic ON/OFF | Ctrl+D | Google Meet |
| Webcam ON/OFF | Ctrl+E | Google Meet |
| Fullscreen | F11 | Everywhere |
| Screenshot (spectacle) | PRTSC |everywhere|
| Blank | -| -|
| Blank | -|- |


An important future part of this program is the shortcuts costumization. If you want to modify it now, you have to 

1) Modify rasp.py and change the button text, and keep note of the name of the index (written in the comment next to it)
2) Go on the corresponding function on pc.py and change the command called by subprocess: `subprocess.Popen("insert the command here", shell=True)`. The command will be the one that, as terminal, launches the application

The same goes for keyboard shortcuts, with the difference that, for example, if you want to add the `Ctrl+F` shortcut, write:

```
with keyboard.pressed(Key.ctrl):
    keyboard.press("f")
    keyboard.release("f")
```
If you want to know more about keyboard shortcuts, view [PyNput documentation](https://pynput.readthedocs.io/en/latest/keyboard.html).


I know that's a crappy way to do that, I'm working about that. If you have any suggestion about how to do that, please open a documentation issue and let me know!


## Technologies
- Python 3
- Socket - communication between pc and raspberry
- Subprocess - execute commands on pc
- [pynput](https://pypi.org/project/pynput) - emulates keyboard shortcuts
- [PyQt5](https://riverbankcomputing.com/software/pyqt/) - GUI for rasp component
- amixer - mute the pc
- [pycrypto](https://pypi.org/project/pycrypto/) - encrypt packets with AES-128 


## Compatibility
I've tested components on these machines/os:
| Component | OS | Device |
|:----------|:----:|:-------:|
| PC | Manjaro GNU/Linux (Plasma) | Laptop |
| RASP/RASPBIG | Raspbian GNU/Linux 10 (Buster) | Raspberry Pi 3B+ - 800x480 5 inch touchscreen monitor|
| RASP/RASPBIG | Manjaro GNU/Linux (Plasma) | Laptop |
| RASPCLI | Android 10 (Termux) | Google Pixel 3a |

Feel free to test it on your machine and open an issue to let me know if it works.

Should work on most linux distributions.
Functioning on windows is unlikely.

## ToDo
- [x] Basic "PC" component (server)
- [x] Basic "RASP" component (client)
- [x] Add reqirements.txt
- [X] GUI for RASP component (PyQt5)
- [X] Add logging on rasp
- [X] Add more shortcuts
- [X] Add logging on pc
- [X] Implement a better way to choose the pc address on rasp (using rasp.conf file)
- [X] Add CLI arguments on PC component (host and port)
- [X] Add possibility to deny connection on PC and verify that is a RASP component
- [X] Avoid execution by unauthorized devices
- [X] Add tooltips on RASP
- [X] Add popups on rasp component instead of cli messages
- [X] Improve communication security using AES
- [X] Comment the code
- [ ] Improve error handling
- [ ] Implement multilevel communication([see here](https://github.com/seepiol/Rasp2Pc/issues/6))
- [ ] Resolution-responsive UI on rasp component. [See here](https://www.blog.pythonlibrary.org/2015/08/18/getting-your-screen-resolution-with-python/) and [here](https://stackoverflow.com/questions/43904594/pyqt-adjusting-for-different-screen-resolution)
- [ ] Add better way to change shortcuts, functions and button text on RASP component from pc
- [ ] Android component
- [ ] Windows support
- [ ] Mac Os support (but i haven't a mac so idk)

## Known Issues
* If the PC component is turned off (Ctrl+C) with a RASP component still connected, PC will give you `Something went wrong: [Errno 98] Address already in use`. This is a system issue. Close the RASP component and wait 1 minute more or less, and restart the PC component


## License
GNU General Public License v3.

See [LICENSE](https://github.com/seepiol/Rasp2Pc/blob/master/LICENSE) for more details .

###### Made with 🖤 during COVID-19 Quarantine
