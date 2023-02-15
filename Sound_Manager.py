import winsound
import sounddevice as sd
import time
from datetime import datetime
from multiprocessing import Process
import multiprocessing
import numpy as np
import matplotlib.pyplot as plt


class Sound_Manager:
    
    @classmethod
    def get_Time_Now(self):
        now = datetime.now()
        return str(now.strftime("%H:%M:%S") + ':' + str(now.microsecond))


    @classmethod
    def record(self, duration, return_dict):
        if 'Microphone (USB Audio Device )' in list(sd.query_devices()):
            sd.default.device = 'Microphone (USB Audio Device )'
        else:
            print('microphone not connected')
        fs = 44100
        recording = sd.rec(duration * fs, samplerate=fs, channels=1, dtype='float64')
        print (f"Recording Audio for {duration} seconds at {self.get_Time_Now()}")
        sd.wait()
        print (f"Audio recording complete at {self.get_Time_Now()}")
        return_dict['recording'] = recording

    @classmethod
    def play_Sounds(self, frequenties):
        print(f'starting the sound playing at {self.get_Time_Now()}')
        time.sleep(5)
        for frequency in frequenties:
            print(f"playing frequenty {frequency} at: {self.get_Time_Now()}")
            winsound.Beep(frequency, 1000)
            time.sleep(4)
        print(f'done playing frequencies at {self.get_Time_Now()}')

    @classmethod
    def run_Test_Experiment(self):
        manager = multiprocessing.Manager()
        return_dict = manager.dict()
        record_sound_async = Process(target=self.record, args=(40,return_dict))
        record_sound_async.start()
        play_sound_async = Process(target=self.play_Sounds, args=([200,400,600,800,1000,1200,1400],))
        play_sound_async.start()
        play_sound_async.join()
        record_sound_async.join()
        get_Min = lambda sound_sample: float(sound_sample[0])
        recording = list(map(get_Min, return_dict['recording']))
        timestamps = np.linspace(0,40,40*44100)
        return recording, timestamps
    
    @classmethod
    def data_Analysis(self):
        recording, timestamps = self.run_Test_Experiment()
        plt.plot(timestamps, recording)
        plt.show()
