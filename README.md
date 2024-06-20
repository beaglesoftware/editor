# beagleeditor
A minimal editor called BeagleEditor
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
##### FreeBSD (Termux doesn't work because BeagleEditor is a GUI application)
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
4. More features coming soon
## Adding Plugins
First, download plugins from [BeagleEditor Plugins GitHub repository](https://github.com/MaArasteh/beagleeditor-plugins) (You can clone it with Git, going to Code > Download ZIP or select the plugin you want)

Then, put it in a folder named "plugins" in BeagleEditor destination

Open BeagleEditor, then you see the plugin/plugins added to Plugins menu in editor (If you don't put plugins, Plugins menu will be empty)
### How to write plugins
You can fork [this repository](https://github.com/MaArasteh/beagleeditor-plugins) or create repository yourself

Create a Python file

Write the plugin

Then put a function in your code to run plugin from beagleeditor with name: run_from_beagleeditor() like the example:
```py
def run_from_beagleeditor():
    print("Test of a plugin for BeagleEditor")
```
or
```py
class BeagleEditorPluginExample():
    def __init__(self):
        print("Test of a plugin for BeagleEditor")

def run_from_beagleeditor():
    example = BeagleEditorPluginExample()
    example() # I'm not sure this is correct
```
Note: If you are writing GUI plugin, you can't use PyQt6 because it may cause "QtCoreApplication::exec: The event loop is already running" error

Then test it by putting the file into "plugins" folder.

Even, you can open a pull request
## Future of BeagleEditor
1. Support for Markdown
2. A terminal for BeagleEditor
3. Undo, Redo
4. Running Python file
