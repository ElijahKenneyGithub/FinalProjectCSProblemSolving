import tkinter as tk
from tkinter.filedialog import askopenfilename
import matplotlib.pyplot as plt
import scipy.io
import numpy as np
import pydub
import pygame
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from scipy.io import wavfile
from pydub import AudioSegment
from tkinter import filedialog


class View:
    def __init__(self, root):

        # All the stuff relating towards plotting, all set to none to prevent errors
        self.sample_rate = None
        self.data = None
        self.spectrum = None
        self.freqs = None
        self.t = None
        self.target_frequency = None
        self.data_in_db = None
        self.rt60 = None
        self.file_path = None

        self.root = root
        self.root.title("Directory of GUI")
        self.root.geometry("1200x800")

        self.play_button = tk.Button(root, text="Play", command=self.play)
        self.play_button.pack()

        self.load_file()

        self.combine_button = tk.Button(root, text="Combine Plots", command=self.combine_plots)
        self.combine_button.pack()

        self.display_button = tk.Button(root, text="Display RT60 Plots", command=self.display_plots)
        self.display_button.pack()

    def play(self):
        pygame.mixer.init() #initialize pygame mixer so we can play the files

        try: #Attempts to play wav file
            pygame.mixer.music.load(self.file_path)
            pygame.mixer.music.play(loops=0)

        except: #Prints error message and prevents fatal error
            print("Could not load, either no file selected or wrong file type")

    def load_file(self):

        try:  # Try to import it into WAV
            def browse():  # Function that will grab the file from the window created when the buttn is clicked n
               self.file_path = askopenfilename(initialdir="/", title="Select File", filetypes=(("Text files", "*.wav"), ("All Files", "*.*")))

            self.root.button = tk.Button(root, text="Load File", command=browse) #Button as seen on GUI
            self.root.button.pack() #displays button

            self.sample_rate, self.data = wavfile.read(self.file_path) #Sample rate and data taken from the file
        except Exception as e:
            print("Error, will not load - Debug further")

    def combine_plots(self):
        # Code for combine_plots function goes here
        pass

    def display_plots(self):

        try:  # Try Except Block for if the wav file is or isn't Mono, if it is mono, it will use the first block,
            # else it will use the second
            self.spectrum, self.freqs, self.t, im = plt.specgram(self.data, Fs=self.sample_rate, NFFT=1024,
                                                                 cmap=plt.get_cmap('autumn_r'))
            plt.title("Frequency Spectrum (?), Frequency vs. Time")
            plt.xlabel("Time (s)")
            plt.ylabel("Frequency (Hz)")
            cbar = plt.colorbar(im)

        except:
            self.spectrum, self.freqs, self.t, im = plt.specgram(np.mean(self.data, axis=1), Fs=self.sample_rate,
                                                                 NFFT=1024,
                                                                 cmap=plt.get_cmap('autumn_r'))
            plt.xlabel("Time (s)")
            plt.ylabel("Frequency (Hz)")
            plt.title("Frequency Spectrum (?), Frequency vs. Time")
            cbar = plt.colorbar(im)

        def find_target_frequency(freqs_para):
            for x in freqs_para:
                print(x)
                if x > 10000:  # This can be changed to find a specific range, standard is 1000
                    break
            return x

        # Finding data/frequency check
        def frequency_check():
            global target_frequency
            target_frequency = find_target_frequency(self.freqs)
            index_of_frequency = np.where(self.freqs == target_frequency)[0][0]
            data_for_frequency = self.spectrum[index_of_frequency]
            if np.any(data_for_frequency == 0):  # Cleans the data incase shenanigans ensue
                data_for_frequency[data_for_frequency == 0] = 1e-10  # Replace zeros with a small non-zero value

            self.data_in_db_fun = 10 * np.log10(data_for_frequency)
            self.data_in_db_fun = 10 * np.log10(data_for_frequency)
            return self.data_in_db_fun

        # Ploting Reverb

        self.data_in_db = frequency_check()
        plt.figure(2)
        plt.plot(self.t, self.data_in_db, linewidth=1, alpha=0.7, color='#004bc6')
        plt.xlabel("Time (s)")
        plt.ylabel("Power (db)")

        canvas = FigureCanvasTkAgg(plt,
                                   master=window)
        canvas.draw()

        index_of_max = np.argmax(self.data_in_db)
        value_of_max = self.data_in_db[index_of_max]
        plt.plot(self.t[index_of_max], self.data_in_db[index_of_max], 'ro')

        sliced_array = self.data_in_db[index_of_max:]
        value_of_max_less_5 = value_of_max - 5

        # Finding nearest Values of -5 and -25 db fr0m max

        def find_nearest_value(array, value):
            array = np.asarray(array)
            idx = (np.abs(array - value)).argmin()
            return array[idx]

        value_of_max_less_5 = find_nearest_value(sliced_array, value_of_max_less_5)
        index_of_max_less_5 = np.where(self.data_in_db == value_of_max_less_5)
        plt.plot(self.t[index_of_max_less_5], self.data_in_db[index_of_max_less_5], 'yo')

        value_of_max_less_25 = value_of_max - 25
        value_of_max_less_25 = find_nearest_value(sliced_array, value_of_max_less_25)
        index_of_max_less_25 = np.where(self.data_in_db == value_of_max_less_25)
        plt.plot(self.t[index_of_max_less_25], self.data_in_db[index_of_max_less_25], 'go')

        # RT20 & RT60
        rt20 = (self.t[index_of_max_less_5] - self.t[index_of_max_less_25])[0]
        self.rt60 = 3 * rt20

        ################### End of Slide's Code ###################

        plt.grid()
        plt.title("Line Plot w/ Maximum, -5 from Max, and -25 from Max")

        plt.show()  # Shows the plot unchanged, line plot

        # Plotting the scatter plot
        alpha = 0.5
        plt.grid()
        plt.title("Scatter + Line Plot w/ Maximum, -5 from Max, and -25 from Max")
        plt.xlabel("Time (s)")
        plt.ylabel("Power (db)")
        plt.plot(self.t, self.data_in_db, linewidth=1, alpha=0.7, color='#004bc6')
        plt.scatter(self.t, self.data_in_db, linewidth=1, alpha=0.7, color='#00008B', )
        plt.plot(self.t[index_of_max], self.data_in_db[index_of_max], 'ro')
        plt.plot(self.t[index_of_max_less_5], self.data_in_db[index_of_max_less_5], 'yo')
        plt.plot(self.t[index_of_max_less_25], self.data_in_db[index_of_max_less_25], 'go')
        plt.show()  # Shows the line plot + scatter plot of the wav file

        # Statistical Analysis of Frequency
        Standard_Dev_Freq = (np.std(self.freqs))
        Average_Freq = np.average(abs(self.freqs))
        Median_Freq = np.median(self.freqs)
        Max_Freq = np.max(self.freqs)
        Min_Freq = np.min(self.freqs)

        # Statistical Analysis of Decibels
        Standard_Dev_db = int(np.std(self.data_in_db))
        Average_db = np.average(abs(self.data_in_db))
        Median_db = np.median(self.data_in_db)
        Max_db = np.max(self.data_in_db)
        Min_db = np.min(self.data_in_db)

        print("\nThe RT60 reverb time at Freq", (target_frequency), "Hz is", round(abs(rt60), 2) * 1.5, "seconds.\n")
        print("Standard Deviation for frequency is:", Standard_Dev_Freq)
        print("Average for frequency from 0 is:", Average_Freq)
        print("Median for frequency is:", Median_Freq)
        print("Maximum for frequency is:", Max_Freq)
        print("Minimum for frequency is:", Min_Freq)

        print("\n")

        print("Standard Deviation for decibels is:", Standard_Dev_db)
        print("Average for decibels from 0 is:", Average_db)
        print("Median for decibels is:", Median_db)
        print("Maximum for decibels is:", Max_db)
        print("Minimum for decibels is:", Min_db)


if __name__ == "__main__":
    root = tk.Tk()
    app = View(root)
    root.mainloop()
