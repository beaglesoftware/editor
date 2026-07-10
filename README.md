![BeagleEditor Poster](https://github.com/user-attachments/assets/32bb23ee-f5b4-414d-a715-7e140c07b559)

# BeagleEditor

A code editor powered by beagles.

> [!NOTE]
> A new version of BeagleEditor is released. This version of it will from now be called BeagleEditor Legacy

## Installation

### Using Python (good for someone who uses Mac)

#### Mac

Install Python by going to [Python site](https://www.python.org) or Homebrew:

```shell
brew install python
```

Download this repository by going to Code > Download ZIP or use Git to clone

```shell
git clone https://github.com/beaglesoftware/editor.git
```

Now, install requirements:

```shell
# If you get an error, try using --break-system-packages switch (but be careful!)
python3 -m pip install -r requirements.txt

```

Now, run editor by using

```shell
python3 beagleeditor.py
```

#### Linux

Install Python by installing it via your package manager:

##### Debian-based (Ubuntu/Debian/Linux Mint)

```shell
sudo apt install python3
```

##### Red Hat-based (Fedora/CentOS/RHEL)

```shell

sudo dnf install python
```

##### Arch (btw)-based (Arch/Manjaro/CachyOS/EndeavourOS)

```shell

sudo pacman -S python
```

Download this repository by going to Code > Download ZIP or use Git to clone

```shell
git clone https://github.com/beaglesoftware/editor.git
```

Now, install requirements:

```shell
# If you get an error, try using --break-system-packages switch (but be careful)
python3 -m pip install -r requirements.txt
```

Now, run editor by using

```shell
python3 beagleeditor.py
```

#### Windows

Install Python by going to [Python site](https://python.org)

Clone repository:

```shell
git clone https://github.com/beaglesoftware/editor.git
```

Now install requirements:

```powershell
py -m pip install -r requirements.txt
```

Run editor using

```shell
python beagleeditor.py
```

### Using executable file

#### Windows and Mac

Download from [Releases](https://github.com/beaglesoftware/editor/releases) page and download `BeagleEditor-{latest version}-Installer.exe` for Windows or `BeagleEditor-{latest version}-Mac.zip` or `BeagleEditor-{latest version}-Mac.dmg` for Mac

#### Using 'winget'

Run this command:

```shell
winget install BeagleSoftware.BeagleEditor
```

#### Using Homebrew

```shell
brew install beaglesoftware/tap/beagleeditor
```

## Features

1. Syntax highlighting
2. Autocomplete
3. Compatible with Python, C, CSS, C++, C#, HTML, JavaScript
4. Plugins support
5. Running Python file
6. A terminal for BeagleEditor (It's avaliable through a plugin)
7. More features coming soon

## What are Plugins?

Read them in [BeagleEditor Plugins wiki](https://github.com/ManiArasteh/editor/wiki/Plugins)

## Future of BeagleEditor

The future of BeagleEditor is already here. See [beagleeditor/editor](https://github.com/beagleeditor/editor) for the new version of BeagleEditor

## Screenshot

<img width="1376" alt="Screenshot 1403-10-07 at 3 30 34 PM" src="https://github.com/user-attachments/assets/d1398c27-9259-4e9b-b6ac-a7be2de7a19f" />

A preview of BeagleEditor on macOS
