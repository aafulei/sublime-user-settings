#!/usr/bin/env python3

# Update "Installed Packages" Section in Readme

# standard
import json
import os
import shutil

# self
import common


DESC = "Update \"Installed Packages\" Section in Readme"
PACKAGE_CONTROL = "Package Control.sublime-settings"
README = "README.md"


def main():
    # 0. ask for confirmation
    if not common.confirm(desc=DESC):
        return

    # 1. change working dir
    os.chdir(os.path.join(os.path.dirname(__file__), ".."))

    # 2. check file existence
    file_list = [PACKAGE_CONTROL, README]
    if not common.check_existence(file_list, required=file_list):
        return

    # 3. package list ===> temp readme
    with open(PACKAGE_CONTROL, "r") as file:
        pc = json.load(file)
        pkg = []
        for p in pc["installed_packages"]:
            # rule out "zzz A File Icon zzz"
            if not p.startswith("zzz"):
                pkg.append(p)
    with common.Prompt("% Create a temp readme"):
        tmp = "{}.tmp".format(README)
    with open(README, "r") as ifile:
        with open(tmp, "w") as ofile:
            # assumption: exactly one "installed packages" header in readme
            inside = False
            written = False
            for line in ifile:
                if ((not inside and line.strip("# \n") == "Installed Packages")
                        or (inside and line.strip().startswith("#"))):
                    inside = not inside
                    if not inside:
                        ofile.write("\n")
                    ofile.write(line)
                    continue
                if inside:
                    if not written:
                        ofile.write("\n```\n")
                        for p in pkg:
                            ofile.write(p + "\n")
                            print("% [P]", p)
                        ofile.write("```\n")
                        written = True
                else:
                    ofile.write(line)
    print("% {} installed package(s)".format(len(pkg)))

    # 4. temp readme ===> readme
    common.move(tmp, README)


if __name__ == "__main__":
    main()
