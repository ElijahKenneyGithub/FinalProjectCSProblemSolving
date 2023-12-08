import time
import tkinter as tk
from tkinter.filedialog import askopenfilename
import matplotlib.pyplot as plt
import numpy as np
import pygame
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from pydub import AudioSegment as AS
import ffmpeg
import ffprobe



class View:
    def __init__(self, root):

        # All the stuff relating towards plotting, all set to none to prevent errors

        # Statistic vars
        self.Min_db = None
        self.Max_db = None
        self.Median_db = None
        self.Average_db = None
        self.Standard_Dev_db = None
        self.Min_Freq = None
        self.Max_Freq = None
        self.Median_Freq = None
        self.Average_Freq = None
        self.Standard_Dev_Freq = None

        # Plotting vars
        self.sample_rate = None
        self.data = None
        self.spectrum = None
        self.freqs = None
        self.t = None
        self.target_frequency = None
        self.data_in_db = None
        self.rt60 = None


        # GUI vars
        self.file_path = None
        self.file_name = None
        self.wav_version = None
        self.duration = None

        # GUI initialization
        self.root = root
        self.root.title("Directory of GUI")
        self.root.geometry("200x100")

        self.play_button = tk.Button(root, text="Play", command=self.play)
        self.play_button.pack()

        self.load_file()

        self.combine_button = tk.Button(root, text="Combine Plots", command=self.combine_plots)
        self.combine_button.pack()

        self.display_button = tk.Button(root, text="Display Plots", command=self.display_plots)
        self.display_button.pack()






    def play(self):  # This function, when called by a button, plays the song given to it
        global start


        def get_duration(file_path):  # Grabs the duration of the file for display
            audio_file = AS.from_file(file_path)
            self.duration = audio_file.duration_seconds

        # Displaying the name in new window

        new_window = tk.Toplevel(self.root)  # New window is called to start a new window to show songs playing
        new_window.title("Now Playing...")  # Title display
        header = tk.Label(new_window, font=("Times New Roman", 40), text="Now Playing....")  # Header display
        now_playing = tk.Label(new_window, font=("Impact", 120), text=self.file_name)  # Name of File Display
        get_duration(self.file_path)  # Grabs the duration of the file, for later ( in update_time() )

        def update_time():
            # Calculate the time elapsed
            time_elapsed = int(time.time())

            # Update the label with the new time
            wav_duration.config(text=str(int(time_elapsed - start)) + "/" + str(int(self.duration)) + " seconds")

            # Schedule the update after 100 milliseconds (adjust as needed)
            new_window.after(1000, update_time)

        header.pack()
        now_playing.pack()

        try:  # displays the time, errors can occur here occasionally which is why a try block is here
            start = time.time()
            wav_duration = tk.Label(new_window, font=("Times New Roman", 40), text="")
            wav_duration.pack()
        except:
            print("Error getting time")

        pygame.mixer.init()  # initialize pygame mixer so we can play the files

        try:  # Attempts to play wav file
            pygame.mixer.music.load(self.file_path)
            pygame.mixer.music.play(loops=0)

        except:  # Prints error message and prevents fatal error
            print("Could not load, either no file selected or wrong file type")
        update_time()
        new_window.mainloop()

    def load_file(self):
        try:
            def name_getter():  # grabs the name of the file for GUI purposes, only needs to be called the once in practice
                i = len(self.file_path)
                counter = 0
                for x in self.file_path:  # Finds the name of the file and gets rid of the directory parts to display
                    if self.file_path[(i - counter - 4)] == '/':
                        self.file_name = self.file_path[(i - 3 - counter):i - 4]
                        break
                    counter = counter + 1


            def file_finder():
                self.file_path = askopenfilename(initialdir="/", title="Select File",
                                                 filetypes=(
                                                     ("wav File", ".wav"), ("mp3 file", ".mp3"),
                                                     ("All Files", "*.*")))

                def extract_raw_audio(file_path):
                    audio = AS.from_file(file_path)
                    self.sample_rate = audio.frame_rate
                    self.data = np.array(audio.get_array_of_samples())

                extract_raw_audio(self.file_path)



                name_getter()

            self.root.button = tk.Button(root, text="Load File", command=file_finder)
            self.root.button.pack()
            print(self.file_path)
        except:
            print("Error, will not load - Debug further")

    def combine_plots(self):
        # Code for combine_plots function goes here
        pass

    def display_plots(self):
        try:
            fig1, ax1 = plt.subplots(1, 1, figsize=(6, 4))
            fig2, ax2 = plt.subplots(1, 1, figsize=(6, 4))
            fig3, ax3 = plt.subplots(1, 1, figsize=(6, 4))



            if len(self.data.shape) == 1:
                self.spectrum, self.freqs, self.t, im = ax1.specgram(self.data, Fs=self.sample_rate, NFFT=1024,
                                                                     cmap=plt.get_cmap('autumn_r'))
            else:
                self.spectrum, self.freqs, self.t, im = ax1.specgram(np.mean(self.data, axis=1), Fs=self.sample_rate,
                                                                     NFFT=1024, cmap=plt.get_cmap('autumn_r'))
        except:
            print("Error occured trying to display plot")

        ax1.set_title("Frequency Spectrum (?), Frequency vs. Time")
        ax1.set_xlabel("Time (s)")
        ax1.set_ylabel("Frequency (Hz)")

        def find_target_frequency(freqs):
            for x in freqs:
                print(x)
                if x > 1000:  # This can be changed to find a specific range, standard is 1000
                    break
            return x

        def frequency_check():
            global target_frequency
            target_frequency = find_target_frequency(self.freqs)
            index_of_frequency = np.where(self.freqs == target_frequency)[0][0]
            data_for_frequency = self.spectrum[index_of_frequency]
            if np.any(data_for_frequency == 0):  # Cleans the data incase shenanigans ensue
                data_for_frequency[data_for_frequency == 0] = 1e-10  # Replace zeros with a small non-zero value

            data_in_db_fun = 10 * np.log10(data_for_frequency)
            data_in_db_fun = 10 * np.log10(data_for_frequency)
            return data_in_db_fun

        def find_nearest_value(array, value):
            array = np.asarray(array)
            idx = (np.abs(array - value)).argmin()
            return array[idx]

            # Plotting Reverb

        self.data_in_db = frequency_check()
        ax2.plot(self.t, self.data_in_db, linewidth=1, alpha=0.7, color='#004bc6')
        ax2.set_xlabel("Time (s)")
        ax2.set_ylabel("Power (db)")

        index_of_max = np.argmax(self.data_in_db)
        value_of_max = self.data_in_db[index_of_max]
        ax2.plot(self.t[index_of_max], self.data_in_db[index_of_max], 'ro')

        sliced_array = self.data_in_db[index_of_max:]
        value_of_max_less_5 = value_of_max -
        # Finding nearest Values of -5 and -25 db from max
        value_of_max_less_5 = find_nearest_value(sliced_array, value_of_max_less_5)
        index_of_max_less_5 = np.where(self.data_in_db == value_of_max_less_5)
        ax2.plot(self.t[index_of_max_less_5], self.data_in_db[index_of_max_less_5], 'yo')

        value_of_max_less_25 = value_of_max - 25
        value_of_max_less_25 = find_nearest_value(sliced_array, value_of_max_less_25)
        index_of_max_less_25 = np.where(self.data_in_db == value_of_max_less_25)
        ax2.plot(self.t[index_of_max_less_25], self.data_in_db[index_of_max_less_25], 'go')

        # RT20 & RT60
        rt20 = (self.t[index_of_max_less_5] - self.t[index_of_max_less_25])[0]
        self.rt60 = 3 * rt20

        ################### End of Slide's Code ###################

        # Scatter + Line Plot
        ax3.plot(self.t, self.data_in_db, linewidth=1, alpha=0.7, color='#004bc6')
        ax3.scatter(self.t, self.data_in_db, linewidth=1, alpha=0.7, color='#00008B')
        ax3.plot(self.t[index_of_max], self.data_in_db[index_of_max], 'ro')
        ax3.plot(self.t[index_of_max_less_5], self.data_in_db[index_of_max_less_5], 'yo')
        ax3.plot(self.t[index_of_max_less_25], self.data_in_db[index_of_max_less_25], 'go')
        ax3.set_xlabel("Time (s)")
        ax3.set_ylabel("Power (db)")
        ax3.set_title("Scatter + Line Plot w/ Maximum, -5 from Max, and -25 from Max")

        new_window1 = tk.Toplevel(self.root)
        new_window2 = tk.Toplevel(self.root)
        new_window3 = tk.Toplevel(self.root)

        frame1 = tk.Frame(new_window1)
        frame1.pack(side=tk.LEFT)

        frame2 = tk.Frame(new_window2)
        frame2.pack()

        frame3 = tk.Frame(new_window3)
        frame3.pack()

        # Packing canvas widgets after frames have been created
        canvas3 = FigureCanvasTkAgg(fig3, master=frame3)
        canvas2 = FigureCanvasTkAgg(fig2, master=frame2)
        canvas1 = FigureCanvasTkAgg(fig1, master=frame1)

        canvas3.get_tk_widget().pack(expand=1, padx=110, pady=10)
        canvas2.get_tk_widget().pack(expand=1, padx=10, pady=10)
        canvas1.get_tk_widget().pack(expand=1, padx=100, pady=10)


if __name__ == "__main__":
    root = tk.Tk()
    app = View(root)
    root.mainloop()
