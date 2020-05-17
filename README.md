# RASP2PC
A program based on socket protocol that uses a Raspberry Pi with touchscreen to control a computer via shortcuts

## Index
  - [Index](#index)
  - [How it Works](#how-it-works)
  - [Configuration](#configuration)
  - [Usage](#usage)
    - [PC Component](#pc-component)
    - [RASP Component](#rasp-component)
  - [Default Shortcuts](#default-shortcuts)
    - [Programs / Commands](#programs--commands)
    - [Keyboard shortcuts](#keyboard-shortcuts)
  - [Technologies](#technologies)
  - [Compatibility](#compatibility)
  - [ToDo](#todo)
  - [Known Issues](#known-issues)
  - [License](#license)
         


## How it Works
The project is divided in the PC component (that acts as a socket server) and the RASP component (is made for raspberry but can be used on other devices).

The most complex part is on the pc. The RASP component send just an index to the PC, which corresponds to a certain function. The PC get the index, run the command and eventually return the result or the status of the command.

![Rasp2Pc functioning](https://user-images.githubusercontent.com/60071372/81484790-cd6d1480-9248-11ea-8d92-9ec84f5cc686.png)

## Configuration
You have to add the ip address of the PC on the rasp.conf configuration file.
For example, if the ip address of the PC is 192.168.1.20, and the socket is listening to the port 10000 (as default), rasp.conf will be:
```
192.168.1.20, 10000
```

By default is used the port 10000, and the PC accept connection for every IP address. See [usage](#usage) to learn how to bind the server on different address/port.

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

If you want to bind the server on a different address or port, you can specify that with CLI arguments
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
If you want to change the pc ip address, see [Configuration](#configuration)

## Default Shortcuts

![Rasp component ui](https://user-images.githubusercontent.com/60071372/82146951-e418fa00-984c-11ea-8a1d-da66f3169d89.png)

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
| Blank |- | -|
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

## Compatibility
I've tested it on Manjaro Linux.
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
- [X] Comment the code
- [X] Implement a better way to choose the pc address on rasp (using rasp.conf file)
- [X] Add CLI arguments on PC component (host and port)
- [X] Add possibility to deny connection on PC and verify that is a RASP component
- [X] Avoid execution by unauthorized devices
- [X] Add tooltips on RASP
- [X] Add popups on rasp component instead of cli messages
- [ ] Resolution-responsive UI on rasp component. [See here](https://www.blog.pythonlibrary.org/2015/08/18/getting-your-screen-resolution-with-python/) and [here](https://stackoverflow.com/questions/43904594/pyqt-adjusting-for-different-screen-resolution)
- [ ] Improve exception
- [ ] Improve communication security
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
