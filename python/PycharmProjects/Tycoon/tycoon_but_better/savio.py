# saveio.py
from __future__ import annotations
import os
from pathlib import Path
from dataclasses import dataclass

GAME_NAME = "TYCOON"

# Cross-platform save root (Documents/TYCOON/saves)
DEFAULT_ROOT = Path.home() / "Documents" / GAME_NAME / "saves"
DEFAULT_ROOT.mkdir(parents=True, exist_ok=True)

# Your exact original 12-line format, preserved
NEW_FILE_FORMAT = (
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

@dataclass
class Profile:
    user: str
    root: Path = DEFAULT_ROOT

    @property
    def save_path(self) -> Path:
        return self.root / self.user

    @property
    def pass_path(self) -> Path:
        return self.root / f"{self.user}pass"

    def exists(self) -> bool:
        return self.save_path.exists()

    def ensure(self) -> None:
        # Creates the data file if missing (same behavior as your doesSaveExist)
        if not self.save_path.exists():
            self.save_path.write_text(NEW_FILE_FORMAT, encoding="utf-8")

    def create_with_password(self, password: str) -> None:
        self.ensure()
        # Create pass file only if missing (original used "x")
        if not self.pass_path.exists():
            self.pass_path.write_text(password, encoding="utf-8")

    def set_password(self, password: str) -> None:
        # mimic your setPassword (open x + append) safely:
        if self.pass_path.exists():
            raise FileExistsError("Password file already exists.")
        self.pass_path.write_text(password, encoding="utf-8")

    def read_password(self) -> str:
        return self.pass_path.read_text(encoding="utf-8") if self.pass_path.exists() else ""

    # --- Data access (lineGrabber/lineUpdater equivalents) ---

    def read_lines(self) -> list[str]:
        self.ensure()
        text = self.save_path.read_text(encoding="utf-8").splitlines()
        # your original returns list[str]
        return [str(x) for x in text]

    def write_lines(self, stats: list[str | int]) -> None:
        self.ensure()
        with self.save_path.open("w", encoding="utf-8") as f:
            for i, val in enumerate(stats):
                f.write(str(val))
                if i < len(stats) - 1:
                    f.write("\n")

# --------- High-level helpers to replace console login ----------

def quick_login(username: str, password: str | None = None) -> tuple[bool, Profile | None, str]:
    """
    Use this from your GUI login screen.
    Returns: (success, profile_or_none, message)
    """
    p = Profile(username)
    if p.exists():
        # existing profile path MUST also have pass file
        saved = p.read_password()
        if saved == "" and password is None:
            return (False, None, "Existing user has no password set; please enter one.")
        if password is None:
            return (False, None, "Password required.")
        if password == saved:
            return (True, p, f"Welcome back {username}!")
        else:
            return (False, None, "Incorrect password.")
    else:
        # create new profile (original: set password and ask to restart)
        if not password:
            return (False, None, "New user—please choose a password.")
        p.create_with_password(password)
        return (True, p, f"Welcome to {GAME_NAME}, {username}! Profile created.")
