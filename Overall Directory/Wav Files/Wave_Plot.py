# audioSpectrum mono only
import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile

# Code below is taken directly from slides, it takes in audio in a mono (single) channel for simplicity later on

try: #Try Except Block for if the wav file is or isn't Mono, if it is mono, it will use the first block, else it will use the second
    sample_rate, data = wavfile.read('16bit1chan.wav')
    spectrum, freqs, t, im = plt.specgram(data, Fs=sample_rate, NFFT=1024, cmap=plt.get_cmap('autumn_r'))
    cbar = plt.colorbar(im)

except:
    data_mono = np.mean(data, axis = 1)
    spectrum, freqs, t, im = plt.specgram(data_mono, Fs=sample_rate, NFFT=1024, cmap=plt.get_cmap('autumn_r'))
    cbar = plt.colorbar(im)

# Measuring Reverb (taken from slides)
def find_target_frequency(freqs):
    for x in freqs:
        if x > 1000:
            break
    return x


#Finding data/frequency check
def frequency_check():
    global target_frequency
    target_frequency = find_target_frequency(freqs)
    index_of_frequency = np.where(freqs == target_frequency)[0][0]
    data_for_frequency = spectrum[index_of_frequency]
    data_in_db_fun = 10 * np.log10(data_for_frequency)
    return data_in_db_fun



#Ploting Reverb

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

#Finding nearest Values of -5 and -25 db fr0m max

def find_nearest_value(array, value):
    array = np.asarray(array)
    idx = (np.abs(array-value)).argmin()
    return array[idx]

value_of_max_less_5 = find_nearest_value(sliced_array, value_of_max_less_5)
index_of_max_less_5 = np.where(data_in_db == value_of_max_less_5)
plt.plot(t[index_of_max_less_5], data_in_db[index_of_max_less_5], 'yo')

value_of_max_less_25 = value_of_max -25
value_of_max_less_25 = find_nearest_value(sliced_array, value_of_max_less_25)
index_of_max_less_25 = np.where(data_in_db == value_of_max_less_25)
plt.plot(t[index_of_max_less_25], data_in_db[index_of_max_less_25], 'go')


#RT20 & RT60
rt20 = (t[index_of_max_less_5] - t[index_of_max_less_25])[0]
rt60 = 3*rt20

plt.grid()
plt.show()


print("The RT60 reverb time at Freq", int(target_frequency), "Hz is", round(abs(rt60), 2)*1.5, "seconds")