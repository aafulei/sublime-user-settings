#!/usr/bin/env python3

# Align Linux and Windows Keymaps with macOS Keymap

# standard
import argparse
import os
import platform
import shutil

# self
import common


MACOS = "Default (OSX).sublime-keymap"
LINUX = "Default (Linux).sublime-keymap"
WINDOWS = "Default (Windows).sublime-keymap"


# platform.system() returns Linux, Darwin, Java, Windows or an empty string
SYSTEM = platform.system()
if SYSTEM == "Darwin":
    SYSTEM = "macOS"
    TO_SYS = "Windows"
    SOURCE = MACOS
    TARGET = WINDOWS
elif SYSTEM == "Windows":
    TO_SYS = "macOS"
    SOURCE = WINDOWS
    TARGET = MACOS
else:
    SOURCE = TARGET = ""

ERROR = f"Unsupported system \"{SYSTEM}\". Only supports macOS <---> Windows."
DESC = f"Align Linux and {TO_SYS} Keymaps with {SYSTEM} Keymap"


def _append(log, lineno, old, new):
    def trim(line):
        if len(line) < 100:
            return line
        return line[:96] + " ...\n"
    log += "% Line {} (old) : {}".format(lineno, trim(old))
    log += "% Line {} (new) : {}".format(lineno, trim(new))
    return log


def main():
    # 0. check target system and ask for confirmation
    if not TARGET:
        print(ERROR)
        return

    if not common.confirm(desc=DESC):
        return

    # 1. change working dir
    os.chdir(os.path.join(os.path.dirname(__file__), ".."))

    # 2. check file existence
    if not common.check_existence([LINUX, MACOS, WINDOWS], required=[SOURCE]):
        return

    # 3. Create a temp target keymap
    tmp = "{}.tmp".format(TARGET)
    log = ""
    with common.Prompt(f"% Create a temp {TO_SYS} keymap"):
        with open(SOURCE, "r") as ifile:
            with open(tmp, "w") as ofile:
                for lineno, line in enumerate(ifile):
                    ls = line.strip()
                    if ls.startswith("//") and ls.endswith(TO_SYS):
                        new = line.replace("// ", "", 1)
                        log = _append(log, lineno, line, new)
                        ofile.write(new)
                    elif not ls.startswith("//") and ls.endswith(SYSTEM):
                        new = line.replace("{", "// {", 1)
                        log = _append(log, lineno, line, new)
                        ofile.write(new)
                    else:
                        ofile.write(line)
    print(log, end="")

    # 4. temp target keymap ===> target keymap
    common.move(tmp, TARGET)

    # 5. macOS keymap ===> Linux keymap
    common.copy(MACOS, LINUX)


if __name__ == "__main__":
    main()
