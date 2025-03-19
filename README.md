![BeagleEditor Poster](https://github.com/user-attachments/assets/32bb23ee-f5b4-414d-a715-7e140c07b559)
# BeagleEditor
A code editor powered by beagles.

## Installation
### Using Python (good for someone who uses Mac)
#### Mac
Install Python by going to [Python site](https://www.python.org) or Homebrew:
```
brew install python3
```
Download this repository by going to Code > Download ZIP or use Git to clone
```
git clone https://github.com/beaglesoftware/editor.git
```
Now, install requirements:
```shell
# If you get an error, try using --break-system-packages switch
python3 -m pip install -r requirements.txt
```
Now, run editor by using
```
python3 beagleeditor.py
```
#### Windows
Install Python by going to [Python site](https://python.org)

Clone repository:
```
git clone https://github.com/beaglesoftware/editor.git
```
Now install requirements:
```powershell
py -m pip install -r requirements.txt
```
Run editor using
```
python3 beagleeditor.py
```
### Using executable file
## Windows and Mac
Download from [Releases](https://github.com/beaglesoftware/editor/releases) page and download `BeagleEditor-{latest version}-Installer.exe` for Windows or `BeagleEditor-{latest version}-Mac.zip` or `BeagleEditor-{latest version}-Mac.dmg` for Mac

### Using 'winget'
Run this command:
```
winget install BeagleSoftware.BeagleEditor
```

### Using Homebrew
```
brew install beaglesoftware/tap/beagleeditor
```

## Features
1. Syntax highlighting
2. Autocomplete
3. Compatible with Python, C, CSS, C++, C#, HTML, JavaScript
4. Plugins support
5. Running Python file
6. A terminal for BeagleEditor (It is be avaliable through a plugin)
6. More features coming soon

## What are Plugins?
Read them in [BeagleEditor Plugins wiki](https://github.com/ManiArasteh/editor/wiki/Plugins)

## Future of BeagleEditor
1. Undo, Redo button (There is undo, redo shortcut with Ctrl-Z, Ctrl-Y or Cmd-Z, Cmd-Y)
2. Search and Replace
3. Migrate to TypeScript and Monaco Editor

## Screenshot
<img width="1376" alt="Screenshot 1403-10-07 at 3 30 34 PM" src="https://github.com/user-attachments/assets/d1398c27-9259-4e9b-b6ac-a7be2de7a19f" />

A preview of BeagleEditor
