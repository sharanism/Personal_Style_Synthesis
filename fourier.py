import numpy as np
import matplotlib.pyplot as plt
from scipy.fftpack import fft, fftfreq
import random

f = 5  # Frequency [Hz]
f_s = 100  # Sampling rate (number of measurements per second)
w = 2 * np.pi * f
t = np.linspace(0, 2, 2 * f_s)
x = np.sin(w * t)  # x(t) = sin(2*pi*f*t) = sin(wt)
# x = np.full(2 * f_s, w)


def plot_amplitude_vs_time():
    plt.plot(t, x)
    plt.xlabel('Time [s]')
    plt.ylabel('Signal amplitude')
    plt.show()


def plot_freq_magnitude_vs_freq():
    X = fft(x)
    freq = fftfreq(len(x)) * f_s
    plt.plot(freq, np.abs(X))
    plt.xlabel('Frequency [Hz]')
    plt.ylabel('Frequency Magnitude')
    plt.show()


# plot_amplitude_vs_time()
# plot_freq_magnitude_vs_freq()