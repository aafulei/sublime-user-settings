#!/usr/bin/env python3

# Common code for scripts

import argparse
import os
import shutil


YES = "don't ask and yes to all"


class Prompt():
    """A context manager that prints a msg before task and DONE/ERROR after.

    Example
    -------
    with Prompt("Clean up"):
        os.remove("1.tmp")

    will show

    Clean up ... DONE/ERROR
    """
    def __init__(self, msg):
        self.msg = msg

    def __enter__(self):
        print(self.msg, end=" ... ")

    def __exit__(self, e_type, e_value, e_traceback):
        if e_type is not None:
            print("ERROR")
        else:
            print("DONE")


class Result:
    SAME = 0
    DIFFERENT = 1
    NOT_FOUND = 2


def confirm(desc):
    """Ask for confirmation from user."""
    parser = argparse.ArgumentParser(description=desc)
    parser.add_argument("-y", "--yes", action="store_true", help=YES)
    args = parser.parse_args()
    print("-" * len(desc), desc, "-" * len(desc), sep="\n")
    if not args.yes:
        try:
            print()
            ans = input("Do you want to continue (y/N)? ")
        except KeyboardInterrupt:
            print()
            ans = False
        if not ans or not "YES".startswith(ans.upper()):
            return False
        else:
            print()
    return True


def check_existence(file_list, required=[]):
    """Check file existence. Stop if any required file is missing."""
    for x in file_list:
        print("% {}".format(x), end=" ... ")
        if os.path.exists(x):
            print("FOUND")
        else:
            print("NOT FOUND")
            if x in required:
                print("% Cannot proceed without {}. Stop.".format(x))
                return False
    return True


def diff(filename1, filename2):
    """Check if two small text files are different.

    Return
    ------
    Integer.
    0 : same
    1 : different content
    2 : file(s) not found
    """
    try:
        with open(filename1, "r") as f1:
            with open(filename2, "r") as f2:
                a = f1.readlines()
                b = f2.readlines()
                return a != b
    except FileNotFoundError:
        return Result.NOT_FOUND


def _copy_move(src, dest, move=False):
    """Copy/Move from src to dest. Back up if needed.

    Return
    ------
    Boolean.
    True  : Real copy/move happened.
    False : Real copy/move did not happen.
    """
    if dest == src:
        return False
    action = "Move" if move else "Copy"
    func = shutil.move if move else shutil.copy2
    res = diff(dest, src)
    if res:
        if res == Result.DIFFERENT:
            old = dest + ".old"
            with Prompt("% Move {} ===> {}".format(dest, old)):
                shutil.move(dest, old)
        with Prompt("% {} {} ===> {}".format(action, src, dest)):
            func(src, dest)
            return True
    else:
        print("% {} and {} have the same content.".format(src, dest))
        if move:
            with Prompt("% Remove {}".format(src)):
                os.remove(src)
        return False


def copy(src, dest):
    """Copy from src to dest. Back up if needed."""
    return _copy_move(src, dest, move=False)


def move(src, dest):
    """Move src to dest. Back up if needed."""
    return _copy_move(src, dest, move=True)
