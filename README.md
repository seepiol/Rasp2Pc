# RASP2PC
A program based on socket protocol that uses a Raspberry Pi with touchscreen to control a computer via shortcuts

## Compatibility
I've tested it on Manjaro Linux.
Feel free to test it on your machine and open an issue to let me know if it works.

Should work on most linux distributions.
Functioning on windows is unlikely due to the 

## How it Works
The project is divided in the PC component (that acts as a socket server) and the RASP component (is made for raspberry but can be used on other devices).

The most complex part is on the pc. The RASP component send just an index to the PC, which corresponds to a certain function. The PC get the index, run the command and eventually return the result or the status of the command.

![Rasp2Pc functioning](https://user-images.githubusercontent.com/60071372/81484790-cd6d1480-9248-11ea-8d92-9ec84f5cc686.png)

## Configuration
You have to add the ip address of the PC [here](https://github.com/seepiol/Rasp2Pc/blob/master/rasp.py#L25).

By default is used the port 10000, and the PC accept connection for every IP address. To change it, [write the RASP IP here](https://github.com/seepiol/Rasp2Pc/blob/master/pc.py#L27)

## Default Shortcuts
By default, the program has 6 shortcuts for launching programs / commands and 6 keyboard shortcuts.

Programs / Commands

- Firefox Web Browser
- Terminal (Konsole)
- Virtualbox
- File manager (Dolphin)
- VS Codium
- Lock the session (using loginctl)

Keyboard shortcuts

- Undo (Ctrl+Z) (Usable everywhere)
- Copy (Ctrl+C) (Usable everywhere)
- Cut (Ctrl+X) (Usable everywhere)
- Paste (Ctrl+V) (Usable everywhere)
- Turn on/off webcam on GMeet (Ctrl+D) (Usable on meet.google.com)
- Turn on/off mic on Gmeet (Ctrl+E) (Usable on meet.google.com)

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

## ToDo
- [x] Basic "PC" component (server)
- [x] Basic "RASP" component (client)
- [x] Add reqirements.txt
- [X] GUI for RASP component (PyQt5)
- [X] Add logging on rasp
- [ ] Add more shortcuts
- [ ] Improve communication security and avoid execution by unauthorized devices
- [ ] Add logging on pc
- [ ] Comment the code
- [ ] Add GUI way for choose the pc address on rasp component
- [ ] Add better way to change shortcuts, functions and button text on RASP component
- [ ] Possibility to modify the shortcuts from pc
- [ ] Android component


###### Made with 🖤 during COVID-19 Quarantine
