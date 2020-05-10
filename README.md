# RASP2PC
A program based on socket protocol that uses a Raspberry Pi with touchscreen to control a computer via shortcuts

## Compatibility
I've tested it on Manjaro Linux.
Feel free to test it on your machine and open an issue to let me know if it works.

Should work on most linux distributions.
Functioning on windows is unlikely

## How it Works
The project is divided in the PC component (that acts as a socket server) and the RASP component (is made for raspberry but can be used on other devices).

The most complex part is on the pc. The RASP component send just an index to the PC, which corresponds to a certain function. The PC get the index, run the command and eventually return the result or the status of the command.
![Rasp2Pc functioning](https://user-images.githubusercontent.com/60071372/81484790-cd6d1480-9248-11ea-8d92-9ec84f5cc686.png)


## Technologies
- Python 3
- Socket - communication between pc and raspberry
- Subprocess - execute commands on pc
- [pynput](https://pypi.org/project/pynput) - emulates keyboard shortcuts
- [PyQt5](https://riverbankcomputing.com/software/pyqt/) (Coming soon) - GUI for rasp component

## ToDo
- [x] Basic "PC" component (server)
- [x] Basic "RASP" component (client)
- [x] Add reqirements.txt
- [X] GUI for RASP component (PyQt5)
- [ ] Improve communication security and avoid execution by unauthorized devices
- [ ] Add logging
- [ ] Comment the code
- [ ] GUI mode for choose the pc address on rasp component
- [ ] Better way to change shortcuts, functions and button text on RASP component
- [ ] Possibility to modify the shortcuts from pc
- [ ] Android component


###### Made with 🖤 during COVID-19 Quarantine