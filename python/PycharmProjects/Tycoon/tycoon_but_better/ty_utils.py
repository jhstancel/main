# ty_utils.py
# Safe, project-relative save I/O with the same behavior/format as your original utils.py

import os
from pathlib import Path
from typing import List, Union

gameName = "TYCOON"

# Default save root = <this folder>/saveFiles (the game can override this at runtime)
_DEFAULT_ROOT = Path(__file__).resolve().parent / "saveFiles"
_DEFAULT_ROOT.mkdir(parents=True, exist_ok=True)
root: str = str(_DEFAULT_ROOT) + os.sep

# Exact 12-line format preserved from your original file
newFileFormat: str = (
    "0\n"
    "0\n"
    "0\n"
    "0\n"
    "32000000\n"
    "21000000\n"
    "10000000\n"
    "00000000\n"
    "00000000\n"
    "00000000\n"
    "00000000\n"
    "00000000"
)

NOEVENT: int = 0


def _ensure_parent(path_str: str) -> Path:
    """Ensure parent dirs exist and return a Path for the exact file path."""
    p = Path(path_str)
    p.parent.mkdir(parents=True, exist_ok=True)
    return p


def logIn():
    """
    Console login flow (unchanged semantics):
      - If profile file doesn't exist: create it with newFileFormat, ask for password, write <username>pass, and return False
        (so caller can show 'restart to play' and exit).
      - If it exists: prompt password and validate (with retries); on success return username.
    """
    loggedIn = False
    while not loggedIn:
        userName = input("What is your username?\n-->")
        saveName = root + userName
        if doesSaveExist(saveName):
            attempt = input("What is your password?\n-->")
            truePassword = str(passGetter(saveName + "pass"))
            if attempt != truePassword:
                passwordLoopFinished = False
                while not passwordLoopFinished:
                    passAttempts = passwordAuthenticator(attempt, truePassword)
                    if passAttempts == "true":
                        print("Welcome back " + userName + "!")
                        passwordLoopFinished = True
                        loggedIn = True
                        return userName
                    elif passAttempts == "restart":
                        passwordLoopFinished = True
            else:
                loggedIn = True
                print("Welcome back " + userName + "!")
                return userName
        else:
            truePassword = input("Please create a password.\n-->")
            setPassword(saveName + "pass", truePassword)
            print("Please restart the game to play.")
            return False


def doesSaveExist(file: str) -> bool:
    """
    If the save file doesn't exist, create it with newFileFormat and print a welcome.
    Return False in that case (signals 'new user created').
    If it already exists, return True.
    """
    try:
        p = _ensure_parent(file)
        with p.open("x", encoding="utf-8") as inFile:
            inFile.write(newFileFormat)
        print("Welcome to " + gameName + "!")
        return False
    except FileExistsError:
        return True


def passFileCreator(file: str, password: str) -> None:
    p = _ensure_parent(file + "pass")
    with p.open("x", encoding="utf-8") as passFile:
        passFile.write(password)


def passwordAuthenticator(attempt: str, password: str) -> Union[str, bool]:
    """
    Returns:
      - "true" if a retry succeeds
      - "restart" if user cancels with 'c'
      - True if the original attempt matched (kept for backward-compat)
    """
    if attempt != password:
        print('If the username you entered is incorrect, type "c" to cancel.')
        for _ in range(4):
            attempt = input("The password you entered is incorrect. Please reenter your password.\n-->")
            if attempt == password:
                return "true"
            elif attempt == "c":
                return "restart"
    else:
        return True


def setPassword(file: str, password: str) -> None:
    p = _ensure_parent(file)
    if p.exists():
        raise FileExistsError("Password file already exists.")
    with p.open("x", encoding="utf-8") as tempFile:
        tempFile.write(password)


def strToInt(arg) -> Union[int, bool]:
    try:
        return int(arg)
    except ValueError:
        return False


def lineGrabber(file: str) -> List[str]:
    """
    Read all lines as strings. If the save file is missing for some reason,
    create it first with the default format to keep behavior consistent.
    """
    p = _ensure_parent(file)
    if not p.exists():
        p.write_text(newFileFormat, encoding="utf-8")
    with p.open("r", encoding="utf-8") as tempFile:
        ret = tempFile.read().splitlines()
    return [str(x) for x in ret]


def passGetter(file: str) -> str:
    p = _ensure_parent(file)
    if not p.exists():
        return ""
    return p.read_text(encoding="utf-8")


def lineUpdater(file: str, stats: List[Union[str, int]]) -> None:
    """
    Overwrite the save file with the provided list, one value per line.
    Matches your original newline behavior (no trailing newline after last line).
    """
    p = _ensure_parent(file)
    with p.open("w", encoding="utf-8") as tempFile:
        for i, val in enumerate(stats):
            tempFile.write(str(val))
            if i < len(stats) - 1:
                tempFile.write("\n")


def evenOrOdd(num: int) -> str:
    return 'Even' if num % 2 == 0 else 'Odd'
