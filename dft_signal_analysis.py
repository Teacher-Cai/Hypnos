import numpy as np
import pyaudio
from matplotlib import pyplot as plt

p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paInt16,
                channels=2,
                rate=44100,
                input=True,
                frames_per_buffer=4096)

while True:
    data = stream.read(4096)
    audio_data = np.frombuffer(data, dtype=np.short)
    # plt.subplot(121)
    plt.xlim(0, 5500)
    plt.ylim(-600, 600)
    plt.plot(audio_data)
    plt.pause(0.1)
    plt.cla()
    ##
    # plt.subplot(122)
    # plt.xlim(0, 5000)
    #
    # plt.ylim(0, 5)
    # per = np.abs(np.fft.fft(audio_data)[40:409]) / (44100 * 2)
    # plt.plot(per)
    # print('\r', sum(per))
    # plt.pause(0.1)
    # plt.cla()
