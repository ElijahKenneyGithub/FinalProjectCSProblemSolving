import time
import tkinter as tk
from tkinter.filedialog import askopenfilename
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from pydub import AudioSegment as AS
import pygame
import subprocess


class View:
    def __init__(self, root):

        # All the stuff relating towards plotting, all set to none to prevent errors

        # Statistic vars
        self.Max_db = None
        self.Median_db = None
        self.Average_db = None
        self.Standard_Dev_db = None
        self.Average_Freq = None
        self.Standard_Dev_Freq = None

        # Plotting vars
        self.freq_low_med_high = None
        self.sample_rate = None
        self.data = None
        self.spectrum = None
        self.freqs = None
        self.t = None
        self.target_frequency = None
        self.data_in_db = None
        self.rt60 = None
        self.past_name = None

        # GUI vars
        self.file_path = None
        self.file_name = None
        self.duration = None
        self.playing = 0
        self.low_data = None
        self.med_data = None
        self.high_data = None
        self.play_window = None
        self.new_window1 = None
        self.new_window2 = None
        self.new_window_combine = None
        self.spectrum_display = 0
        self.new_window_additional = None
        self.new_window_stats = None
        self.play_window = None

        def low_freq():
            self.display_plots(1000)

        def med_freq():
            self.display_plots(5000)

        def high_freq():
            self.display_plots(10000)

        # GUI initialization
        self.root = root
        self.root.title("Directory of GUI")
        self.root.geometry("200x150")

        # Button for playing the file
        self.play_button = tk.Button(root, text="Play File", command=self.play)
        self.play_button.pack()

        # Button for loading the file
        self.load_button = tk.Button(root, text="Load File", command=self.load_file)
        self.load_button.pack()

        # Button for displaying low frequency plot
        self.display_low_button = tk.Button(root, text="Graph Low Frequency Plots", command=low_freq)
        self.display_low_button.pack()

        # Button for displaying med frequency plot
        self.display_med_button = tk.Button(root, text="Graph Medium Frequency Plots", command=med_freq)
        self.display_med_button.pack()

        # Button for displaying high frequency plot
        self.display_high_button = tk.Button(root, text="Graph High Frequency Plots", command=high_freq)
        self.display_high_button.pack()

        # Button for displaying combined plot
        self.combine_button = tk.Button(root, text="Combine Plots", command=self.combine_plots)
        self.combine_button.pack()

        # Button for displaying statistics
        self.statistics_button = tk.Button(root, text="Display Statistics", command=self.display_statistics)
        self.statistics_button.pack()

    def play(self):  # This function, when called by a button, plays the song given to it
        global start
        if self.file_name is None:
            return

        def get_duration():
            # Grabs the duration of the file for display
            audio_file = AS.from_file(self.file_path)
            self.duration = audio_file.duration_seconds

        # Displaying the name in new window
        self.play_window = tk.Toplevel(self.root)  # New window is called to start a new window to show songs playing
        self.play_window.title("Now Playing...")  # Title display
        header = tk.Label(self.play_window, font=("Times New Roman", 40), text="Now Playing....")  # Header display
        now_playing = tk.Label(self.play_window, font=("Impact", 80), text=self.file_name)  # Name of File Display
        get_duration()  # Grabs the duration of the file, for later ( in update_time() )

        def update_time():
            # Calculate the time elapsed
            time_elapsed = int(time.time())

            # Updates the label with the elapsed time
            wav_duration.config(text=str(int(time_elapsed - start + 1)) + "/" + str(int(self.duration)) + " seconds")

            self.play_window.after(1000, update_time)  # Updates the window after a second
            if int(time_elapsed - start) == int(self.duration):  # if the elapsed time is equal to the file time,
                # delete window
                time.sleep(3)
                self.play_window.destroy()

        header.pack()
        now_playing.pack()

        try:  # displays the time, errors can occur here occasionally which is why a try block is here
            wav_duration = tk.Label(self.play_window, font=("Times New Roman", 40), text="")
            wav_duration.pack()
        except:
            print("Error getting time")

        pygame.mixer.init()  # initialize pygame mixer so we can play the files

        try:  # Attempts to play wav file
            pygame.mixer.music.load(self.file_path)
            start = time.time()
            pygame.mixer.music.play(loops=0)

        except:  # Prints error message and prevents fatal error
            print("Could not load, either no file selected or wrong file type")

        # Loop to update the time passed from when the file is loaded and playing
        update_time()
        self.play_window.mainloop()

    def load_file(self):
        # erases any relevant data to make sure it's starting from scratch
        self.spectrum_display = 0
        self.file_path = None
        self.file_name = None
        self.duration = None
        self.low_data = None
        self.med_data = None
        self.high_data = None

        def name_getter():  # grabs the name of the file for GUI purposes, only needs to be called the once in practice
            i = len(self.file_path)
            counter = 0
            for x in self.file_path:  # Finds the name of the file and gets rid of the directory parts to display
                if self.file_path[(i - counter - 4)] == '/':
                    self.file_name = self.file_path[(i - 3 - counter):i - 4]
                    break
                counter = counter + 1

        def file_finder():
            #
            self.file_path = askopenfilename(initialdir="/", title="Select File", filetypes=(
                ("wav File", ".wav"), ("mp3 file", ".mp3"), ("All Files", "*.*")))
            if self.file_path is None:
                return

        def extract_raw_audio():  # Extracts the raw audio data and assigns it to vars to be used later in display

            # Command to make ffmpeg function properly
            # It takes in the data from the file given, and puts in into output.wav to be read later
            command = f'ffmpeg -y -i {self.file_path} output.wav'

            # Executes the command
            subprocess.run(command, shell=True)

            # reads the data from output.wav
            audio = AS.from_file("output.wav")
            self.sample_rate = audio.frame_rate
            self.data = np.array(audio.get_array_of_samples())
            audio_file = AS.from_file('output.wav')
            self.duration = audio_file.duration_seconds
            print(self.duration)

        file_finder()
        name_getter()
        extract_raw_audio()
        self.destroyer()

        # Call destroyer to close previous windows
        self.root.mainloop()

    def destroyer(self):  # If new file is loaded, get rid of the old plots (GUI windows)
        if self.new_window1:
            self.new_window1.destroy()

        if self.new_window2:
            self.new_window2.destroy()

        if self.new_window_combine:
            self.new_window_combine.destroy()

        if self.new_window_additional:
            self.new_window_additional.destroy()

        if self.new_window_stats:
            self.new_window_stats.destroy()

    def display_statistics(self):
        # All the statistics variables calculated for
        if self.data_in_db is None:  # If there is no file selected, don't display this
            return
        self.Max_db = np.max(self.data_in_db)
        self.Median_db = np.median(self.data_in_db)
        self.Average_db = np.mean(self.data_in_db)
        self.Standard_Dev_db = np.std(self.data_in_db)
        self.Average_Freq = np.mean(self.freqs)
        self.Standard_Dev_Freq = np.std(self.freqs)

        self.new_window_stats = tk.Toplevel(self.root)
        self.new_window_stats.geometry("500x100")
        self.new_window_stats.title("Statistics of Most Recently Opened High / Medium / Low Plot")

        stats_text = f"Max Decibels: {self.Max_db:.2f}\n" \
                     f"Median Decibels: {self.Median_db:.2f}\n" \
                     f"Average Decibels: {self.Average_db:.2f}\n" \
                     f"Standard Deviation of_Decibels: {self.Standard_Dev_db:.2f}\n" \
                     f"Average Frequency: {self.Average_Freq:.2f}\n" \
                     f"Standard Deviation of Frequency: {self.Standard_Dev_Freq:.2f}"

        stats_label = tk.Label(self.new_window_stats, text=stats_text, font=("Helvetica", 12))
        stats_label.pack(padx=10, pady=10)
        self.new_window_stats.mainloop()

    def combine_plots(self):
        if self.file_name is None:
            return
        if self.new_window_combine is not None:
            self.new_window_combine.destroy()

        # New window to display
        new_window_combine = tk.Toplevel(self.root)
        new_window_combine.title("Combined Plots")

        # Combined plot for the GUI
        fig_combined, ax_combined = plt.subplots(1, 1, figsize=(8, 6))

        # Plots low-frequency data if already plotted
        if self.low_data is not None:
            ax_combined.plot(self.t, self.low_data, label='Low Frequency', linewidth=1, alpha=0.7, color='blue')

        # Plots medium-frequency data if already plotted
        if self.med_data is not None:
            ax_combined.plot(self.t, self.med_data, label='Medium Frequency', linewidth=1, alpha=0.7, color='green')

        # Plots high-frequency data if already plotted
        if self.high_data is not None:
            ax_combined.plot(self.t, self.high_data, label='High Frequency', linewidth=1, alpha=0.7, color='red')

        ax_combined.set_xlabel("Time (s)")
        ax_combined.set_ylabel("Power (db)")
        ax_combined.legend()

        # Packs the combined plots for the GUI
        frame_combine = tk.Frame(new_window_combine)
        frame_combine.pack()

        canvas_combine = FigureCanvasTkAgg(fig_combined, master=frame_combine)
        canvas_combine.get_tk_widget().pack(expand=1, padx=10, pady=10)

        self.new_window_combine = new_window_combine

        self.root.mainloop()

    def display_plots(self, freq_low_med_high):
        if self.file_name is None:
            return
        self.past_name = self.file_path

        self.freq_low_med_high = freq_low_med_high  # Sets the imported value to the class's version for easy of use later

        try:
            fig1, ax1 = plt.subplots(1, 1, figsize=(6, 4))
            fig2, ax2 = plt.subplots(1, 1, figsize=(6, 4))

            try:  # Try Except Block for if the wav file is or isn't Mono, if it is mono, it will use the first block,
                # else it will use the second
                self.spectrum, self.freqs, self.t, im = ax1.specgram(self.data, Fs=self.sample_rate, NFFT=1024,
                                                                     cmap=plt.get_cmap('autumn_r'))
            except:
                self.spectrum, self.freqs, self.t, im = ax1.specgram(np.mean(self.data, axis=1), Fs=self.sample_rate,
                                                                     NFFT=1024,
                                                                     cmap=plt.get_cmap('autumn_r'))
        except:
            print("Error occured trying to display plot")

        # Spectrum Graph
        ax1.set_title("Frequency Spectrum, Frequency vs. Time")
        ax1.set_xlabel("Time (s)")
        ax1.set_ylabel("Frequency (Hz)")

        ################### Beginning of Slide's Code ###################

        def find_target_frequency(freqs):

            for x in freqs:
                print(x)
                if x > self.freq_low_med_high:  # This can be changed to find a specific range, standard is 1000
                    break
            return x

        def frequency_check():
            global target_frequency
            target_frequency = find_target_frequency(self.freqs)
            index_of_frequency = np.where(self.freqs == target_frequency)[0][0]
            data_for_frequency = self.spectrum[index_of_frequency]
            if np.any(data_for_frequency == 0):  # Cleans the data in case shenanigans ensue
                data_for_frequency[data_for_frequency == 0] = 0.001  # Replace zeros with a small non-zero value
            data_in_db_fun = 10 * np.log10(data_for_frequency)
            return data_in_db_fun

        def find_nearest_value(array, value):
            array = np.asarray(array)
            idx = (np.abs(array - value)).argmin()
            return array[idx]

        # Plotting Reverb
        self.data_in_db = frequency_check()
        if self.data_in_db is not None:
            if self.freq_low_med_high == 1000:
                ax2.plot(self.t, self.data_in_db, linewidth=1, alpha=0.5, color='blue')
                self.low_data = self.data_in_db
            if self.freq_low_med_high == 5000:
                ax2.plot(self.t, self.data_in_db, linewidth=1, alpha=0.5, color='green')
                self.med_data = self.data_in_db
            if self.freq_low_med_high == 10000:
                ax2.plot(self.t, self.data_in_db, linewidth=1, alpha=0.5, color='red')
                self.high_data = self.data_in_db

            ax2.set_xlabel("Time (s)")
            ax2.set_ylabel("Power (db)")

            index_of_max = np.argmax(self.data_in_db)
            value_of_max = self.data_in_db[index_of_max]
            ax2.plot(self.t[index_of_max], self.data_in_db[index_of_max], 'ro')

            sliced_array = self.data_in_db[index_of_max:]
            value_of_max_less_5 = value_of_max - 5

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

            if self.new_window2 is not None:
                self.new_window2.destroy()
            new_window2 = tk.Toplevel(self.root)
            self.new_window2 = new_window2

            if self.freq_low_med_high == 1000:
                new_window2.title("Low Frequency Graph (1000 Hz)")
            if self.freq_low_med_high == 5000:
                new_window2.title("Medium Frequency Graph (5000 Hz)")
            if self.freq_low_med_high == 10000:
                new_window2.title("High Frequency Graph (10000 Hz)")

            # Labeling details like max decibels, rt60, etc
            frame2 = tk.Frame(new_window2)
            frame2.pack()
            rt60_label = tk.Label(frame2, text=f"RT60: {self.rt60:.2f} seconds")
            max_label = tk.Label(frame2, text=f"Max Decibels (Red Dot): {value_of_max:.2f} db")
            five_less_label = tk.Label(frame2,
                                       text=f"5 db less than Max Decibels (Yellow Dot): {value_of_max_less_5:.2f} db")
            twenty_five_less_label = tk.Label(frame2,
                                              text=f"25 db less than Max Decibels (Green Dot): {value_of_max_less_25:.2f} db")
            rt60_label.pack()
            max_label.pack()
            five_less_label.pack()
            twenty_five_less_label.pack()

            # Packing canvas widgets after frames have been created
            canvas2 = FigureCanvasTkAgg(fig2, master=frame2)

            if self.spectrum_display == 0:
                # creates a new plot for the spectrum graph
                new_window1 = tk.Toplevel(self.root)
                self.new_window1 = new_window1
                new_window1.title("Spectrum Display")
                frame1 = tk.Frame(new_window1)
                frame1.pack(side=tk.LEFT)
                canvas1 = FigureCanvasTkAgg(fig1, master=frame1)
                canvas1.get_tk_widget().pack(expand=1, padx=10, pady=10)

                # creates a new additional graph that marks out decibels over time
                additional_fig, additional_ax = plt.subplots(1, 1, figsize=(6, 4))
                additional_ax.plot(self.t, self.spectrum[0] + self.data_in_db, label='Combined Data')
                additional_ax.set_xlabel("Time (s)")
                additional_ax.set_ylabel("Combined Power (db)")
                additional_ax.set_title("Decibels from 0 over File Duration")
                self.new_window_additional = tk.Toplevel(self.root)
                self.new_window_additional.title("Decibels over File Duration")
                frame_additional = tk.Frame(self.new_window_additional)
                frame_additional.pack()
                canvas_additional = FigureCanvasTkAgg(additional_fig, master=frame_additional)
                canvas_additional.get_tk_widget().pack(expand=1, padx=10, pady=10)

                self.spectrum_display = self.spectrum_display + 1

            canvas2.get_tk_widget().pack(expand=1, padx=10, pady=10)
            self.freq_low_med_high = 0  # resets this var so it can be reused later


if __name__ == "__main__":
    root = tk.Tk()
    app = View(root)
    root.mainloop()
