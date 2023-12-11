# Main Branch

Hello and welcome to the contents of our audio analysis software.
Contained within this repository are the files necessary to insert WAV and mp3 files to compute visual data that informs the user of the time between reverberations. The exact order of the procedures is that this program will clean the audio file to remove background elements and interference, analyze the data, and create a spectrogram using multiple Python extentions. Finally, using a series of filtration and mathematics, the system will compute and display within the console the decibel peaks and intervals between reverberations as a numeric value. This project is run using pycharm as a compiler, however, any compiler that can interpret python code should suffice. To utilize this program follow the procedures listed below:


1) Load a file (Either wav or mp3, it doesn't matter which) using the load file button. No buttons will work until a file is loaded.
  
2) Click to Graph low / med / high frequency plot plots, or play an audio file (which will show the duration of the file)
   2a) Clicking on display low / medium / high frequency plots will display the spectrogram and the additional plot as required by the assignment
       if it is the first time you are displaying any of the low / medium / high frequency plots after loading a file
  
3) Once a low / medium / high plot is displayed, you can press the 'Display Statistics' button and display the statistics of the most recent low / medium / high plot or use 'Combine plots' buttons, which will combine all the low / medium / high frequency plots created at the time

4.) Enjoy.


Notes: 

To stop an audio file from playing after loading a new file, play the new file

If you display a new low / medium / high plot after having opened another, it will take down the previous plot and display the new one.
