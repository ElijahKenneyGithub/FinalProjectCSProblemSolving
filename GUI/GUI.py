import tkinter as tk
from tkinter import filedialog
import scipy.io
from scipy.io import wavfile
import pydub
from pydub import AudioSegment
import pygame
import matplotlib.pyplot as plt

class View:
    def __init__(self, root):

        self.root = root
        self.root.title("Directory of GUI")
        self.root.geometry("500x200")

        self.play_button = tk.Button(root, text="Play", command=self.play)
        self.play_button.pack()

        self.load_button = tk.Button(root, text="Load", command=self.load_file)
        self.load_button.pack()

        self.combine_button = tk.Button(root, text="Combine Plots", command=self.combine_plots)
        self.combine_button.pack()

        self.display_button = tk.Button(root, text="Display RT60 Plots", command=self.display_plots)
        self.display_button.pack()

    def play(self):
        # Code for play function goes here
        pass

    def load_file(self):
        # Code for load_file function goes here
        pass

    def combine_plots(self):
        # Code for combine_plots function goes here
        pass

    def display_plots(self):
        # Code for display_plots function goes here
        pass


if __name__ == "__main__":
    root = tk.Tk()
    app = View(root)
    root.mainloop()
