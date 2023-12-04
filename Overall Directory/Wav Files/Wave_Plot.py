import matplotlib.pyplot as plt
import numpy as np
from scipy.io import wavfile

# Some of the Code below is taken directly from slides


sample_rate, data = wavfile.read('16bit4chan.wav')  # Initialization, can be changed to be modular later

try:  # Try Except Block for if the wav file is or isn't Mono, if it is mono, it will use the first block,
    # else it will use the second
    spectrum, freqs, t, im = plt.specgram(data, Fs=sample_rate, NFFT=1024, cmap=plt.get_cmap('autumn_r'))
    plt.title("Frequency Spectrum (?), Frequency vs. Time")
    plt.xlabel("Time (s)")
    plt.ylabel("Frequency (Hz)")
    cbar = plt.colorbar(im)

except:
    spectrum, freqs, t, im = plt.specgram(np.mean(data, axis=1), Fs=sample_rate, NFFT=1024,
                                          cmap=plt.get_cmap('autumn_r'))
    plt.xlabel("Time (s)")
    plt.ylabel("Frequency (Hz)")
    plt.title("Frequency Spectrum (?), Frequency vs. Time")
    cbar = plt.colorbar(im)


################### Start of Slide's Code ###################

# Measuring Reverb (taken from slides)
def find_target_frequency(freqs_para):
    x = 0
    for x in freqs_para:
        if x > 1000:  # This can be change to find a specific range, standard is 1000
            break
    return x


# Finding data/frequency check
def frequency_check():
    global target_frequency
    target_frequency = find_target_frequency(freqs)
    index_of_frequency = np.where(freqs == target_frequency)[0][0]
    data_for_frequency = spectrum[index_of_frequency]
    data_in_db_fun = 10 * np.log10(data_for_frequency)
    return data_in_db_fun


# Ploting Reverb

data_in_db = frequency_check()
plt.figure(2)
plt.plot(t, data_in_db, linewidth=1, alpha=0.7, color='#004bc6')
plt.xlabel("Time (s)")
plt.ylabel("Power (db)")

index_of_max = np.argmax(data_in_db)
value_of_max = data_in_db[index_of_max]
plt.plot(t[index_of_max], data_in_db[index_of_max], 'ro')

sliced_array = data_in_db[index_of_max:]
value_of_max_less_5 = value_of_max - 5


# Finding nearest Values of -5 and -25 db fr0m max

def find_nearest_value(array, value):
    array = np.asarray(array)
    idx = (np.abs(array - value)).argmin()
    return array[idx]


value_of_max_less_5 = find_nearest_value(sliced_array, value_of_max_less_5)
index_of_max_less_5 = np.where(data_in_db == value_of_max_less_5)
plt.plot(t[index_of_max_less_5], data_in_db[index_of_max_less_5], 'yo')

value_of_max_less_25 = value_of_max - 25
value_of_max_less_25 = find_nearest_value(sliced_array, value_of_max_less_25)
index_of_max_less_25 = np.where(data_in_db == value_of_max_less_25)
plt.plot(t[index_of_max_less_25], data_in_db[index_of_max_less_25], 'go')

# RT20 & RT60
rt20 = (t[index_of_max_less_5] - t[index_of_max_less_25])[0]
rt60 = 3 * rt20

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
plt.plot(t, data_in_db, linewidth=1, alpha=0.7, color='#004bc6')
plt.scatter(t, data_in_db, linewidth=1, alpha=0.7, color='#00008B', )
plt.plot(t[index_of_max], data_in_db[index_of_max], 'ro')
plt.plot(t[index_of_max_less_5], data_in_db[index_of_max_less_5], 'yo')
plt.plot(t[index_of_max_less_25], data_in_db[index_of_max_less_25], 'go')
plt.show()  # Shows the line plot + scatter plot of the wav file

plt.grid()

# Statistical Analysis of Frequency
Standard_Dev_Freq = int(np.std(freqs))
Average_Freq = np.average(abs(freqs))
Median_Freq = np.median(freqs)
Max_Freq = np.max(freqs)
Min_Freq = np.min(freqs)

# Statistical Analysis of Decibels
Standard_Dev_db = int(np.std(data_in_db))
Average_db = np.average(abs(data_in_db))
Median_db = np.median(data_in_db)
Max_db = np.max(data_in_db)
Min_db = np.min(data_in_db)

print("\nThe RT60 reverb time at Freq", int(target_frequency), "Hz is", round(abs(rt60), 2) * 1.5, "seconds.\n")
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
