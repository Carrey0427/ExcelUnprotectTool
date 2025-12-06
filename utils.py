# utils.py
import os
from pathlib import Path
from tkinter import messagebox

def get_ext(filepath: str) -> str:
    return Path(filepath).suffix.lower()

def is_encrypted(filepath: str) -> bool:
    return False  # 預留未來擴充

def generate_output_name(filepath: str) -> str:
    p = Path(filepath)
    base = p.stem + "_unprotected"
    newfile = p.with_name(base + p.suffix)

    index = 2
    while newfile.exists():
        newfile = p.with_name(f"{base}_v{index}{p.suffix}")
        index += 1
    return str(newfile)

def alert(msg: str):
    messagebox.showinfo("Excel Unprotect Tool", msg)
