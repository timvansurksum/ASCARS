import winsound
import sounddevice as sd
import time
from datetime import datetime
from multiprocessing import Process
import multiprocessing
import numpy as np
import json
import os


class Sound_Manager:
    
    @classmethod
    def get_Time_Now(self):
        now = datetime.now()
        return str(now.strftime("%H:%M:%S") + ':' + str(now.microsecond))


    @classmethod
    def set_Audio_Devices(self):
        record_device_names  = []
        play_device_names  = []
        for audio_device in list(sd.query_devices()):
            if int(audio_device["max_input_channels"]) > 0:
                record_device_names.append(audio_device['name'])
            if int(audio_device["max_output_channels"]) > 0:
                play_device_names.append(audio_device['name'])
        
        os.system('cls')
        record_device_names_string = '\n    '.join(record_device_names)
        record_device_name = input(f'please type the recording device you want to use your available devices are:\n {record_device_names_string}\n enter the name of the device here: ')

        while not record_device_name in record_device_names:
            record_device_name = input(f'you entered an invalid device name these are the possible device names:\n  {record_device_names_string}\n enter the name of the device here: ')


        os.system('cls')
        play_device_names_string = '\n  '.join(play_device_names)
        play_device_name = input(f'please type the playback device you want to use your available devices are:\n    {play_device_names_string}\n enter the name of the device here: ')

        while not play_device_name in play_device_names_string:
            play_device_name = input(f'you entered an invalid device name these are the possible device names:\n    {play_device_names_string}\n enter the name of the device here: ')
        os.system('cls')
        
        return  {
                'record_device_name': record_device_name,
                'play_device_name': play_device_name
                }

    @classmethod
    def record(self, duration, return_dict, audio_device_name):
            sd.default.device = audio_device_name
            fs = 44100
            recording = sd.rec(duration * fs, samplerate=fs, channels=1, dtype='float64')
            print (f"Recording Audio for {duration} seconds at {self.get_Time_Now()}")
            sd.wait()
            print (f"Audio recording complete at {self.get_Time_Now()}")
            return_dict['recording'] = recording


    @classmethod
    def play_Sounds(self, frequenties, audio_device_name):
        sd.default.device = audio_device_name
        print(f'starting the sound playing at {self.get_Time_Now()}')
        time.sleep(5)
        for frequency in frequenties:
            print(f"playing frequenty {frequency} at: {self.get_Time_Now()}")
            winsound.Beep(frequency, 1000)
            time.sleep(4)
        print(f'done playing frequencies at {self.get_Time_Now()}')

    @classmethod
    def run_Test_Experiment(self):
        audio_device_name  = self.set_Audio_Devices()
        manager = multiprocessing.Manager()
        return_dict = manager.dict()
        record_sound_async = Process(target=self.record, args=(40, return_dict, audio_device_name['record_device_name']))
        record_sound_async.start()
        play_sound_async = Process(target=self.play_Sounds, args=([200,400,600,800,1000,1200,1400], audio_device_name['play_device_name']))
        play_sound_async.start()
        play_sound_async.join()
        record_sound_async.join()
        get_Min = lambda sound_sample: float(sound_sample[0])
        recording = list(map(get_Min, return_dict['recording']))
        timestamps = np.linspace(0,40,40*44100)
        return recording, timestamps
