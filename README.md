# BeagleEditor
A code editor called BeagleEditor
## Installation
### By using Python (good for people who uses Mac or Linux)
#### Mac
Install Python by going to [Python site](https://www.python.org) or Homebrew (I only have Windows. I'm not sure this is the correct command)
```
brew install python3
```
(If it's not correct please Google it)
then, install PyQt6 using Pip
```
pip install PyQt6
```
Download this repository by going to Code > Download ZIP or use Git to clone
```
git clone github.com/MaArasteh/beagleeditor.git
```
Now, run editor by using
```
python3 main.py <filename>
```
#### Linux
Install Python3 (No needed, but you can check if Python installed or not)
##### Debian / Ubuntu
```
sudo apt install python3
```
##### Fedora / Red Hat
```
sudo dnf install python3
```
##### FreeBSD (Termux doesn't work anymore because BeagleEditor is now a GUI application)
```
pkg install python
```
(Install or Update Python depending on your Linux distribution)
Then, install git depending on your Linux distribution
Clone repository by using command below
```
git clone https://github.com/MaArasteh/beagleeditor.git
```
Install PyQt6 by using command below
```
pip install PyQt6
```
Run Editor by changing directory to beagleeditor and running main.py by using argument below
```
python main.py <filename>
```
#### Windows
Install Python and Git from their website
[https://python.org/](https://www.python.org)
[https://git-scm.com/](https://git-scm.com/)
Then, install PyQt6 by using Pip
```
pip install PyQt6
```
Clone repository
```
git clone https://github.com/MaArasteh/beagleeditor.git
```
Run editor by using command below
```
python main.py <filename>
```
### By using executable file (Only on Windows) (Windows 8, 8.1, 10 and 11)
Download .exe file from [Releases page](https://github.com/MaArasteh/beagleeditor/releases)

Run it by double-clicking on it
## Features
1. Syntax highlighting
2. Autocomplete
3. Compatible with Python, C, CSS, C++, C#, HTML, JavaScript
4. Plugins support
5. Running Python file
6. A terminal for BeagleEditor (It is be avaliable through a plugin)
6. More features coming soon
## What is Plugins
Read them in [BeagleEditor Plugins wiki](https://github.com/MaArasteh/beagleeditor/wiki/Plugins)
## BeagleEditor shell
A terminal only for BeagleEditor with its specified commands.
I don't think terminal works on EXE file. I will test and say the result in Releases page (in v3 release)
### Commands
help - Shows avaliable commands.

help {command} - Shows detail of the command you want

gotodir - Same function with CD command in terminals (Don't confuse with a CD/DVD). Changes directory
goto {env} - Go to an environment

exit - Getting out of BeagleEditor shell
### Environments
git - Git environment with Git commands

py or python - Python environment with running Python executable ability and Python shell
#### Git Commands
status - Show the git status

checkout {branch} - Checkout a specific branch

commit -m {message} - Commit with a message

push - Push the repository to GitHub

exit - Return to the default environment
#### Python Commands
run - Runs Python file

pyshell - Opens Python shell

exit - Return to the default environment
## Future of BeagleEditor
2. Undo, Redo button (There is undo, redo shortcut with Ctrl-Z, Ctrl-Y or Cmd-Z, Cmd-Y)
3. Search and Replace
