import logging

import numpy as np
import pyaudio

import global_var
from global_var import *
from loud_warn_window import show_warming

p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paInt16,
                channels=2,
                rate=frequency,
                input=True,
                frames_per_buffer=1024)


def voice_detect_func():
    logging.info("mic working")
    check_surroundings_volume()
    while True:
        data = stream.read(4096)
        audio_data = np.frombuffer(data, dtype=np.short)
        temp = np.sum(np.abs(np.fft.fft(audio_data)[int(HearFrequency.lowFre / (frequency / 2) * 4096):
                                                    int(HearFrequency.highFre / (frequency / 2) * 4096)]) / (
                              frequency * 2))
        db = 10 * np.log(temp / global_var.total_ave_pows)

        logging.debug("current db:{} {}".format(db, temp))
        if db >= Flags.dbThres and not Flags.noiseFlag:
            logging.debug('特喵的，有点吵了啊！当前阈值:{}'.format(temp))
            Flags.noiseFlag = True
            show_warming(5)
        else:
            logging.debug('还挺安静的')
            Flags.noiseFlag = False


def check_surroundings_volume():
    fragment_power_list = []
    frag_cnt = global_var.frequency * global_var.check_surroundings_db_second // 4096
    cnt = frag_cnt
    while cnt > 0:
        cnt -= 1
        data = stream.read(4096)
        audio_data = np.frombuffer(data, dtype=np.short)
        temp = np.sum(np.abs(np.fft.fft(audio_data)[
                             int(HearFrequency.lowFre / (frequency / 2) * 4096):
                             int(HearFrequency.highFre / (frequency / 2) * 4096)]) / (
                              frequency * 2))
        fragment_power_list.append(temp)

    global_var.total_ave_pows = sum(fragment_power_list) / frag_cnt
    logging.info('finish calculate {}'.format(global_var.total_ave_pows))
