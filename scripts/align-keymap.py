#!/usr/bin/env python3

# Align Linux and Windows Keymaps with macOS Keymap

# standard
import argparse
import os
import shutil

# self
import common


DESC = "Align Linux and Windows Keymaps with macOS Keymap"
MACOS = "Default (OSX).sublime-keymap"
LINUX = "Default (Linux).sublime-keymap"
WINDOWS = "Default (Windows).sublime-keymap"


def _append(log, lineno, old, new):
    def trim(line):
        if len(line) < 100:
            return line
        return line[:96] + " ...\n"
    log += "% Line {} (old) : {}".format(lineno, trim(old))
    log += "% Line {} (new) : {}".format(lineno, trim(new))
    return log


def main():
    # 0. ask for confirmation
    if not common.confirm(desc=DESC):
        return

    # 1. change working dir
    os.chdir(os.path.join(os.path.dirname(__file__), ".."))

    # 2. check file existence
    if not common.check_existence([MACOS, LINUX, WINDOWS], required=[MACOS]):
        return

    # 3. macOS keymap ===> Linux keymap
    common.copy(MACOS, LINUX)

    # 4. Create a temp Windows keymap
    tmp = "{}.tmp".format(WINDOWS)
    log = ""
    with common.Prompt("% Create a temp Windows keymap"):
        with open(MACOS, "r") as ifile:
            with open(tmp, "w") as ofile:
                for lineno, line in enumerate(ifile):
                    ls = line.strip()
                    if ls.startswith("//") and ls.endswith("Windows"):
                        new = line.replace("// ", "", 1)
                        log = _append(log, lineno, line, new)
                        ofile.write(new)
                    elif not ls.startswith("//") and ls.endswith("macOS"):
                        new = line.replace("{", "// {", 1)
                        log = _append(log, lineno, line, new)
                        ofile.write(new)
                    else:
                        ofile.write(line)
    print(log, end="")

    # 5. temp Windows keymap ===> Windows keymap
    common.move(tmp, WINDOWS)


if __name__ == "__main__":
    main()
