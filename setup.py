# Program Name: Mp3 Music Player
# Created by: Bryant Liu
# Date Created: January 24 2021

from cx_Freeze import setup, Executable

executables = [
    Executable(
        "main_up.py",
        targetName="Unidentified Player.exe",
        icon="icoUP.ico"
        )
    ]

setup(
    name="Unidentified Player",
    version="1.0.0",
    description="Beta Release",
    executables=executables,
    options={"build_exe": {"include_files": ["iconUP.png"]}}
)
