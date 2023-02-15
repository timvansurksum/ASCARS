import winsound
import sounddevice as sd
import time
from datetime import datetime
from multiprocessing import Process
import multiprocessing
import numpy as np
import matplotlib.pyplot as plt
import json


class Sound_Manager:
    
    @classmethod
    def get_Time_Now(self):
        now = datetime.now()
        return str(now.strftime("%H:%M:%S") + ':' + str(now.microsecond))


    @classmethod
    def check_Audio_Device(self, device_name):
        if device_name in list(sd.query_devices()):
            return True
        else:
            
            available_devices = []
            for available_device in sd.query_devices():
                if int(available_device["max_input_channels"]) > 0:
                    available_devices.append(available_device)
            available_devices = json.dumps(list(available_devices), indent='    ')
            print(f'available devices: \n {available_devices}')
            print('microphone not connected')
            return False

    @classmethod
    def record(self, duration, return_dict):
            sd.default.device = 'Microphone (USB Audio Device )'
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
        if self.check_Audio_Device('Microphone (USB Audio Device )'):
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
        else:
            return [], []
    

    @classmethod
    def data_Analysis(self):
        recording, timestamps = self.run_Test_Experiment()
        if not (recording == [] or timestamps == []):
            plt.plot(timestamps, recording)
            plt.show()
