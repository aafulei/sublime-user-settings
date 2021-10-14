# My User Settings for Sublime Text

The `User` directory of my Sublime Text, including

1. Key Bindings
2. Preferences
3. Other Overrides
4. User Macros
5. List of Installed Packages
6. Automation Scripts

## Install

*Prerequisite - Package Control*

#### macOS

```sh
cd ~/Library/Application\ Support/Sublime\ Text\ 3/Packages
[ -d "User" ] && mv User User.old && echo "Move directory User ===> User.old"
git clone http://github.com/aafulei/sublime-user-settings.git User
```

#### Windows

```bat
cd %APPDATA%\Sublime Text 3\Packages
if exist User (move /Y User User.old) && (echo "Move directory User ===> User.old")
git clone http://github.com/aafulei/sublime-user-settings.git User
```

## Automate

### 1. Align Linux and Windows Keymaps with macOS Keymap

```sh
./scripts/align-keymap.py
```

#### Sample Run

```
-------------------------------------------------
Align Linux and Windows Keymaps with macOS Keymap
-------------------------------------------------

Do you want to continue (y/N)? Y

% Default (OSX).sublime-keymap ... FOUND
% Default (Linux).sublime-keymap ... FOUND
% Default (Windows).sublime-keymap ... FOUND
% Move Default (Linux).sublime-keymap ===> Default (Linux).sublime-keymap.old ... DONE
% Copy Default (OSX).sublime-keymap ===> Default (Linux).sublime-keymap ... DONE
% Create a temp Windows keymap ... DONE
% Line 137 (old) :     { "keys": ["primary+o"], "command": "prompt_open" }, // macOS
% Line 137 (new) :     // { "keys": ["primary+o"], "command": "prompt_open" }, // macOS
...
% Move Default (Windows).sublime-keymap ===> Default (Windows).sublime-keymap.old ... DONE
% Move Default (Windows).sublime-keymap.tmp ===> Default (Windows).sublime-keymap ... DONE

```

### 2. Update `Installed Packages` Section In Readme

```sh
./scripts/update-readme.py
```

#### Sample Run

```
---------------------------------------------
Update "Installed Packages" Section in Readme
---------------------------------------------

Do you want to continue (y/N)? Y

% Package Control.sublime-settings ... FOUND
% README.md ... FOUND
% Create a temp readme ... DONE
% [P] A File Icon
...
% [P] ToggleSettings
% 32 installed package(s)
% README.md.tmp and README.md have the same content.
% Remove README.md.tmp ... DONE
```

## Installed Packages

```
A File Icon
AutoHotkey
Clang Format
CMake
Compare Side-By-Side
Deselect
Exact Quick Find
Expand Selection to Line Upwards
Expand Selection to Quotes
ExpandRegion
Fold Comments
HexViewer
iOpener
MarkAndMove
Move By Paragraph
MoveTab
OpenHere
Origami
Package Control
PackageResourceViewer
PlantUmlDiagrams
Pretty JSON
RemoteSubl
Save Copy As
SideBarTools
sublime-adapted-plugins
sublime-expand-and-edit
SublimeLinter
SublimeLinter-pycodestyle
Switch View in Group
ToggleSettings
```

## Sublime Text Version

```
Version 3.2.2 (Build 3211) 1 October 2019
```