#!/usr/bin/env python3

import os
import sys
import glob
import tkinter as tk
from tkinter import filedialog, messagebox

from Hachoir import Hachoir


def show_message(msg):
    box = tk.Toplevel(root)
    box.title("Terminé!")
    box.geometry("800x200")  # Adjust width/height as desired
    tk.Label(box, text=msg, wraplength=380).pack(expand=True, fill="both", padx=20, pady=20)
    tk.Button(box, text="OK", command=box.destroy).pack(pady=10)
    box.transient(root)
    box.grab_set()
    root.wait_window(box)

def run_hachoir():
    in_dir = input_dir_var.get()
    pattern = pattern_var.get()
    if not in_dir or not pattern:
        return
    out_dir = os.path.join(in_dir, "hached")
    os.makedirs(out_dir, exist_ok=True)
    for fn in glob.glob(os.path.join(in_dir, pattern)):
        basename = os.path.basename(fn)
        outpath = os.path.join(out_dir, basename)
        Hachoir(fn, outpath)
    show_message(f"Les fichiers résultants sont dans:\n{out_dir}")

def select_input_dir():
    # Create a temporary Toplevel to control dialog size
    temp = tk.Toplevel(root)
    temp.geometry("1024x768+20+20")  # Adjust as desired
    temp.withdraw()
    d = filedialog.askdirectory(parent=temp, title="Choisir répertoire")
    temp.destroy()
    if d:
        input_dir_var.set(d)

root = tk.Tk()
root.title("Hachoir GUI")

input_dir_var = tk.StringVar()
pattern_var = tk.StringVar(value="*.jpg")

frame = tk.Frame(root)
frame.pack(padx=10, pady=10)

tk.Label(frame, text="Répertoire des images sources:").grid(row=0, column=0, sticky="e")
tk.Entry(frame, textvariable=input_dir_var, width=40).grid(row=0, column=1, padx=5)
tk.Button(frame, text="Choisir...", command=select_input_dir).grid(row=0, column=2)

tk.Label(frame, text="Filtre:").grid(row=1, column=0, sticky="e")
tk.Entry(frame, textvariable=pattern_var, width=40).grid(row=1, column=1, padx=5)

tk.Button(frame, text="Démarrer", command=run_hachoir).grid(row=2, column=1, pady=10)

root.mainloop()

